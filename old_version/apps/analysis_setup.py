# -*- coding: utf-8 -*-
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dash import no_update

from app import app
from .manage_projects import *	# [SECTION 1]
from .select_analysis import *	# [SECTION 2]
from .upload_files import *	# [SECTION 3]

### LAYOUT COMPONENTS




#-----------------------TAB LAYOUT: ANALYSIS SETUP-----------------------#

analysis_setup = html.Div([
#    dcc.Store(id="path-to-project", data='', storage_type='session'),
#    dcc.Store(id="project-name", storage_type='session'),
    
    dbc.Row([
        #-- SECTION: 1. Manage Projects
        dbc.Col([
            html.Label('1. Manage project(s)', className="label-basic label-primary"),
            dbc.Accordion([
                dbc.AccordionItem(list_all_projects,
                title="A. manage saved projects", item_id="item-1"),
                dbc.AccordionItem(name_save_opts,
                title="B. open or create project", item_id="item-2"),
            ], id="accordion-manage-project", start_collapsed=True, flush=False, always_open=True,),
            dbc.ButtonGroup([dbc.Button("VOID", color="white", outline=True, disabled=True, style={"color":"white"})], style={'margin-top':'2.4vh', 'width':'100%'}),
            html.Hr(),
            html.Div(settings_manage_projects),
        ], width=4, className='dbc-col-30'),

        #-- SECTION: 2. Select type of the analysis
        dbc.Col([
            html.Label('2. Select type of the analysis', className="label-basic label-primary"),
            html.Div([
                dbc.Accordion([
                    dbc.AccordionItem(ready_pipeline_opts,
                    title="A. use pre-defined pipeline", id="ready-pipeline-opts"),
                    dbc.AccordionItem(custom_analysis_opts,
                    title="B. add custom analysis", id="custom-analysis-opts"),
                ], id="accordion-analysis-setup", start_collapsed=True, flush=False, always_open=True,),
                dbc.ButtonGroup([
                    dbc.Button("Reset", color="danger", outline=True,id="reset-btn", n_clicks=0, disabled=True),
                    dbc.Button("", color="white", outline=True, disabled=True),
                    dbc.Button("Apply", color="secondary", outline=True, id="apply-btn", n_clicks=0, disabled=True),
                ], style={'margin-top':'2.4vh', 'width':'100%'}),
            ], id="select-analysis-div"),
            html.Hr(),
            html.Div(settings_select_analysis),
        ], width=4, id="select-analysis", className='dbc-col-30', style={'border-left':'1px solid #e4d1d1'}),

        #-- SECTION: 3. Upload input files
        dbc.Col([
            html.Label('3. Upload input files', className="label-basic label-primary"),
            html.Div([
                dbc.Accordion([
                    dbc.AccordionItem(example_upload_files,
                    title="A. load example dataset", item_id="example-upload-files"),
                    dbc.AccordionItem(pipeline_upload_files,
                    title="B. load pipeline input data", item_id="pipeline-upload-files"),
                    dbc.AccordionItem(custom_upload_files,
                    title="C. load custom input data", item_id="custom-upload-files"),
                ], id="accordion-data-loading", start_collapsed=True, flush=False, always_open=True,),
            ], id="upload-inputs-div"),
            html.Hr(),
            html.Div(settings_upload_inputs),
        ], width=4, className='dbc-col-30', style={'border-left':'1px solid #e4d1d1'}),
    
    ], justify="evenly",),

], id='analysis-setup')


###-------------------------------------------------
### CALLBACKS

#-- SECTION 2: Select the interface for loading Section 2: Select type of the analysis; (and reset options)
@app.callback(
    [Output("selected-pipelines", "value"), Output("selected-charts", "value"), 
     Output("select-analysis-div", "className")],
    [Input("type-of-project", "value"), Input("project-name", "data"), Input("reset-btn", "n_clicks"),
     Input("add-tab-btn", "n_clicks"), Input("add-tab-btn2", "n_clicks")])
def display_analysis_options(action_type, project_name, reset, add_tab_pipeline, add_tab_chart):
    ctx = dash.callback_context.triggered
    if len(ctx):
        ctx = ctx[0]['prop_id'].split('.')[0]

    if project_name == '':
        return ['none', [], 'd-none']

    elif ctx == "type-of-project":
        if action_type == 'tmp' or action_type == 'create':
            return ['none', [], 'd-block']
        elif action_type == "open":
            return [no_update, [], 'd-block']		### UPDATE REQUIRED: read database record for a project and select a pipeline/charts

    elif ctx == "reset-btn":
        if action_type == 'tmp' or action_type == 'create':
            return ['none', [], 'd-block']
        elif action_type == "open":
            return [no_update, [], 'd-block']

    elif ctx == "add-tab-btn":
        return ['none', no_update, 'd-block']

    elif ctx == "add-tab-btn2":
        return [no_update, [], 'd-block']

    else:
        return [no_update, no_update, 'd-block']


#-- SECTION 2: Reset counts of apply btn with reset btn
@app.callback(Output("apply-btn", "n_clicks"),
    [Input("reset-btn", "n_clicks"), Input("select-analysis-div", "className")], State("apply-btn", "n_clicks"))
def update_apply_btn(reset, analysis, apply):
    if reset or analysis == 'd-none':
        return 0
    else:
        raise PreventUpdate


#-- SECTION 3: Select the interface for loading Section 3: Upload input files; update only when 'reset' or 'apply' button is triggered
@app.callback(Output("upload-inputs-div", "className"),
    [Input("apply-btn", "n_clicks"), Input("type-of-project", "value")])
def display_loading_inputs(apply, action_type):
    if apply == 0:
        return 'd-none'
    else:
        return 'd-block'



