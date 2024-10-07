import re
from collections import defaultdict
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html, callback_context, no_update, Patch
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_draggable
from src.functions.io import decode_base64, format_length
from src.functions.widgets import get_triggered_info
from src.functions.graph import load_dataframe, extract_genome_names, process_chromosomes, generate_synteny_lines, create_genome_options, assign_chromosome_positions, create_chromosome_traces, create_bezier_synteny_lines, update_layout 

from src.options.analysis import synteny
from src.options.graph_custom import opts_synteny

def register_left_panel_callbacks(app):
    
    # color scale modal open-close
    @app.callback(Output("modal-cs", "is_open"),
                 [Input("modal-cs-btn-open", "n_clicks"), Input("modal-cs-btn-close", "n_clicks"),],
                 [State("modal-cs", "is_open")])
    def toggle_modal_cs(n_open, n_close, is_open):
        if n_open or n_close:
            return not is_open
        return is_open


    # Update graph config 
    @app.callback(Output("graph-config", "data"),
                 [Input('img-format', 'value'), Input('img-name', 'value'), 
                  Input('img-height', 'value'), Input('img-width', 'value'), Input('img-scale', 'value')],
                 [State("graph-config", "data")])
    def update_config(imgtype, name, height, width, scale, config):
        config['toImageButtonOptions'] = {'format': str(imgtype), 'filename': str(name), 'height': int(height), 'width': int(width),  'scale': float(scale)}
        return config


    # Update Analysis settings options: display analysis settings for currently open graphing tab, e.g., synteny
    @app.callback(Output("opts-analysis", "children"),
                  Input('tabs', 'value'),
                  State('opts-analysis', 'children'),
    )
    def update_analysis_opts(active_tab, content):
        print("\ncallback 1: update_analysis_opts()")                                         ########## DEBUG
        if active_tab == 'tab-home' or active_tab == 'tab-about':
            raise PreventUpdate
        else:
            var_name = active_tab.split('_')[0].split('-')[1]
            if content:
                return content
            elif var_name in globals():
                return globals()[var_name]
            else:
                return html.Label(f"No analysis settings available for {var_name} plot type.", className="label-s")


    # Update Custom Graph settings options: display analysis settings for currently open graphing tab, e.g., synteny
    @app.callback(Output("opts-graph-cutom", "children"),
                  Input('tabs', 'value'),
                  State('opts-graph-cutom', 'children'),
    )
    def update_custom_graph_opts(active_tab, content):
        print("\ncallback 1: update_custom_graph_opts()")                                         ########## DEBUG
        if active_tab == 'tab-home' or active_tab == 'tab-about':
            raise PreventUpdate
        else:
            var_name = active_tab.split('_')[0].split('-')[1]
            if content:
                return content
            elif f"opts_{var_name}" in globals():
                return globals()[f"opts_{var_name}"]
            else:
                return html.Label(f"No custom graph options available for {var_name} plot type.", className="label-s")


    # Update Analysis settings options: synteny input dropdown
    @app.callback(Output("synteny-inputs", "options"),
                 [Input("opts-analysis", "children"), Input('user-files-list', 'data'), Input('edition-content', 'data'), ],
                 [State("synteny-inputs", "options"), State("synteny-inputs", "value")]
    )
    def update_synteny_inputs(opts_analysis, files, edits, current, value):
        print("\ncallback 2: update_synteny_inputs()")                                         ########## DEBUG
        df_ids = sorted(set(files.keys()).union(edits.keys()))
        if df_ids != current:
            return df_ids
        else:
            raise PreventUpdate


    # Backend calculations for the synteny plot; Update Analysis settings options: synteny genomes checkboxes
    @app.callback(
        [Output("graph-data", "data"), Output("synteny-genomes-all", "data"), Output("synteny-chromosomes-all", "data")],
         Input("synteny-inputs", "value"),
        [State('user-files-list', 'data'), State('edition-content', 'data'), State('tabs', 'value'), State("graph-data", "data"), State("synteny-genomes-all", "data")] 
    )
    def extract_synteny_genomes(df_id, files, edits, active_tab, graph_data, genomes_all):
        print("\ncallback 3: extract_synteny_genomes()")                                         ########## DEBUG
        if not df_id or genomes_all:
            raise PreventUpdate

        df = load_dataframe(df_id, files, edits)
        if df.empty:
            raise PreventUpdate

        if graph_data is None:
            graph_data = {}

        # Initialize graph data for the active tab if it doesn't exist
        graph_data[active_tab] = {
            "genomes": {},
            "synteny_lines": [],
            "chr_connections": {}
        }

        genome_names = extract_genome_names(df)
        chromosome_names = {}

#        # Generate colors for each genome
#        palette = ["Tealgrn", "solar_r", "Plotly3_r"]
#        palette.extend(px.colors.named_colorscales())

        for ix, genome in enumerate(genome_names):
            genome_data = process_chromosomes(df, genome)
            graph_data[active_tab]["genomes"][genome] = genome_data
            chromosomes = list(genome_data['chromosomes'].keys())
            chromosome_names[genome] = chromosomes

        synteny_lines = generate_synteny_lines(df, genome_names, graph_data[active_tab])
        graph_data[active_tab]["synteny_lines"] = synteny_lines

        # Count synteny connections for each chromosome
        chr_connections = graph_data[active_tab]["chr_connections"]
        for line in synteny_lines:
            genome_1, chr_1 = line["genome_1"], line["chr_1"]
            genome_2, chr_2 = line["genome_2"], line["chr_2"]
            chr_1_key = f"{genome_1}:{chr_1}"
            chr_2_key = f"{genome_2}:{chr_2}"

            chr_connections.setdefault(chr_1_key, {}).setdefault(genome_2, {"count": 0, "chromosomes": []})
            chr_connections.setdefault(chr_2_key, {}).setdefault(genome_1, {"count": 0, "chromosomes": []})
            chr_connections[chr_1_key][genome_2]["count"] += 1
            chr_connections[chr_2_key][genome_1]["count"] += 1
            if chr_2 not in chr_connections[chr_1_key][genome_2]["chromosomes"]:
                chr_connections[chr_1_key][genome_2]["chromosomes"].append(chr_2)
            if chr_1 not in chr_connections[chr_2_key][genome_1]["chromosomes"]:
                chr_connections[chr_2_key][genome_1]["chromosomes"].append(chr_1)

        return [graph_data, genome_names, chromosome_names]


    # Creates the initial options for genome and chromosome selection
    @app.callback([Output('genome-draggable', 'children'), Output('genome-draggable', 'layout'),  Output('genome-draggable', 'gridCols'), Output("synteny-chromosome-selection", "children")],
                  [Input("synteny-genomes-all", "data")],
                  [State("synteny-chromosomes-all", "data"), State('synteny-genomes-selected', 'data'), State('synteny-chr-selected', 'data')], 
                   prevent_initial_call = True
    )
    def create_genome_selection(all_genomes, all_chromosomes, sel_genomes, sel_chr):
        print("\ncallback 4: create_genome_selection()")                                         ########## DEBUG
        if not all_genomes:
            raise PreventUpdate
        else:
            layout = []
            children = []
            chr_opts = []
            buttons = []
            cards = []
            d = 3 if all(len(word) <= 6 for word in all_genomes) else 2 if all(len(word) <= 11 for word in all_genomes) else 1
            print("divider: ", d)                                                                ############ DEBUG

            genomes = all_genomes
#            genomes = all_genomes if not sel_genomes else sel_genomes[:]                           ########## UPDATE: keep genome order on page reload 
#            if len(genomes) == len(sel_genomes) and len(genomes) < len(all_genomes):
#                selected_set = set(sel_genomes)
#                genomes.extend([item for item in all_genomes if item not in selected_set])

            for i, genome in enumerate(genomes):
                x = i % d           # alternates between 0 and 1 for two columns
                y = i // d          # increments every two items for a new row
                children.append(html.Div(dbc.Switch(id={'index': i, 'type': 'genome-switch-'}, label=genome, value=False, persistence=True, persistence_type="session", className=""), id=f"genome-switch-{i}"))
                layout.append({"i": f"genome-switch-{i}", "x": x, "y": y, "w":1, "h":1})
                chr_children = []
                chr_layout = []
                # Creates draggable switches for all chromosomes in a given genome
                chromosomes = all_chromosomes[genome]
                dd = 3 if all(len(word) <= 6 for word in chromosomes) else 2 if all(len(word) <= 11 for word in chromosomes) else 1
                for j, chr in enumerate(chromosomes):
                    xx = j % dd
                    yy = j // dd
                    chr_children.append(html.Div(dbc.Switch(id={'index': j, 'type': 'chr-switch-', 'id':genome}, label=chr, value=True, persistence=True, persistence_type="session", className=""), id=f"chr-switch-{genome}-{j}"))
                    chr_layout.append({"i": f"chr-switch-{genome}-{j}", "x": xx, "y": yy, "w":1, "h":1})
                draggable = dash_draggable.GridLayout(id={'type':'chr-draggable', 'id': genome}, children=chr_children, layout=chr_layout, gridCols=dd, width=300, height=30, className="w-100 mt-0 pt-0 shift-up")
                buttons.append(dbc.Button(f"{genome}", id={"type":"collapse-btn", "id":f"{genome}"}, className="mb-3 me-2", color="secondary", n_clicks=0,))
                cards.append(dbc.Card(dbc.CardBody(draggable), id={"type":"collapse-card", "id":f"{genome}"}, body=True, class_name="d-none"))
            buttons.append(dbc.Button("×", id="close-collapse", className="mb-3 me-2", color="primary", n_clicks=0,))
            collapse = html.Div([
                    html.Div(buttons),
                    dbc.Collapse(html.Div(cards), id="collapse", is_open=True,),
            ], className="w-100")
            chr_opts.append(collapse)
            print("    children len: ", len(children))
            return [children, layout, d, chr_opts]


    @app.callback(Output("collapse", 'is_open'),
                 [Input("close-collapse", 'n_clicks'), Input({"type":"collapse-btn", "id":ALL}, 'n_clicks')], 
    )
    def toggle_cards(n_clicks, genomes):
        ctx = callback_context.triggered
        btn_id = get_triggered_info(ctx)[1]
        if btn_id == "close-collapse" and n_clicks > 0:
            return False
        else:
            return True


    @app.callback(Output({"type":"collapse-card", "id":ALL}, 'class_name'),
                  Input({"type":"collapse-btn", "id":ALL}, 'n_clicks'),
                 [State({"type":"collapse-card", "id":ALL}, 'class_name'), State({"type":"collapse-card", "id":ALL}, 'id')],
    )
    def toggle_cards(n_clicks, styles, ids):                                                         ########## UPDATE : can be moved to universal widget_toogle module, when generalized
        print("\n callback: toggle_cards(): ", n_clicks, styles, ids)                                ########## DEBUG

        # Determine which button was clicked
        ctx = callback_context.triggered
        if not ctx:
            return styles
        button_id = get_triggered_info(ctx)[1]

        # Find the index of the button clicked
        for i, item in enumerate(ids):
            if button_id == item['id']:
                return ['d-block' if i == j else 'd-none' for j in range(len(ids))]
        return styles


    # Returns ordered list of selected genomes, use it to update the plot
    @app.callback(Output('synteny-genomes-selected', 'data'),
                [Input({'type': 'genome-switch-', 'index': ALL}, 'value'), Input('genome-draggable', 'layout')],
                [State("synteny-genomes-all", "data"), State('synteny-genomes-selected', 'data')],
    )
    def update_selected_genomes(switch_values, layout, genomes, selected):
        print("\ncallback 5A: update_selected_genomes()")                                             ########## DEBUG
#        print("    : ", switch_values, "\n", layout, "\n", genomes, "\n", selected)                   ########## DEBUG
        ctx = callback_context.triggered
        print("   triggered: ", get_triggered_info(ctx))
        if not switch_values:
            raise PreventUpdate

        selected_genomes = []

        print("    layout input: ", layout)                                                          ########## DEBUG
        print("    switch values: ", switch_values)                                                  ########## DEBUG

        # Sort by 'y' first, then by 'x' to get the correct order
        sorted_layout = sorted(layout, key=lambda item: (item['y'], item['x']))

        for layout_item in sorted_layout:
            match = re.search(r'\d+', layout_item['i'])
            if match:
                idx = int(match.group())
                if switch_values[idx]:
                    selected_genomes.append(genomes[idx])

        print("    genomes order: ", selected_genomes)                                                ########### DEBUG        
        return selected_genomes if selected_genomes else []


    # Returns ordered list of selected chromosomes, use it to update the plot
    @app.callback(Output('synteny-chr-selected', 'data'),
                [Input({'type': 'chr-switch-', 'index': ALL, 'id': ALL}, 'value'), Input({'type':'chr-draggable', 'id': ALL}, 'layout')],
                [State("synteny-chromosomes-all", "data"), State("synteny-genomes-all", "data")],
                prevent_initial_call = True
    )
    def update_selected_chromosomes(switch_values, layout, chromosomes_all, genomes_all):
        print("\ncallback 5B: update_selected_chromosomes()")                                             ########## DEBUG
        if not switch_values or len(genomes_all) != len(layout):
            raise PreventUpdate

        selected_chr = {}
        l_bound = 0
        for ix, dataset in enumerate(layout):
            genome = dataset[0]['i'].split('-')[-2]
            chromosomes = chromosomes_all[genome]
            n_chr = len(dataset)
            switches = switch_values[l_bound : l_bound + n_chr]
            l_bound += n_chr

#            print("    layout input: ", genome, "\n", dataset)                                                          ########## DEBUG
#            print("    switch values: ", switches)                                                  ########## DEBUG
#            print("    length: ", len(dataset), len(switches))                                       ########## DEBUG

        # Sort by 'y' first, then by 'x' to get the correct order
            sorted_layout = sorted(dataset, key=lambda item: (item['y'], item['x']))
            selected_chr[genome] = []
            for layout_item in sorted_layout:
                match = re.search(r'\d+', layout_item['i'])
                if match:
                    idx = int(match.group())
                    if switches[idx]:
                        selected_chr[genome].append(chromosomes[idx])

            print("    genomes order: ", genome, len(selected_chr[genome]), selected_chr[genome])                                                ########### DEBUG        
        return selected_chr



    # Generate synteny plot
    @app.callback(Output("graph", "figure", allow_duplicate=True),
                 [Input("synteny-genomes-selected", "data"), Input('synteny-chr-selected', 'data'),
                  Input("synteny-chr-spacing", "value"), Input("synteny-chr-height", "value"), Input("synteny-chr-alignment", "value"), Input("synteny-line-position", "value")],
                 [State('tabs', 'value'), State("graph-data", "data")],
                 prevent_initial_call = True
    )
    def generate_synteny_graph(selected_genomes, selected_chromosomes, spacing, bar_height, alignment, position_mode, active_tab, graph_data):
        print("\ncallback 6: generate_synteny_graph()")                                         ########## DEBUG
        if not selected_genomes or not graph_data or active_tab not in graph_data:
            raise PreventUpdate

        tab_data = graph_data[active_tab]
        
        fig = go.Figure()
        # Add a dummy trace to force the use of y2 (displays total genome length)
        fig.add_trace(go.Scatter(x=[None], y=[None], showlegend=False, yaxis="y2"))

        # Ensure user-selected genomes order is respected: track y-offset for genomes
        genome_y_positions = {}
        for idx, genome in enumerate(selected_genomes):
            genome_y_positions[genome] = -20 * idx

        # Update graph layout
        update_layout(fig, selected_genomes, tab_data, height=bar_height)

        # Calculate and assign x-positions for chromosomes based on selection and ordering
        chromosome_positions, x_range = assign_chromosome_positions(selected_genomes, selected_chromosomes, tab_data, alignment, spacing=spacing)

        fig.update_xaxes(range=x_range)

        # Plot synteny lines only for neighboring selected genomes
        line_traces = create_bezier_synteny_lines(
            tab_data["synteny_lines"],
            selected_genomes,
            selected_chromosomes,
            chromosome_positions,
            genome_y_positions,
            position_mode=position_mode,
            height=bar_height
        )
        for trace in line_traces:
            fig.add_trace(trace)

        # Plot chromosomes for each selected genome with proper colors
        for genome in selected_genomes:
            if genome in tab_data["genomes"]:
                genome_data = tab_data["genomes"][genome]
                chromosomes_to_plot = selected_chromosomes.get(genome, genome_data["chromosomes"].keys())
                chromosome_traces = create_chromosome_traces(
                    genome, genome_data, chromosomes_to_plot, chromosome_positions, genome_y_positions[genome], graph_data, active_tab, height=bar_height
                )
                for trace in chromosome_traces:
                    fig.add_trace(trace)

        return fig


    # Callback to update the graph layout using Patch
    @app.callback(Output("graph", "figure", allow_duplicate=True),
                 [Input('graph-title', 'value'), Input('X-title', 'value'), Input('Y-title', 'value')],
                 prevent_initial_call = True
    )
    def update_graph_layout(title, xaxis_label, yaxis_label):
        patch = Patch()
        if title:
            patch['layout']['title'] = title
        if xaxis_label:
            patch['layout']['xaxis']['title'] = xaxis_label
        if yaxis_label:
            patch['layout']['yaxis']['title'] = yaxis_label
        
        if patch:
            return patch
        else:
            raise PreventUpdate