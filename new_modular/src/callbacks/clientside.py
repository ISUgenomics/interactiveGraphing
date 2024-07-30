from dash import ClientsideFunction
from dash.dependencies import Input, Output, State, ALL

def register_clientside_callbacks(app):
    # toggle the display of the options panel on the left
    app.clientside_callback(
        """
        function(n_clicks) {
            window.dash_clientside.optionsPanel.toggleOptions(n_clicks);
            return {};
        }
        """,
        Output('optionsDiv', 'style'),
        Input('btn-options', 'n_clicks')
    )
    # automatically unfold the Edit Input Data panel when a file is selected for editing
    app.clientside_callback(
        """
        function(n_clicks, activeItems) {
            return window.dash_clientside.rightPanel.unfoldEditPanel(n_clicks, activeItems);
        }
        """,
        Output('accordion2', 'active_item'),
        [Input({'type': 'edit-', 'id': ALL}, 'n_clicks')],
        [State('accordion2', 'active_item')],
        prevent_initial_call=True
    )
    # create item buttons for DataTables
    app.clientside_callback(
        ClientsideFunction(
            namespace='rightPanel',
            function_name='createItemButtons'
        ),
        Output('void1', 'value'),
        [Input({'type': 'item-', 'id': ALL}, 'n_clicks')]
    )
    # move DataTable buttons
    app.clientside_callback(
        ClientsideFunction(
            namespace='rightPanel',
            function_name='moveDataTableButtons'
        ),
        Output('void2', 'value'),
        [Input('edition-items', 'children')]
    )
