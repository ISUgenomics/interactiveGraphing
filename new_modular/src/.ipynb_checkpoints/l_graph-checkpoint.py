## 3. GENERAL GRAPH SETTINGS

graph_advanced_layout = [
  html.Div([
    html.Label('margins:', className='col-4 d-inline label-s', title=tooltip['margin']),
    html.Div([
      dcc.Input(id="margin-l", type="text", placeholder="left", value='0', debounce=False, className='w-25'),
      dcc.Input(id="margin-t", type="text", placeholder="top", value='d', debounce=False, className='w-25'),
      dcc.Input(id="margin-r", type="text", placeholder="right", value='350', debounce=False, className='w-25'),
      dcc.Input(id="margin-b", type="text", placeholder="bottom", value='d', debounce=False, className='w-25'),
    ], className='col-8'),    
  ], className="row align-items-center h34"),
  html.Div([
    html.Label('background:', className='col-4 d-inline label-s', title=tooltip['bg-colors']),
    html.Div([
      dcc.Dropdown(COLOR_OPTS, id="plotting-c", placeholder="plotting bgc", style=drop50), 
      dcc.Dropdown(COLOR_OPTS, id="drawing-c", placeholder="drawing bgc", style=drop50),
    ], className='col-8'),
  ], className="row align-items-center h34 mt-2"),
]

graph_advanced_title = [
  html.Div([
    html.Label('title font:', className='col-4 d-inline label-s', title=tooltip['title-font']),
    html.Div([
      dcc.Dropdown(FONT_OPTS, id="title-font", multi=False, placeholder="font", className="wide-opts-plus", style=drop33),
      dcc.Dropdown(COLOR_OPTS, id="title-color", multi=False, placeholder="color", className="wide-opts", style=drop33),
      dcc.Input(id="title-size", type="number", min=1, placeholder="size", value=24, debounce=True, className='align-top w33'),
    ], className='col-8'),
  ], className="row align-items-center h34"),
  html.Div([
    html.Label('title position:', className='col-4 d-inline label-s', title=tooltip['title-position']),
    html.Div([
      dcc.Input(id="title-posX", type="number", min=0, step=0.01, placeholder="pos X", value=0.38, debounce=True, className='w-50'),
      dcc.Input(id="title-posY", type="number", min=0, step=0.01, placeholder="pos Y", value=0.9, debounce=True, className='w-50'),
    ], className='col-8'),
  ], className="row align-items-center h34 mt-2"),
]

graph_advanced_X = [
  html.Div([
    html.Label('X title font:', className='col-4 d-inline label-s', title=tooltip['X-axis-font']),
    html.Div([
      dcc.Dropdown(FONT_OPTS, id="X-axis-font", placeholder="font", className="wide-opts-plus", style=drop33),
      dcc.Dropdown(COLOR_OPTS, id="X-axis-color", placeholder="color", className="wide-opts", style=drop33),
      dcc.Input(id="X-axis-size", type="number", min=1, placeholder="size", value=20, debounce=True, className='align-top w33'),
    ], className='col-8'),
  ], className="row align-items-center h34"),
  html.Hr(),
  html.Div([
    html.Label('X line: ', className='col-4 d-inline label-s', title=tooltip['X-line']),
    html.Div([
      dcc.Checklist(id='X-line', options=CHECK, value=[], inline=True, className='d-inline me-2 w33', labelClassName='checkbox-label'),
      dcc.Dropdown(COLOR_OPTS, id="X-line-color", placeholder="color", className="wide-opts", style=drop33),
      dcc.Input(id="X-line-width", type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w33'),
    ], className='col-8',),
  ], className="row align-items-center h34 mt-2"),
  html.Div([
    html.Label('X mirror: ', className='col-4 d-inline label-s', title=tooltip['X-mirror']),
    html.Div([
      dcc.Checklist(id='X-mirror', options=CHECK, value=[], inline=True, className='d-inline me-2 w33'),
    ], className='col-8',),
  ], className="row align-items-center h34 mt-2"),
  html.Hr(),
  html.Div([
    html.Label('X ticks: ', className='col-4 d-inline label-s pt-2', title=tooltip['X-ticks']),
    html.Div([
      dcc.Dropdown(TICKS, id="X-ticks", placeholder="type", className="wide-opts", style=drop50),
      dcc.Dropdown(COLOR_OPTS, id="X-ticks-color", placeholder="color", className="wide-opts", style=drop50),
      dcc.Input(id="X-ticks-width", type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w-50'),
      dcc.Input(id="X-ticks-len", type="number", placeholder="length", min=0, value=5, step=0.1, debounce=True, className='align-top w-50'),
    ], className='col-8',),
  ], className="row align-items-top"),
  html.Hr(),
  html.Div([
    html.Label('tick labels: ', className='col-4 d-inline label-s pt-2', title=tooltip['X-tick-labels']),
    html.Div([
      dcc.Checklist(id='X-tick-labels', options=CHECK, value=True, inline=True, className='d-inline me-4 pe-3 w-50', labelClassName='checkbox-label'),
      dcc.Dropdown(COLOR_OPTS, id="X-tick-font-color", placeholder="color", className="wide-opts", style=drop50),
    ], className='col-8',),
  ], className="row align-items-top"),
  html.Div([
      dcc.Input(id="X-tick-font-size", type="number", placeholder="size", min=1, value=14, step=1, debounce=True, className='d-inline align-top w33'),
      dcc.Dropdown(['top', 'bottom'], id="X-tick-font-pos", placeholder="position", className="d-inline wide-opts", style=drop33),
      dcc.Input(id="X-tick-font-angle", type="number", placeholder="angle", min=0, max=360, value=45, step=1, debounce=True, className='d-inline align-top w33'),
      html.Br(),
      dcc.Input(id="X-tick-labels-list", type="text", placeholder="comma-separated custom X-tick labels", debounce=False, className='mt-1 w-100'),
  ], className="row align-items-top mx-0"),
]

graph_advanced_Y = [
  html.Div([
    html.Label('Y title font:', className='col-4 d-inline label-s', title=tooltip['Y-axis-font']),
    html.Div([
      dcc.Dropdown(FONT_OPTS, id="Y-axis-font", placeholder="font", className="wide-opts-plus", style=drop33),
      dcc.Dropdown(COLOR_OPTS, id="Y-axis-color", placeholder="color", className="wide-opts", style=drop33),
      dcc.Input(id="Y-axis-size", type="number", min=1, placeholder="size", value=20, debounce=True, className='align-top w33'),
    ], className='col-8'),
  ], className="row align-items-center h34"),
  html.Div([
    html.Label('Y title pos:', className='col-4 d-inline label-s', title=tooltip['Y-title-pos']),
    html.Div([
      dcc.Input(id="Y-axis-posX", type="number", placeholder="pos X", value=1.24, debounce=True, className='w33'),
      dcc.Input(id="Y-axis-posY", type="number", placeholder="pos Y", value=0.42, debounce=True, className='w33'),
      dcc.Input(id="Y-axis-angle", type="number", placeholder="angle", value=90, debounce=True, className='w33'),
    ], className='col-8'),
  ], className="row align-items-center h34 mt-2"),
  html.Hr(),
  html.Div([
    html.Label('Y axis line: ', className='col-4 d-inline label-s', title=tooltip['Y-line']),
    html.Div([
      dcc.Checklist(id='Y-line', options=CHECK, value=[], className='d-inline me-2 w33', labelClassName='checkbox-label'),
      dcc.Dropdown(COLOR_OPTS, id="Y-line-color", placeholder="color", className="wide-opts", style=drop33), # , style={**inline, **h34, **w33}
      dcc.Input(id="Y-line-width", type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w33'),
    ], className='col-8',),
  ], className="row align-items-center h34 mt-2"),
  html.Div([
    html.Label('Y mirror: ', className='col-4 d-inline label-s', title=tooltip['Y-mirror']),
    html.Div([
      dcc.Checklist(id='Y-mirror', options=CHECK, value=[], inline=True, className='d-inline me-2 w33'),
    ], className='col-8',),
  ], className="row align-items-center h34 mt-2"),
  html.Hr(),
  html.Div([
    html.Label('Y ticks: ', className='col-4 d-inline label-s pt-2', title=tooltip['Y-ticks']),
    html.Div([
      dcc.Dropdown(TICKS, id="Y-ticks", placeholder="type", className="wide-opts", style=drop50),
      dcc.Dropdown(COLOR_OPTS, id="Y-ticks-color", placeholder="color", className="wide-opts", style=drop50),
      dcc.Input(id="Y-ticks-width", type="number", placeholder="width", min=0, value=1, step=0.1, debounce=True, className='align-top w-50'),
      dcc.Input(id="Y-ticks-len", type="number", placeholder="length", min=0, value=5, step=0.1, debounce=True, className='align-top w-50'),
    ], className='col-8',),
  ], className="row align-items-top"),
  html.Hr(), 
  html.Div([
    html.Label('tick labels: ', className='col-4 d-inline label-s pt-2', title=tooltip['Y-tick-labels']),
    html.Div([
      dcc.Checklist(id='Y-tick-labels', options=CHECK, value=[], inline=True, className='d-inline me-4 pe-3 w-50', labelClassName='checkbox-label'),
      dcc.Dropdown(COLOR_OPTS, id="Y-tick-font-color", placeholder="color", className="wide-opts", style=drop50),
    ], className='col-8',),
  ], className="row align-items-top"),
  html.Div([
      dcc.Input(id="Y-tick-font-size", type="number", placeholder="size", min=1, value=14, step=1, debounce=True, className='d-inline align-top w33'),
      dcc.Dropdown(['left', 'right'], id="Y-tick-font-pos", placeholder="position", className="d-inline wide-opts", style=drop33),
      dcc.Input(id="Y-tick-font-angle", type="number", placeholder="angle", min=0, max=360, value=0, step=1, debounce=True, className='d-inline align-top w33'),
  ], className="row align-items-top mx-0"),
  html.Hr(), 
  html.Div([
    html.Label('data labels: ', className='col-4 d-inline label-s pt-2', title=tooltip['Y-labels-data']),
    html.Div([
      dcc.Checklist(id='Y-labels-data', options=CHECK, value=[], inline=True, className='d-inline me-4 pe-3 w-50', labelClassName='checkbox-label'),
      dcc.Dropdown([], id="Y-labels-col", placeholder="data column", className="wide-opts", style=drop50),
    ], className='col-8',),
  ], className="row align-items-top"),
  html.Div([
      dcc.Input(id="Y-labels-number", type="number", placeholder="ticks number", min=1, value=10, step=1, debounce=True,  className='d-inline align-top w33'),
      dcc.Input(id="Y-labels-zoom-from", type="number", placeholder="zoom from", min=0, max=1, step=0.01, debounce=True, className='w33'),
      dcc.Input(id="Y-labels-zoom-to", type="number", placeholder="zoom to", min=0, max=1, step=0.01, debounce=True, className='w33'),
    ], className='row align-items-top mx-0 h34',),
]

opts_graph = [
  html.Div([
    html.Label('graph title: ', className='col-4 d-inline label-s', title=tooltip['graph-title']),
    dcc.Input(id="graph-title", type="text", placeholder="enter graph title", value='', debounce=False, className='col-8'),
  ], className="row align-items-center pe-2 h34"),
  html.Div([
    html.Label('graph size:', className='col-4 d-inline label-s', title=tooltip['graph-size']),
    dcc.Input(id="graph-height", type="number", min=100, placeholder="height", value=600, debounce=True, className='col-4'),
    dcc.Input(id="graph-width", type="number", min=100, placeholder="width", value=800, debounce=True, className='col-4'),
  ], className="row align-items-center mt-2 pe-2 h34"),
  html.Hr(),
  html.Div([
    html.Label('X-axis title: ', className='col-4 d-inline label-s', title=tooltip['X-title']),
    dcc.Input(id="X-title", type="text", placeholder="enter X-axis title", value='', debounce=False, className='col-8'),
  ], className="row align-items-center mt-2 pe-2 h34"),
  html.Div([
    html.Label('Y-axis title: ', className='col-4 d-inline label-s', title=tooltip['Y-title']),
    dcc.Input(id="Y-title", type="text", placeholder="enter Y-axis title", value='', debounce=False, className='col-8'),
  ], className="row align-items-center mt-2 pe-2 h34"),
  html.Hr(),
  html.Div([
    html.Label('legend: ', className='col-4 d-inline label-s', title=tooltip['graph-legend']),
    html.Div([
      dcc.Checklist(id='graph-legend', options=CHECK, value=[], inline=True, className='d-block mt-2 w-50', labelClassName='checkbox-label'),
      dcc.Input(id="legend-X", type="number", placeholder="X position", value=1.24, step=0.01, debounce=True, className='w-50'),
      dcc.Input(id="legend-Y", type="number", placeholder="Y position", value=1.00, step=0.01, debounce=True, className='w-50'),
    ], className='col-8 ps-0 pe-1', style={'position':'relative', 'left': '-0.2rem'}),
  ], className="row align-items-top"),

  html.Div([
    dbc.Accordion([
      dbc.AccordionItem(graph_advanced_layout, title="ADVANCED LAYOUT", item_id="graph-1"),
      dbc.AccordionItem(graph_advanced_title, title="ADVANCED TITLE", item_id="graph-2"),
      dbc.AccordionItem(graph_advanced_X, title="ADVANCED X-AXIS", item_id="graph-3"),
      dbc.AccordionItem(graph_advanced_Y, title="ADVANCED Y-AXIS", item_id="graph-4"),
    ], id="graph-advanced", class_name='accordion2', start_collapsed=True, always_open=True, flush=False, className='w-100 p-0'),
  ], className="row align-items-center mt-3"), 
]