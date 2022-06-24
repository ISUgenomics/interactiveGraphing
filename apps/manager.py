# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bio as dashbio

from app import app
from .analysis_setup import *
from .sqlite_db import *



### CONNECT DATABASE ('projects' and 'tabs' tables)
dbmgr = DBM("projects.db")			# create sqlite connection
dbmgr.create_table(create_projects_table)	# create projects table (if NOT exist)
dbmgr.create_table(create_tabs_table)		# create tabs table (if NOT exist)

#dbmgr.delete_entry('projects', '', '')
#dbmgr.delete_entry('tabs', '', '')
#for row in dbmgr.query('projects', '', ''):
#  print("here2: ", row)

#tab = ('pipeline', 1, 2, 'pipelines', '')
#tid = dbmgr.insert_entry(insert_tab, tab);

dbmgr.conn.close()




### LAYOUT COMPONENTS
#-- Container for all void objects
voids = html.Div([
         dcc.Input(id="void", value='', type='hidden'),
         dcc.Input(id="void0", value='', type='hidden'),	# used in the JS to add tab's close btn
         dcc.Input(id="void1", value='', type='hidden'),	# used in the update_projects_table()
        ], style={'visibility' : 'hidden'})


#-- Initial tab: analysis setup; next tabs are added dynamically
tab_1 = {'props': {'children': None, 'id': 'tab-1', 'className': 'plotly-tab', 'label': 'Analysis SetUp', 'selected_className': 'plotly-tab-selected', 'value': 'tab-1'}, 'type': 'Tab', 'namespace': 'dash_core_components'}
basic_tabs = [dcc.Tabs(id='plotly-tabs', value='tab-1', mobile_breakpoint=400,
               children=[
                 dcc.Tab(id='tab-1', label='Analysis SetUp', value='tab-1', className='plotly-tab', selected_className='plotly-tab-selected'),
               ], className='plotly-tabs', parent_className='plotly-tabs-parent', persistence=True, persistence_type='session')
             ]


#-- Container for session storage variables
storage = html.Div([
         dcc.Store(id="project-name", data='', storage_type='session'),
         dcc.Store(id="path-to-project", data='', storage_type='session'),
         dcc.Store(id="tabs", data=basic_tabs, storage_type='session'),				# real content of tabs-bar robust for page refreshing
         dcc.Store(id="all-tabs", data={1:'setup'}, storage_type='session'),		# all tabs created (and not deleted) in a given project; dictionary = int : tab-label
         dcc.Store(id="open-tabs", data={}, storage_type='session'),		# currently opened tabs; list of tab ids
         dcc.Store(id="list-of-files", data='', storage_type='session'),
         dcc.Store(id="pid", data=0, storage_type='session'),				# project_id in the projects table in the DB; 0 for temporary projects
        ], style={'visibility' : 'hidden'})


tab_close_btn = html.Button('x', id='close', )


#-------------------------
### Main Layout of the app
layout = html.Div([
              storage, voids,

              html.Div(children = basic_tabs, id='tabs-bar',),
              html.Div(id='plotly-tab-content', className='plotly-tab-content'),
         ], id="layout", style={'background-color' : '#f9f9f9'})


#----------------------------
#### PLOTLY CALLBACKS SECTION: python functions that manages changes on the interactive graph

#-- Display content of selected tab
@app.callback(Output('plotly-tab-content', 'children'),
             [Input('plotly-tabs', 'value')],
              prevent_initial_call = False)
def display_tab_content(selected_tab):
    if selected_tab == 'tab-1':
        return analysis_setup
    else:
        return html.Div()		###!!! UPDATE REQUIRED: display content for the corresponding tab (now just empty div)


#-- Add close btn for new tabs
#app.clientside_callback(
#    """
#    function (tabs) {
#      if tabs {
#        var close = 'close-';
#        var ids = Object.keys(tabs);
#        alert(tabs);
#        for (var i = 0; i < ids.length; i++) {
#          alert(i);
#          var tmp = document.getElementById(close.concat(ids[i]));
#          if (ids[i] !== 'tab-1' && tmp == null) {
#            var tab = document.getElementById(ids[i]);
#            tab.style.position = "relative";
#            var buttonEl = document.createElement("a");
#            buttonEl.id = close.concat(ids[i]);
#            buttonEl.style.position = "absolute";
#            buttonEl.style.right = "5px";
#            var buttonTextEl = document.createElement("span");
#            buttonTextEl.innerText = "x";
#            buttonEl.appendChild(buttonTextEl);
#            buttonEl.addEventListener('click', closeTabOnClick);
#            tab.appendChild(buttonEl);
#          };
#        };
#      };
#    };
#    """,
#    Output('void0', 'value'),
#    [Input("open-tabs", "data"), ]
#)


### -------------------------------------------
# CALLBACKS to manage database content

#-- Add / remove entries (records for projects) from the 'project' table in the database; return pid of a current project
@app.callback(Output('pid', 'data'),
             [Input('all-projects', 'options'), Input('project-name', 'data')],
              prevent_initial_call = False)
def update_projects_table(projects, current_project):
    pid = 0
    db = DBM("projects.db")
    db_vals = db.cur.execute("SELECT name FROM projects").fetchall()
    db_vals = set([i[0] for i in db_vals])				# projects available in the table
    projects = set(projects)						# projects saved on disk
    removing = list(sorted(db_vals - projects))
    adding = list(sorted(projects - db_vals))

    for i in adding:
        project = (i, 'path/to/project', '')
        db.insert_entry(insert_project, project)
    for i in removing:
        p_id = int(db.query('projects', 'id', 'name', i)[0][0])		# identifies project id
        db.delete_entry('tabs', 'project_id', p_id)			# removes tabs related to the project
        db.delete_entry('projects', 'name', i)				# removes project

    if not current_project.startswith('tmp'):
        pid = int(db.query('projects', 'id', 'name', current_project)[0][0])	# [(2,)]
    db.conn.close()

    return pid


#-- add new tab into the 'tabs' table in the database and update open-tabs list
@app.callback(Output('open-tabs', 'data'),
             [Input('add-tab-btn', 'n_clicks'), Input('add-tab-btn2', 'n_clicks'), Input('pid', 'data')],
             [State('custom-tab-name', 'value'), State('custom-tab-name2', 'value'),
              State("selected-pipelines", "value"), State("selected-charts", "value")],
              prevent_initial_call = True)
def add_new_tab(add_tab_pipeline, add_tab_custom, pid, tab_name_pipeline, tab_name_chart, pipelines, charts):	###!!! UPDATE REQUIRED: remove closed tabs and change status in the table
    open_tabs = {}
    ctx = dash.callback_context.triggered_id
    if pid != 0:
        n = 2
        db = DBM("projects.db")
        tids = [i[0] for i in db.query('tabs', 'id', 'project_id', pid)]
        if len(tids):
            n = max(map(int, tids)) + 1					# unique index of a new tab
        if ctx == 'add-tab-btn' and tab_name_pipeline != '':		# add new tab based on a pipeline
            db_tab = ('tab-'+str(n), tab_name_pipeline, 1, int(pid), pipelines, '')
        elif ctx == 'add-tab-btn2' and tab_name_chart != '':		# add new tab based on custom charts
            db_tab = ('tab-'+str(n), tab_name_chart, 1, int(pid), '', str(charts))
        try:
            tid = db.insert_entry(insert_tab, db_tab)			# add record into tabs table in the database
        except:
            pass

        for i in db.cur.execute("SELECT tab_id, name FROM tabs WHERE project_id=? and status_id=?", (pid, 1)):
            if not i in open_tabs:
                open_tabs[i[0]] = i[1]
        db.conn.close()
    return open_tabs



#-- generate 'tabs' content for current project:
@app.callback(Output('tabs', 'data'),
             [Input('open-tabs', 'data')],
             [State('pid', 'data'), State('tabs-bar', 'children')],
              prevent_initial_call = True)
def add_tabs_content(open_tabs, pid, tabs_bar):

    tabs = tabs_bar
    tabs[0]['props']['children'] = [tab_1]
    if pid != 0:
        for tag in open_tabs:
            new_tab = {'props': {'children': None, 'id': tag, 'className': 'plotly-tab', 'label': open_tabs[tag], 'selected_className': 'plotly-tab-selected', 'value': tag}, 'type': 'Tab', 'namespace': 'dash_core_components'}
            tabs[0]['props']['children'].append(new_tab)

    return tabs


#-- Update displayed tabs
@app.callback(Output('tabs-bar', 'children'),
             [Input('tabs', 'data')],
              prevent_initial_call = True)
def update_displayed_tabs(tabs):
    return tabs





