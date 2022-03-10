# -*- coding: utf-8 -*-
import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bio as dashbio

from app import app

### Default dataset
  ## must be in github repo in order for the path to work properly
  ## eventually this will be replaced with load
  ## these data or other data can be used as example
path = os.getcwd()+'/static/data/volcano/'
df = pd.read_csv(path+"volcano.csv")
uniprot_ids = df.GENE.tolist()

### BASIC CSS
  ## dictionary: key:value
  ## reference: https://www.w3schools.com/cssref/default.asp
  ## variables are user defined. 
drops = {'margin': '0 0 0.4vh 2vw', 'width': '13vw', 'display': 'inline-block', 'font-size': '2vh',
         'font-family': 'Ubuntu, sans-serif', 'color': 'dimgrey'}
btn_basic = {'margin': '0 0.5vw 0 0', 'padding': '0.2vh 0', 'font-size': '6vh', 'height': '3vh', 'width': '7vw'}
btn_style = {'background-color': '#eeece7', 'color': '#63533c'}
btn_selected_style = {'borderBottom': '3px solid #4682B4', 'borderTop': '0px solid #4682B4',
                      'background-color': '#95C8D8', 'color': 'black'}
btn_disabled_style = {'background-color': '#F8F9F9', 'color': '#95A5A6'}
btn_opts = {'height': '3vw', 'width': '3vw', 'border': '1px', 'margin-bottom': '0.45vw', 'font-size': '3vh'}
settings_style = {'width': 'fit-content', 'height': 'auto', 'display': 'block', 'background': '#eeece7', 'opacity': '0.95',
                  'border-radius': '5px 5px 5px 5px', 'position': 'absolute', 'top': '0', 'left': '0.5vw', 'z-index': '101',
                  'padding': '1vh 1vw 1vh 1vw'}
settings_close = {'margin': '0 0.5vw 0 0', 'border': '0px', 'color': '#63533c', 'font-size': '3vh', 'vertical-align': 'top',
                  'height':'2vw', 'width':'2vw', 'position':'absolute', 'top':'0', 'right':'0', 'z-index':'105'}

### Set comprehensive options
  ## define the layout 
  ## add widgets

  ## Buttons
#set_opts0 = html.Div(['opts0 - inputs loading options (now default data only)'], id='set_opts0', style={'display':'none', 'z-index':'110'})
set_opts1 = html.Div(['opts1 - inputs loading options (now default data only)'], id='set_opts1', style={'display':'none', 'z-index':'110'})
set_opts2 = html.Div([
    html.Div([
	## widgets in Button 2
	## https://github.com/ISUgenomics/interactiveGraphing -- dash core components dcc
# widget1
#        html.Div([
#            html.Label('Some options 1', className="labs"),
#            dcc.Dropdown(id='variable_1', placeholder="Select option", clearable=False, className="drops",
#                options=["black":"#000000"], value="#000000")], className="drops1",),
# widget2
        html.Div([ 
            html.Label('Select point size', className="labs labs2"),
            dcc.Input(id='variable_2', type='number', min=1, step=1, max=30, value=11)], className="drops1",),
# widget3
        html.Div([ 
            html.Label('Select Genome Wide line', className="labs labs2"),
            dcc.Input(id='variable_3', type='number', min=0, step=0.1, max=5, value=2.5)], className="drops1",),
    ], style={'display': 'inline-block'}),
# widget4
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
    ], style={'width':'40vw', 'display':'inline-block', 'vertical-align': 'middle', 'margin-left':'5px'}),
], id='set_opts2', style={'display':'none', 'z-index':'110'})
set_opts3 = html.Div(['opts3 - adjust title and axes'], id='set_opts3', style={'display':'none', 'z-index':'110'})
set_opts4 = html.Div(['opts4 - customize outputs for download'], id='set_opts4', style={'display':'none', 'z-index':'110'})

### HTML layout
layout = html.Div([
### void outputs from client side JS finctions
    dcc.Input(id="void1", value='', type='hidden'),


    html.Div([
#        html.Button('⚙', id='opts0', className='hovertext', style={**btn_basic, **btn_style, **btn_opts}, title='display settings'),
        html.Button('⚙', id='opts1', className='hovertext', style={**btn_basic, **btn_style, **btn_opts}, title='display settings'),
        html.Button('✾', id='opts2', style={**btn_basic, **btn_style, **btn_opts},
                    title='see objects and interactions'),
        html.Button('◩', id='opts3', style={**btn_basic, **btn_style, **btn_opts, 'color': '#95A5A6'},
                    title='see contact map'),
        html.Button('⟱', id='opts4', style={**btn_basic, **btn_style, **btn_opts}, title='download data'),
        html.Div([set_opts1, set_opts2, set_opts3, set_opts4,
#            html.Div(id='settings', style={'display':'block', 'z-index':'110'}),
            html.Button('×', id='close', style={**btn_style, **settings_close}, title='close options window'),
        ], id='settings-dir', style={**settings_style, 'left': '3.5vw', 'min-width': '45vw'}),
    ], style={'width': '4vw', 'position': 'absolute', 'left': '0', 'z-index': '100', 'marginLeft':'0.5vw'}),
# load plot
    html.Div([
# TODO: Add other types to plot circle square, triangle etc
        dcc.Loading(id='loading-volcano', children=[html.Div(dcc.Graph(id='graph-volcano', className="graph",
            config={'toImageButtonOptions': {'format':'png', 'width':1400, 'height':800, 'scale':1.5}, 'responsive': True,},))], type='circle'),
    ], className="graph-parent", style={'width':'94vw', 'marginLeft':'4vw'}),
])


### Clientside JS functions
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
      }
    };
    """,
    Output('void1', 'value'),
    [Input('opts1', 'n_clicks_timestamp'), Input('opts2', 'n_clicks_timestamp'),
     Input('opts3', 'n_clicks_timestamp'), Input('opts4', 'n_clicks_timestamp'),
     Input('close', 'n_clicks_timestamp')]
)


### Back end python functions


@app.callback(Output('graph-volcano', 'figure'),
              [Input('variable_1', 'value'), Input('variable_2', 'value'),
               Input('variable_3', 'value'), Input('volcano-input', 'value')])
def plot_volcano(var1, var2, var3, effects):

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
        title=dict(text='',),
        margin=dict(t=0),
        autosize=True,
    )

    return fig
