import re
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html, callback_context, no_update, Patch
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
import dash_draggable
from src.functions.widgets import get_triggered_info, get_triggered_dict, get_triggered_index
from src.functions.graph import load_dataframe, extract_genome_names, process_chromosomes, generate_synteny_lines, create_genome_options, assign_chromosome_positions, create_chromosome_traces, create_bezier_synteny_lines, update_layout 
from src.params.generic import CONFIG



def register_synteny_callbacks(app):

    # Update Analysis settings options: synteny input dropdown (the same for all synteny tabs)
    @app.callback(Output({'id':"synteny-inputs", 'tab':ALL}, "options"),
                 [Input('user-files-list', 'data'), Input('edition-content', 'data')],
                 [State({'id':"synteny-inputs", 'tab':ALL}, "options"), State({'id':"synteny-inputs", 'tab':ALL}, "id"), State('tabs', 'active_tab')]
    )
    def update_synteny_inputs(files, edits, current, items, active_tab):
        print("\ncallback 2: update_synteny_inputs()")                                         ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        if active_tab in ['home', 'tab']:
            raise PreventUpdate
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
        active_tab = active_tab.split('-')[-1]
        if active_tab in ['home', 'tab']:
            raise PreventUpdate
        gtd = get_triggered_dict(callback_context.triggered)
        print("triggered: ", gtd, active_tab)                                                      ########## DEBUG
        try:
            key = gtd.get('tab')
            if active_tab != key:
                print('prevent update in c3: 0')
                raise PreventUpdate
            ix = get_triggered_index(items, value=key)
            df_id = df_ids[ix]
        except:
            print('prevent update in c3: 1')
            raise PreventUpdate

        if not df_id: #or genomes_all[key]:     # if not data siurce selected
            print('prevent update in c3: 2')
            raise PreventUpdate

        df = load_dataframe(df_id, files, edits)
        if df.empty:
            print('prevent update in c3: 3')
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
#        print(genomes_all)                                                                                   ######## DEBUG
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
        print("\ncallback 4: create_genome_selection()")                                          ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        if active_tab in ['home', 'tab']:
            raise PreventUpdate
        gtd = get_triggered_dict(callback_context.triggered)
        print("triggered: ", gtd, active_tab)                                                      ########## DEBUG
        if not active_tab in all_genomes:
            raise PreventUpdate

        ix = get_triggered_index(items, value=active_tab)
#        print(ix, " : ", len(items))                                                              ######## DEBUG
        if 0 <= ix < len(items):
            output = [no_update] * len(items)
            layout = []
            children = []
            chr_opts = []
            buttons = []
            cards = []
            d = 3 if all(len(word) <= 6 for word in all_genomes[active_tab]) else 2 if all(len(word) <= 11 for word in all_genomes[active_tab]) else 1
#            print("divider: ", d)                                                                ############ DEBUG

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
#            print("    children len: ", len(children))                                                              ########## DEBUG

            children_all, layout_all, d_all, chr_opts_all = [output.copy() for _ in range(4)]
            children_all[ix] = children
            layout_all[ix] = layout
            d_all[ix] = d
            chr_opts_all[ix] = chr_opts
            return [children_all, layout_all, d_all, chr_opts_all]
        else:
            raise PreventUpdate
        

    # Returns ordered list of selected genomes, use it to update the plot
    @app.callback(Output('synteny-genomes-selected', 'data'),
                [Input({'type': 'genome-switch-', 'index': ALL, 'tab': ALL}, 'value'), Input({'id':'genome-draggable', 'tab':ALL}, 'layout')],
                [State("synteny-genomes-all", "data"), State('synteny-genomes-selected', 'data'), State('tabs', 'active_tab')], 
                 prevent_initial_call = True
    )
    def update_selected_genomes(switchers, layouts, genomes, selected_genomes, active_tab):
        print("\ncallback 5A: update_selected_genomes()")                                             ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        if active_tab in ['home', 'tab']:
            raise PreventUpdate
        gtd = get_triggered_dict(callback_context.triggered)
#        print("triggered: ", gtd)                                                                    ########## DEBUG
        if gtd.get('tab') != active_tab or not switchers:
            raise PreventUpdate

        genomes = genomes[active_tab]
        switch_values = []
        layout = []
        # Loop over inputs and filter them based on the active tab
        for input_group in callback_context.inputs_list:
            for i, input_item in enumerate(input_group):
                input_id = input_item['id']
                
                # Filter genome-switch- based on the active tab
                if 'type' in input_id and input_id['type'] == 'genome-switch-' and input_id['tab'] == active_tab:
                    switch_values.append(input_item['value'])

                # Filter genome-draggable layout based on the active tab
                elif 'id' in input_id and input_id['id'] == 'genome-draggable' and input_id['tab'] == active_tab:
                    layout = input_item['value']

#        print("    layout input: ", layout)                                                          ########## DEBUG
#        print("    switch values: ", switch_values)                                                  ########## DEBUG
        selected = []
        # Sort by 'y' first, then by 'x' to get the correct order
        sorted_layout = sorted(layout, key=lambda item: (item['y'], item['x']))

        for layout_item in sorted_layout:
            match = re.search(r'\d+', layout_item['i'])
            if match:
                idx = int(match.group())
                if switch_values[idx]:
                    selected.append(genomes[idx])
        selected_genomes[active_tab] = selected if selected else []
        selected_genomes['@changed'] = active_tab
        print("    genomes order: ", selected_genomes)                                                ########### DEBUG        
        return selected_genomes


    # Returns ordered list of selected chromosomes, use it to update the plot
    @app.callback(Output('synteny-chr-selected', 'data'),
                [Input({'type': 'chr-switch-', 'index': ALL, 'id': ALL, 'tab': ALL}, 'value'), Input({'type':'chr-draggable', 'id': ALL, 'tab': ALL}, 'layout')],
                [State("synteny-chromosomes-all", "data"), State("synteny-genomes-all", "data"), State('synteny-chr-selected', 'data'), State('tabs', 'active_tab')],
                 prevent_initial_call = True
    )
    def update_selected_chromosomes(switchers, layouts, chromosomes_all, genomes_all, selected_chromosomes, active_tab):
        print("\ncallback 5B: update_selected_chromosomes()")                                             ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        if active_tab in ['home', 'tab']:
            raise PreventUpdate
        gtd = get_triggered_dict(callback_context.triggered)
        if gtd.get('tab') != active_tab:
            raise PreventUpdate
        try:
            genomes_all = genomes_all[active_tab]
            chromosomes_all = chromosomes_all[active_tab]
        except:
            raise PreventUpdate

        switch_values = []
        layout = []
#        print(callback_context.inputs_list)
        for input_group in callback_context.inputs_list:
            for i, input_item in enumerate(input_group):
                input_id = input_item['id']
                
                # Filter genome-switch- based on the active tab
                if 'type' in input_id and input_id['type'] == 'chr-switch-' and input_id['tab'] == active_tab:
                    switch_values.append(input_item['value'])

                # Filter genome-draggable layout based on the active tab
                elif 'type' in input_id and input_id['type'] == 'chr-draggable' and input_id['tab'] == active_tab:
                    layout.append(input_item['value'])

#        print(switch_values)
#        print(layout)

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

#            print("    chr order: ", genome, len(selected_chr[genome]), selected_chr[genome])                                                ########### DEBUG        
        selected_chromosomes[active_tab] = selected_chr
        selected_chromosomes['@changed'] = active_tab
        return selected_chromosomes



    # Generate synteny plot
    @app.callback(Output({'id':"graph", 'tab':MATCH}, "figure", allow_duplicate=True),
                 [Input("synteny-genomes-selected", "data"), Input('synteny-chr-selected', 'data'),
                  Input({'id':"synteny-chr-spacing", 'tab':MATCH}, "value"), Input({'id':"synteny-chr-height", 'tab':MATCH}, "value"), 
                  Input({'id':"synteny-chr-alignment", 'tab':MATCH}, "value"), Input({'id':"synteny-line-position", 'tab':MATCH}, "value")],
                 [State('tabs', 'active_tab'), State("graph-data", "data"), State({'id':"graph", 'tab':MATCH}, "id")],
                 prevent_initial_call = True
    )
    def generate_synteny_graph(selected_genomes, selected_chromosomes, spacing, bar_height, alignment, position_mode, active_tab, graph_data, graph_id):
        print("\ncallback 6: generate_synteny_graph()")                                                      ########## DEBUG
        active_tab = active_tab.split('-')[-1]
        if active_tab in ['home', 'tab']:
            raise PreventUpdate
        if active_tab != graph_id.get('tab'):
            raise PreventUpdate
        gtd = get_triggered_dict(callback_context.triggered)
#        print("active tab: ", active_tab)                                                                    ########## DEBUG
#        print("graph id: ", graph_id.get('tab'))                                                             ########## DEBUG
#        print("triggered: ", gtd)                                                                            ########## DEBUG

        try:
            selected_genomes = selected_genomes[active_tab]
            selected_chromosomes = selected_chromosomes[active_tab]
            tab_data = graph_data[active_tab]
        except:
            raise PreventUpdate

        if not gtd or not selected_genomes or not graph_data or active_tab not in graph_data:
            raise PreventUpdate

        print('    selected genomes: ', selected_genomes)                                                     #############  DEBUG

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