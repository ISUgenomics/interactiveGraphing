from dash import html, dcc
import dash_bootstrap_components as dbc
#from src.options.uploads import opts_inputs
#from src.options.analysis import opts_analysis
#from src.options.graph_general import opts_graph
#from src.options.export import opts_config

# OPTIONS Components assembly

# Define the specific accordion items for the Synteny app
#accordion_items = [
#    dbc.AccordionItem(opts_inputs, title="1. UPLOAD INPUTS", item_id="item-1"),
#    dbc.AccordionItem(opts_analysis, title="2. ADJUST ANALYSIS SETTINGS", item_id="item-2"),
#    dbc.AccordionItem(opts_graph, title="3. GENERAL GRAPH SETTINGS", item_id="item-3"),
#    dbc.AccordionItem(html.Div(), title="4. CUSTOMIZE SYNTENY PLOT", item_id="item-4"),
#    dbc.AccordionItem(opts_config, title="5. EXPORT GRAPH", item_id="item-7", class_name=".container")
#]

# Add the accordion to the optionsDiv
#left_panel.children[1].children.insert(-1,
#    dbc.Accordion(accordion_items, id="accordionA", start_collapsed=True, always_open=True, flush=False)
#)

# Set up the app layout
layout = html.Div([

], id='app', className="d-flex", style={'width':'100%', 'height':'100%', 'overflowY':'hidden'})