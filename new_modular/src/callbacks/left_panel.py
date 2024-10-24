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
from src.functions.widgets import get_triggered_info, get_triggered_dict, get_triggered_index
from src.functions.graph import load_dataframe, extract_genome_names, process_chromosomes, generate_synteny_lines, create_genome_options, assign_chromosome_positions, create_chromosome_traces, create_bezier_synteny_lines, update_layout 
from src.params.generic import CONFIG


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
                 [Input({'id':'img-format', 'tab':ALL}, 'value'), Input({'id':'img-name', 'tab':ALL}, 'value'), 
                  Input({'id':'img-height', 'tab':ALL}, 'value'), Input({'id':'img-width', 'tab':ALL}, 'value'), Input({'id':'img-scale', 'tab':ALL}, 'value')],
                 [State("graph-config", "data"), State('tabs', 'active_tab'), State({'id':'img-format', 'tab':ALL}, 'id')], 
                  prevent_initial_call = True)
    def update_config(imgtype, name, height, width, scale, config, active_tab, items):
        try:
            active_tab = active_tab.split('-')[-1]
            tnv = get_triggered_info(callback_context.triggered)
            key = tnv[0]
            if active_tab != key:
                raise PreventUpdate
            ix = get_triggered_index(items, value=tnv[0])
        except:
            raise PreventUpdate
        if not key in config:
            config[key] = CONFIG
        config[key]['toImageButtonOptions'] = {'format': str(imgtype[ix]), 'filename': str(name[ix]), 'height': int(height[ix]), 'width': int(width[ix]),  'scale': float(scale[ix])}
        config['changed'] = key
        return config


    # Update Analysis settings options: synteny input dropdown (the same for all synteny tabs)
    @app.callback(Output({'id':"synteny-inputs", 'tab':ALL}, "options"),
                 [Input('user-files-list', 'data'), Input('edition-content', 'data')],
                 [State({'id':"synteny-inputs", 'tab':ALL}, "options"), State({'id':"synteny-inputs", 'tab':ALL}, "id")]
    )
    def update_synteny_inputs(files, edits, current, items):
        print("\ncallback 2: update_synteny_inputs()")                                         ########## DEBUG
        df_ids = sorted(set(files.keys()).union(edits.keys()))
        if df_ids != current[0]:
            return [df_ids] * len(items)
        else:
            raise PreventUpdate


    # Backend calculations for the synteny plot; Update Analysis settings options: synteny genomes checkboxes
    @app.callback([Output("graph-data", "data"), Output("synteny-genomes-all", "data"), Output("synteny-chromosomes-all", "data")],
                   Input({'id':"synteny-inputs", 'tab':ALL}, "value"),
                  [State('user-files-list', 'data'), State('edition-content', 'data'), 
                   State("graph-data", "data"), State("synteny-genomes-all", "data"), State("synteny-chromosomes-all", "data"),
                   State('tabs', 'active_tab'), State({'id':"synteny-inputs", 'tab':ALL}, "id")],
                   prevent_initial_call = True
    )
    def extract_synteny_genomes(df_ids, files, edits, graph_data, genomes_all, chr_all, active_tab, items):
        print("\ncallback 3: extract_synteny_genomes()")                                         ########## DEBUG
        try:
            active_tab = active_tab.split('-')[-1]
            print("triggered: ", callback_context.triggered)                                    ########## DEBUG
            tnv = get_triggered_info(callback_context.triggered)
            print(active_tab, tnv[0], tnv[1], tnv[2], len(items))                                                       ########## DEBUG
            key = tnv[0]
            if active_tab != key:
                print('   prevent update 0')                                                        ######### DEBUG
                raise PreventUpdate
            ix = get_triggered_index(items, value=tnv[0])
            print(key, " : ", ix)                                                               ######### DEBUG
            df_id = df_ids[ix]
        except:
            print('   prevent update 1')                                                        ######### DEBUG
            raise PreventUpdate

        if not df_id: #or genomes_all[key]:     # if not data siurce selected
            print('   prevent update 2')                                                        ######### DEBUG
            raise PreventUpdate

        df = load_dataframe(df_id, files, edits)
        if df.empty:
            print('   prevent update 3')                                                        ######### DEBUG
            raise PreventUpdate

        if not key in graph_data:
            graph_data[key] = {}

        # Initialize graph data for the active tab if it doesn't exist
        graph_data[key] = {
            "genomes": {},
            "synteny_lines": [],
            "chr_connections": {}
        }

        genome_names = extract_genome_names(df)
        genomes_all[key] = genome_names
        chromosome_names = {}

#        # Generate colors for each genome
#        palette = ["Tealgrn", "solar_r", "Plotly3_r"]
#        palette.extend(px.colors.named_colorscales())

        for ix, genome in enumerate(genome_names):
            genome_data = process_chromosomes(df, genome)
            graph_data[key]["genomes"][genome] = genome_data
            chromosomes = list(genome_data['chromosomes'].keys())
            chromosome_names[genome] = chromosomes
        chr_all[key] = chromosome_names

        synteny_lines = generate_synteny_lines(df, genome_names, graph_data[key])
        graph_data[key]["synteny_lines"] = synteny_lines

        # Count synteny connections for each chromosome
        chr_connections = graph_data[key]["chr_connections"]
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
        print(genomes_all)                                                                                   ######## DEBUG
        return [graph_data, genomes_all, chr_all]


    # Creates the initial options for genome and chromosome selection
    @app.callback([Output({'id':'genome-draggable', 'tab':ALL}, 'children'), Output({'id':'genome-draggable', 'tab':ALL}, 'layout'), 
                   Output({'id':'genome-draggable', 'tab':ALL}, 'gridCols'), Output({'id':"synteny-chromosome-selection", 'tab':ALL}, "children")],
                  [Input("synteny-genomes-all", "data")],
                  [State("synteny-chromosomes-all", "data"), State('synteny-genomes-selected', 'data'), State('synteny-chr-selected', 'data'),
                   State('tabs', 'active_tab'), State({'id':'genome-draggable', 'tab':ALL}, 'id')], 
                   prevent_initial_call = True
    )
    def create_genome_selection(all_genomes, all_chromosomes, sel_genomes, sel_chr, active_tab, items):
        print("\ncallback 4: create_genome_selection()")                                         ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        if not active_tab in all_genomes:
            raise PreventUpdate

        ix = get_triggered_index(items, value=active_tab)
        print(ix, " : ", len(items))                                                                ######## DEBUG
        if 0 <= ix < len(items):
            output = [no_update] * len(items)
            layout = []
            children = []
            chr_opts = []
            buttons = []
            cards = []
            d = 3 if all(len(word) <= 6 for word in all_genomes[active_tab]) else 2 if all(len(word) <= 11 for word in all_genomes[active_tab]) else 1
            print("divider: ", d)                                                                ############ DEBUG

            genomes = all_genomes[active_tab]
#            genomes = all_genomes if not sel_genomes else sel_genomes[:]                           ########## UPDATE: keep genome order on page reload 
#            if len(genomes) == len(sel_genomes) and len(genomes) < len(all_genomes):
#                selected_set = set(sel_genomes)
#                genomes.extend([item for item in all_genomes if item not in selected_set])

            for i, genome in enumerate(genomes):
                x = i % d           # alternates between 0 and 1 for two columns
                y = i // d          # increments every two items for a new row
                children.append(html.Div(dbc.Switch(id={'index': i, 'type': 'genome-switch-', 'tab':active_tab}, label=genome, value=False, persistence=True, persistence_type="session", className=""), id=f"genome-switch-{i}"))
                layout.append({"i": f"genome-switch-{i}", "x": x, "y": y, "w":1, "h":1})
                chr_children = []
                chr_layout = []
                # Creates draggable switches for all chromosomes in a given genome
                chromosomes = all_chromosomes[active_tab][genome]
                dd = 3 if all(len(word) <= 6 for word in chromosomes) else 2 if all(len(word) <= 11 for word in chromosomes) else 1
                for j, chr in enumerate(chromosomes):
                    xx = j % dd
                    yy = j // dd
                    chr_children.append(html.Div(dbc.Switch(id={'index': j, 'type': 'chr-switch-', 'id':genome, 'tab':active_tab}, label=chr, value=True, persistence=True, persistence_type="session", className=""), id=f"chr-switch-{genome}-{j}"))
                    chr_layout.append({"i": f"chr-switch-{genome}-{j}", "x": xx, "y": yy, "w":1, "h":1})
                draggable = dash_draggable.GridLayout(id={'type':'chr-draggable', 'id': genome, 'tab':active_tab}, children=chr_children, layout=chr_layout, gridCols=dd, width=300, height=30, className="w-100 mt-0 pt-0 shift-up")
                buttons.append(dbc.Button(f"{genome}", id={"type":"collapse-btn", "id":f"{genome}", 'tab':active_tab}, className="mb-3 me-2", color="secondary", n_clicks=0,))
                cards.append(dbc.Card(dbc.CardBody(draggable), id={"type":"collapse-card", "id":f"{genome}", 'tab':active_tab}, body=True, class_name="d-none"))
            buttons.append(dbc.Button("×", id="close-collapse", className="mb-3 me-2", color="primary", n_clicks=0,))
            collapse = html.Div([
                    html.Div(buttons),
                    dbc.Collapse(html.Div(cards), id="collapse", is_open=True,),
            ], className="w-100")
            chr_opts.append(collapse)
            print("    children len: ", len(children))                                                              ########## DEBUG

            children_all, layout_all, d_all, chr_opts_all = [output.copy() for _ in range(4)]
            children_all[ix] = children
            layout_all[ix] = layout
            d_all[ix] = d
            chr_opts_all[ix] = chr_opts
            return [children_all, layout_all, d_all, chr_opts_all]
        else:
            raise PreventUpdate


    @app.callback(Output("collapse", 'is_open'),
                 [Input("close-collapse", 'n_clicks'), Input({"type":"collapse-btn", "id":ALL, 'tab': ALL}, 'n_clicks')], 
    )
    def toggle_cards(n_clicks, genome_btns):
        print("\ncallback: toggle_cards()", callback_context.triggered)                                                              ########## DEBUG
        gtd = get_triggered_dict(callback_context.triggered)
        print(gtd, n_clicks)
        if 'close-collapse' in {gtd.get('type'), gtd.get('id')} and n_clicks > 0:
            return False
        else:
            return True


    @app.callback(Output({"type":"collapse-card", "id":ALL, 'tab': MATCH}, 'class_name'),
                  Input({"type":"collapse-btn", "id":ALL, 'tab': MATCH}, 'n_clicks'),
                 [State({"type":"collapse-card", "id":ALL, 'tab': MATCH}, 'class_name'), State({"type":"collapse-card", "id":ALL, 'tab':MATCH}, 'id')],
    )
    def display_cards(n_clicks, styles, ids):                                                         ########## UPDATE : can be moved to universal widget_toogle module, when generalized
        print("\n callback: display_cards()")                                                         ########## DEBUG

        # Return current styles if nothing was triggered
        gtd = get_triggered_dict(callback_context.triggered)
        if not gtd:
            return styles

        # Find the index of the button clicked
        index = next((i for i, item in enumerate(ids) if gtd['id'] == item['id']), None)
        return ['d-block' if i == index else 'd-none' for i in range(len(ids))] if index is not None else styles


    # Returns ordered list of selected genomes, use it to update the plot
    @app.callback(Output('synteny-genomes-selected', 'data'),
                [Input({'type': 'genome-switch-', 'index': ALL}, 'value'), Input({'id':'genome-draggable', 'tab':ALL}, 'layout')],
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
                [State("synteny-chromosomes-all", "data"), State("synteny-genomes-all", "data"), State('synteny-chr-selected', 'data'), State('tabs', 'active_tab')],
                prevent_initial_call = True
    )
    def update_selected_chromosomes(switch_values, layout, chromosomes_all, genomes_all, selected_chromosomes, active_tab):
        print("\ncallback 5B: update_selected_chromosomes()")                                             ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        try:
            chromosomes_all = chromosomes_all[active_tab]
            genomes_all = genomes_all[active_tab]
        except:
            raise PreventUpdate

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
        selected_chromosomes[active_tab] = selected_chr
        return selected_chromosomes



    # Generate synteny plot
    @app.callback(Output({'id':"graph", 'tab':MATCH}, "figure", allow_duplicate=True),
                 [Input("synteny-genomes-selected", "data"), Input('synteny-chr-selected', 'data'),
                  Input({'id':"synteny-chr-spacing", 'tab':MATCH}, "value"), Input({'id':"synteny-chr-height", 'tab':MATCH}, "value"), 
                  Input({'id':"synteny-chr-alignment", 'tab':MATCH}, "value"), Input({'id':"synteny-line-position", 'tab':MATCH}, "value")],
                 [State('tabs', 'active_tab'), State("graph-data", "data")],
                 prevent_initial_call = True
    )
    def generate_synteny_graph(selected_genomes, selected_chromosomes, spacing, bar_height, alignment, position_mode, active_tab, graph_data):
        print("\ncallback 6: generate_synteny_graph()")                                         ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        ctx = callback_context
        if not ctx.triggered or not selected_genomes or not graph_data or active_tab not in graph_data:
            raise PreventUpdate

#        tnv = get_triggered_info(ctx)  # [type, name, value]
#        print('    triggered: ', tnv[1])                                                                          #############  DEBUG

        selected_chromosomes = selected_chromosomes[active_tab]

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
    @app.callback(Output({'id':"graph", 'tab':MATCH}, "figure", allow_duplicate=True),
                 [Input({'id':'graph-title', 'tab':MATCH}, 'value'), Input({'id':'X-title', 'tab':MATCH}, 'value'), Input({'id':'Y-title', 'tab':MATCH}, 'value')],
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