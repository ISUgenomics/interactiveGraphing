import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objs as go
from src.functions.io import decode_base64, format_length




###------ GENERAL ------###



###------ SYNTENY PLOT ------###


def load_dataframe(df_id, files, edits):
    if '#' in df_id and df_id in edits:
        return pd.DataFrame.from_dict(edits[df_id].get('data', {}))
    elif df_id in files:
        return decode_base64(df_id, files[df_id])
    else:
        raise KeyError(f"Key '{df_id}' not found.")


def split_text_by_length(text, max_length=200, delimiter=", "):
    parts = text.split(delimiter)
    result = []
    current_line = ""
    for part in parts:
        if len(current_line) + len(part) + len(delimiter) <= max_length:
            if current_line:
                current_line += delimiter + part
            else:
                current_line = part
        else:
            result.append(current_line)
            current_line = part

    # Append the last line if it exists
    if current_line:
        result.append(current_line)

    return result


# Function to convert 'rgb(r,g,b)' to a normalized tuple
def rgb_string_to_normalized_tuple(color_string):
    if color_string.startswith('rgb'):
        rgb_tuple = tuple(map(int, color_string.strip('rgb()').split(',')))
        return tuple(c / 255 for c in rgb_tuple)
    else:
        return mcolors.to_rgba(color_string)[:3]


# Function to generate N discrete colors from a continuous color scale [CHROMOSOMES]
def get_discrete_colors_from_scale(colorscale, num_colors):
    colors = [mcolors.to_hex(rgb_string_to_normalized_tuple(c)) for c in px.colors.sample_colorscale(colorscale, num_colors + 10)]
    colors = colors[6:-4]
    return colors


def extract_genome_names(df):
    return sorted(set(col.split('_')[0] for col in df.columns if '_' in col))


def process_chromosomes(df, genome):
    len_col = f'{genome}_length'
    if genome not in df.columns or len_col not in df.columns:
        return None

    # Group by chromosome and get the first length value for each
    chromosomes = df.groupby(genome).agg({len_col: 'first'}).reset_index()

    # Create genome data structure without assigning positions initially
    genome_data = {"chromosomes": {}, "total_length": 0}

    # Assign a color palette for the chromosomes
    num_chr = len(chromosomes)
    colors = get_discrete_colors_from_scale("viridis", num_chr)

    # Populate genome data with chromosome information (length, color, name)
    for i, (_, row) in enumerate(chromosomes.iterrows()):
        chr_name = row[genome]
        chr_length = pd.to_numeric(row[len_col], errors='coerce')
        chr_color = colors[i % len(colors)]

        genome_data["chromosomes"][chr_name] = {
            "name": chr_name,
            "length": chr_length,
            "color": chr_color,  # Ensure each chromosome gets a color
            "position": None  # Position will be calculated later dynamically
        }

        genome_data["total_length"] += chr_length

    return genome_data



def generate_synteny_lines(df, genome_names, graph_data):
    synteny_lines = []

    for index, row in df.iterrows():
        for i in range(len(genome_names)):
            for j in range(i + 1, len(genome_names)):
                genome_1 = genome_names[i]
                genome_2 = genome_names[j]

                chr_1 = row[genome_1]
                chr_2 = row[genome_2]

                if chr_1 not in graph_data["genomes"][genome_1]["chromosomes"] or \
                   chr_2 not in graph_data["genomes"][genome_2]["chromosomes"]:
                    continue

                # Retrieve chromosome data for both genomes
                chr_1_data = graph_data["genomes"][genome_1]["chromosomes"][chr_1]
                chr_2_data = graph_data["genomes"][genome_2]["chromosomes"][chr_2]

                start_1 = row[f"{genome_1}_start"]
                start_2 = row[f"{genome_2}_start"]

                # Store synteny line data without absolute positions
                synteny_lines.append({
                    "genome_1": genome_1,
                    "chr_1": chr_1,
                    "start_1": start_1,
                    "end_1": row[f"{genome_1}_end"],
                    "chr_1_length": chr_1_data["length"],
                    "genome_2": genome_2,
                    "chr_2": chr_2,
                    "start_2": start_2,
                    "end_2": row[f"{genome_2}_end"],
                    "chr_2_length": chr_2_data["length"],
                    "color_1": chr_1_data["color"],
                    "color_2": chr_2_data["color"]
                })

    return synteny_lines


def assign_chromosome_positions(selected_genomes, selected_chromosomes, tab_data, alignment="left", spacing=0.1):
    chromosome_positions = {}
    max_genome_length = 0
    genome_lengths = {}
    genome_data = {}
    chromosomes = {}

    # Step 1: Identify the maximum genome length and calculate lengths with spacing
    for genome in selected_genomes:
        genome_data[genome] = tab_data["genomes"][genome]["chromosomes"]
        chromosomes[genome] = selected_chromosomes.get(genome, genome_data.keys())
        num_chromosomes = len(chromosomes[genome])

        total_length = 0
        total_length = sum(genome_data[genome][chr_name]["length"] for chr_name in chromosomes[genome])
        genome_lengths[genome] = total_length
        total_spacing = (num_chromosomes - 1) * (spacing * total_length)
        total_length_with_spacing = total_length + total_spacing

        if total_length_with_spacing > max_genome_length:
            max_genome_length = total_length_with_spacing
            consistent_spacing = spacing * total_length
            reference_genome = genome

    # Step 2: Assign chromosome positions based on the selected alignment
    for genome in selected_genomes:
        block_spacing = consistent_spacing
        if genome == reference_genome:                              # assign positions for the reference genome (same for any alignment)
            x_offset = 0
        else:
            num_chromosomes = len(chromosomes[genome])
            total_spacing = (num_chromosomes - 1) * consistent_spacing

            alignment_offsets = {
                "left": 0,                                                                      # all genomes start at 0
                "center": (max_genome_length - genome_lengths[genome] - total_spacing) / 2,     # center all genomes in relation to reference genome
                "right": max_genome_length - genome_lengths[genome] - total_spacing,            # align all genomes to the right
                "block": 0                                                                      # distribute chromosomes evenly across the full x range
            }
            x_offset = alignment_offsets.get(alignment, 0)

            if alignment == "block":                                                            # calculate the spacing dynamically per genome
                block_spacing = (max_genome_length - genome_lengths[genome]) / (num_chromosomes - 1) if num_chromosomes > 1 else 0

        # Assign positions for chromosomes in the current genome
        for chr_name in chromosomes[genome]:
            chr_length = genome_data[genome][chr_name]["length"]
            chromosome_positions[(genome, chr_name)] = x_offset
            x_offset += chr_length + block_spacing

    # Step 3: Define the x-axis range
    x_range = [-consistent_spacing, max_genome_length + consistent_spacing]                     # defined relative to the reference genome with a small buffer

    return chromosome_positions, x_range



def create_genome_options(genome_names):
    return [{"label": name, "value": name} for name in genome_names]


def create_chromosome_traces(genome_name, genome_data, chromosomes_to_plot, chromosome_positions, y_offset, graph_data, active_tab, height=2):
    traces = []
    chr_connections = graph_data[active_tab]["chr_connections"]

    # Iterate over selected chromosomes and create bar traces
    for chr_name in chromosomes_to_plot:
        chromosome = genome_data["chromosomes"][chr_name]
        legend_group = f"{genome_name}_{chr_name}"                                              # unique identifier for legend group
        x_pos = chromosome_positions[(genome_name, chr_name)] + chromosome["length"] / 2        # center of the bar

        chr_key = f"{genome_name}:{chr_name}"
        connections = chr_connections.get(chr_key, {})
        connection_info = []
        for connected_genome, details in connections.items():
            if isinstance(details, dict) and "count" in details and "chromosomes" in details:
                count = details["count"]
                connected_chromosomes = details["chromosomes"]
                text_chunks = split_text_by_length(", ".join(connected_chromosomes), max_length=50)
                text_formatted = "<br>".join(text_chunks)
                connection_info.append(f"Synteny to {connected_genome}: {count}<br>{text_formatted}")
        synteny_info = "<br><br>".join(connection_info) if connection_info else "Synteny Connections: 0"

        trace = go.Bar(
            x=[x_pos],   # center of the bar
            y=[height],  # constant height for chromosomes
            base=y_offset,
            width=[chromosome["length"]],
            marker_color=chromosome["color"],
            marker_line_color="black",
            marker_line_width=1,
            opacity=0.8,
            name=f"{genome_name} - {chr_name}",
            hovertemplate=f'<b>{chr_name}</b><br>Length: {chromosome["length"]}<br><br>{synteny_info}<extra></extra>',
            customdata=[[chr_name, chromosome["length"]]],
            legendgroup=legend_group
        )
        traces.append(trace)

    return traces



def create_bezier_synteny_lines(synteny_lines, selected_genomes, selected_chromosomes, chromosome_positions, genome_y_positions, position_mode="exact", height=2):
    line_traces = []
    num_segments = 5

    # Iterate over selected genomes and create synteny lines for neighboring pairs
    for i in range(len(selected_genomes) - 1):
        genome_1 = selected_genomes[i]
        genome_2 = selected_genomes[i + 1]

        # Filter synteny lines for the current neighboring genomes
        for line in synteny_lines:
            # Check if the line corresponds to the current pair of neighboring genomes, in any order
            if (line["genome_1"] == genome_1 and line["genome_2"] == genome_2) or \
               (line["genome_1"] == genome_2 and line["genome_2"] == genome_1):
                
                # Ensure that the chromosomes involved in the line are currently selected
                if line["chr_1"] not in selected_chromosomes.get(line["genome_1"], []) or \
                   line["chr_2"] not in selected_chromosomes.get(line["genome_2"], []):
                    continue
                
                # Get positions of the chromosomes from chromosome_positions
                chr_1_start_position = chromosome_positions.get((line["genome_1"], line["chr_1"]))
                chr_2_start_position = chromosome_positions.get((line["genome_2"], line["chr_2"]))

                # Skip if chromosome positions are not available (could happen if chromosomes were not properly selected)
                if chr_1_start_position is None or chr_2_start_position is None:
                    continue

                # Calculate start positions based on the position_mode
                if position_mode == "exact":
                    # Use exact start positions from the data
                    start_1_position = int(chr_1_start_position) + int(line["start_1"])
                    start_2_position = int(chr_2_start_position) + int(line["start_2"])
                elif position_mode == "middle":
                    # Use the middle position of the chromosome segment
                    start_1_position = chr_1_start_position + (line["chr_1_length"] / 2)
                    start_2_position = chr_2_start_position + (line["chr_2_length"] / 2)
                else:
                    raise ValueError("Invalid position_mode. Must be 'exact' or 'middle'.")

                # Extract y-offsets based on the current genome positions
                y1 = genome_y_positions[line["genome_1"]]
                y2 = genome_y_positions[line["genome_2"]]

                # Adjust y positions to avoid overlap; height is added to ensure the curve reaches the right height
                y1, y2 = (y1 + height, y2) if y1 < y2 else (y1, y2 + height)

                # Create Bezier curve points for a smooth line between the chromosomes
                bezier_x, bezier_y = bezier_curve(start_1_position, y1, start_1_position, (y1 + y2) / 2, start_2_position, (y1 + y2) / 2, start_2_position, y2)

                # Create gradient colors between start and end
                colors = get_gradient_colors(line["color_1"], line["color_2"], num_segments)

                # Split the Bezier curve into segments for gradient coloring
                segment_length = len(bezier_x) // num_segments
                for j in range(num_segments):
                    # Segment the curve for gradient effect
                    segment_x = bezier_x[j * segment_length:(j + 1) * segment_length + 1]
                    segment_y = bezier_y[j * segment_length:(j + 1) * segment_length + 1]
                    legend_group = f"{line['genome_1']}_{line['chr_1']}"  # Use the same legend group as chromosomes

                    # Create scatter trace for each segment
                    trace = go.Scatter(
                        x=segment_x,
                        y=segment_y,
                        mode='lines',
                        opacity=0.8,
                        line=dict(color=colors[j], width=1),
                        showlegend=False,
                        hoverinfo='text',
                        text=f"<b>{line['genome_1']} - {line['chr_1']}</b>: {line['start_1']} to {line['end_1']}<br>"
                             f"<b>{line['genome_2']} - {line['chr_2']}</b>: {line['start_2']} to {line['end_2']}",
                        legendgroup=legend_group
                    )
                    line_traces.append(trace)

    return line_traces



def update_layout(fig, selected_genomes, tab_data, height=2, spacing=0.1):
    num_genomes = len(selected_genomes)
    yaxis_tickvals = [-20 * i + (height/2) for i in range(num_genomes)]
    yaxis_ticktext = [f"{genome.capitalize()}  " for genome in selected_genomes]
    yaxis2_tickvals = yaxis_tickvals
    yaxis2_ticktext = [f'  {format_length(tab_data["genomes"][genome]["total_length"])}' for genome in selected_genomes]

    max_genome = max(selected_genomes, key=lambda genome: tab_data["genomes"][genome]["total_length"])              ##### UPDATE: can be moved to higher-level code and passed as an argument
    max_len = tab_data["genomes"][max_genome]["total_length"]                                                       #####
    chromosomes = tab_data["genomes"][max_genome]["chromosomes"]                                                    #####
    num_chr = len(set(chromosomes.keys()))                                                                          #####

    fig.update_layout(
        height=240 + 50 * num_genomes,
        width=1200,  # Fixed width to ensure enough space for all components
        plot_bgcolor='white',
        title={'text':'Synteny Visualization', 'x':0.4, 'xanchor':'center', 'yanchor':'top', 'y':0.95},
        showlegend=True,
        xaxis=dict(
            range=[-0.005 * max_len, (num_chr/8.5 * spacing + 1) * max_len],
            title='Position',
            title_standoff=0,
            showticklabels=False
        ),
        yaxis=dict(
            title='Genomes',
            tickvals=yaxis_tickvals,
            ticktext=yaxis_ticktext,
            titlefont=dict(size=16, color='navy'),
            tickfont=dict(size=14, color='black'),
            range=[-14 * num_genomes, 10],
            showgrid=False,
            zeroline=False,
            automargin=True
        ),
        yaxis2=dict(
            title='Genome Length',
            tickvals=yaxis2_tickvals,
            ticktext=yaxis2_ticktext,
            titlefont=dict(size=16, color='navy'),
            tickfont=dict(size=14, color='black'),
            range=[-14 * num_genomes, 10],
            overlaying='y',  # Overlay on the main y-axis
            side='right',
            showticklabels=True,
        ),
        barcornerradius=5,
        legend=dict(
            x=1.13,
            y=0.5,
            yanchor='middle',
            title='Chromosome Legend'
        ),
        margin=dict(
            l=90,  # Increase left margin for better visibility of genome names
            r=60,  # Increase right margin to allow room for genome length labels
            t=30,
            b=20
        )
    )









#-------




# Function to calculate cubic Bezier points [SYNTENY CURVES]
def bezier_curve(x1, y1, x2, y2, x3, y3, x4, y4, num_points=100):
    t = np.linspace(0, 1, num_points)
    x = (1-t)**3 * x1 + 3*(1-t)**2 * t * x2 + 3*(1-t) * t**2 * x3 + t**3 * x4
    y = (1-t)**3 * y1 + 3*(1-t)**2 * t * y2 + 3*(1-t) * t**2 * y3 + t**3 * y4
    return x, y

# Function to find the color of a chromosome [SYNTENY CURVES]
def get_chromosome_color(genomes, genome, chromosome_name):
    for chromosome in genomes[genome]:
        if chromosome['name'] == chromosome_name:
            return chromosome['color']
    return 'black'  # Default color if not found



# Function to interpolate colors [SYNTENY CURVES]
def interpolate_color(start_color, end_color, factor: float):
    start_color = np.array(rgb_string_to_normalized_tuple(start_color))
    end_color = np.array(rgb_string_to_normalized_tuple(end_color))
    return mcolors.to_hex((1 - factor) * start_color + factor * end_color)

# Function to get gradient colors
def get_gradient_colors(start_color, end_color, num_segments):
    return [interpolate_color(start_color, end_color, i / (num_segments - 1)) for i in range(num_segments)]




###------ X PLOT ------###