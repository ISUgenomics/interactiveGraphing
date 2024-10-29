import json
import dash_bootstrap_components as dbc
from dash import dcc, html, no_update, callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
from plotly.utils import PlotlyJSONEncoder
from src.layout.options import create_left_panel
from src.layout.database import insert_tab, parse_and_insert_content



def register_basic_callbacks(app):

    # Add a new app-tab based on the selected analysis/graphing (at Home tab); make Tabs persistent using storage solution;
    @app.callback([Output('tabs', 'children'), Output('add-app-tab-num', 'data'),                       # tabs & storage
                   Output('optionsDiv', 'children'), Output('left-panel-children', 'data'),             # options & storage
                   Output('graph-panelDiv', 'children'), Output('graph-panel-children', 'data'),        # graphs & storage
                   Output('lower-panelDiv', 'children'), Output('output-panel-children', 'data')],      # outputs & storage
                   Input('add-app-tab', 'n_clicks'),
                  [State('visualizations', 'value'), State('tabs', 'children'), State('add-app-tab-num', 'data'), 
                   State('optionsDiv', 'children'), State('left-panel-children', 'data'), 
                   State('graph-panel-children', 'data'), State('output-panel-children', 'data')],
                   prevent_initial_call = True
    )
    def manage_app_tabs(n_clicks, selected_app, existing_tabs, app_tabs, left_options, left_content, graph_content, output_content):
        print('\ncallback: manage_app_tabs()')                                                                                      ######### DEBUG
        if n_clicks == 0:
            if not len(app_tabs):                           # if tabs register empty, create it based on existing tabs
                return [no_update, existing_tabs, no_update, no_update, no_update, no_update, no_update, no_update]
            elif len(app_tabs) > len(existing_tabs):        # on page reload, display all tabs
                return [app_tabs, no_update, no_update, no_update, no_update, no_update, no_update, no_update]
            else:
                raise PreventUpdate
        if len(app_tabs) >= 10:                                                                                                      # UPGRADE: (optional) use 'disable_n_clicks' to prevent creating more app-tabs than n=10
            raise PreventUpdate

        def find_max_suffix_from_keyword(tabs, keyword):
            matching_values = [tab['props']['tab_id'] for tab in tabs if keyword in tab['props'].get('tab_id', '')]
            if not matching_values:
                return None

            # Extract numerical suffixes from matching tab_id values
            suffixes = [int(value.split('_')[-1]) for value in matching_values if value.split('_')[-1].isdigit()]
            return max(suffixes) if suffixes else None

        found_value = find_max_suffix_from_keyword(existing_tabs, selected_app)
        num = found_value + 1 if found_value else 1

        tab_name = f"{selected_app}_{num}"
        print(f'add new tab: {tab_name}')                                                                                           ########## DEBUG
        new_tab = dbc.Tab(label=tab_name, id={'id':"app-tab-",'tab': tab_name}, tab_id=f"tab-{tab_name}", class_name='index-tab')
        existing_tabs.append(new_tab)
 
        opts = html.Div(children=create_left_panel(tab_name), id={'id':"lopts-",'tab': tab_name}, className='d-none')
        # Insert the tab and the components into the database
        insert_tab(tab_name, tab_name.capitalize().replace('_', ' Tab '), selected_app)
        parse_and_insert_content(tab_name, json.dumps(opts.to_plotly_json(), cls=PlotlyJSONEncoder))                                                                   ########## UPGRADE: improve to make sure the nested structure is complete (same as passed via dcc.Store)
#        print(opts, "\n\n")
#        print(opts.to_dict())
#        print(opts.to_plotly_json())

        if left_content:
            print(len(left_content), '\n\n', left_content)

        left_content.append(opts)
        graph_content.append(html.Div(children=[dcc.Graph(id={'id': "graph", 'tab': tab_name})], id={'id':"graphing-",'tab': tab_name}, className='d-none'))
        output_content.append(html.Div(id={'id': "outputs-", 'tab': tab_name}, className='d-none'))

        return [existing_tabs, existing_tabs, left_content, left_content, graph_content, graph_content, output_content, output_content]


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
            return [[no_update] * len(items), [no_update] * len(items), [no_update] * len(items), 'd-none']
        else:
            tab_name = active_tab.split('-')[-1]
            show_active = ['d-none' if item['tab'] != tab_name else 'd-block' for item in items]
            return [show_active, show_active, show_active, 'd-flex']



