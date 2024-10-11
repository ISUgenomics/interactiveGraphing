from dash import html, dcc
import dash_bootstrap_components as dbc
from src.params.variables import tooltip
from src.params.styles import *


## D. EXPORT GRAPH IMAGE 
# [static_img_format, static_img_filename, static_img_height, static_img_width, static_img_scale]
# ('img-format', 'value'), ('img-name', 'value'), ('img-height', 'value'), ('img-width', 'value'), ('img-scale', 'value'), ('export-html', 'value'), ('html-name', 'value')
def create_opts_export_config(tab_name):
    return  [
        html.Div([
          html.Label('format: ', className='col-4 d-inline label-s', title=tooltip['img-format']),
          html.Div([
            dcc.Dropdown(id={'id':'img-format', 'tab': tab_name}, placeholder="select IMG format", clearable=False, style=drop50,
              options=[{'label': i, 'value': i} for i in ['png', 'svg', 'jpeg', 'webp', 'pdf', 'eps']], value='svg'),
          ], className='col-8'),
        ], className="row align-items-center h34"),
        html.Div([
          html.Label('filename: ', className='col-4 d-inline label-s', title=tooltip['img-filename']),
          html.Div([
            dcc.Input(id={'id':"img-name", 'tab': tab_name}, type="text", placeholder="enter IMG filename", value='clustergram', debounce=False, className='w-100',),
          ], className='col-8'),
        ], className="row align-items-center mt-2 h34"),
        html.Div([
          html.Label('height [px]:', className='col-4 d-inline label-s', title=tooltip['img-height']),
          html.Div([
            dcc.Input(id={'id':"img-height", 'tab': tab_name}, type="number", min=1200, placeholder="height", value=1200, debounce=True, className='w-50'),
          ], className='col-8'),
        ], className="row align-items-center mt-2 h34"),
        html.Div([
          html.Label('width [px]:', className='col-4 d-inline label-s', title=tooltip['img-width']),
          html.Div([
            dcc.Input(id={'id':"img-width", 'tab': tab_name}, type="number", min=800, placeholder="width", value=800, debounce=True, className='w-50'),
          ], className='col-8'),
        ], className="row align-items-center mt-2 h34"),
        html.Div([
          html.Label('scale ratio:', className='col-4 d-inline label-s', title=tooltip['img-scale']),
          html.Div([
            dcc.Input(id={'id':"img-scale", 'tab': tab_name}, type="number", min=0.1, placeholder="scale", value=1, debounce=True, className='w-50'),
          ], className='col-8'),
        ], className="row align-items-center mt-2 h34"),
        html.Hr(),
        html.Div([
          html.Label('HTML export: ', className='col-3 me-3 d-inline label-s', title=tooltip['export-html']),
          dbc.Switch(id={'id':'export-html', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 ms-4",),
          html.Div([
            dcc.Input(id={'id':"html-name", 'tab': tab_name}, type="text", placeholder="enter HTML filename", value='clustergram', debounce=False, className='w-100'),
          ], className='col-8 p-0', style={'width':'14.5em', 'margin-left':'-1.7em'}),
        ], className="row align-items-center"),
    ]