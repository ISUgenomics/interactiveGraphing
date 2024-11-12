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


app_synteny = DjangoDash('Synteny', add_bootstrap_links=True, 
                         external_stylesheets=[dbc.themes.BOOTSTRAP, "/static/assets/custom.css"], 
                         external_scripts = [{'src': '/static/assets/custom.js'}]
                        )

app_synteny.layout = dbc.Container([
#    dcc.Location(id='location', refresh=False),
#    void, identifiers, storage,

        html.Div(id='left-panelDivX', children=[
            html.Button('≡', id='options-synteny', n_clicks=0, style=css_btn),
            html.Div(id='optionsDivX', children=[], style={'marginRight': '1px', 'width': '100%', 'display':'none'})
        ], className='css-lpd'),

        dbc.Accordion([
            dbc.AccordionItem(html.Div(id='graph-panelDiv'), title="DISPLAY INTERACTIVE GRAPHS", item_id="item-12"),
            dbc.AccordionItem(html.Div(id='lower-panelDiv'), title="EXTRACT OUTPUT DATA", item_id="item-13"),
        ], id="accordion", className='data-graph', always_open=True, flush=False, start_collapsed=True),

], id='app-bodyDiv', fluid=True, class_name="px-0")       # style={'width':'100%', 'height':'100%', 'overflowY':'hidden'}

#register_callbacks(app_synteny)

