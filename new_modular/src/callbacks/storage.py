from urllib import request
from pathlib import Path
import base64
import json
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context, no_update, Patch
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL, MATCH
from src.params.defaults import tooltip
from src.functions.io import decode_base64, export_df
from src.functions.widgets import get_triggered_info, generate_html_label, generate_dbc_button, generate_dcc_input_scroll


def register_storage_callbacks(app):

    # [MANAGE FILES 1/4] The function creates a dict of user-loaded files that can be used for plotting; user-purged inputs are removed from memory
    @app.callback(Output('user-files-list', 'data'),
                 [Input({'id':'upload-box', 'tab': ALL}, 'filename'), Input({'id':'upload-box', 'tab': ALL}, 'contents'), Input({'id':"download-btn", 'tab': ALL}, 'n_clicks'), Input('captured-name-store', 'data')],
                 [State({'id':"custom-url", 'tab': ALL}, 'value'), State('user-files-list', 'data'), State({'id':'upload-box', 'tab': ALL}, 'id')],
                  prevent_initial_call = True)
    def create_input_list(files_box, contents_box, download_clicks, removed_input, urls, files, ids):
        print('0. update files list triggered')                                                                                #############  DEBUG
        print('0. removed input: ', removed_input)
        ctx = callback_context.triggered
        if ctx:
            tnv = get_triggered_info(ctx)  # [type, name, value]
            print('0. CTX: ', tnv[0], ' ; ', tnv[1])                                                                          #############  DEBUG
            index = next((i for i, d in enumerate(ids) if d['tab'] == tnv[0]), None)
            fbox = files_box[index]
            cbox = contents_box[index]
            url = urls[index]
            
            # Handle remove button clicks
#            print("0. HERE: ", remove_clicks, remove_ids)    #######
#            if len(remove_clicks):
#                remove_clicks = remove_clicks[0]
#                if any(click > 0 for index, click in enumerate(remove_clicks)):
#                        ix = index
#                    print("0. index: ", index, remove_ids[index]['id'])
#                for remove_id, click_count in zip(remove_clicks, remove_clicks):
#                    if click_count > 0:
#                        files.pop(remove_id['id'], None)
#                        print('0. -by remove ', str(len(files)), files.keys())                                                 #############  DEBUG
#                return no_update
            
            # Handle file uploads
            if tnv[1] == 'upload-box' and fbox:
                for num, i in enumerate(fbox):
                    if i != '' and i not in files:
                        try:
                            content_type, content_string = cbox[num].split(',')
                            files[str(i)] = content_string
                        except Exception as e:
                            print(f"Error processing upload content: {e}")
                print('0. -by upload ', str(len(files)), files.keys())                                                         #############  DEBUG
                
            # Handle URL-based file additions
            elif url:
                filename = url.strip().split('/')[-1]
                if filename not in files:
                    try:
                        with request.urlopen(url) as f:
                            content = f.read().decode('utf-8')
                            content = base64.b64encode(content.encode('ascii')).decode('ascii')
                        files[filename] = content
                        print('0. -by URL ', str(len(files)))                                                                  #############  DEBUG
                    except Exception as e:
                        print(f"Error processing URL content: {e}")
            return files
        return no_update


    # [MANAGE FILES 2/4] Display summary of loaded inputs
    @app.callback([Output({'id':"settings-upload-label", 'tab': ALL}, "children"), Output({'id':"settings-upload-inputs", 'tab': ALL}, "children"), 
                   Output("user-files-status", "data")],
                  [Input("user-files-list", "data")],
                  [State("user-files-list", "modified_timestamp"), State("inputs-clicks", 'data'), State({'id':"settings-upload-label", 'tab': ALL}, "children")],
                  prevent_initial_call = True)
    def display_inputs_settings(loaded_files, time_stamp, counts, items):
        print('1. display-inputs triggered')                                                                                    #############  DEBUG
        if not len(loaded_files):
            print('1. -no update')                                                                                              #############  DEBUG
            return [["Please load inputs using available options."] * len(items), [[]] * len(items), time_stamp]
    
        print('1. -update ', str(len(loaded_files)), '\n')  #, loaded_files                                                     #############  DEBUG
        info = "The following files were loaded: "
        inputs = []
        for filename, content in loaded_files.items():
            try:
                n_clicks = counts.get(filename, 0) if counts else 0
                file_size_kb = round(len(content) * (3 / 4) / 1000, 1)
                item = html.Div([
                    generate_dcc_input_scroll(f"- {filename}   ({file_size_kb} kB)", "col-8 p-0 me-3 d-inline border-0"),
                    html.Div([
                        generate_dbc_button(["edit ", html.I(className="fa fa-external-link")], {'type': "edit-", 'id': str(filename)}, n_clicks, "sm", True, "secondary", "col-9 h34", style={}),
                        dbc.Tooltip(children=tooltip['edit-'], target={'type':"edit-",'id': str(filename)}, placement='bottom-start', style={'width': '400px'}),
                        generate_dbc_button([html.I(className="fa fa-times")], f"remove-{str(filename)}", 0, "sm", True, "danger", "col-3 h34 remove-inputs", style={}),
                        dbc.Tooltip(children=tooltip['remove-'], target={'type':"remove-",'id': str(filename)}, placement='bottom-start', style={'width': '400px'}),
                    ], className="col-4 row ps-1 pe-3"),
                ], id=f"file-{str(filename)}", className="row ms-0 align-items-center d-flex") #{'type':"file-",'id': str(filename)}
                inputs.append(item)
            except Exception as e:
                print(f"Error processing file '{filename}': {e}")

        return [[info] * len(items), [inputs] * len(items), time_stamp]


    # [MANAGE FILES 3/4] Clear Upload Box (filename & contents)
    @app.callback(
        [Output({'id':'upload-box', 'tab': MATCH}, 'filename'), Output({'id':'upload-box', 'tab': MATCH}, 'contents')],
        [Input("user-files-status", 'modified_timestamp')], 
        [State({'id':'upload-box', 'tab': MATCH}, 'last_modified')],
         prevent_initial_call = True)
    def clear_upload_form(list_stamp, upload_stamp):
        result = [no_update, no_update]
        print('2. clear-upload triggered')                                                                                         #############  DEBUG
        print('2. -stamp: ', list_stamp)                                                                                           #############  DEBUG
        if list_stamp and upload_stamp:
            if len(upload_stamp) > 1:
                upload_stamp = max(upload_stamp)
                if list_stamp > upload_stamp:
                    retsult = [[], []]
                    print('2. -clear DONE')                                                                                        #############  DEBUG
        return result


    # [MANAGE FILES 4/4] Remove input-related items from the display (once purged by the user); removes content not a component
#    @app.callback(Output({'type': 'file-', 'id': MATCH}, 'children'),
#                 [Input({'type': 'remove-', 'id': MATCH}, 'n_clicks')], [State({'type': 'file-', 'id': MATCH}, 'children')],
#                  prevent_initial_call = True)
#    def remove_files(n_clicks, state):
#        print('3. remove-input from display triggered', state)                                                                             #############  DEBUG
#        return None


    ################################################################################################# 

    # [MANGE EDITIONS 1/1] Returns the counter of edition modes for every filename and identifier of a new dataframe that will be added to the data store
    @app.callback([Output('inputs-clicks', 'data'), Output('df-add-id', 'value')],
                  [Input({'type': 'edit-', 'id': ALL}, 'n_clicks')],
                  [State('inputs-clicks', 'data')],
                   prevent_initial_call = True)
    def count_edition_modes(n_clicks, counts):
        print('\n4.1 count editions per file:')                                                                                     ############# DEBUG
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None
        print("4.1 TNV: ", tnv, "counts: ", counts)                                                                                 ############# DEBUG
        if tnv and tnv[2] and int(tnv[2]) > 0:
            if not counts:
                counts = {}
            filename = str(tnv[1])
            if tnv[1] in counts and int(tnv[2]) <= int(counts[filename]):
                print("4.1 wrong trigger! PreventUpdate")                                                                           ############# DEBUG
                raise PreventUpdate
            else:
                counts[filename] = counts.get(filename, 0) + 1
                identifier = filename+' #'+str(counts[filename])
                print("4.1 \n-new counts: ", counts, "\n-new dataframe: ", identifier)                                              ############# DEBUG
                return [counts, identifier]
        else:
            raise PreventUpdate       


    ### MANAGE DataFrames

    # [DataFrames PART 1/X] Manage DataFrames storage: create, cache, close, and update with user-provided changes 
    @app.callback([Output('edition-content', 'data'), Output('dt-add-id', 'value')],
                  [Input('df-add-id', 'value'), Input('df-delete', 'value'), Input('df-keepit', 'value'), Input('df-saveit', 'placeholder')],
                  [State('user-files-list', 'data'), State('edition-content', 'data'), State("inputs-clicks", 'data')],
                   prevent_initial_call = True)
    def manage_dataframes(add_id, delete_id, cache_id, save_id, files, data_store, counts):
        print('\n4.2 data storage updates:')                                                                                        ############# DEBUG
        ctx = callback_context
        tnv = get_triggered_info(ctx.triggered) if ctx else None
        print("4.2 TNV: ", tnv)                                                                                                     ############# DEBUG
    
        #1 Add new DataFrame to in-session storage
        if tnv[1] == 'df-add-id':                                                # expected trigger: ['', 'df-add-id', 'input_3.csv #1']
            print("variant: add-df-id")                                                                                             ############# DEBUG
            filename = add_id.split()[0]
            try:   
                df = decode_base64(filename, files[filename])
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                print('4.2 ERROR: file can NOT be decoded!')                                                                        ############# DEBUG
                raise PreventUpdate
            data_store[add_id] = {'data' : df.to_dict(), 'status' : ['edit']}
            print('4.2 ADDED DF: ', len(data_store))                                                                                ############# DEBUG
            return [data_store, add_id]
            
        #2 Remove selected DataFrame (closed DTs) from in-session storage        
        elif tnv[1] == 'df-delete' and delete_id:                                # expected trigger: ['', 'df-delete', 'input_3.csv #1']
            patched_store = Patch()
            if not 'cached' in data_store[delete_id]['status']:
                del patched_store[delete_id]
                print('4.2 REMOVED DF: ', len(data_store))                                                                          ############# DEBUG
            else:
                patched_store[delete_id]['status'].append('closed')
            return [patched_store, no_update]
            
        #3 Cache selected DataFrame to be kept in-session memory after closing edition mode
        elif tnv[1] == 'df-keepit' and cache_id:                                 # expected trigger: ['', 'df-keepit', 'input_3.csv #1']
            patched_store = Patch()
            if not 'cached' in data_store[cache_id]['status']:
                patched_store[cache_id]['status'].append('cached')
            return [patched_store, no_update]

        #4 Update status of the DataFrame saved to a local file
        elif tnv[1] == 'df-saveit' and save_id:
            patched_store = Patch()
            if not 'saved' in data_store[save_id]['status']:
                patched_store[save_id]['status'].append('saved')
            return [patched_store, no_update]
    
        #5 Update DataFrames with chnages made in the interactive DataTables
#        if tnv[0].startswith('dtbl'):
        
        else:
            raise PreventUpdate


    # [DataFrames PART 2/X] Save selected DataFrame
    @app.callback([Output('opts-save-df', 'value'), Output('download-dataframe', 'data'), Output('df-saveit', 'placeholder')],
                  [Input('df-saveit', 'readOnly')],
                  [State('opts-save-df', 'value'),
                   State('opts-save-df-storage', 'value'), State('opts-save-df-custom', 'value'), 
                   State('opts-save-df-filename', 'value'), State('opts-save-df-format', 'value'),
                   State('df-saveit', 'value'), State('edition-content', 'data')],
                   prevent_initial_call = True)
    def save_df_to_local_file(if_save, opts, storage, custom, filename, to_format, df_id, data_store):
        print('\n4.3 save dataframe')                                                                                               ############# DEBUG
        ctx = callback_context                                                                                                      ############# DEBUG
        tnv = get_triggered_info(ctx.triggered) if ctx else None                                                                    ############# DEBUG
        print('4.3 TNV: ', tnv, "\n-if_save: ", if_save, "\n-df_id: ", df_id)                                                       ############# DEBUG
        if if_save and opts:
            print("4.3 selected: ", opts)                                                                                           ############# DEBUG
            print("4.3 values: \n storage: ", storage, '\n custom: ', custom, '\n filename: ', filename, '\n format: ', to_format)  ############# DEBUG
            # extract dataframe and convert to format variant
            storage = storage if 'storage' in opts else None
            custom = custom if 'custom' in opts else None
            download = True if 'download' in opts else False
            status = df_id if any(action for action in [storage, custom, download]) else ''
            print("4.3 Download triggered here")                                                                                    ############# DEBUG
            df = pd.DataFrame(data_store[df_id]["data"])
            return [[], export_df(df, to_format, filename, storage=storage, custom=custom, download=download), status]

        return [[], no_update, '']                                     # Clear the checklist in a modal (for future reuse)
  
    