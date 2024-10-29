from dash import dcc, html, callback_context, no_update, Patch
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
from src.functions.widgets import get_triggered_dict

def register_graph_callbacks(app):
    
    # Callback to update the graph layout using Patch
    @app.callback(Output({'id':"graph", 'tab':MATCH}, "figure", allow_duplicate=True),
                 [Input({'id':'graph-title', 'tab':MATCH}, 'value'), Input({'id':'X-title', 'tab':MATCH}, 'value'), Input({'id':'Y-title', 'tab':MATCH}, 'value')],
                 [State({'id':"graph", 'tab':MATCH}, "figure"), State('tabs', 'active_tab')],
                  prevent_initial_call = True
    )
    def update_graph_layout(title, xaxis_label, yaxis_label, figure, active_tab):
        print("\ncallback 7: update_graph_layout()")                                                           ########## DEBUG
        if not figure:
            raise PreventUpdate
        active_tab = active_tab.split('-')[-1]
        gtd = get_triggered_dict(callback_context.triggered)
        if gtd.get('tab') != active_tab:
            raise PreventUpdate

        patch = Patch()
        if title:
            patch['layout']['title'] = title
        if xaxis_label:
            patch['layout']['xaxis']['title'] = xaxis_label
        if yaxis_label:
            patch['layout']['yaxis']['title'] = yaxis_label

        return patch


    # Return a clustergram graph
#    @app.callback(
#        Output("graph-panelDiv", "children"),
#        [Input("graph-config", "data")]
#    )
#    def return_clustergram(config):
#        return dcc.Graph(figure=fig, id='clustergram', config=config)       # UPDATE fig !!! (empty: go.Figure())


    # Update a clustergram graph - not efficient, update layout on the client side
#    @app.callback(
#        Output("clustergram", "figure"),
#        [Input("graph-title", "value")], 
#        [State("clustergram", "figure")]
#    )
#    def update_clustergram(new_title, figure):
#        print(figure['layout']['title'])
#        figure['layout']['title']['text'] = new_title
#        return figure
 

    # Return the last triggered layout component
#    @app.callback(
#        Output("last_trig_layout", "value"),
#        [Input(key, "value") for key in PARAMS]
#    )
#    def return_layout_triggered(*args):
#        trigger = get_triggered_info(callback_context.triggered)
#        print(trigger)
#        it = trigger[1]
#        val = trigger[2]
#        if is_component_type(it, dcc.Checklist) and not val:
#            val = False
#        if it != '':
#            path = PARAMS[it]
#            print(path, val)
#            return [path, val]


    # Export HTML app
#    @app.callback(
#        Output("void0", "value"),
#        [Input('export-html', 'value'), Input('html-name', 'value')],
#        [State("clustergram", "figure")]
#    )
#    def write_graph_html(if_export, html_name, figure):
#        if if_export == 'True':
#            figure.write_html(html_name)
#        return ''

