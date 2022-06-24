# -*- coding: utf-8 -*-
from urllib import request
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dash import no_update


from app import app
from .paths import *

### LAYOUT COMPONENTS


#-- SECTION A: Use pre-defined pipeline
list_of_pipelines = [
    {'label' : 'pipeline-1 (scatter, volcano)', 'value' : 'pipeline-1', 'title' : 'The pipeline is composed of scatter and volcano plots.'},
    {'label' : 'pipeline-2 (scatter, heatmap)', 'value' : 'pipeline-2', 'title' : 'The pipeline is composed of scatter and heatmap plots.'},
    {'label' : 'pipeline-3 (scatter, clustergram)', 'value' : 'pipeline-3', 'title' : 'The pipeline is composed of scatter and clustergram plots.'},
]		# later write an automatic function that reads ready-made piplines from the sqlite db

list_of_pipelines.insert(0, {'label' : 'none', 'value' : 'none', 'title' : ''})

ready_pipeline_opts = [
    dcc.RadioItems(
        options=list_of_pipelines,
        value='none',
        persistence=True,
        persistence_type='session',
        inline=False,
        id="selected-pipelines",
        labelClassName="checkbox-label", labelStyle = {'width' : '100%'}
    ),
    html.Hr(),
    dcc.Input(id="custom-tab-name", type="text", placeholder="enter tab name", value='', debounce=True),
    dbc.Button("add tab", id="add-tab-btn", n_clicks=0, size="sm", outline=True, color="secondary", className="me-1 align-top", style={'marginLeft':'1vw', 'width':'29%'}),
]


#-- SECTION B: Add custom analysis
list_of_charts = ['scatter', 'volcano', 'heatmap', 'dendrogram', 'clustergram']		# later write an automatic function that checks available types of plots

custom_analysis_opts = [
    dcc.Checklist(
        options=[{'label' : i, 'value' : i, 'title' : 'The '+i+' plot will be added to your analysis.'} for i in list_of_charts],
        value=[],
        persistence=True,
        persistence_type='session',
        inline=True,
        labelClassName="checkbox-label",
        id="selected-charts",
    ),
    html.Hr(),
    dcc.Input(id="custom-tab-name2", type="text", placeholder="enter tab name", value='', debounce=True),
    dbc.Button("add tab", id="add-tab-btn2", n_clicks=0, size="sm", outline=True, color="secondary", className="me-1 align-top", style={'marginLeft':'1vw', 'width':'29%'}),
]


#-- SECTION C. summary of selected settings

settings_select_analysis = [
    html.Div(id="settings-select-analysis", className="mt-3")
]


### CALLBACKS

#-------------------------------------------------
#-- SECTION A: Activate add tab button for pipelines
@app.callback(
    [Output("add-tab-btn", "color"), Output("add-tab-btn", "disabled"), Output("custom-tab-name", "value")],
    [Input("selected-pipelines", "value")])
def activate_addtab_btn(pipeline):
    if pipeline == 'none':
        return ["secondary", True, '']
    else:
        tab_name = pipeline + "-" + str(dt.datetime.now().strftime("%f"))
        return ["success", False, tab_name]


#-- SECTION B: Activate add tab button for custom charts
@app.callback(
    [Output("add-tab-btn2", "color"), Output("add-tab-btn2", "disabled"), Output("custom-tab-name2", "value")],
    [Input("selected-charts", "value")])
def activate_addtab_btn2(chart):
    if not len(chart):
        return ["secondary", True, '']
    else:
        tab_name = "custom-" + str(dt.datetime.now().strftime("%f"))
        return ["success", False, tab_name]


#-- SECTION C: Activate reset button
@app.callback(
    [Output("reset-btn", "color"), Output("reset-btn", "disabled")],
    [Input("selected-pipelines", "value"), Input("selected-charts", "value"), Input("type-of-project", "value")])
def activate_reset_btn(pipelines, charts, action_type):
    if action_type == "open" and not len(charts):
        return ["secondary", True]
    elif pipelines != 'none' or len(charts):
        return ["danger", False]
    else:
        return ["secondary", True]


#-- SECTION C: Activate apply button
@app.callback(
    [Output("apply-btn", "color"), Output("apply-btn", "disabled")],
    [Input("selected-pipelines", "value"), Input("selected-charts", "value")])
def activate_apply_btn(pipelines, charts):
    if pipelines != 'none' or len(charts):
        return ["success", False]
    else:
        return ["secondary", True]


#-- SECTION C: Display summary of settings
@app.callback(
    Output("settings-select-analysis", "children"),
    [Input("selected-pipelines", "value"), Input("selected-charts", "value"), Input("project-name", "data")])
def display_analysis_settings(pipelines, charts, project_name):
    info1 = "Analysis options will be displayed when you select a project in section 1. Manage project(s)."
    info2 = ""
    if project_name != "":
        if pipelines == 'none' and not len(charts):
            info1 = "Please select pre-defined pipline and/or customize your analysis with selected charts."
        else:
            info1 = "The following pipeline will be applied in your analysis: " + str(pipelines)
            info2 = "The following charts will be added to your analysis: " + str(', '.join(charts))
    return [
        html.Label(info1, className="label-tertiary grayed"),
        html.Label(info2, className="label-tertiary grayed"),
    ]
