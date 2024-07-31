from dash import dcc, html, callback_context
from dash.dependencies import Input, Output
from src.params.generic import PARAMS
from src.functions.widgets import get_triggered_info

def register_graph_callbacks(app):
    
    pass

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

