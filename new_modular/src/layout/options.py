from dash import html
import dash_bootstrap_components as dbc
from src.options.uploads import create_opts_inputs
from src.options.analysis import create_opts_analysis
from src.options.graph_general import create_graph_options
from src.options.graph_custom import create_opts_graph_custom
from src.options.export import create_opts_export_config


def create_left_panel(tab_name):
    return [
        dbc.Accordion([
            dbc.AccordionItem(create_opts_inputs(tab_name), title="1. UPLOAD INPUTS", item_id="item-1"),
            dbc.AccordionItem(create_opts_analysis(tab_name), title="2. ADJUST ANALYSIS SETTINGS", item_id="item-2"),
            dbc.AccordionItem(create_graph_options(tab_name), title="3. GENERAL GRAPH SETTINGS", item_id="item-3"),
            dbc.AccordionItem(create_opts_graph_custom(tab_name), title="4. SPECIFIC GRAPH SETTINGS", item_id="item-4"),
            dbc.AccordionItem(create_opts_export_config(tab_name), title="5. EXPORT GRAPH", item_id="item-5", class_name=".container")
        ], id="accordion", always_open=True, flush=False, start_collapsed=True),
        html.Div(id="accordion-contents", className="mt-3"),
    ]