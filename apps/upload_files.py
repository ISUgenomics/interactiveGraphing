# -*- coding: utf-8 -*-
from urllib import request
import json
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


from app import app
from .paths import *

### VARIABLES

#-- UPLOAD FILES - VARIANTS

#-- SECTION A. Load example dataset
example_upload_files = html.Div([
    dcc.Checklist(
        options=[{'label': 'use default data', 'value': '0', 'disabled': False}],
        value=[],
        style={'margin':'0 0 0 0.5vw'},
        labelClassName="checkbox-label",
        labelStyle={'margin-top':'0'},
        id='default-data',),
], id='example-upload-files')

#-- SECTION B. Load pipeline input data
pipeline_upload_files = html.Div([

], id='pipeline-upload-files')


#-- SECTION C. Load custom input data
custom_upload_files = html.Div([
    html.Label('from file system: ', id='custom-label', className="label-tertiary"),
    dcc.Upload(id='upload-box',
        children=html.Div(['drag & drop or browse']),
        className='upload-box',
        max_size=-1,
        multiple=True),						# Allow multiple files to be uploaded
    html.Label('from online: ', id='custom-url-label', className="label-tertiary", style={'marginTop':'2vh'}),
    dcc.Input(id="custom-url", type="url", placeholder="enter URL", value='', debounce=False),
    dcc.Input(id="custom-url-file", type="text", placeholder="enter filename", value='', debounce=True),
    dbc.Button("download", id="download-btn", n_clicks=0, size="sm", outline=True, color="secondary", className="me-1 align-top", style={'marginLeft':'1vw', 'width':'29%'}),
    
    dcc.Store(id="custom-box-files", data='', storage_type='session'),
    dcc.Store(id="custom-url-files", data='', storage_type='session'),
    dcc.Store(id="user-files-list", data='', storage_type='session'),
], id='custom-upload-files',)



#-- SECTION D. summary of selected settings

settings_upload_inputs = [
    html.Div(id="settings-upload-inputs", className="mt-3")
]



### CALLBACKS

#-------------------------------------------------
#-- SECTION A:


#-- SECTION B:


#-- SECTION C: The function returns updated dictionary of filename:file_content for all user-loaded files via upload-box
@app.callback(Output('custom-box-files', 'data'),
              [Input('upload-box', 'filename'), Input('upload-box', 'contents')],
              State('custom-box-files', 'data'), prevent_initial_call = True)
def upload_files_box(names, contents, files):
    if names is not None:
        if files == '':
            files = {i:contents[num] for num,i in enumerate(names)}
        else:
            files = json.loads(files)
            for num,i in enumerate(names):
                files[i] = contents[num]
        return json.dumps(files)


#-- SECTION C: The function returns updated dictionary of filename:file_content for all user-loaded files via online-url
@app.callback(Output('custom-url-files', 'data'),
              [Input('download-btn', 'n_clicks')],
              [State('custom-url', 'value'), State('custom-url-file', 'value'),
               State('path-to-project', 'data'), State('custom-url-files', 'data')], prevent_initial_call = True)
def upload_files_url(download, url, filename, project_path, files):
    if url != '':
        if filename == '':
            filename = url.split('/')[-1]
        saving_path = path.Path.joinpath(path.Path(str(project_path)), str(filename)).absolute()
        request.urlretrieve(url, saving_path.as_posix())
        if files == '':
            files = {}
            files[filename] = saving_path.as_posix()
        else:
            files = json.loads(files)
            files[filename] = saving_path.as_posix()
        return json.dumps(files)
    else:
        raise PreventUpdate


#-- SECTION C: The function creates a list of user-loaded files that can be used for plotting
@app.callback(Output('user-files-list', 'data'),
             [Input('custom-box-files', 'data'), Input('custom-url-files', 'data')], prevent_initial_call = True)
def create_list_of_custom_files(files_box, files_url):
    files = []
    for i in [files_box, files_url]:
        if i != '':
            files.extend(list(json.loads(i).keys()))
    return files


#-- SECTION D: Display summary of settings
@app.callback(
    Output("settings-upload-inputs", "children"),
    [Input("apply-btn", "n_clicks"), Input("user-files-list", "data")])
def display_inputs_settings(apply, loaded_files):
    info1 = "Inputs options will be displayed when you select analysis in section 2. Select type of analysis."
    if apply > 0:
        if loaded_files == '':
            info1 = "Please load inputs using available options."
        else:
            info1 = "The following files were sucessfully loaded: " + str(', '.join(loaded_files))
    return [
        html.Label(info1, className="label-tertiary grayed"),
    ]

