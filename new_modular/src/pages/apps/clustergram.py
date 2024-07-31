from dash import html, dcc
import dash_bootstrap_components as dbc
from src.options.uploads import opts_inputs
from src.options.analysis import opts_analysis
from src.options.graph_general import opts_graph
from src.options.graph_custom import opts_heatmap, opts_dendro, opts_bars
from src.options.export import opts_config
#from src.layout.options import left_panel
#from src.layout.graphing import right_panel

# OPTIONS Components assembly

# Define the specific accordion items for the Clustergram app
#accordion_items = [
#    dbc.AccordionItem(opts_inputs, title="1. UPLOAD INPUTS", item_id="item-1"),
#    dbc.AccordionItem(opts_analysis, title="2. ADJUST ANALYSIS SETTINGS", item_id="item-2"),
#    dbc.AccordionItem(opts_graph, title="3. GENERAL GRAPH SETTINGS", item_id="item-3"),
#    dbc.AccordionItem(opts_heatmap, title="A. CUSTOMIZE HEATMAP", item_id="item-4"),
#    dbc.AccordionItem(opts_dendro, title="B. CUSTOMIZE DENDROGRAMS", item_id="item-5"),
#    dbc.AccordionItem(opts_bars, title="C. CUSTOMIZE CLUSTER BARS", item_id="item-6"),
#    dbc.AccordionItem(opts_config, title="4. EXPORT GRAPH", item_id="item-7", class_name=".container")
#]

# Add the accordion to the optionsDiv
#left_panel.children[1].children.append(
#    dbc.Accordion(accordion_items, id="accordion", start_collapsed=True, always_open=True, flush=False)
#)

# Set up the app layout
layout = html.Div([
#    left_panel,
#    right_panel
], id='app', className="d-flex", style={'width':'100%', 'height':'100%', 'overflowY':'hidden'})