from dash import ClientsideFunction
from dash.dependencies import Input, Output, State, ALL

def register_clientside_callbacks(app):
    
    # toggle the display of the options panel on the left
    app.clientside_callback(
        """
        function(n_clicks) {
            return window.dash_clientside.clientside.toggleOptionsPanel(n_clicks);
        }
        """,
        Output('optionsDiv', 'style'),
        Input('options', 'n_clicks'),
        prevent_initial_call=True
    )

    # toggle the display of EDIT INPUT DATA section with the first/any input edited
    app.clientside_callback(
        """
        function(n_clicks, activeItems) {
            if (!activeItems) { activeItems = []; }
            activeItems.push('item-11');
            return activeItems;
        }
        """,
        Output('accordion2', 'active_item'),
        [Input('inputs-clicks', 'data')],
        [State('accordion2', 'active_item')],
        prevent_initial_call=True
    )
    
    # style and move DataTable buttons
    app.clientside_callback(
        """
        function(content) {
            return window.dash_clientside.clientside.moveDataTableButtons(content);
        }
        """,
        Output('void2', 'value'),
        [Input('edition-items', 'children')]
    )
    
        # style and move DataTable buttons
#    app.clientside_callback(
#        """
#        function(content) {
#            return window.dash_clientside.clientside.setValue(content);
#        }
#        """,
#        Output('captured-name-store', 'data'),
#        [Input('settings-upload-inputs', 'children')]
#    )