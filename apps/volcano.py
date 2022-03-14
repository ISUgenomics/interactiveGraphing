# -*- coding: utf-8 -*-
import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bio as dashbio

from app import app

#### Default dataset
# -- must be in github repo in order for the path to work properly
# -- eventually this will be replaced with load option for user-provided dataset

path = os.getcwd()+'/static/data/volcano/'
df = pd.read_csv(path+"volcano.csv")
uniprot_ids = df.GENE.tolist()

#### BASIC CSS
# -- Styles for HTML/DCC components can be set as a style dictionary composed of key:value pairs, where the keys are predefined CSS attributes
# -- A good reference for avaialble CSS atributes of style is https://www.w3schools.com/cssref/default.asp
# -- names of the variables below are user defined and can be used multiple times when defining styles of HTML/DCC components in the app layout

drops = {'margin': '0 0 0.4vh 2vw', 'width': '13vw', 'display': 'inline-block', 'font-size': '2vh',
         'font-family': 'Ubuntu, sans-serif', 'color': 'dimgrey'}
btn_basic = {'margin': '0 0.5vw 0 0', 'font-size': '6vh', 'height': '3vh', 'width': '7vw', 'text-align': 'center', 'padding':'0'}
btn_style = {'background-color': '#eeece7', 'color': '#63533c'}
btn_selected_style = {'borderBottom': '3px solid #4682B4', 'borderTop': '0px solid #4682B4',
                      'background-color': '#95C8D8', 'color': 'black'}
btn_disabled_style = {'background-color': '#F8F9F9', 'color': '#95A5A6'}
btn_opts = {'height': '3vw', 'width': '3vw', 'border': '1px', 'margin-bottom': '0.45vw', 'font-size': '3vh'}
settings_style = {'width': 'fit-content', 'height': 'auto', 'display': 'block', 'background': '#eeece7', 'opacity': '0.95',
                  'border-radius': '5px 5px 5px 5px', 'position': 'absolute', 'top': '8vh', 'left': '0.5vw', 'z-index': '101',
                  'padding': '1vh 1vw 1vh 1vw', 'marginLeft':'0.5vw'}
settings_close = {'margin': '0 0.5vw 0 0', 'border': '0px', 'color': '#63533c', 'font-size': '3vh', 'vertical-align': 'top',
                  'height':'2vw', 'width':'2vw', 'position':'absolute', 'top':'0', 'right':'0', 'z-index':'105'}

#### SET OPTIONS SECTION (left panel)
# -- HTML content for options displayed on-click for a given button
# -- HTML components (widgets) can be added programmatically using python Dash libaray:
# -- * dcc (dash core components) can be referenced here: https://dash.plotly.com/dash-core-components
# -- * html (classic html components) can be referenced here: https://dash.plotly.com/dash-html-components

# widgets displayed via Button 1
set_opts1 = html.Div([
    html.Label('Load inputs', className="main_labs"),
    html.Div([
        html.Label('Load example dataset', className="labs"),
        dcc.Checklist(id='default-data', options=['use default data'], value=["use default data"], style={'font-size':'2vh'})], className="drops1",),
    html.Div([
        html.Label('Load custom input data', className="labs"),
        dcc.Upload(id='upload-data',
                   children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                   style={'width': '100%', 'height': '120px', 'lineHeight': '120px', 'font-size': '2.5vh',
                          'margin': '2px 0.85vw 1.5vh 0', 'borderWidth': '2px', 'border-color': '#006699',
                          'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center',},
                   multiple=True)], className="drops1",),	# Allow multiple files to be uploaded

], id='set_opts1', style={'display':'none', 'z-index':'110'})

# widgets displayed via Button 2
set_opts2 = html.Div([
    html.Label('Set analytical params', className="main_labs"),
    html.Div([
        html.Div([
            html.Label('Some options 1', className="labs"),
            dcc.Dropdown(id='variable_1', placeholder="Select option", clearable=False, className="drops",
                options={"black":"#000000"}, value="#000000")], className="drops1",),
        html.Div([ 
            html.Label('Select point size', className="labs labs2"),
            dcc.Input(id='variable_2', type='number', min=1, step=1, max=30, value=11)], className="drops1",),
        html.Div([ 
            html.Label('Select Genome Wide line', className="labs labs2"),
            dcc.Input(id='variable_3', type='number', min=0, step=0.1, max=5, value=2.5)], className="drops1",),
    ], style={'display': 'inline-block'}),
    html.Div([ 
        html.Label('Select Effect Size range', className="labs labs2"),
        dcc.RangeSlider(
            id='volcano-input',
            min=-3,
            max=3,
            step=0.05,
            marks={i: {'label': str(i)} for i in range(-3, 3)},
            value=[-0.5, 1],
        ),
    ], style={'width':'22vw', 'display':'inline-block'}),
], id='set_opts2', style={'display':'none', 'z-index':'110'})

# widgets displayed via Button 3
set_opts3 = html.Div([
    html.Label('Adjust graph descriptions', className="main_labs"),
    html.Div([
        html.Label('Enter chart title', className="labs"),
        dcc.Input(id="input-title", type="text", placeholder="Customize the title", style={'width':'100%', 'margin': '2px 0.85vw 1.5vh 0',}),], className="drops1",),
    html.Div([
        html.Label('Enter chart title font size', className="labs"),
        dcc.Input(id="title-size", type="number", min=8, max=30, step=1, value=20, style={'width':'20%', 'margin': '2px 0.85vw 1.5vh 0',}),], className="drops1",),
], id='set_opts3', style={'display':'none', 'z-index':'110'})

# widgets displayed via Button 4
set_opts4 = html.Div([
    html.Label('Customize outputs for download', className="main_labs"),
    'opts4 - customize outputs for download'
], id='set_opts4', style={'display':'none', 'z-index':'110'})


#### HTML layout - the direct definition/assignment of components in the application layout
# -- layout is formally an HTML Div container
# -- the components in the content can be provided as a comma-separated list of mixed html/dcc Dash components
# -- each component can have its unique "id" attribute, which is used directly in the Input/Output arguments of plotly callbacks
# -- any other attribute of the component (options, value, style, etc.) can be used/changed via plotly callbacks
layout = html.Div([
# -- options container (left panel in the layout)
    html.Div([		# options parent container
	# a container holding buttons - always visible
        html.Div([
            html.Button('⇭', id='opts1', style={**btn_basic, **btn_style, **btn_opts}, title='input settings'),
            html.Button('⚙', id='opts2', style={**btn_basic, **btn_style, **btn_opts},
                    title='analysis settings'),
            html.Button('Ꭵ', id='opts3', style={**btn_basic, **btn_style, **btn_opts},
                    title='description settings'),
            html.Button('⤋', id='opts4', style={**btn_basic, **btn_style, **btn_opts}, title='download settings'),
        ], ),
        #style={ 'height': '100%', 'position': 'absolute', 'top': '1.5vh'}
        # a container holding options for a agiven button - visible via button on-click
        html.Div([set_opts1, set_opts2, set_opts3, set_opts4,
            html.Div(id='settings', style={'display':'block', 'z-index':'110'}),
            html.Button('×', id='close', style={**btn_style, **settings_close}, title='close options window'),
        ], id='settings-dir', style={**settings_style, 'width': '23vw'}),
    ], id='options', style={'display':'inline-block', 'height':'100vh', 'background-color':'#006699', 'position':'absolute', 'top':'0', 'margin':'0', 'padding':'1vw'}),		# id and style of "options" parent container
# -- graph container (right panel in the layout) - here we only declare the graph container and dcc.Graph component
    html.Div([
        dcc.Loading(id='loading-volcano', children=[html.Div(dcc.Graph(id='graph-volcano', className="graph",
            config={'toImageButtonOptions': {'format':'png', 'width':1400, 'height':800, 'scale':1.5}, 'responsive': True,},))], type='circle'),
    ], id='graph', className="graph-parent", style={'width':'80vw', 'marginLeft':'2vw', 'position':'absolute', 'right': '0'}),
# -- void outputs from client side JS finctions - plotly callbacks always require output argument, it can be void if none value is returned
    dcc.Input(id="void1", value='', type='hidden', style={'height':'0', 'width':'0'}),
], style={'position':'relative', 'margin':'0', 'padding':'0'})


#### Clientside JS functions - to add user-triggered interactivity in the options panel
app.clientside_callback(
    """
    function (n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5) {
      var targetDiv = document.getElementById("settings-dir");
      var vals = [n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5];
      var vals2 = vals.map((e)=>isNaN(e)?"":e)
      var max = Math.max(...vals2);
      var selected = 'none';
      if (n_clicks1 === max) {
          var selected = "set_opts1";
      } else if (n_clicks2 === max) {
          var selected = "set_opts2";
      } else if (n_clicks3 === max) {
          var selected = "set_opts3";
      } else if (n_clicks4 === max) {
          var selected = "set_opts4";
      } else {
          targetDiv.style.display = "none";
      }
      if (selected != "none") {
          const a = ["set_opts1", "set_opts2", "set_opts3", "set_opts4"];
          for (const element of a) {
             document.getElementById(element).style.display = "none";
          }
          document.getElementById(selected).style.display = "inline-block";
          targetDiv.style.display = "block";
          document.getElementById("graph").style.width = "72vw";
          document.getElementById("options").style.width = "25vw";
      }
      else {
          document.getElementById("graph").style.width = "82vw";
          document.getElementById("options").style.width = "14vw";
      }
    };
    """,
    Output('void1', 'value'),
    [Input('opts1', 'n_clicks_timestamp'), Input('opts2', 'n_clicks_timestamp'),
     Input('opts3', 'n_clicks_timestamp'), Input('opts4', 'n_clicks_timestamp'),
     Input('close', 'n_clicks_timestamp')]
)


#### PLOTLY CALLBACKS SECTION: python functions that manages changes on the interactive graph

@app.callback(Output('graph-volcano', 'figure'),
              [Input('variable_1', 'value'), Input('variable_2', 'value'),
               Input('variable_3', 'value'), Input('volcano-input', 'value'), 
               Input('input-title', 'value'), Input('title-size', 'value')])
def plot_volcano(var1, var2, var3, effects, title, ti_size):

    fig = dashbio.VolcanoPlot(
        dataframe=df,
        genomewideline_value=var3,
        effect_size_line=effects,
        effect_size="log2(FC)",
        p="raw.pval",
        snp="GENE",
        gene="GENE",
        logp=True,
        xlabel="effect size",
        ylabel="-log10(p)",
        point_size=var2,
    )

    fig.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 1)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
        font_color="rgba(0,0,0,1)",
        title=dict(text=title, font=dict(size=ti_size)),
        margin=dict(t=0),
        autosize=True,
    )

    return fig
