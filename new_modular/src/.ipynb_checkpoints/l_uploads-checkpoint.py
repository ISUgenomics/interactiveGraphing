## 1. UPLOAD INPUTS
opts_inputs = [
  html.Label('from file system: ', id='custom-label', className='mb-1 label-s'),
  dcc.Upload(id='upload-box', filename='', className='upload-box', max_size=-1, multiple=True,
      children=html.Div([html.P('drag & drop', className='color2'), html.P('or click to browse', className='color2')]),
  ),
  html.Label('from online resources: ', id='custom-url-label', className='mb-1 mt-3 label-s'),
  html.Div([
    dcc.Input(id="custom-url", type="url", placeholder="enter URL", value='', debounce=False, className='col-8 d-inline ps-2'),
    html.Div([
      dbc.Button("download", id="download-btn", n_clicks=0, size="sm", outline=True, color="secondary", className="w-100 align-top h34"),
    ], className="col-4 d-inline ps-2"),
  ], className="row ms-0 align-items-center"),    
  html.P(''),
  html.Label(id="settings-upload-label", className='label-l'),
  html.Div(children=[], id="settings-upload-inputs", className="mt-3")
]