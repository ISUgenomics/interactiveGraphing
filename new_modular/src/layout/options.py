from dash import html
import dash_bootstrap_components as dbc
from src.params.styles import *

left_panel = html.Div([
    html.Button('Show Options', id='btn-options', n_clicks=0, style=css_btn),
    html.Div(id='optionsDiv', children=[], style={'margin-right': '1px', 'width': '100%'})
], id='left-panelDiv', style=css_lpd)
