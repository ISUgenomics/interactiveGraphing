import dash_bootstrap_components as dbc
from dash import dcc, html, no_update
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from src.pages import index, about
from src.pages.apps import synteny, clustergram
from src.pages.config import visualizations

def register_basic_callbacks(app):
    # Decide on the layout displayed depending on the selected app tab
    @app.callback([Output('info-mode', 'children'), Output('app-mode', 'style'), Output('info-mode', 'hidden')],
                  [Input('tabs', 'value')])
    def render_content(tab):
        if tab == 'tab-home':
            return index.layout, {"display": "none"}, False
        elif tab == 'tab-about':
            return about.layout, {"display": "none"}, False
        else:
            return no_update, {'width':'100%', 'height':'100%', 'overflow-y':'hidden', "display": "flex"}, True

    # Add a new app-tab based on the selected analysis/graphing (at Home tab); make Tabs persistent using storage solution;        # UPGRADE: (optional) use 'disable_n_clicks' to prevent creating more app-tabs than n=10
    @app.callback([Output('tabs', 'children'), Output('add-app-tab-num', 'data')],
                   Input('add-app-tab', 'n_clicks'),
                  [State('tabs', 'children'), State('visualizations', 'value'), State('add-app-tab-num', 'data')])
    def manage_app_tabs(n_clicks, existing_tabs, selected_app, app_tabs):
#        print(n_clicks, len(existing_tabs), existing_tabs[0])                                                                     # DEBUG
        if n_clicks == 0:
            if not len(app_tabs):
                return [no_update, existing_tabs]
            elif len(app_tabs) > len(existing_tabs):
                return [app_tabs, no_update]
            else:
                raise PreventUpdate

        def find_max_suffix_from_keyword(tabs, keyword):
            matching_values = [tab['props']['value'] for tab in tabs if keyword in tab['props']['value']]
            if not matching_values:
                return None
            suffixes = [int(value.split('_')[-1]) for value in matching_values if value.split('_')[-1].isdigit()]
            return max(suffixes) if suffixes else None

        found_value = find_max_suffix_from_keyword(existing_tabs, selected_app)
        num = found_value + 1 if found_value else 1

        tab_name = f"{selected_app}_{num}"
        new_tab = dcc.Tab(label=tab_name, id={'type':"app-tab-",'id': tab_name}, value=f"tab-{tab_name}", className='index-tab')
        existing_tabs.append(new_tab)
#        print(n_clicks, len(existing_tabs))                                                                                       # DEBUG
        
        return [existing_tabs, existing_tabs]

    
    @app.callback(Output('app-mode', 'children'),
                  Input('tabs', 'value'),
                  [State('tabs', 'children'), State('app-mode', 'children')])
    def update_app_layout(active_tab, existing_tabs, content):
        if active_tab == 'tab-home' or active_tab == 'tab-about':
            return no_update
        
#        for tab in existing_tabs:
#            if tab['props']['value'] == active_tab:
#                selected_visualization = tab['props']['label'].split()[0].lower()
#                if selected_visualization == 'synteny':
#                    return content #synteny.layout
#                elif selected_visualization == 'clustergram':
#                    return content #clustergram.layout

        return content
