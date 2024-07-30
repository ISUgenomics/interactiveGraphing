from dash import html, dcc
import dash_bootstrap_components as dbc
from src.params.variables import tooltip
from src.params.styles import *


## D. EXPORT GRAPH IMAGE [static_img_format, static_img_filename, static_img_height, static_img_width, static_img_scale]
# ('img-format', 'value'), ('img-name', 'value'), ('img-height', 'value'), ('img-width', 'value'), ('img-scale', 'value'), ('export-html', 'value'), ('html-name', 'value')
opts_config = [
  html.Div([
    html.Label('format: ', className='col-4 d-inline label-s', title=tooltip['img-format']),
    html.Div([
      dcc.Dropdown(id='img-format', placeholder="select IMG format", clearable=False, style=drop50,
        options=[{'label': i, 'value': i} for i in ['png', 'svg', 'jpeg', 'webp', 'pdf', 'eps']], value='svg'),
    ], className='col-8'),
  ], className="row align-items-center h34"),
  html.Div([
    html.Label('filename: ', className='col-4 d-inline label-s', title=tooltip['img-filename']),
    html.Div([
      dcc.Input(id="img-name", type="text", placeholder="enter IMG filename", value='clustergram', debounce=False, className='w-100',),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('height [px]:', className='col-4 d-inline label-s', title=tooltip['img-height']),
    html.Div([
      dcc.Input(id="img-height", type="number", min=1200, placeholder="height", value=1200, debounce=True, className='w-50'),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('width [px]:', className='col-4 d-inline label-s', title=tooltip['img-width']),
    html.Div([
      dcc.Input(id="img-width", type="number", min=800, placeholder="width", value=800, debounce=True, className='w-50'),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('scale ratio:', className='col-4 d-inline label-s', title=tooltip['img-scale']),
    html.Div([
      dcc.Input(id="img-scale", type="number", min=0.1, placeholder="scale", value=1, debounce=True, className='w-50'),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),
  html.Hr(),
  html.Div([
    html.Label('HTML export: ', className='col-4 d-inline label-s', title=tooltip['export-html']),
    html.Div([
      dcc.Checklist(id='export-html', options=[{'label': 'YES', 'value': 'True'}], value=[], inline=True, className='d-inline w-50'),
      dcc.Input(id="html-name", type="text", placeholder="enter HTML filename", value='clustergram', debounce=False, className='w-100 mt-2'),
    ], className='col-8',),
  ], className="row align-items-top mt-2"),
]