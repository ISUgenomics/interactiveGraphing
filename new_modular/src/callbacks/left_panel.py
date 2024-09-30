import pandas as pd
import plotly.colors as pc
import plotly.graph_objs as go
from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from src.functions.io import decode_base64, format_length
from src.functions.graph import get_discrete_colors_from_scale, create_chromosome_bars, get_chromosome_color, get_gradient_colors, bezier_curve

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
        

    # Update Analysis settings options: synteny genomes checkboxes
    @app.callback([Output("graph-data", "data"), Output("synteny-genomes", "options")],
                  Input("synteny-inputs", "value"),
                 [State('user-files-list', 'data'), State('edition-content', 'data'), State('tabs', 'value'), State("graph-data", "data")] 
    )
    def extract_synteny_genomes(df_id, files, edits, active_tab, graph_data):
        if not df_id:
            raise PreventUpdate
        elif '#' in df_id:
            df = pd.DataFrame.from_dict(edits[df_id['data']])
        else:
            df = decode_base64(df_id, files[df_id])
        if not df.empty:
            graph_data[active_tab] = df.to_dict('records')
            genome_names = sorted(set(col.split('_')[0] for col in df.columns if '_' in col))
            options = {key: key for key in genome_names} 
            return [graph_data, options] 
        else:
            raise PreventUpdate


    # Backend calculations for the synteny plot
    @app.callback(Output("graph", "figure"),
                  Input("synteny-genomes", "value"),
                 [State('tabs', 'value'), State("graph-data", "data")] 
    )
    def extract_synteny_genomes(selected, active_tab, graph_data):
        if not selected:
            raise PreventUpdate
        df = pd.DataFrame.from_dict(graph_data[active_tab])
        palette = ["Plotly3_r", "Tealgrn", "solar_r"]
        palette.extend(pc.named_colorscales())

        genomes = {}
        n_chr = 0
        for ix, genome in enumerate(selected):
            len_col = f'{genome}_length'
            if genome in df.columns and len_col in df.columns:
                chromosomes = df.groupby(genome).agg({len_col: 'first'}).reset_index()
                num_chr = len(chromosomes)
                n_chr = num_chr if num_chr > n_chr else n_chr
                colors = get_discrete_colors_from_scale(palette[ix], num_chr)
                genomes[genome] = [{"name": row[genome], "length": row[f'{genome}_length'], "color": colors[i % len(colors)]}
                              for i, (_, row) in enumerate(chromosomes.iterrows())
                ]
        total_length = max(sum(chromosome['length'] for chromosome in genomes[genome]) for genome in genomes)
        factor = 0.05
        spacing = total_length * factor

        columns_to_extract = [col for genome in selected for col in [genome, f"{genome}_start", f"{genome}_end"]]
        ex_synteny = df[columns_to_extract].copy()

        # Initialize lists to collect traces
        bar_traces = []
        line_traces = []
        chromosome_positions = {}
        nx = 20
        step = 1
        y_offset = 0
        chromosome_positions = {}
        genome_lengths = {}

        # Add bars for each genome
        for genome_name, chromosome_data in genomes.items():
            x_positions, widths, colors, names, lengths, formatted_lengths, positions = create_chromosome_bars(chromosome_data, spacing)
            bar_traces.append(go.Bar(
                x=x_positions,
                y=[2 * step] * len(x_positions),
                base=y_offset,
                width=widths,
                marker_color=colors, marker_line_color="black", marker_line_width=1,
                opacity=0.8,
                name=genome_name,
                hovertemplate='<b>%{customdata[0]}</b><br>Length: %{customdata[1]}<extra></extra>',
                customdata=list(zip(names, formatted_lengths))
            ))
            chromosome_positions[genome_name] = positions
            genome_lengths[genome_name] = sum(lengths)
            y_offset -= nx  # Move to the next row for the next genome


        for genome_name, chromosome_data in genomes.items():
            for chromosome in chromosome_data:
                bar_traces.append(go.Bar(
                    x=[chromosome['x_position']],  # Single chromosome x-position
                    y=[2 * step],
                    base=y_offset,
                    width=[chromosome['length']],
                    marker_color=chromosome['color'], marker_line_color="black", marker_line_width=1,
                    opacity=0.8,
                    name=f"{genome_name} - {chromosome['name']}",
                    hovertemplate=f'<b>{chromosome["name"]}</b><br>Length: {chromosome["length"]}<extra></extra>',
                    customdata=[[chromosome['name'], chromosome['length']]]
                ))
            y_offset -= nx  # Move to the next row for the next genome


        # Add synteny lines as Bezier curves
        num_segments = 5
        for index, row in ex_synteny.iterrows():
            print("ROW: ", row)                     ######## DEBUG
            genome_positions = {}
            genome_colors = {}

            # Step 1: Extract positions and colors for all genomes
            print("SELECTED: ", selected)           ############ DEBUG
            print("CHR POSITIONS: ", chromosome_positions)           ############ DEBUG
            for genome in selected:
                genome_start_col = f"{genome.lower()}_start"
                genome_chr_col = f"{genome.lower()}"
                
                # Extract the x position from chromosome_positions and add start offset
                if genome in chromosome_positions and genome_chr_col in row:
                    genome_positions[genome] = chromosome_positions[genome][row[genome_chr_col]] + row[genome_start_col]

                # Get the color of the chromosome
                if genome_chr_col in row:
                    genome_colors[genome] = get_chromosome_color(genomes, genome, row[genome_chr_col])
            
            print("GENOME POSITIONS: ", genome_positions)                           ########
            # Step 2: Add Bezier curves between each pair of consecutive genomes
            for i in range(len(selected) - 1):
                genome_1 = selected[i]
                genome_2 = selected[i + 1]

                # Get the x positions of the genomes
                x1 = genome_positions[genome_1]
                x2 = genome_positions[genome_2]

                y_genome_1 = -i * nx * step
                y_genome_2 = -(i + 1) * nx * step

                # Define control points (adjust as needed for proper visualization)
                control_x1, control_y1 = x1, y_genome_1
                control_x2, control_y2 = x1, (y_genome_1 + y_genome_2) / 2
                control_x3, control_y3 = x2, (y_genome_1 + y_genome_2) / 2
                control_x4, control_y4 = x2, y_genome_2

                # Calculate the Bezier curve
                bezier_x, bezier_y = bezier_curve(control_x1, control_y1, control_x2, control_y2, control_x3, control_y3, control_x4, control_y4)

                # Create hover text dynamically based on genome data
                hover_text = f'<b>{genome_1}:</b> {row[genome_1.lower()]}<br>' \
                            f'start: {row[genome_1.lower() + "_start"]}, end: {row[genome_1.lower() + "_end"]}<br>' \
                            f'<b>{genome_2}:</b> {row[genome_2.lower()]}<br>' \
                            f'start: {row[genome_2.lower() + "_start"]}, end: {row[genome_2.lower() + "_end"]}'

                # Get the gradient colors between two genomes
                color_1 = genome_colors[genome_1]
                color_2 = genome_colors[genome_2]
                colors = get_gradient_colors(color_1, color_2, num_segments)
                segment_length = len(bezier_x) // num_segments
                for i in range(num_segments):
                    segment_x = bezier_x[i * segment_length:(i + 1) * segment_length + 1]
                    segment_y = bezier_y[i * segment_length:(i + 1) * segment_length + 1]
                    line_traces.append(go.Scatter(
                        x=segment_x,
                        y=segment_y,
                        mode='lines',
                        opacity=0.9,
                        line=dict(color=colors[i], width=1),
                        showlegend=False,
                        hoverinfo='text',
                        text=hover_text
                    ))


        # Create the figure
        fig = go.Figure()
        # Add a dummy trace to use y2
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            showlegend=False,
            yaxis="y2"
        ))

        # Add all line traces (synteny lines) dynamically
        for trace in line_traces:
            fig.add_trace(trace)

        # Add all bar traces (representing chromosomes) dynamically
        for trace in bar_traces:
            fig.add_trace(trace)

        # Calculate dynamic properties based on the number of genomes in `selected`
        num_genomes = len(selected)
        yaxis_tickvals = []
        yaxis_ticktext = []
        yaxis2_tickvals = []
        yaxis2_ticktext = []

        for idx, genome in enumerate(selected):
            y_position = -idx * nx * step
            yaxis_tickvals.append(y_position + 1)
            yaxis_ticktext.append(genome)
            yaxis2_tickvals.append(y_position + 1)
            yaxis2_ticktext.append(format_length(genome_lengths[genome]))

        # Set the range for y-axis
        yaxis_range = [-num_genomes * nx * step, step * 2]

        # Update the layout to accommodate multiple genomes
        fig.update_layout(
            height=600,
            plot_bgcolor='white',
            title='Chromosome Visualization',
            showlegend=True,
            xaxis_title='',
            xaxis=dict(
                showticklabels=False
            ),
            yaxis=dict(
                tickvals=yaxis_tickvals,
                ticktext=yaxis_ticktext,
                title='Genomes',
                showticklabels=True,
                tickfont=dict(size=16),
                range=yaxis_range
            ),
            yaxis2=dict(
                tickvals=yaxis2_tickvals,
                ticktext=yaxis2_ticktext,
                title='Genome Length',
                overlaying='y',
                side='right',
                showticklabels=True,
                range=yaxis_range,
                tickfont=dict(size=14)
            ),
            legend=dict(
                x=1.042,
                y=0.88
            ),
            bargap=factor,
            barcornerradius=5,
        )

        # Update x-axis range dynamically to match the chromosomes' span
        fig.update_xaxes(range=[-spacing, total_length + ((n_chr - 1) * spacing)])

        return fig