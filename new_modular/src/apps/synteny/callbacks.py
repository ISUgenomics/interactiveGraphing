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

        if key not in graph_data:
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

            chr_connections.setdefault(chr_1_key, {}).setdefault(genome_2, {"count": 0, "chromosomes": {}})
            chr_connections.setdefault(chr_2_key, {}).setdefault(genome_1, {"count": 0, "chromosomes": {}})
            chr_connections[chr_1_key][genome_2]["count"] += 1
            chr_connections[chr_1_key][genome_2]["chromosomes"].setdefault(chr_2, 0)
            chr_connections[chr_1_key][genome_2]["chromosomes"][chr_2] += 1

            chr_connections[chr_2_key][genome_1]["count"] += 1
            chr_connections[chr_2_key][genome_1]["chromosomes"].setdefault(chr_1, 0)
            chr_connections[chr_2_key][genome_1]["chromosomes"][chr_1] += 1

        # Create sorting for each genome
        sorting_data = {}
        for genome in genome_names:
            genome_chromosomes = list(graph_data[key]["genomes"][genome]["chromosomes"].keys())
            
            # Define original order
            original_order = list(range(len(genome_chromosomes)))

            # Define length-based order
            length_order = sorted(
                range(len(genome_chromosomes)),
                key=lambda idx: graph_data[key]["genomes"][genome]["chromosomes"][genome_chromosomes[idx]]["length"],
                reverse=True
            )

            # Initialize connection and mutual connection sorting structures for each genome
            connections_sorting = {}
            mutual_connections_sorting = {}

            for other_genome in genome_names:
                if other_genome == genome:
                    continue

                # Connections order for this genome relative to `other_genome`
                connections_order = sorted(
                    range(len(genome_chromosomes)),
                    key=lambda idx: (
                        sum(
                            chr_connections.get(f"{genome}:{genome_chromosomes[idx]}", {}).get(other_genome, {}).get("count", 0)
                            for other_genome in chr_connections.get(f"{genome}:{genome_chromosomes[idx]}", {})
                        ),
                        len(chr_connections.get(f"{genome}:{genome_chromosomes[idx]}", {}))
                    ),
                    reverse=True
                )
                connections_sorting[other_genome] = connections_order

                # Mutual connections order (to prioritize chromosomes that share the most connections with chromosomes in other_genome)
                mutual_connections_order = sorted(
                    range(len(genome_chromosomes)),
                    key=lambda idx: (
                        max(chr_connections.get(f"{genome}:{genome_chromosomes[idx]}", {}).get(other_genome, {}).get("chromosomes", {}).values(), default=0),
                        sum(chr_connections.get(f"{genome}:{genome_chromosomes[idx]}", {}).get(other_genome, {}).get("chromosomes", {}).values()),
                        graph_data[key]["genomes"][genome]["chromosomes"][genome_chromosomes[idx]]["length"]
                    ),
                    reverse=True
                )
                mutual_connections_sorting[other_genome] = mutual_connections_order

            # Add all sorting types to the sorting_data for the current genome
            sorting_data[genome] = {
                "original": original_order,
                "length": length_order,
                "connections": connections_sorting,
                "mutual": mutual_connections_sorting
            }

        # Add sorting data to graph_data
        graph_data[key]["sorting"] = sorting_data
        print(graph_data[key]["sorting"])                                                       # DEBUG

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


    @app.callback([Output({'type': 'chr-draggable', 'id': ALL, 'tab': MATCH}, 'children'), Output({'type': 'chr-draggable', 'id': ALL, 'tab': MATCH}, 'layout')], 
                  [Input({'id':'chr-sort', 'tab': MATCH}, 'value'), Input('synteny-genomes-selected', 'data')],
                  [State({'type': 'chr-draggable', 'id': ALL, 'tab': MATCH}, 'children'), State({'type': 'chr-draggable', 'id': ALL, 'tab': MATCH}, 'layout'),
                   State('graph-data', 'data'), State('tabs', 'active_tab')],
    )
    def update_draggable_layout(sorting, selected_genomes, children, layout, graph_data, active_tab):
        print("\ncallback 4B: update_draggable_layout()")                                          ########## DEBUG
        active_tab = active_tab.split('-')[-1] 
        
        if selected_genomes['@changed'] != active_tab or not sorting or not active_tab in selected_genomes:
            raise PreventUpdate
        genomes_selected = selected_genomes[active_tab]
        tab_data = graph_data[active_tab]
        if not genomes_selected or 'sorting' not in tab_data or len(genomes_selected) < 2:
            raise PreventUpdate
        
        updated_children = []
        updated_layouts = []

        gtd = get_triggered_dict(callback_context.triggered)
        print("triggered: ", gtd, active_tab)                                                      ########## DEBUG

        # Determine sorted indexes for each genome in genomes_selected order
        sorted_indexes_all = {}
        for i, genome in enumerate(genomes_selected):
            order = tab_data["sorting"][genome]["original"]
            if i == 0:                                                                            # sort first genome based on the next genome in the list
                next_genome = genomes_selected[i + 1] if len(genomes_selected) > 1 else None
                if sorting == "connections" and next_genome:
                    sorted_indexes_all[genome] = tab_data["sorting"][genome]["connections"].get(
                        next_genome, tab_data["sorting"][genome]["original"])
                elif sorting == "mutual" and next_genome:
                    sorted_indexes_all[genome] = tab_data["sorting"][genome]["mutual"].get(
                        next_genome, tab_data["sorting"][genome]["original"])
                else:
                    sorted_indexes_all[genome] = tab_data["sorting"][genome].get(sorting, order)
            else:                                                                                  # sort subsequent genomes based on the previous genome in the list
                previous_genome = genomes_selected[i - 1]
                if sorting == "connections":
                    sorted_indexes_all[genome] = tab_data["sorting"][genome]["connections"].get(
                        previous_genome, order)
                elif sorting == "mutual":
                    sorted_indexes_all[genome] = tab_data["sorting"][genome]["mutual"].get(
                        previous_genome, order)
                else:
                    sorted_indexes_all[genome] = tab_data["sorting"][genome].get(sorting, order)



        # Iterate over each genome's draggable layout within the active tab
        for genome_children, genome_layout in zip(children, layout):
            genome = genome_children[0]['props']['children']['props']['id']['id']

            # Get sorted indexes for the current genome and sorting type
            if genome in genomes_selected:
                sorted_indexes = sorted_indexes_all[genome]
            else:
                sorted_indexes = tab_data["sorting"][genome]["original"]
            print(genome, sorted_indexes)                                                                                   ########## DEBUG

            # Map each html.Div and layout entry to its `j` index from the id
            children_map = {child['props']['children']['props']['id']['index']: child for child in genome_children}
            layout_map = {layout_item['i'].split('-')[-1]: layout_item for layout_item in genome_layout}

            # Reorder children and layout based on the sorted indexes
            reordered_children = [children_map[j] for j in sorted_indexes]
            reordered_layout = [layout_map[str(j)] for j in sorted_indexes]

            # Update `x` and `y` positions in reordered layout to arrange items in grid format
            grid_width = max(item["w"] for item in reordered_layout)                            # use initial width for column count
            for idx, item in enumerate(reordered_layout):
                item["x"] = idx % grid_width
                item["y"] = idx // grid_width

            updated_children.append(reordered_children)
            updated_layouts.append(reordered_layout)
        return updated_children, updated_layouts



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
                [State("synteny-chromosomes-all", "data"), State("synteny-genomes-all", "data"), State('synteny-chr-selected', 'data'), State('graph-data', 'data'), State('tabs', 'active_tab')],
                 prevent_initial_call = True
    )
    def update_selected_chromosomes(switchers, layouts, chromosomes_all, genomes_all, selected_chromosomes, graph_data, active_tab):
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
            graph_data = graph_data[active_tab]
        except:
            raise PreventUpdate

        switch_values = {}
        layout = {}
        index = {}
        for input_group in callback_context.inputs_list:
            for input_item in input_group:
                input_id = input_item['id']
                genome = input_id.get('id')
                
                if input_id.get('tab') == active_tab:
                    input_type = input_id.get('type')
                    
                    if input_type == 'chr-switch-':
                        switch_values.setdefault(genome, []).append(input_item.get('value'))
                        index.setdefault(genome, []).append(input_id.get('index'))
                        
                    elif input_type == 'chr-draggable':
                        layout[genome] = input_item.get('value')

        if not switch_values or len(genomes_all) != len(layout):
            raise PreventUpdate

        selected_chr = {}
        for genome, dataset in layout.items():
            selected = {chromosomes_all[genome][i] for i, val in zip(index[genome], switch_values[genome]) if val}
            selected_chr[genome] = [chromosome for item in sorted(dataset, key=lambda item: (item['y'], item['x']))
                if (chromosome := chromosomes_all[genome][(ix := int(item['i'].split('-')[-1]))]) in selected
            ]

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
#        position_mode = 'ribbon'
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
        genome_y_positions = {genome: -20 * idx for idx, genome in enumerate(selected_genomes)}

        # Update graph layout
        update_layout(fig, selected_genomes, tab_data, height=bar_height)

        # Calculate and assign x-positions for chromosomes based on selection and ordering
        chromosome_positions, x_range = assign_chromosome_positions(selected_genomes, selected_chromosomes, tab_data, alignment, spacing=spacing)

        fig.update_xaxes(range=x_range)

        # Plot synteny lines only for neighboring selected genomes
        line_traces, shape_traces = create_bezier_synteny_lines(
            tab_data,
            selected_genomes,
            selected_chromosomes,
            chromosome_positions,
            genome_y_positions,
            position_mode=position_mode,
            height=bar_height
        )
        fig.update_layout(shapes=shape_traces)
        fig.add_traces(line_traces)
    #    for trace in line_traces:
    #        fig.add_trace(trace)

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