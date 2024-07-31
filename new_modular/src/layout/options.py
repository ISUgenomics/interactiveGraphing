from dash import html
import dash_bootstrap_components as dbc
from src.params.styles import *
from src.options.uploads import opts_inputs
from src.options.analysis import opts_analysis
from src.options.graph_general import opts_graph
from src.options.graph_custom import opts_graph_types
from src.options.export import opts_config

left_panel = html.Div([
    html.Button('Show Options', id='options', n_clicks=0, style=css_btn),
    html.Div(id='optionsDiv', children=[
        dbc.Accordion([
            dbc.AccordionItem(opts_inputs, title="1. UPLOAD INPUTS", item_id="item-1"),
            dbc.AccordionItem(opts_analysis, title="2. ADJUST ANALYSIS SETTINGS", item_id="item-2"),
            dbc.AccordionItem(opts_graph, title="3. GENERAL GRAPH SETTINGS", item_id="item-3"),
            dbc.AccordionItem(opts_graph_types, title="4. SPECIFIC GRAPH SETTINGS", item_id="item-4"),
            dbc.AccordionItem(opts_config, title="5. EXPORT GRAPH", item_id="item-5", class_name=".container")            
        ], id="accordion", always_open=True, flush=False, start_collapsed=True), #,active_item="item-4"
        html.Div(id="accordion-contents", className="mt-3"),
    ], style={'marginRight': '1px', 'width': '100%'})
], id='left-panelDiv', style=css_lpd)
