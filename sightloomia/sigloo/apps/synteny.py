from django_plotly_dash import DjangoDash
from django_plotly_dash.consumers import send_to_pipe_channel

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from sigloo.apps.src.params.styles import *
from sigloo.apps.src.layout.storage import storage, void, identifiers
from sigloo.apps.src.functions.widgets import find_component_ids
from sigloo.apps.src.callbacks import register_callbacks
from sigloo.apps.src.layout.options import create_left_panel


app_name = 'synteny'

app_synteny = DjangoDash(app_name.capitalize(), serve_locally=True, add_bootstrap_links=True, 
                         external_stylesheets=[dbc.themes.BOOTSTRAP, "/static/assets/custom.css"], 
                         external_scripts = [{'src': '/static/assets/custom.js'}]
                        )

app_synteny.layout = dbc.Container([
#    dcc.Location(id='location', refresh=False),
    void, identifiers, storage,

        html.Div(id='left-panelDiv', children=[
            html.Button('≡', id='options-btn', n_clicks=0, style=css_btn),
            html.Div(id='optionsDiv', children=create_left_panel(app_name), style={'marginRight': '1px', 'width': '100%', 'display':'none', 'overflowY':'auto'})
        ], className='css-lpd'),

        dbc.Accordion([
            dbc.AccordionItem(html.Div(id='graph-panelDiv'), title="DISPLAY INTERACTIVE GRAPHS", item_id="item-12"),
            dbc.AccordionItem(html.Div(id='lower-panelDiv'), title="EXTRACT OUTPUT DATA", item_id="item-13"),
        ], id="data-graph", className='data-graph', always_open=True, flush=False, start_collapsed=True),

        dcc.Dropdown(['NYC', 'MTL', 'SF'], 'MTL', id='demo-dropdown', className="ml-5 mt-10 w-25", style={'top': '200px', 'position': 'relative'}, persistence=True, persistence_type='session'), #
        html.Div(id="output-two", className="ml-5 mt-10 pt-20 t-20", style={'top': '200px', 'position': 'relative'})


], id='app-bodyDiv', fluid=True, class_name="px-0")       # style={'width':'100%', 'height':'100%', 'overflowY':'hidden'}



# GENERAL: toogle option sidebar
app_synteny.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            window.dash_clientside.clientside.toggleSidebar(n_clicks);
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("options-btn", "n_clicks"),
    Input("options-btn", "n_clicks")
)


#register_callbacks(app_synteny)

@app_synteny.expanded_callback(
    Output('output-two', 'children'),
    [Input('demo-dropdown', 'value')]
    )
def callback_c(*args, **kwargs):
    'Update the output following a change of the input selection'
    #da = kwargs['dash_app']

#    session_state = kwargs['session_state']

#    calls_so_far = session_state.get('calls_so_far', 0)
#    session_state['calls_so_far'] = calls_so_far + 1

#    user_counts = session_state.get('user_counts', None)
#    user_name = str(kwargs['user'])
#    if user_counts is None:
#        user_counts = {user_name:1}
#        session_state['user_counts'] = user_counts
#    else:
#        user_counts[user_name] = user_counts.get(user_name, 0) + 1

    return "Args are [%s] and kwargs are %s" %(",".join(args), str(kwargs))