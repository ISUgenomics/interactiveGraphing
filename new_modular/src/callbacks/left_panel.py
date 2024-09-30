import pandas as pd
import plotly.colors as pc
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from src.functions.io import decode_base64, format_length
from src.functions.graph import load_dataframe, extract_genome_names, process_chromosomes, generate_synteny_lines, create_genome_options, create_chromosome_traces, filter_synteny_lines, create_synteny_line_traces, update_layout 

from src.options.analysis import synteny


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


    # Update Analysis settings options
    @app.callback(Output("opts-analysis", "children"),
                  Input('tabs', 'value'),
    )
    def update_analysis_opts(active_tab):
        if active_tab == 'tab-home' or active_tab == 'tab-about':
            raise PreventUpdate
        else:
            var_name = active_tab.split('_')[0].split('-')[1]
            if var_name in globals():
                return globals()[var_name]
            else:
                return html.Label(f"No analysis settings available for {var_name} plot type.", className="label-s")
            

    # Update Analysis settings options: synteny input dropdown
    @app.callback(Output("synteny-inputs", "options"),
                  Input("opts-analysis", "children"),
                 [State('user-files-list', 'data'), State('edition-content', 'data'), State("synteny-inputs", "options")]
    )
    def update_synteny_inputs(opts_analysis, files, edits, current):
        if not current:
            df_ids = sorted(set(files.keys()).union(edits.keys()))
            return df_ids
        else:
            return current
        

    # Backend calculations for the synteny plot; Update Analysis settings options: synteny genomes checkboxes
    @app.callback(
        [Output("graph-data", "data"), Output("synteny-genomes", "options")],
        Input("synteny-inputs", "value"),
        [State('user-files-list', 'data'), State('edition-content', 'data'), State('tabs', 'value'), State("graph-data", "data")] 
    )
    def extract_synteny_genomes(df_id, files, edits, active_tab, graph_data):
        if not df_id:
            raise PreventUpdate

        df = load_dataframe(df_id, files, edits)
        if df.empty:
            raise PreventUpdate

        if graph_data is None:
            graph_data = {}

        # Initialize graph data for the active tab if it doesn't exist
        graph_data[active_tab] = {
            "genomes": {},
            "synteny_lines": []
        }

        genome_names = extract_genome_names(df)

        # Generate colors for each genome
        palette = ["Tealgrn", "solar_r", "Plotly3_r"]
        palette.extend(px.colors.named_colorscales())

        for ix, genome in enumerate(genome_names):
            genome_data = process_chromosomes(df, genome, ix, palette[ix], spacing=0.2)
            graph_data[active_tab]["genomes"][genome] = genome_data

        synteny_lines = generate_synteny_lines(df, genome_names, graph_data[active_tab])
        graph_data[active_tab]["synteny_lines"] = synteny_lines

        # Create options for synteny-genomes UI
        options = [{"label": name, "value": name} for name in genome_names]

        return [graph_data, options]




    # Generate synteny plot
    @app.callback(
        Output("graph", "figure"),
        Input("synteny-genomes", "value"),
        [State('tabs', 'value'), State("graph-data", "data")]
    )
    def generate_synteny_graph(selected_genomes, active_tab, graph_data):
        if not selected_genomes or not graph_data or active_tab not in graph_data:
            raise PreventUpdate

        tab_data = graph_data[active_tab]
        bar_height = 3                      ####### UPDATE: pass as user selected value 

        fig = go.Figure()
        # Add a dummy trace to force the use of y2 (displays total genome length)
        fig.add_trace(go.Scatter(x=[None], y=[None], showlegend=False, yaxis="y2"))

        # Ensure user-selected genomes order is respected: track y-offset for genomes
        genome_y_positions = {}
        for idx, genome in enumerate(selected_genomes):
            genome_y_positions[genome] = -20 * idx

        # Update graph layout
        update_layout(fig, selected_genomes, tab_data, height=bar_height)

        # Plot synteny lines for all neighboring genomes
        line_traces = create_synteny_line_traces(tab_data["synteny_lines"], selected_genomes, genome_y_positions, tab_data, height=bar_height)
        for trace in line_traces:
            fig.add_trace(trace)

        # Plot chromosomes for each selected genome
        for genome in selected_genomes:
            if genome in tab_data["genomes"]:
                genome_data = tab_data["genomes"][genome]
                chromosome_traces = create_chromosome_traces(genome, genome_data, genome_y_positions[genome], height=bar_height)
                for trace in chromosome_traces:
                    fig.add_trace(trace)

        return fig