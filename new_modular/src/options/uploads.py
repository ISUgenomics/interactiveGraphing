from dash import html, dcc
import dash_bootstrap_components as dbc

## 1. UPLOAD INPUTS

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