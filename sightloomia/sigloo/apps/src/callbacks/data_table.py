from dash import dcc, html, callback_context, no_update, Patch
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
from sigloo.apps.src.functions.widgets import get_triggered_info, generate_dash_table


def register_datatable_callbacks(app):
    
    ### MANAGE DataTables

    # [DataTables PART 1/X] Create a new DataTable and display for interactive edition (items of dbc.Accordion)
    @app.callback(Output('edition-items', 'children'),
                  [Input('dt-add-id', 'value')],
                  [State('edition-content', 'data'), State('edition-current', 'data')])
    def add_datatables(identifier, data_store, current_table):
#        print('\n5.1 add_datatables triggered:')                        ############# DEBUG
#        print('5.1 data store: ', len(data_store), " identifier: ", identifier)
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None
#        print("5.1 TNV: ", tnv)                                         ############# DEBUG
        if tnv and tnv[1] and tnv[1] == 'dt-add-id':                    # Add a new DataTable
            patched_children = Patch()
            patched_children.append(generate_dash_table(identifier, data_store[identifier]["data"]))
#            print('5.1 updated children [ADD]: ', identifier)           ############# DEBUG
            return patched_children
        elif not tnv[1] and data_store:                                 # Update display content after page refresh
            children = []
            for key in data_store:
                if not 'closed' in data_store[key]["status"]:
                    if key in current_table:                            # If changes in the number of columns or rows use (current) DT store
                        print(f"5.1 update DT on page reload: {key}, {len(current_table[key]['data'])}")
                        child = generate_dash_table(key, [current_table[key]["data"], current_table[key]["columns"]])
                    else:
                        child = generate_dash_table(key, data_store[key]["data"])
                    children.append(child)
#            print('5.1 updated children [ADD ALL] after reload')        ############# DEBUG
            return children
        else:
#            print('5.1 nothing added')                                  ############# DEBUG
            raise PreventUpdate            


#     [DataTables PART 2/X] Disable n_clicks property on close- button for selected DataTable
    @app.callback([Output({'type': 'close-', 'id': MATCH}, 'disable_n_clicks')],
                  [Input({'type': 'close-', 'id': MATCH}, 'n_clicks')])
    def disable_clicks(n_clicks):
#        print('\n5.2 disable_close triggered:')                         ############# DEBUG
        ctx = callback_context                                          ############# DEBUG
        tnv = get_triggered_info(ctx.triggered) if ctx else None        ############# DEBUG
#        print("5.2 TNV: ", tnv)                                         ############# DEBUG
        if n_clicks:
            print("5.2 ", tnv[1], " disabled")                          ############# DEBUG
            return [True]
        else:
            raise PreventUpdate


#     [DataTables PART 3/X] Hide selected DataTables from interactive edition (items of dbc.Accordion);
    @app.callback([Output({'type': 'item-', 'id': MATCH}, 'class_name'), 
                   Output({'type': 'dtbl-', 'id': MATCH}, 'data')],
                  [Input({'type': 'close-', 'id': MATCH}, 'disable_n_clicks')],
                   prevent_initial_call = True)
    def close_datatables(n_close):
#        print('\n5.3 close_datatables triggered:')                       ############# DEBUG
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None
#        print("5.3 TNV: ", tnv)                                          ############# DEBUG
        if tnv and tnv[2] and tnv[2] == True:                              # expected trigger: ['close-', 'input_3.csv #3', True]
            return ['hidden', []]
        else:
            print('5.3 nothing hidden')                                  ############# DEBUG
            raise PreventUpdate   


    # [DataTables PART 4/X] Pass id of closed DataTable (to delete the corresponding DataFrame in memory)
    @app.callback(Output('df-delete', 'value'),
                 [Input({'type': 'item-', 'id': ALL}, 'class_name')],
                  prevent_initial_call = True)
    def pass_closed(hidden):
#        print('\n5.4 pass_hidden triggered:')                            ############# DEBUG
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None
#        print("5.4 TNV: ", tnv)                                          ############# DEBUG    
        if tnv and tnv[2] and tnv[2] == 'hidden':                        # expected trigger: ['item-', 'input_3.csv #3', 'hidden']
            return tnv[1]
        else:
            raise PreventUpdate


    # [DataTables PART 5/X] Disable n_clicks property on cache- button for selected DataTable
    @app.callback([Output({'type': 'cache-', 'id': MATCH}, 'disable_n_clicks')],
                  [Input({'type': 'cache-', 'id': MATCH}, 'n_clicks')])
    def disable_clicks(n_clicks):
#        print('\n5.5 disable_cache triggered:')                          ############# DEBUG
        ctx = callback_context                                           ############# DEBUG
        tnv = get_triggered_info(ctx.triggered) if ctx else None         ############# DEBUG
#        print("5.5 TNV: ", tnv)                                          ############# DEBUG
        if n_clicks:
            print("5.5 ", tnv[1], " disabled")                           ############# DEBUG
            return [True]
        else:
            raise PreventUpdate
        

    # [DataTables PART 6/X] Pass id of cached DataTable (to preserve its status in the corresponding DataFrame in memory)
    @app.callback(Output('df-keepit', 'value'),
                 [Input({'type': 'cache-', 'id': ALL}, 'disable_n_clicks')],
                  prevent_initial_call = True)
    def pass_cached(cached):
#        print('\n5.6 pass_hidden triggered:')                            ############# DEBUG
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None
#        print("5.6 TNV: ", tnv)                                          ############# DEBUG    
        if tnv and tnv[2] and tnv[2] == True:                            # expected trigger: ['cache-', 'input_3.csv #3', True]
            return tnv[1]
        else:
            raise PreventUpdate


#     [DataTables PART 7/X] Update displayed status of each edition instance: edit, cached, cached-closed, saved locally
    @app.callback([Output({'type': 'status-', 'id': ALL}, 'value')],
                 [Input('edition-content', 'modified_timestamp')],
                 [State({'type': 'status-', 'id': ALL}, 'value'), State('edition-content', 'data')])
    def display_current_status(stamp, state_status, data_store):
#        print('\n5.7 current_status triggered:')                         ############# DEBUG
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None         ############# DEBUG expected trigger: ['', 'edition-content', 1702062750985]
#        print("5.7 TNV: ", tnv)                                          ############# DEBUG
#        print("5.7 state_status: ", state_status)                        ############# DEBUG
#        print("5.7 data_store_items: ", list(data_store.keys()))         ############# DEBUG
#        print("5.7 context_outputs: ", ctx.outputs_list)                 ############# DEBUG
        status_ids = [item['id']['id'] for sublist in ctx.outputs_list for item in sublist]
        for i, id in enumerate(status_ids):
            if id in data_store and len(data_store[id]['status']) > 1:
                state_status[i] = f"status: {', '.join(data_store[id]['status']).replace('edit', '').lstrip(',')}"
            else:
                state_status[i] = no_update
        return [state_status]
        
################################################################################################ 
        
# [PART 4] Create a dropdown of inputs for a graph: uploaded files + edited files
## - check if data is good for this kind of a plot