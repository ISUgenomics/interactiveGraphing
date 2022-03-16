# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bio as dashbio

from app import app

#### Default dataset
# -- must be in github repo in order for the path to work properly
# -- eventually this will be replaced with load option for user-provided dataset

path = os.getcwd()+'/static/data/volcano/'
df = pd.read_csv(path+"volcano.csv")
uniprot_ids = df.GENE.tolist()

#### Global variables
fonts = ["Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", 
         "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"]
colors = ["aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", "black", 
          "blanchedalmond", "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", 
          "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan",
          "darkgoldenrod", "darkgray", "darkgrey", "darkgreen", "darkkhaki", "darkmagenta", "darkolivegreen",
          "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen", "darkslateblue", 
          "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue",
          "dimgray", "dimgrey", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
          "ghostwhite", "gold", "goldenrod", "gray", "grey", "green", "greenyellow", "honeydew", "hotpink", 
          "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", 
          "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgrey",
          "lightgreen", "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", 
          "lightslategrey", "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", 
          "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", 
          "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue",
          "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace", "olive", "olivedrab", 
          "orange", "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", 
          "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue", "purple", "red", "rosybrown",
          "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna", "silver", 
          "skyblue", "slateblue", "slategray", "slategrey", "snow", "springgreen", "steelblue", "tan", "teal",
          "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen"]

#### BASIC CSS
# -- Styles for HTML/DCC components can be set as a style dictionary composed of key:value pairs, where the keys are predefined CSS attributes
# -- A good reference for avaialble CSS atributes of style is https://www.w3schools.com/cssref/default.asp
# -- names of the variables below are user defined and can be used multiple times when defining styles of HTML/DCC components in the app layout

drops = {'margin': '0 0 0.4vh 2vw', 'width': '13vw', 'display': 'inline-block', 'font-size': '2vh',
         'font-family': 'Ubuntu, sans-serif', 'color': 'dimgrey'}
btn_basic = {'margin': '0 0.5vw 0 0', 'font-size': '3vh', 'min-height':'25px', 'max-height':'52px', 'min-width':'25px', 'max-width':'52px', 'text-align': 'center', 'padding':'0'}
btn_style = {'background-color': '#eeece7', 'color': '#63533c'}
btn_selected_style = {'borderBottom': '3px solid #4682B4', 'borderTop': '0px solid #4682B4',
                      'background-color': '#95C8D8', 'color': 'black'}
btn_disabled_style = {'background-color': '#F8F9F9', 'color': '#95A5A6'}
btn_opts = {'height': '3vw', 'width': '3vw', 'border': '1px', 'margin-bottom': '0.45vw', 'font-size': '3vh'}
settings_style = {'width': '23vw', 'height': 'auto', 'display': 'block', 'background': '#eeece7', 'opacity': '1',
                  'border-radius': '5px 5px 5px 5px', 'position': 'absolute', 'top': '8vh', 'left': '0.5vw', 'z-index': '101',
                  'padding': '1vh 1vw 1vh 1vw', 'marginLeft':'0.5vw'}
settings_close = {'margin': '0', 'border': '0px', 'color': '#63533c', 'font-size': '24px', 'vertical-align': 'top',
                  'min-height':'25px', 'max-height':'52px', 'min-width':'25px', 'max-width':'52px',
                  'position':'absolute', 'top':'0', 'right':'0', 'z-index':'105'}

#### SET OPTIONS SECTION (left panel)
# -- HTML content for options displayed on-click for a given button
# -- HTML components (widgets) can be added programmatically using python Dash libaray:
# -- * dcc (dash core components) can be referenced here: https://dash.plotly.com/dash-core-components
# -- * html (classic html components) can be referenced here: https://dash.plotly.com/dash-html-components

# widgets displayed via Button 1: upload inputs
set_opts1 = html.Div([
    html.Label('Load inputs', className="main_labs"),
    html.Div([
        html.Label('Load example dataset', className="labs"),
        dcc.Checklist(id='default-data', options=[{'label': 'use default data', 'value': '0', 'disabled': False}], value=['0'], style={'font-size':'2vh'})], className="drops",),
    html.Div([
        dcc.Input(id="user-files", value='', type='hidden', style={'height':'0', 'width':'0'}),
        html.Label('Load custom input data', className="labs"),
        dcc.Upload(id='upload-data',
                   children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                   style={'width': '100%', 'height': '120px', 'lineHeight': '120px', 'font-size': '2.5vh',
                          'margin': '2px 0.85vw 1.5vh 0', 'borderWidth': '2px', 'border-color': '#006699',
                          'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center',},
                   multiple=True)], className="drops", style={'width':'99%'}),	# Allow multiple files to be uploaded
    html.Div([
        html.Label('Select dataset(s) for plotting', className="labs"),
        dcc.Checklist(id='select-data', options=[], value=[], style={'font-size':'2vh'})], className="drops",),

], id='set_opts1', style={'display':'none', 'z-index':'110'})

# widgets displayed via Button 2: set analytical params
set_opts2 = html.Div([
    html.Label('Set analytical params', className="main_labs"),
    html.Div([
        html.Div([
            html.Label('Some options 1', className="labs"),
            dcc.Dropdown(id='variable_1', placeholder="Select option", clearable=False, style={'width':'6.5vw'},
                options={"black":"#000000"}, value="#000000")], className="drops",),
        html.Div([ 
            html.Label('Select point size', className="labs labs2"),
            dcc.Input(id='variable_2', type='number', min=1, step=1, max=30, value=11, style={'width':'6.5vw'},)], className="drops",),
        html.Div([ 
            html.Label('Select Genome Wide line', className="labs labs2"),
            dcc.Input(id='variable_3', type='number', min=0, step=0.1, max=5, value=2.5, style={'width':'6.5vw'},)], className="drops",),
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

# widgets displayed via Button 3: adjust graph descriptions
set_opts3 = html.Div([
    html.Label('Adjust graph descriptions', className="main_labs"),
    
    html.Button("Edit title", id="title", className="collapsible",),
    html.Div([
        html.Div([
            html.Label('Enter chart title �', title="Type custom title and press enter.\nTo introduce a multi-line title, split the lines using the <br> syntax.", className="labs"),
            dcc.Input(id="chart-title", type="text", placeholder="Customize the title", value="Example Volcano Plot", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'width':'12vw'}),
        html.Div([
            html.Label('Font family �', title="HTML font family - the typeface that will be applied by the web browser.", className="labs"),
            dcc.Dropdown(id="title-font", options=[{'label': i, 'value': i} for i in fonts], value="Arial", style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'10vw', 'verticalAlign':'top'}),

        html.Div([
            html.Label('Font: size', className="labs"),
            dcc.Input(id="title-size", type="number", min=1, step=1, value=30, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'width':'4.5vw'}),
        html.Div([
            html.Label('- color �', title="Enter color value and press enter.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="title-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),
        html.Div([
            html.Label('- pos X �', title="The title will be centered horizontally on the entered value. Allowed range from 0 to 1 in 0.01 increments.", className="labs"),
            dcc.Input(id="title-x", type="number", min=0, max=1, step=0.01, value=0.6, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- pos Y �', title="The title will be centered vertically on the entered value. Allowed range from 0 to 1 in 0.01 increments.", className="labs"),
            dcc.Input(id="title-y", type="number", min=0, max=1, step=0.01, value=1, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
    ], id="title-content", className="coll-content"),


    html.Button("Edit X-axis", id="xaxis", className="collapsible",),
    html.Div([
        html.Div([
            html.Label('� X-axis Title:', title="Type custom title for X-axis and press enter.\nTo introduce a multi-line title, split the lines using the <br> syntax.", className="labs"),
            dcc.Input(id="xaxis-title", type="text", placeholder="Customize the title", value="Effect size", debounce=True, style={'width':'100%', 'margin': '2px 0.85vw 0 0',}),], className="drops", style={'width':'10vw'}),
        html.Div([
            html.Label('- size', className="labs"),
            dcc.Input(id="xaxis-size", type="number", min=1, step=1, value=30, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Enter color value of X-label and press enter.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="xaxis-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Hr([], style={'margin':'0 0 1vh 0'}),

        html.Div([
            html.Label('� Line:', className="labs"),
            dcc.Dropdown(id="xline-show", options=[{'label': str(i), 'value': i} for i in [True, False]], value=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- mirror �', title="Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area.\nIf 'True', the axis lines are mirrored.\nIf 'ticks', the axis lines and ticks are mirrored.\nIf 'False', mirroring is disable.\nIf 'all', axis lines are mirrored on all shared-axes subplots.\nIf 'allticks', axis lines and ticks are mirrored on all shared-axes subplots.", className="labs"),
            dcc.Dropdown(id="xline-mirror", options=[{'label': str(i), 'value': i} for i in [True, "ticks", False, "all", "allticks"]], value=False, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'verticalAlign':'top'}),
        html.Div([
            html.Label('- width �', title="Sets the width (in px) of the axis line. Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="xline-width", type="number", min=0, step=1, value=1, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Sets the axis line color.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="xline-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Hr([], style={'margin':'0 0 1vh 0'}),

        html.Div([
            html.Label('� Grid:', className="labs"),
            dcc.Dropdown(id="xgrid-show", options=[{'label': str(i), 'value': i} for i in [True, False]], value=False, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- width �', title="Sets the tick width (in px). Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="xgrid-width", type="number", min=0, step=1, value=1, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Sets the color of the grid lines.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="xgrid-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Hr([], style={'margin':'0 0 1vh 0'}),

        html.Div([
            html.Label('� Ticks:', className="labs"),
            dcc.Dropdown(id="xtick-show", options=[{'label': 'outside', 'value': 'outside'}, {'label': 'inside', 'value': 'inside'}, {'label': 'none', 'value': ''}], value='outside', style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- width �', title="Sets the tick width (in px). Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="xtick-width", type="number", min=0, step=1, value=1, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- len �', title="Sets the tick length (in px). Type number greater than or equal to 0, default = 5.", className="labs"),
            dcc.Input(id="xtick-length", type="number", min=0, step=1, value=5, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Enter color value and press enter.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="xtick-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Div([
            html.Label('� Labels:', className="labs"),
            dcc.Dropdown(id="xtilab-show", options=[{'label': str(i), 'value': i} for i in [True, False]], value=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- size �', title="Sets the tick width (in px). Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="xtilab-size", type="number", min=1, step=1, value=20, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- angle �', title="Sets the angle of the tick labels with respect to the horizontal, e.g., a value of -90 draws the tick labels vertically.", className="labs"),
            dcc.Input(id="xtilab-angle", type="number", min=-359, max=359, step=1, value=0, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Enter color value and press enter.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="xtilab-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

    ], id="xaxis-content", className="coll-content"),


    html.Button("Edit Y-axis", id="yaxis", className="collapsible",),
    html.Div([
        html.Div([
            html.Label('� Y-axis Title:', title="Type custom label for Y-axis and press enter.\nTo introduce a multi-line title, split the lines using the <br> syntax.", className="labs"),
            dcc.Input(id="yaxis-title", type="text", placeholder="Customize the title", value="-log10(p)", debounce=True, style={'width':'100%', 'margin': '2px 0.85vw 0 0',}),], className="drops", style={'width':'10vw'}),
        html.Div([
            html.Label('- size', className="labs"),
            dcc.Input(id="yaxis-size", type="number", min=1, step=1, value=30, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Enter color value of Y-label and press enter.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="yaxis-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Hr([], style={'margin':'0 0 1vh 0'}),

        html.Div([
            html.Label('� Line:', className="labs"),
            dcc.Dropdown(id="yline-show", options=[{'label': str(i), 'value': i} for i in [True, False]], value=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- mirror �', title="Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area.\nIf 'True', the axis lines are mirrored.\nIf 'ticks', the axis lines and ticks are mirrored.\nIf 'False', mirroring is disable.\nIf 'all', axis lines are mirrored on all shared-axes subplots.\nIf 'allticks', axis lines and ticks are mirrored on all shared-axes subplots.", className="labs"),
            dcc.Dropdown(id="yline-mirror", options=[{'label': str(i), 'value': i} for i in [True, "ticks", False, "all", "allticks"]], value=False, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'verticalAlign':'top'}),
        html.Div([
            html.Label('- width �', title="Sets the width (in px) of the axis line. Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="yline-width", type="number", min=0, step=1, value=1, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Sets the axis line color.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="yline-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Hr([], style={'margin':'0 0 1vh 0'}),

        html.Div([
            html.Label('� Grid:', className="labs"),
            dcc.Dropdown(id="ygrid-show", options=[{'label': str(i), 'value': i} for i in [True, False]], value=False, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- width �', title="Sets the tick width (in px). Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="ygrid-width", type="number", min=0, step=1, value=1, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Sets the color of the grid lines.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="ygrid-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Hr([], style={'margin':'0 0 1vh 0'}),

        html.Div([
            html.Label('� Ticks:', className="labs"),
            dcc.Dropdown(id="ytick-show", options=[{'label': 'outside', 'value': 'outside'}, {'label': 'inside', 'value': 'inside'}, {'label': 'none', 'value': ''}], value='outside', style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- width �', title="Sets the tick width (in px). Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="ytick-width", type="number", min=0, step=1, value=1, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- len �', title="Sets the tick length (in px). Type number greater than or equal to 0, default = 5.", className="labs"),
            dcc.Input(id="ytick-length", type="number", min=0, step=1, value=5, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Enter color value and press enter.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="ytick-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),

        html.Div([
            html.Label('� Labels:', className="labs"),
            dcc.Dropdown(id="ytilab-show", options=[{'label': str(i), 'value': i} for i in [True, False]], value=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops", style={'verticalAlign':'top', 'width':'4.5vw'}),
        html.Div([
            html.Label('- size �', title="Sets the tick width (in px). Type number greater than or equal to 0, default = 1.", className="labs"),
            dcc.Input(id="ytilab-size", type="number", min=1, step=1, value=20, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- angle �', title="Sets the angle of the tick labels with respect to the vertical, e.g., a value of -90 draws the tick labels horizontally.", className="labs"),
            dcc.Input(id="ytilab-angle", type="number", min=-359, max=359, step=1, value=0, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec"),
        html.Div([
            html.Label('- color �', title="Enter color value and press enter.\nAvailable options include: \n-common name, e.g., black\n-hex, e.g., #000000\n-rgb, e.g., rgb(0, 0, 0)\n-hsl, e.g., hsl(0, 100%, 0%) ", className="labs"),
            dcc.Input(id="ytilab-color", type="text", placeholder="#000000", value="black", debounce=True, style={'width':'100%', 'margin': '2px 0 0 0',}),], className="drops drops_sec", style={'width':'6.5vw'}),
    ], id="yaxis-content", className="coll-content"),

], id='set_opts3', style={'display':'none', 'zIndex':'110'})


# widgets displayed via Button 4: outputs for download
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
        # a container holding options for a agiven button - visible via button on-click
        html.Div([set_opts1, set_opts2, set_opts3, set_opts4,
            html.Div(id='settings', style={'display':'block', 'z-index':'110'}),
            html.Button('×', id='close', style={**btn_style, **settings_close}, title='close options window'),
        ], id='settings-dir', style=settings_style),
    ], id='options', style={'display':'inline-block', 'height':'100vh', 'background-color':'#006699', 'position':'absolute', 'top':'0', 'margin':'0', 'padding':'1vh 1vw', 'overflow-y': 'scroll'}),		# id and style of "options" parent container
# -- graph container (right panel in the layout) - here we only declare the graph container and dcc.Graph component
    html.Div([
        dcc.Loading(id='loading-volcano', children=[html.Div(dcc.Graph(id='graph-volcano', className="graph",
            config={'toImageButtonOptions': {'format':'png', 'width':1400, 'height':800, 'scale':1.5}, 'responsive': True,},))], type='circle'),
    ], id='graph', className="graph-parent", style={'width':'80vw', 'marginLeft':'2vw', 'position':'absolute', 'right': '0'}),
# -- void outputs from client side JS finctions - plotly callbacks always require output argument, it can be void if none value is returned
    dcc.Input(id="void1", value='', type='hidden', style={'height':'0', 'width':'0'}),
    dcc.Input(id="void2", value='', type='hidden', style={'height':'0', 'width':'0'}),
], style={'position':'relative', 'margin':'0', 'padding':'0'})


#### Clientside JS functions - to add user-triggered interactivity in the options panel

# Display content for a given settings section (action Button.onClick())
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
          document.getElementById("graph").style.width = "71.3vw";
          document.getElementById("options").style.width = "25.7vw";
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

# Display content of a given subsection for setting section of 'Adjust graph decription'
app.clientside_callback(
    """
    function (n_title, n_xaxis, n_yaxis) {
      var content = "";
      var vals = [n_title, n_xaxis, n_yaxis];
      for (let i = 0; i < vals.length; i++) {
        if (vals[i] === undefined) {
          vals[i] = 0;
        }
      }
      var max = Math.max(...vals);
      if (n_title === max) {
        var content = document.getElementById("title-content");
        document.getElementById("title").classList.toggle("active");
      } else if (n_xaxis === max) {
        var content = document.getElementById("xaxis-content");
        document.getElementById("xaxis").classList.toggle("active");
      } else if (n_yaxis === max) {
        var content = document.getElementById("yaxis-content");
        document.getElementById("yaxis").classList.toggle("active");
      }
      if (content != "") {
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      }
    };
    """,
    Output('void2', 'value'),
    [Input('title', 'n_clicks_timestamp'), Input('xaxis', 'n_clicks_timestamp'), Input('yaxis', 'n_clicks_timestamp')]
)


#### PLOTLY CALLBACKS SECTION: python functions that manages changes on the interactive graph

# The function returns updated dictionary of filename:file_content for all user-loaded files
@app.callback(Output('user-files', 'value'),
              [Input('upload-data', 'filename'), Input('upload-data', 'contents')],
              State('user-files', 'value'), prevent_initial_call = True)
def plot_volcano(names, contents, files):
    if names is not None:
        if files == '':
            files = {i:contents[num] for num,i in enumerate(names)}
        else:
            files = json.loads(files)
            for num,i in enumerate(names):
                files[i] = contents[num]
        return json.dumps(files)


# The function updates a radio-button list of user-loaded files that can be used for plotting
@app.callback(Output('select-data', 'options'),
              Input('user-files', 'value'), prevent_initial_call = True)
def plot_volcano(files):
    if files != '':
        return list(json.loads(files).keys())


# The function switches off the default dataset once the radio-button with user-provided data is selected
@app.callback([Output('default-data', 'value'), Output('default-data', 'options'), Output('default-data', 'style')],
              Input('select-data', 'value'), State('default-data', 'style'), prevent_initial_call = True)
def plot_volcano(selected_files, style):
    if selected_files is not None:
        if len(selected_files) > 0:
            return [[], [{'label': 'use default data', 'value': '0', 'disabled': True}], {**style, 'color':'gray'}]
        else:
            return [['0'], [{'label': 'use default data', 'value': '0', 'disabled': False}], {**style, 'color':'black'}]


# The function draws the final volcano plot
@app.callback(Output('graph-volcano', 'figure'),
              [Input('variable_1', 'value'), Input('variable_2', 'value'),
               Input('variable_3', 'value'), Input('volcano-input', 'value'), 
               Input('chart-title', 'value'), Input('title-font', 'value'), Input('title-size', 'value'), Input('title-color', 'value'), Input('title-x', 'value'), Input('title-y', 'value'),	# title
               
               Input('xaxis-title', 'value'), Input('xaxis-size', 'value'), Input('xaxis-color', 'value'),
               Input('xtick-show', 'value'), Input('xtick-width', 'value'), Input('xtick-length', 'value'), Input('xtick-color', 'value'), 
               Input('xtilab-show', 'value'), Input('xtilab-size', 'value'), Input('xtilab-angle', 'value'), Input('xtilab-color', 'value'), 
               Input('xline-show', 'value'), Input('xline-mirror', 'value'), Input('xline-width', 'value'), Input('xline-color', 'value'),
               Input('xgrid-show', 'value'), Input('xgrid-width', 'value'), Input('xgrid-color', 'value'),
               
               Input('yaxis-title', 'value'), Input('yaxis-size', 'value'), Input('yaxis-color', 'value'),
               Input('ytick-show', 'value'), Input('ytick-width', 'value'), Input('ytick-length', 'value'), Input('ytick-color', 'value'), 
               Input('ytilab-show', 'value'), Input('ytilab-size', 'value'), Input('ytilab-angle', 'value'), Input('ytilab-color', 'value'), 
               Input('yline-show', 'value'), Input('yline-mirror', 'value'), Input('yline-width', 'value'), Input('yline-color', 'value'),
               Input('ygrid-show', 'value'), Input('ygrid-width', 'value'), Input('ygrid-color', 'value'),
              ])
def plot_volcano(var1, var2, var3, effects,
                 title, ti_font, ti_size, ti_color, ti_x, ti_y,
                 xlab_ti, xlab_size, xlab_color, 
                 xtick_show, xtick_width, xtick_len, xtick_color,
                 xtilab_show, xtilab_size, xtilab_angle, xtilab_color,
                 xli_show, xli_mirror, xli_width, xli_color, xgr_show, xgr_width, xgr_color,
                 ylab_ti, ylab_size, ylab_color, 
                 ytick_show, ytick_width, ytick_len, ytick_color,
                 ytilab_show, ytilab_size, ytilab_angle, ytilab_color,
                 yli_show, yli_mirror, yli_width, yli_color, ygr_show, ygr_width, ygr_color,
                ):

    selected_colors = [ti_color, xlab_color, xtick_color, xtilab_color, xli_color, xgr_color, ylab_color, ytick_color]
    for num, i in enumerate(selected_colors):
      if not i.startswith('rgb') and not i.startswith('hex') and not i.startswith('hsl'):
        if not i in colors:
          selected_colors[num] = "black"
    ti_color = selected_colors[0]
    xlab_color = selected_colors[1]
    xtick_color = selected_colors[2]
    xtilab_color = selected_colors[3]
    xli_color = selected_colors[4]
    xgr_color = selected_colors[5]
    ylab_color = selected_colors[6]
    ytick_color = selected_colors[7]

    fig = dashbio.VolcanoPlot(
        dataframe=df,
        genomewideline_value=var3,
        effect_size_line=effects,
        effect_size="log2(FC)",
        p="raw.pval",
        snp="GENE",
        gene="GENE",
        logp=True,
        point_size=var2,
    )

    fig.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 1)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
        font_color="rgba(0,0,0,1)",
        title=dict(text=title, font=dict(family=ti_font, size=ti_size, color=ti_color), x=ti_x, y=ti_y),
        xaxis=dict(title=dict(text=xlab_ti, font=dict(family=ti_font, size=xlab_size, color=xlab_color)),
                   ticks=xtick_show, tickwidth=xtick_width, ticklen=xtick_len, tickcolor=xtick_color,
                   showticklabels=xtilab_show, tickfont=dict(family=ti_font, size=xtilab_size, color=xtilab_color), tickangle=xtilab_angle,
                   showline=xli_show, mirror=xli_mirror, linewidth=xli_width, linecolor=xli_color,
                   showgrid=xgr_show, gridwidth=xgr_width, gridcolor=xgr_color,
                  ),
        yaxis=dict(title=dict(text=ylab_ti, font=dict(family=ti_font, size=ylab_size, color=ylab_color)),
                   ticks=ytick_show, tickwidth=ytick_width, ticklen=ytick_len, tickcolor=ytick_color,
                   showticklabels=ytilab_show, tickfont=dict(family=ti_font, size=ytilab_size, color=ytilab_color), tickangle=ytilab_angle,
                   showline=yli_show, mirror=yli_mirror, linewidth=yli_width, linecolor=yli_color,
                   showgrid=ygr_show, gridwidth=ygr_width, gridcolor=ygr_color,
                  ),
        margin=dict(t=0),
        autosize=True,
    )

    return fig

