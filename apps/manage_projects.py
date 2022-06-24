# -*- coding: utf-8 -*-

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dash import no_update

from app import app
from .paths import *

### LAYOUT COMPONENTS

#-- SECTION A. manage saved projects
list_all_projects = [
        html.Label('your projects are saved at: ', className="label-tertiary"),
        dcc.Input(str(path_projects), type='text', className="note-italic", disabled=True),
        html.Hr(style={'marginTop':'0'}),
        html.Label('list of stored projects: ', className="label-tertiary"),
        dcc.Checklist(
            options=list(os.listdir(path_projects)),
            value=[],
            inline=True,
            labelClassName="checkbox-label", labelStyle={'marginTop':'1vh'}, style={'marginLeft':'0.5vw'},
            id="all-projects",
        ),
        html.Div([
            dbc.Button("remove selected", id="remove-project-btn", n_clicks=0, size="sm", outline=True, color="danger"),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("WARNING!")),
                dbc.ModalBody(["Please confirm permanent deletion of selected projects:", 
                                html.P(id='remove-selcted-list', className='warning-bold success'),
                                html.P(id='keep-current-project', className='warning-bold'),
                              ]),
                dbc.ModalFooter([
                    dbc.Button("Cancel", id="cancel-remove-projects", color="danger", className="", n_clicks=0),
                    dbc.Button("Remove", id="yes-remove-projects", color="success", className="", n_clicks=0)
                ], className="d-flex justify-content-between"),
            ], id="modal-remove-projects", is_open=False,),
        ], className="d-md-flex justify-content-md-end mt-2"),
]


#-- SECTION B. tmp or open or create project

tmp_project_opts = [
    html.Label('temporary project name: ', className="label-tertiary"),
    html.Div([
        dcc.Input(id='tmp-project-name', value="tmp"+str(dt.datetime.now().strftime("%f")), persistence=True, persistence_type='session', className="note-italic", disabled=True),
    ]),
]

open_project_opts = [
    html.Label('select project name: ', className="label-tertiary"),
    html.Div([
        dcc.Dropdown(id="select-project-name", placeholder="select project name ⠀▽", value='none', persistence=True, persistence_type='session', style={'width':'15vw', 'height': '32px', 'display': 'inline-block'}),
        dbc.Button("open", id="open-project-btn", n_clicks=0, size="sm", outline=True, color="secondary", className="me-1 align-top", style={'marginLeft':'1vw', 'width':'20%'}),
    ]),
]

create_project_opts = [
    html.Label('enter project name: ', className="label-tertiary"),
    html.Div([
        dcc.Input(id="enter-project-name", type="text", placeholder="enter project name", value='', debounce=True, persistence=True, persistence_type='session', style={'width':'15vw', 'height': '32px', 'display': 'inline-block'}),
        dbc.Button("create", id="create-project-btn", n_clicks=0, size="sm", outline=True, color="secondary", className="me-1 align-top", style={'marginLeft':'1vw', 'width':'20%'}),
    ]),
]

name_save_opts = [
    dcc.RadioItems(
        options=[{'label' : 'tmp project', 'value' : 'tmp'}, {'label' : 'open project', 'value' : 'open'}, {'label' : 'create project', 'value' : 'create'}],
        value='tmp',
        persistence=True,
        persistence_type='session',
        inline=False,
        id="type-of-project",
        labelClassName="checkbox-label", labelStyle = {'width' : '100%'}
    ),
    html.Div(tmp_project_opts, id="tmp-project-opts", className="mt-3 d-block"),
    html.Div(open_project_opts, id="open-project-opts", className="d-none"),
    html.Div(create_project_opts, id="create-project-opts", className="d-none"),
    html.Div([
        html.Label('project location: ', className="label-tertiary"),
        dcc.Input('', id='project-location', className="note-italic", disabled=True)
    ], id="project-settings", className="mt-3"),


]

#-- SECTION C. summary of selected settings

settings_manage_projects = [
    html.Div(id="settings-manage-projects", className="mt-3")
]



###---------------------------
### CALLBACKS

### 1. Manage Project(s) section

#-- SECTION A: Get list of projects selected for removal (to be displayed in modal-remove-projects)
@app.callback(
    [Output("remove-selcted-list", "children"), Output("keep-current-project", "children")],
    [Input("all-projects", "value")], [State("project-name", "data")],
    prevent_initial_call = False
)
def toggle_modal(selected, current_project):
    info = ''
#    print('toggle modal: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    if current_project in selected:
        selected.remove(current_project)
        info = "NOTE: " + current_project + " is a current project and can NOT be removed!"
    return [', '.join(selected), info]


#-- SECTION A: Open modal 'remove projects'
@app.callback(
    Output("modal-remove-projects", "is_open"),
    [Input("remove-project-btn", "n_clicks"), Input("cancel-remove-projects", "n_clicks"), Input("yes-remove-projects", "n_clicks")],
    [State("modal-remove-projects", "is_open")], prevent_initial_call = False
)
def toggle_remove_projects_modal(n1, n2, n3, is_open):
#    print('toggle remove projects: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    if n1 or n2 or n3:
        return not is_open
    return is_open


#-- SECTION A: Remove selected projects after user approval (remove folders from the File System and update list of projects)
@app.callback(
    [Output("all-projects", "options"), Output("all-projects", "value")],
    [Input("yes-remove-projects", "n_clicks"), Input("project-name", "data")],
    [State("all-projects", "value"), State("project-name", "data")], prevent_initial_call = False
)
def remove_selected_projects(remove, project_path, selected, current_project):
#    print('remove selected projects: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    if dash.callback_context.triggered_id == "yes-remove-projects":
        try:
            selected.remove(current_project)		# prevent removing the current project;
        except:
            pass
        for project in selected:
            dir_path = path.Path.joinpath(path_projects, str(project)).absolute()
            remove_dir(dir_path)
        selected = []
    projects_kept = os.listdir(path_projects)
    return [projects_kept, selected]


#-- SECTION B: Update name of the temporary project and remove the temporary dir of the previous one
@app.callback(
    Output("tmp-project-name", "value"),
    [Input("type-of-project", "value")], 
    [State("project-name", "data"), State("tmp-project-name", "value")])
def disable_create_btn(action_type, project_name, tmp_name):
    if action_type == 'tmp':
        if not project_name.startswith('tmp'):
            return "tmp"+str(dt.datetime.now().strftime("%f"))
        else:
            return project_name
    else:
        for project in os.listdir(path_downloads):
            if project.startswith('tmp'):
                dir_path = path.Path.joinpath(path_downloads, str(project)).absolute()
                remove_dir(dir_path)
        return ''


#-- SECTION B: Create new project: name it and mkdir folder in ~/projects/ (or temporary project in ~/downloads/)
@app.callback(
    [Output("path-to-project", "data"), Output("project-name", "data")],
    [Input("create-project-btn", "n_clicks"), Input("open-project-btn", "n_clicks"), Input("tmp-project-name", "value")],
    [State("type-of-project", "value"), State("enter-project-name", 'value'), State("select-project-name", "value"),
     State("path-to-project", "data"), State("project-name", "data")])
def create_open_project(n_create, n_open, tmp_name, action_type, create_name, open_name, path_to_project, project_name):
    ctx = dash.callback_context.triggered_id

    if ctx == "tmp-project-name" and action_type == 'tmp':
        tmp = path.Path.joinpath(path_downloads, tmp_name).absolute()
        if create_dir(tmp.as_posix()):
            return [tmp.as_posix(), tmp_name]
        else:
            raise PreventUpdate

    elif ctx == "open-project-btn" and action_type == 'open':
        tmp = path.Path.joinpath(path_projects, open_name).absolute()
        if path.Path(tmp).is_dir():
            return [tmp.as_posix(), open_name]
        else:
            raise PreventUpdate

    elif ctx == "create-project-btn" and action_type == 'create':
        tmp = path.Path.joinpath(path_projects, create_name).absolute()
        if create_dir(tmp.as_posix()):
            return [tmp.as_posix(), create_name]
        else:
            raise PreventUpdate

    else:
        raise PreventUpdate


#-- SECTION B: Load list of available project to open
@app.callback(
    Output("select-project-name", "options"),
    [Input("all-projects", "options")])
def load_list_of_projects(projects_kept):
#    print('load_list_of_projects: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    selected = ['none']
    if len(projects_kept):
        selected.extend(projects_kept)
    return selected


#-- SECTION B: Display options to a) tmp b) open or b) create project 
@app.callback(
    [Output("tmp-project-opts", "className"), Output("open-project-opts", "className"), Output("create-project-opts", "className"),
     Output("select-project-name", "value"), Output("enter-project-name", 'value')],
    [Input("type-of-project", "value"), Input("open-project-btn", "n_clicks"), Input("create-project-btn", "n_clicks"),], 
    [State("project-name", "data")])
def display_project_opts(action_type, current_project, open_btn, create_btn):
#    print('display_project_opts: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    ctx = dash.callback_context.triggered_id

    if action_type == 'tmp':
        return ["mt-3 d-block", "d-none", "d-none", 'none', '']
    elif action_type == 'open':
        if ctx == 'open-project-btn':
            return ["d-none", "mt-3 d-block", "d-none", no_update, '']
        else:
            return ["d-none", "mt-3 d-block", "d-none", no_update, no_update]
    elif action_type == 'create':
        if ctx == "create-project-btn":
            return ["d-none", "d-none", "mt-3 d-block", 'none', no_update]
        else:
            return ["d-none", "d-none", "mt-3 d-block", no_update, no_update]


#-- SECTION B: Disable create-project button when no value
@app.callback(
    Output("create-project-btn", "disabled"),
    [Input("enter-project-name", 'value'), Input("type-of-project", "value"), Input("select-project-name", "options")])
def disable_create_btn(value, action_type, options):
#    print('disable_create_btn: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    if value == '' or value in options:
        return True
    else:
        return False


#-- SECTION B: Disable open-project button when no value
@app.callback(
    Output("open-project-btn", "disabled"),
    [Input("select-project-name", 'value'), Input("type-of-project", "value")])
def disable_open_btn(value, action_type):
#    print('disable_open_btn: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    if value == 'none':
        return True
    else:
        return False


#-- SECTION B: Update displayed location of current project
@app.callback(
    Output("project-location", "value"),
    [Input("path-to-project", "data"), Input("type-of-project", "value")],
    [State("project-name", "data"), State("select-project-name", "value"), State("enter-project-name", "value")])
def display_project_location(project_path, action_type, project_name, open_project, create_project):
    print('display_project_location: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    if action_type == "tmp" and project_name.startswith('tmp'):
        return project_path
    elif action_type == "open" and project_name == open_project:
        return project_path
    elif action_type == "create" and project_name == create_project:
        return project_path
    else:
        return ''


#-- SECTION C: Display summary of settings
@app.callback(
    Output("settings-manage-projects", "children"),
    [Input("type-of-project", "value"), Input("path-to-project", "data"), Input("project-name", "data")],
    [State("select-project-name", "value"), State("enter-project-name", "value")])
def display_settings_summary(action_type, project_path, project_name, open_name, create_name):
#    print('display_settings_summary: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    info2 = info3 = ''
    if action_type == "tmp":
        info1 = "You are working on a temporary project."
        info2 = "Temporary project path: "
        info3 = "WARNING: All data will be deleted immediately when you open another project or create a new one."
    elif action_type == "open":
        if project_name.startswith('tmp'):
            info1 = "To work on a previously saved project select project name in the dropdown and click 'open'."
        else:
            info1 = "You are working on an opened project."
            info2 = "Path to saved project: "
    elif action_type == "create":
        if project_name != create_name:
            info1 = "To create new project enter customized project name and click 'create'."
            info3 = "Note: The button is disabled when a project with the entered name already exists."
        else:
            info1 = "You are working on newly created project."
            info2 = "Path to saved project: "
    return [
        html.Label(info1, className="label-tertiary grayed"),
        html.Label("Project name: " + str(project_name), className="label-tertiary bold grayed"),
        html.Label(info2, className="label-tertiary grayed"),
        html.Label(str(os.path.dirname(project_path)), className="label-tertiary italic grayed", style={"font-size":"1.6vh"}),
        html.Label(info3, className="label-tertiary bold grayed")
    ]


###---------------------------
### Universal Python functions

#-- Remove directory with all content
def remove_dir(dir_path):
#    print('remove_dir: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


#-- Create directory
def create_dir(dir_path):
#    print('create_dir: ', dash.callback_context.triggered_id, '\n', str(dt.datetime.now()))##################### DEBUG PRINT #####################
    try:
        os.mkdir(dir_path)
        print("INFO: Directory ", dir_path, " created!")
    except FileExistsError:
        print("WARNING: Directory " , dir_path ,  " already exists!")
    if path.Path(dir_path).is_dir():
        return True
    else:
        return False


