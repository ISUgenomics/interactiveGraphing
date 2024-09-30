import numpy as np
import matplotlib.colors as mcolors
import plotly.express as px
from src.functions.io import format_length

###------ SYNTENY PLOT ------###

# Function to create x positions and widths for the bars
def create_chromosome_bars(chromosomes, spacing):
    x_positions = []
    widths = []
    colors = []
    names = []
    lengths = []
    formatted_lengths = []
    positions = {}
    x_offset = 0
    for chromosome in chromosomes:
        x_positions.append(x_offset + chromosome['length'] / 2)
        widths.append(chromosome['length'])
        colors.append(chromosome['color'])
        names.append(chromosome['name'])
        lengths.append(chromosome['length'])
        formatted_lengths.append(format_length(chromosome['length']))
        positions[chromosome['name']] = x_offset
        x_offset += chromosome['length'] + spacing
    return x_positions, widths, colors, names, lengths, formatted_lengths, positions

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

# Function to convert 'rgb(r,g,b)' to a normalized tuple
def rgb_string_to_normalized_tuple(color_string):
    if color_string.startswith('rgb'):
        rgb_tuple = tuple(map(int, color_string.strip('rgb()').split(',')))
        return tuple(c / 255 for c in rgb_tuple)
    else:
        return mcolors.to_rgba(color_string)[:3]

# Function to interpolate colors [SYNTENY CURVES]
def interpolate_color(start_color, end_color, factor: float):
    start_color = np.array(rgb_string_to_normalized_tuple(start_color))
    end_color = np.array(rgb_string_to_normalized_tuple(end_color))
    return mcolors.to_hex((1 - factor) * start_color + factor * end_color)

# Function to get gradient colors
def get_gradient_colors(start_color, end_color, num_segments):
    return [interpolate_color(start_color, end_color, i / (num_segments - 1)) for i in range(num_segments)]

# Function to generate N discrete colors from a continuous color scale [CHROMOSOMES]
def get_discrete_colors_from_scale(colorscale, num_colors):
    colors = [mcolors.to_hex(rgb_string_to_normalized_tuple(c)) for c in px.colors.sample_colorscale(colorscale, num_colors + 10)]
    colors = colors[6:-4]
    return colors


###------ X PLOT ------###