import json
import dash_bootstrap_components as dbc
from dash import dcc, html, no_update, callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
from plotly.utils import PlotlyJSONEncoder
from sigloo.apps.src.layout.options import create_left_panel
#from sigloo.apps.src.layout.database import insert_tab, parse_and_insert_content



def register_basic_callbacks(app):



    # Manage the visibility of options for a currently viewed graphing app; also display/hide the entire app-mode view
    @app.callback([Output({'id': 'lopts-', 'tab': ALL}, 'className'), Output({'id': 'graphing-', 'tab': ALL}, 'className'), Output({'id': 'outputs-', 'tab': ALL}, 'className'), 
                   Output('app-mode', 'className')],
                   Input('tabs', 'active_tab'),
                  [State({'id': 'lopts-', 'tab': ALL}, 'id')],
                   prevent_initial_call = True
    )
    def manage_opts_display(active_tab, items):
        if not callback_context.triggered:
            raise PreventUpdate
        if active_tab == 'tab-home' or active_tab == 'tab-about':
            return [[no_update] * len(items), [no_update] * len(items), [no_update] * len(items), 'd-flex']
        else:
            tab_name = active_tab.split('-')[-1]
            show_active = ['d-none' if item['tab'] != tab_name else 'd-block' for item in items]
            return [show_active, show_active, show_active, 'd-flex']



