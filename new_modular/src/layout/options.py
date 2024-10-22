import importlib
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.params.generic import COLOR_OPTS, FONT_OPTS, CHECK, TICKS
from src.params.defaults import tooltip
from src.params.styles import *


## 1. UPLOAD RAW INPUTS

def create_opts_inputs(tab_name):
    return [
        html.Label('from file system: ', id={'id':'custom-label', 'tab': tab_name}, className='mb-1 label-s'),
        dcc.Upload(id={'id':'upload-box', 'tab': tab_name}, filename='', className='upload-box', max_size=-1, multiple=True,
            children=html.Div([html.P('drag & drop', className='color2'), html.P('or click to browse', className='color2')]),
        ),
        html.Label('from online resources: ', id={'id':'custom-url-label', 'tab': tab_name}, className='mb-1 mt-3 label-s'),
        html.Div([
          dcc.Input(id={'id':"custom-url", 'tab': tab_name}, type="url", placeholder="enter URL", value='', debounce=False, className='col-8 d-inline ps-2'),
          html.Div([
            dbc.Button("download", id={'id':"download-btn", 'tab': tab_name}, n_clicks=0, size="sm", outline=True, color="secondary", className="w-100 align-top h34"),
          ], className="col-4 d-inline ps-2"),
        ], className="row ms-0 align-items-center"),
        html.P(''),
        html.Label('', id={'id':"settings-upload-label", 'tab': tab_name}, className='label-l'),
        html.Div(children=[], id={'id':"settings-upload-inputs", 'tab': tab_name}, className="mt-3")
    ]


## 2. ADJUST ANALYSIS SETTINGS: Final assembly of the user0-selected analysis options

def create_opts_analysis(tab_name):
    variant = tab_name.split('_')[0]                                                   # app type: 'synteny', 'clustergram', etc.
    function_name = f'create_opts_analysis_{variant}'                                  # ensure each app type has such a function defined

    try:
        options_module = importlib.import_module(f'src.apps.{variant}.options')        # dynamically load the app-specific options module
        func = getattr(options_module, function_name)
        return [html.Div(id={'id': "opts-analysis", 'tab': tab_name}, children=func(tab_name))]
    
    except (ModuleNotFoundError, AttributeError) as e:                                 # module or function doesn't exist
        return [html.Div(id={'id': "opts-analysis", 'tab': tab_name}, children=html.Div(f"No options available for {variant} analysis."))]


## 3. GENERAL GRAPH SETTINGS

def create_graph_advanced_layout(tab_name):
    return [
        html.Div([
          html.Label('margins:', className='col-4 d-inline label-s', title=tooltip['margin']),
          html.Div([
            dcc.Input(id={'id':"margin-l", 'tab': tab_name}, type="text", placeholder="left", value='0', debounce=False, className='w-25'),
            dcc.Input(id={'id':"margin-t", 'tab': tab_name}, type="text", placeholder="top", value='d', debounce=False, className='w-25'),
            dcc.Input(id={'id':"margin-r", 'tab': tab_name}, type="text", placeholder="right", value='350', debounce=False, className='w-25'),
            dcc.Input(id={'id':"margin-b", 'tab': tab_name}, type="text", placeholder="bottom", value='d', debounce=False, className='w-25'),
          ], className='col-8'),
        ], className="row align-items-center h34"),
        html.Div([
          html.Label('background:', className='col-4 d-inline label-s', title=tooltip['bg-colors']),
          html.Div([
            dcc.Dropdown(COLOR_OPTS, id={'id':"plotting-c", 'tab': tab_name}, placeholder="plotting bgc", style=drop50),
            dcc.Dropdown(COLOR_OPTS, id={'id':"drawing-c", 'tab': tab_name}, placeholder="drawing bgc", style=drop50),
          ], className='col-8'),
        ], className="row align-items-center h34 mt-2"),
    ]


def create_graph_advanced_title(tab_name):
    return [
        html.Div([
          html.Label('title font:', className='col-4 d-inline label-s', title=tooltip['title-font']),
          html.Div([
            dcc.Dropdown(FONT_OPTS, id={'id':"title-font", 'tab': tab_name}, multi=False, placeholder="font", className="wide-opts-plus", style=drop33),
            dcc.Dropdown(COLOR_OPTS, id={'id':"title-color", 'tab': tab_name}, multi=False, placeholder="color", className="wide-opts", style=drop33),
            dcc.Input(id={'id':"title-size", 'tab': tab_name}, type="number", min=1, placeholder="size", value=24, debounce=True, className='align-top w33'),
          ], className='col-8'),
        ], className="row align-items-center h34"),
        html.Div([
          html.Label('title position:', className='col-4 d-inline label-s', title=tooltip['title-position']),
          html.Div([
            dcc.Input(id={'id':"title-posX", 'tab': tab_name}, type="number", min=0, step=0.01, placeholder="pos X", value=0.38, debounce=True, className='w-50'),
            dcc.Input(id={'id':"title-posY", 'tab': tab_name}, type="number", min=0, step=0.01, placeholder="pos Y", value=0.9, debounce=True, className='w-50'),
          ], className='col-8'),
        ], className="row align-items-center h34 mt-2"),
    ]


def create_graph_advanced_X(tab_name):
    return [
        html.Div([
          html.Label('X title font:', className='col-4 d-inline label-s', title=tooltip['X-axis-font']),
          html.Div([
            dcc.Dropdown(FONT_OPTS, id={'id':"X-axis-font", 'tab': tab_name}, placeholder="font", className="wide-opts-plus", style=drop33),
            dcc.Dropdown(COLOR_OPTS, id={'id':"X-axis-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop33),
            dcc.Input(id={'id':"X-axis-size", 'tab': tab_name}, type="number", min=1, placeholder="size", value=20, debounce=True, className='align-top w33'),
          ], className='col-8'),
        ], className="row align-items-center h34"),
        html.Hr(),
        html.Div([
          html.Label('X line: ', className='col-3 d-inline label-s', title=tooltip['X-line']),
          dbc.Switch(id={'id':'X-line', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 shift-right-2"),
          html.Div([
            dcc.Dropdown(COLOR_OPTS, id={'id':"X-line-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop50),
            dcc.Input(id={'id':"X-line-width", 'tab': tab_name}, type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w-50'),
          ], className='col-8'),
        ], className="row align-items-center h34 mt-2"),
        html.Div([
          html.Label('X mirror: ', className='col-3 d-inline label-s', title=tooltip['X-mirror']),
          dbc.Switch(id={'id':'X-mirror', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 shift-right-2"),
        ], className="row align-items-center h34 mt-2"),
        html.Hr(),
        html.Div([
          html.Label('X ticks: ', className='col-4 d-inline label-s pt-2', title=tooltip['X-ticks']),
          html.Div([
            dcc.Dropdown(TICKS, id={'id':"X-ticks", 'tab': tab_name}, placeholder="type", className="wide-opts", style=drop50),
            dcc.Dropdown(COLOR_OPTS, id={'id':"X-ticks-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop50),
            dcc.Input(id={'id':"X-ticks-width", 'tab': tab_name}, type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w-50'),
            dcc.Input(id={'id':"X-ticks-len", 'tab': tab_name}, type="number", placeholder="length", min=0, value=5, step=0.1, debounce=True, className='align-top w-50'),
          ], className='col-8',),
        ], className="row align-items-top"),
        html.Hr(),
        html.Div([
          html.Label('tick labels: ', className='col-3 d-inline label-s', title=tooltip['X-tick-labels']),
          dbc.Switch(id={'id':'X-tick-labels', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 shift-right-2"),
          html.Div([
            dcc.Dropdown(COLOR_OPTS, id={'id':"X-tick-font-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop50),
          ], className='col-8'),
        ], className="row align-items-center"),
        html.Div([
            dcc.Input(id={'id':"X-tick-font-size", 'tab': tab_name}, type="number", placeholder="size", min=1, value=14, step=1, debounce=True, className='d-inline align-top w33'),
            dcc.Dropdown(['top', 'bottom'], id={'id':"X-tick-font-pos", 'tab': tab_name}, placeholder="position", className="d-inline wide-opts", style=drop33),
            dcc.Input(id={'id':"X-tick-font-angle", 'tab': tab_name}, type="number", placeholder="angle", min=0, max=360, value=45, step=1, debounce=True, className='d-inline align-top w33'),
            dcc.Input(id={'id':"X-tick-labels-list", 'tab': tab_name}, type="text", placeholder="comma-separated custom X-tick labels", debounce=False, className='mt-1 w-100'),
        ], className="row align-items-top ms-2 pe-2"),
    ]


def create_graph_advanced_Y(tab_name):
    return [
        html.Div([
          html.Label('Y title font:', className='col-4 d-inline label-s', title=tooltip['Y-axis-font']),
          html.Div([
            dcc.Dropdown(FONT_OPTS, id={'id':"Y-axis-font", 'tab': tab_name}, placeholder="font", className="wide-opts-plus", style=drop33),
            dcc.Dropdown(COLOR_OPTS, id={'id':"Y-axis-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop33),
            dcc.Input(id={'id':"Y-axis-size", 'tab': tab_name}, type="number", min=1, placeholder="size", value=20, debounce=True, className='align-top w33'),
          ], className='col-8'),
        ], className="row align-items-center h34"),
        html.Div([
          html.Label('Y title pos:', className='col-4 d-inline label-s', title=tooltip['Y-title-pos']),
          html.Div([
            dcc.Input(id={'id':"Y-axis-posX", 'tab': tab_name}, type="number", placeholder="pos X", value=1.24, debounce=True, className='w33'),
            dcc.Input(id={'id':"Y-axis-posY", 'tab': tab_name}, type="number", placeholder="pos Y", value=0.42, debounce=True, className='w33'),
            dcc.Input(id={'id':"Y-axis-angle", 'tab': tab_name}, type="number", placeholder="angle", value=90, debounce=True, className='w33'),
          ], className='col-8'),
        ], className="row align-items-center h34 mt-2"),
        html.Hr(),
        html.Div([
          html.Label('Y line: ', className='col-3 d-inline label-s', title=tooltip['X-line']),
          dbc.Switch(id={'id':'Y-line', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 shift-right-2"),
          html.Div([
            dcc.Dropdown(COLOR_OPTS, id={'id':"Y-line-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop50),
            dcc.Input(id={'id':"Y-line-width", 'tab': tab_name}, type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w-50'),
          ], className='col-8'),
        ], className="row align-items-center h34 mt-2"),
        html.Div([
          html.Label('Y mirror: ', className='col-3 d-inline label-s', title=tooltip['X-mirror']),
          dbc.Switch(id={'id':'Y-mirror', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 shift-right-2"),
        ], className="row align-items-center h34 mt-2"),
        html.Hr(),
        html.Div([
          html.Label('Y ticks: ', className='col-4 d-inline label-s pt-2', title=tooltip['Y-ticks']),
          html.Div([
            dcc.Dropdown(TICKS, id={'id':"Y-ticks", 'tab': tab_name}, placeholder="type", className="wide-opts", style=drop50),
            dcc.Dropdown(COLOR_OPTS, id={'id':"Y-ticks-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop50),
            dcc.Input(id={'id':"Y-ticks-width", 'tab': tab_name}, type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w-50'),
            dcc.Input(id={'id':"Y-ticks-len", 'tab': tab_name}, type="number", placeholder="length", min=0, value=5, step=0.1, debounce=True, className='align-top w-50'),
          ], className='col-8',),
        ], className="row align-items-top"),
        html.Hr(),
        html.Div([
          html.Label('tick labels: ', className='col-3 d-inline label-s', title=tooltip['X-tick-labels']),
          dbc.Switch(id={'id':'Y-tick-labels', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 shift-right-2"),
          html.Div([
            dcc.Dropdown(COLOR_OPTS, id={'id':"Y-tick-font-color", 'tab': tab_name}, placeholder="color", className="wide-opts", style=drop50),
          ], className='col-8'),
        ], className="row align-items-center"),
        html.Div([
            dcc.Input(id={'id':"Y-tick-font-size", 'tab': tab_name}, type="number", placeholder="size", min=1, value=14, step=1, debounce=True, className='d-inline align-top w33'),
            dcc.Dropdown(['top', 'bottom'], id={'id':"X-tick-font-pos", 'tab': tab_name}, placeholder="position", className="d-inline wide-opts", style=drop33),
            dcc.Input(id={'id':"Y-tick-font-angle", 'tab': tab_name}, type="number", placeholder="angle", min=0, max=360, value=45, step=1, debounce=True, className='d-inline align-top w33'),
            html.Br(),
            dcc.Input(id={'id':"Y-tick-labels-list", 'tab': tab_name}, type="text", placeholder="comma-separated custom X-tick labels", debounce=False, className='mt-1 w-100'),
        ], className="row align-items-top ms-2 pe-2"),
    ]


# Final assembly of general graph options
def create_graph_options(tab_name):
    return [
        html.Div([
          html.Label('graph title: ', className='col-4 d-inline label-s', title=tooltip['graph-title']),
          dcc.Input(id={'id':"graph-title", 'tab': tab_name}, type="text", placeholder="enter graph title", value='', debounce=False, className='col-8'),
        ], className="row align-items-center pe-2 h34"),
        html.Div([
          html.Label('graph size:', className='col-4 d-inline label-s', title=tooltip['graph-size']),
          dcc.Input(id={'id':"graph-height", 'tab': tab_name}, type="number", min=100, placeholder="height", value=600, debounce=True, className='col-4'),
          dcc.Input(id={'id':"graph-width", 'tab': tab_name}, type="number", min=100, placeholder="width", value=800, debounce=True, className='col-4'),
        ], className="row align-items-center mt-2 pe-2 h34"),
        html.Hr(),
        html.Div([
          html.Label('X-axis title: ', className='col-4 d-inline label-s', title=tooltip['X-title']),
          dcc.Input(id={'id':"X-title", 'tab': tab_name}, type="text", placeholder="enter X-axis title", value='', debounce=False, className='col-8'),
        ], className="row align-items-center mt-2 pe-2 h34"),
        html.Div([
          html.Label('Y-axis title: ', className='col-4 d-inline label-s', title=tooltip['Y-title']),
          dcc.Input(id={'id':"Y-title", 'tab': tab_name}, type="text", placeholder="enter Y-axis title", value='', debounce=False, className='col-8'),
        ], className="row align-items-center mt-2 pe-2 h34"),
        html.Hr(),
        html.Div([
          html.Label('legend: ', className='col-3 d-inline label-s', title=tooltip['graph-legend']),
          dbc.Switch(id={'id':'graph-legend', 'tab': tab_name}, label='', value=True, persistence=True, persistence_type="session", className="col-1 p-0 shift-right-1"),
          html.Div([
            dcc.Input(id={'id':"legend-X", 'tab': tab_name}, type="number", placeholder="X position", value=1.24, step=0.01, debounce=True, className='w-50'),
            dcc.Input(id={'id':"legend-Y", 'tab': tab_name}, type="number", placeholder="Y position", value=1.00, step=0.01, debounce=True, className='w-50'),
          ], className='col-8 ps-0 pe-1', style={'position':'relative', 'left': '-0.2rem'}),
        ], className="row align-items-center"),

        html.Div([
          dbc.Accordion([
            dbc.AccordionItem(create_graph_advanced_layout(tab_name), title="ADVANCED LAYOUT", item_id={'id':"graph-1", 'tab': tab_name}),
            dbc.AccordionItem(create_graph_advanced_title(tab_name), title="ADVANCED TITLE", item_id={'id':"graph-2", 'tab': tab_name}),
            dbc.AccordionItem(create_graph_advanced_X(tab_name), title="ADVANCED X-AXIS", item_id={'id':"graph-3", 'tab': tab_name}),
            dbc.AccordionItem(create_graph_advanced_Y(tab_name), title="ADVANCED Y-AXIS", item_id={'id':"graph-4", 'tab': tab_name}),
          ], id={'id':"graph-advanced", 'tab': tab_name}, class_name='accordion2 p-0', start_collapsed=True, always_open=True, flush=False, className='w-100 p-0'),
        ], className="row align-items-center mt-3"),
    ]



## 4. SPECIFIC GRAPH SETTINGS: Final assembly of user-selected custom graph settings

def create_opts_graph_custom(tab_name):
    variant = tab_name.split('_')[0]                                                   # app type: 'synteny', 'clustergram', etc.
    function_name = f'create_opts_graph_{variant}'                                     # ensure each app type has such a function defined

    try:
        options_module = importlib.import_module(f'src.apps.{variant}.options')        # dynamically load the app-specific options module
        func = getattr(options_module, function_name)
        return [html.Div(id={'id': "opts-analysis", 'tab': tab_name}, children=func(tab_name))]

    except (ModuleNotFoundError, AttributeError) as e:                                 # module or function doesn't exist
        return [html.Div(id={'id': "opts-analysis", 'tab': tab_name}, children=html.Div(f"No options available for {variant} graph."))]



## 5. EXPORT GRAPH IMAGE 
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


### -------------------------------------- ###

# Final assembly of the Options Panel

def create_left_panel(tab_name):
    return [
        dbc.Accordion([
            dbc.AccordionItem(create_opts_inputs(tab_name), title="1. UPLOAD RAW INPUTS", item_id="item-1"),
            dbc.AccordionItem(create_opts_analysis(tab_name), title="2. ADJUST ANALYSIS SETTINGS", item_id="item-2"),
            dbc.AccordionItem(create_graph_options(tab_name), title="3. GENERAL GRAPH SETTINGS", item_id="item-3"),
            dbc.AccordionItem(create_opts_graph_custom(tab_name), title="4. SPECIFIC GRAPH SETTINGS", item_id="item-4"),
            dbc.AccordionItem(create_opts_export_config(tab_name), title="5. EXPORT GRAPH", item_id="item-5", class_name=".container")
        ], id="accordion", always_open=True, flush=False, start_collapsed=True),
        html.Div(id="accordion-contents", className="mt-3"),
    ]