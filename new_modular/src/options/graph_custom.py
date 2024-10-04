from dash import html, dcc
import dash_bootstrap_components as dbc
from src.params.generic import CS_OPTS, COLOR_OPTS, CS_SEQ, CS_DIV, CS_CYC
from src.params.variables import tooltip
from src.params.styles import *
from src.functions.widgets import generate_pop_up_modal

# 4. CUSTOMIZED OPTIONS FOR SELECTED PLOT TYPE

## A. CUSTOMIZE HEATMAP

modal_body = html.Div([
    html.Div([dcc.Graph(figure=CS_SEQ)], className='d-inline w33'), 
    html.Div([dcc.Graph(figure=CS_DIV)], className='d-inline w33', style={'position':'absolute', 'top':'2.5%', 'left':'30%'}), 
    html.Div([dcc.Graph(figure=CS_CYC)], className='d-inline w33', style={'position':'absolute', 'top':'2.5%', 'left':'58.5%'})
])
modal_cs = html.Div([
  dbc.Button("preview CS", id="modal-cs-btn-open", n_clicks=0, size="sm", outline=True, color="secondary", className="align-top w-50 h34"),
  generate_pop_up_modal("modal-cs", "modal-cs-btn-close", "Close", modal_body, "95 Built-in color scales: sequential (66), diverging (22), and cyclic (7)", "xl")
], className='col-4 d-inline align-top')

heatmap_advanced_colorbar = [
  html.Div([
    html.Label('colorbar: ', className='col-4 d-inline label-s', title=tooltip['colorbar']),   
    html.Div([
      dcc.Checklist(id='colorbar', options=[{'label': 'YES', 'value': 'True'}], value=['True'], inline=True, className='d-inline w-50'),
    ], className='col-8',),
    html.Div([
      dcc.Input(id="cb-length", type="number", min=0, placeholder="length", debounce=True, className='w33 mt-2'),
      dcc.Input(id="cb-X", type="number", placeholder="X position", debounce=True, className='w33 mt-2'),
      dcc.Input(id="cb-Y", type="number", placeholder="Y position", debounce=True, className='w33 mt-2'),
    ], className='col-12',),
  ], className="row align-items-center"),
]

heatmap_advanced_labels = [
  html.Div([
    html.Label('label ID: ', className='col-4 d-inline label-s', title=tooltip['label-name']),
    html.Div([
      dcc.Input(id="label-name", type="text", placeholder="label name", debounce=True, className='w-100'),
    ], className='col-8',),
  ], className="row align-items-center h34"),
  html.Div([
    html.Label('label X: ', className='col-4 d-inline label-s', title=tooltip['label-X']),
    html.Div([
      dcc.Input(id="label-X", type="text", placeholder="label X", debounce=True, className='w-100'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('label Y: ', className='col-4 d-inline label-s', title=tooltip['label-Y']),
    html.Div([
      dcc.Input(id="label-Y", type="text", placeholder="label Y", debounce=True, className='w-100'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('label Z: ', className='col-4 d-inline label-s', title=tooltip['label-Z']),
    html.Div([
      dcc.Input(id="label-Z", type="text", placeholder="label Z", debounce=True, className='w-100'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Hr(),
  html.Div([
    html.Label('label size: ', className='col-4 d-inline label-s', title=tooltip['label-font-size']),
    html.Div([
      dcc.Input(id="label-font-size", type="number", min=1, placeholder="font size", debounce=True, className='w-50'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('label align: ', className='col-4 d-inline label-s', title=tooltip['label-align']),
    html.Div([
      dcc.Dropdown(['left', 'right', 'auto'], id="label-align", placeholder="align text", style=drop50),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"), 
  html.Hr(),
  html.Label('Add custom labels:', className='col-12 label-l mt-0'),
  html.Div([
    html.Label('name: ', className='col-4 d-inline label-s', title=tooltip['label-custom']),
    html.Div([
      dcc.Input(id="label-custom", type="text", placeholder="custom label", debounce=True, className='w-100'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('dimension: ', className='col-4 d-inline label-s', title=tooltip['label-dimension']),
    html.Div([
      dcc.RadioItems(['X', 'Y', 'Z'], id='label-dimension', value='True', inline=True, labelClassName='pe-4'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('filename: ', className='col-4 align-top d-inline label-s', title=tooltip['label-file']),
    html.Div([
      dcc.Dropdown([], id="label-file", placeholder="label file", style={**drop50, 'width':'100%'}),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('data: ', className='col-4 d-inline label-s', title=tooltip['label-data']),
    html.Div([
      dcc.Input(id="label-data", type="text", placeholder="label data", debounce=True, className='w-100'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
]


opts_heatmap = [
  html.Div([
    html.Label('center values: ', className='col-4 d-inline label-s', title=tooltip['center-vals']),
    html.Div([
      dcc.Checklist(id='center-vals', options=[{'label': 'YES', 'value': 'True'}], value=['True'], inline=True, className='d-inline w-50'),
    ], className='col-8',),
  ], className="row align-items-center h34"),
  html.Div([
    html.Label('display cutoff: ', className='col-4 d-inline label-s', title=tooltip['display-cutoff']),
    html.Div([
      dcc.Input(id="display-cutoff", type="number", placeholder="cutoff", step=0.01, debounce=True, className='d-inline w-50'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('color scale: ', className='col-4 d-inline align-top label-s', title=tooltip['color-scale']),
    html.Div([
      dcc.Dropdown(CS_OPTS, id="color-scale", placeholder="color scale", style=drop50),
      modal_cs,
    ], className='col-8',),
  ], className="row align-items-center mt-2"),
    
  html.Div([
    dbc.Accordion([
      dbc.AccordionItem(heatmap_advanced_colorbar, title="COLORBAR", item_id="heatmap-1"),
      dbc.AccordionItem(heatmap_advanced_labels, title="INTERACTIVE LABELS", item_id="heatmap-2"),
    ], id="heatmap-advanced", class_name='accordion2', start_collapsed=True, always_open=True, flush=False, className='w-100 p-0'),
  ], className="row align-items-center mt-3"), 
]    


## B. CUSTOMIZE DENDROGRAMS [row_prefix, col_prefix, leaf_order, dendro_factor, dendro_ratioX, dendro_ratioY, dendro_threshold, dendro_colors, dendro_line_width, list_all_row, n_per_line_row]

dendro_advanced = [
  html.Div([
    html.Label('leaf order: ', className='col-4 d-inline label-s', title=tooltip['leaf-order']),
    dcc.Checklist(id="leaf-order", options=[{'label': 'YES', 'value': 'True'}], value=['True'], inline=True, className='d-inline me-4 pe-2 w-50'),
  ], className="row align-items-center"),

  # scale-ratio
  html.Div([
    html.Label('scale ratio: ', className='col-4 d-inline label-s', title=tooltip['scale-ratio']),
    html.Div([
      dcc.Input(id="ratio-db", type="number", min=0.1, placeholder="bars", value=0.9, debounce=True, className='w33'),
      dcc.Input(id="ratio-hdX", type="number", min=0.1, placeholder="H-X", value=0.15, debounce=True, className='w33'),
      dcc.Input(id="ratio-hdY", type="number", min=0.1, placeholder="H-Y", value=0.3, debounce=True, className='w33'),
    ], className='col-8',),
  ], className="row align-items-center mt-2 h34"),
    
  html.Div([
    html.Label('linkage:', className='col-4 d-inline label-s', title=tooltip['dendro-linkage']),
    html.Div([
      dcc.Input(id="linkage-r", type="number", min=1, placeholder="row", value=3, debounce=True, className='w-50'),
      dcc.Input(id="linkage-c", type="number", min=1, placeholder="column", value=3, debounce=True, className='w-50'),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('linkage colors:', className='col-4 d-inline label-s', title=tooltip['dendro-colors']),
    html.Div([
      dcc.Dropdown(COLOR_OPTS, id="colors-r", multi=True, placeholder="select n=row", className="wide-opts", style=drop50),
      dcc.Dropdown(COLOR_OPTS, id="colors-c", multi=True, placeholder="select n=col", className="wide-opts", style=drop50),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('line width:', className='col-4 d-inline label-s', title=tooltip['dendro-line']),
    html.Div([
      dcc.Input(id="line-row", type="number", min=0.1, max=10, placeholder="row", value=2, debounce=True, className='w-50'),
      dcc.Input(id="line-col", type="number", min=0.1, max=10, placeholder="column", value=2, debounce=True, className='w-50'),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),
  html.Div([
    html.Label('labels: ', className='col-4 d-inline label-s', title=tooltip['dendro-labels']),
    html.Div([
      dcc.Checklist(id="dendro-lab", options=[{'label': 'YES', 'value': 'True'}], value=['True'], inline=True, className='d-inline me-4 pe-2 w-50'),
      dcc.Input(id="dendro-lab-items", type="number", min=1, placeholder="n per line", value=5, debounce=True, className='w-50'),
    ], className='col-8 pe-2',),
  ], className="row align-items-center mt-2 h34"),
]

opts_dendro = [
  html.Div([
    html.Label('row prefix: ', className='col-4 d-inline label-s', title=tooltip['row-prefix']),
    html.Div([
      dcc.Input(id="row-name", type="text", placeholder="enter custom row prefix", value='', debounce=False, className='w-100'),
    ], className='col-8'),
  ], className="row align-items-center h34"),
  html.Div([
    html.Label('col prefix: ', className='col-4 d-inline label-s', title=tooltip['col-prefix']),
    html.Div([
      dcc.Input(id="col-name", type="text", placeholder="enter custom col prefix", value='', debounce=False, className='w-100'),
    ], className='col-8'),
  ], className="row align-items-center mt-2 h34"),

  html.Div([
    dbc.Accordion([
      dbc.AccordionItem(dendro_advanced, title="ADVANCED OPTIONS:", item_id="d-1"),
    ], id="dendro-advanced", class_name='accordion2', start_collapsed=True, always_open=True, flush=False, className='w-100 p-0'),
  ], className="row align-items-center mt-3"), 
]


## C. CUSTOMIZE CLUSTER BARS

opts_bars = [

]


## C. CUSTOMIZE SYNTENY PLOT

opts_synteny = [
    # Chromosome Spacing
    html.Div([
        html.Label('chr spacing:', className='col-4 d-inline label-s', title="Adjust spacing between chromosomes"),
        dcc.Input(id="synteny-chr-spacing", type="number", min=0.001, max=0.5, step=0.001, placeholder="Enter spacing", value=0.01, debounce=True, className='col-8'),
    ], className="row align-items-center pe-2 h34"),

    # Chromosome Height
    html.Div([
        html.Label('chr height:', className='col-4 d-inline label-s', title="Adjust height of chromosomes"),
        dcc.Input(id="synteny-chr-height", type="number", min=0.5, max=19, step=0.1, placeholder="Enter height", value=3, debounce=True, className='col-8'),
    ], className="row align-items-center mt-2 pe-2 h34"),

    # Alignment Selection
    html.Div([
        html.Label('chr align:', className='col-4 d-inline label-s', title="Choose alignment mode"),
        dcc.Dropdown(id="synteny-chr-alignment", options = [{'label': value, 'value': value} for value in ['left', 'right', 'center', 'block']], 
            value='center', className='col-8', clearable=False,
        ),
    ], className="row align-items-center mt-2 pe-2 mb-4 h34"),

    # Position Mode Selection
    html.Div([
        html.Label('synteny position:', className='col-4 d-inline label-s', title="Choose position mode for chromosomes"),
        dcc.RadioItems(['exact', 'middle'], value='exact', id="synteny-line-position", inline=True, className='col-8'),
    ], className="row align-items-center mt-2 pe-2 h34"),    
]

### -------------------------------------- ###

# Final assembly of custom graph settings
opts_graph_types = html.Div(id="opts-graph-cutom")