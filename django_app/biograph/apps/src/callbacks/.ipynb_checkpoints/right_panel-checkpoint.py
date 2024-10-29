from dash import dcc, html, callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
from src.functions.widgets import get_triggered_info



def register_right_panel_callbacks(app):
    

    # Save dataframe modal: open-close pop up, customize contents for selected DF
    @app.callback([Output('modal-save-df', 'is_open'), 
                   Output('opts-save-df-storage', 'value'), Output('opts-save-df-filename', 'value'), 
                   Output('df-saveit', 'value'), Output('df-saveit', 'readOnly')],
                  [Input({'type': 'save-', 'id': ALL}, 'n_clicks'), Input('btn-save-df', 'n_clicks'),],
                  [State('data-dir', 'data'), State('opts-save-df-filename', 'value')],
                   prevent_initial_call = True)
    def toggle_modal_df(n_open, n_close, data_dir, filename):
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None
#        print("8.1 Save DF modal: ", tnv, n_open, n_close, "\ndata_dir: ", data_dir)           ############# DEBUG
        if tnv and tnv[2] > 0:
            if tnv[0] == "save-":
#                print("8.1 return for save-")                                                  ############# DEBUG
                tokens = tnv[1].split()
                filename = tokens[0].split('.')[0]+"_"+tokens[1].replace('#', 'edition-')
#                print("8.1 ", data_dir, filename, tnv[1], 'False')                             ############# DEBUG
                return [True, data_dir, filename, tnv[1], False]
            else:
#                print("8.1 return for btn-save-df")                                            ############# DEBUG
#                print("8.1 ", data_dir, filename)                                              ############# DEBUG
                return [False, no_update, no_update, no_update, True]
        else:
#            print("8.1 raise PreventUpdate")
            raise PreventUpdate


    # Highlight in red required input in save df options modal (not clientside because checking if path exists)
    @app.callback([Output('opts-save-df-custom', 'className'), Output('opts-save-df-custom-wrong', 'children')],
                  [Input('opts-save-df', 'value'), Input('opts-save-df-custom', 'value')],
                  [State('opts-save-df-custom', 'className')],
                   prevent_initial_call=True)
    def highlight_required_input(opts, path, classes):
        ctx = callback_context                                                                 ############# DEBUG 
        tnv = get_triggered_info(ctx.triggered) if ctx else None                               ############# DEBUG 
#        print("8.2 Color input in modal: ", tnv, "\nopts: ", opts, "\npath: ", path, "\nclasses: ", classes)           ############# DEBUG 
        if 'custom' in opts and (not path or not os.path.exists(path)):
            return [f"{classes} required", "Invalid path detected! Please correct it and try again."]
        else:
            return [classes.replace('required', '').strip(), '']
