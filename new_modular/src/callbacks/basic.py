import dash_bootstrap_components as dbc
from dash import dcc, html, no_update, callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
from src.layout.options import create_left_panel
from src.pages.config import visualizations
from src.pages.apps import synteny, clustergram


def register_basic_callbacks(app):

    # Add a new app-tab based on the selected analysis/graphing (at Home tab); make Tabs persistent using storage solution;
    @app.callback([Output('tabs', 'children'), Output('add-app-tab-num', 'data'), Output('optionsDiv', 'children'), Output('left-panel-children', 'data')],
                   Input('add-app-tab', 'n_clicks'),
                  [State('tabs', 'children'), State('visualizations', 'value'), State('add-app-tab-num', 'data'), State('left-panel-children', 'data')]
    )
    def manage_app_tabs(n_clicks, existing_tabs, selected_app, app_tabs, left_content):
#        print(n_clicks, len(existing_tabs), len(app_tabs), existing_tabs[0])                                                          ######### DEBUG
        if n_clicks == 0:
            if not len(app_tabs):
                return [no_update, existing_tabs, left_content, left_content]
            elif len(app_tabs) > len(existing_tabs):
                return [app_tabs, no_update, left_content, left_content]
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
        new_tab = dbc.Tab(label=tab_name, id={'type':"app-tab-",'id': tab_name}, tab_id=f"tab-{tab_name}", class_name='index-tab')
        existing_tabs.append(new_tab)

        left_content.append(html.Div(children=create_left_panel(tab_name), id={'type':"lopts-",'id': tab_name}, className='d-none'))

        return [existing_tabs, existing_tabs, left_content, left_content]


    # Manage the visibility of options for a currently viewed graphing app; also display/hide the entire app-mode view
    @app.callback([Output({'type': 'lopts-', 'id': ALL}, 'className'), Output('app-mode', 'className')],
                  Input('tabs', 'active_tab'),
                 [State({'type': 'lopts-', 'id': ALL}, 'id')]
    )
    def manage_opts_display(active_tab, items):
        if not callback_context.triggered:
            raise PreventUpdate
        if active_tab == 'tab-home' or active_tab == 'tab-about':
            return [[no_update] * len(items), 'd-none']
        else:
            tab_name = active_tab.split('-')[-1]
            hidden = ['d-none' if item['id'] != tab_name else 'd-block' for item in items]
            return [hidden, 'd-flex']



