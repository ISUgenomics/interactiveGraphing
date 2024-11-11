from django_plotly_dash import DjangoDash
from django_plotly_dash.consumers import send_to_pipe_channel


from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from sigloo.apps.src.params.styles import *
from sigloo.apps.src.layout.storage import storage, void, identifiers
from sigloo.apps.src.layout.graphing import right_panel
from sigloo.apps.src.functions.widgets import find_component_ids
from sigloo.apps.src.callbacks import register_callbacks


app = DjangoDash('Synteny', external_stylesheets=["/static/assets/custom.css"], external_scripts = [{'src': '/static/assets/custom.js'}])

app.layout = dbc.Container([
    dcc.Location(id='location', refresh=False),
    void, identifiers, storage,
    html.Div([
        html.Div(id='app-mode', children=[
            html.Div(id='left-panelDiv', children=[
                html.Button('≡', id='options', n_clicks=0, style=css_btn),
                html.Div(id='optionsDiv', children=[], style={'marginRight': '1px', 'width': '100%', 'display':'none'})
            ], className='css-lpd'),
            right_panel
        ], style={'width':'100%', 'height':'100%', 'overflowY':'hidden'}, className='d-none')], id="visible-app", style={'height': 'calc(100vh - 45px)'}),
], fluid=True, class_name="px-0")

register_callbacks(app)

