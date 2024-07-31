from dash import html, dcc
import dash_bootstrap_components as dbc
from src.params.styles import *
from src.functions.widgets import generate_pop_up_modal


m_body = html.Div([
    html.Label('Choose the location(s) to save your file:', className='col-12 d-block mb-1 label-s', title=''),
    dcc.Checklist(id='opts-save-df', value='', inline=False, className='col-6 d-inline w-50', labelClassName='label-l spaced',
        options=[
            {'label': "Save to the app's default storage location.", 'value': 'storage'},
            {'label': 'Enter a custom path on your local file system.', 'value': 'custom'},
            {'label': 'Save to your default Downloads folder.', 'value': 'download'},
        ]
    ),
    html.Div([
        dcc.Input(id="opts-save-df-storage", type="text", value='', disabled=True, debounce=False, className='col-12 d-inline ps-2 disabled smaller'),
        dcc.Input(id="opts-save-df-custom", type="text", placeholder="enter an absolute path", value=None, debounce=False, className='col-12 d-inline ps-2 mt-1 smaller'),
        html.Label(id="opts-save-df-custom-wrong", children=[], className='col-12 d-block my-1 px-2 label-s text-danger', title=''),
    ], className='col-6 d-block'),
    html.Div([
        html.Label('Optionally change the name of the output:', className='col-12 d-block mt-1 label-s', title=''),
        html.Label('Optionally change the format of the output:', className='col-12 d-block mt-3 label-s', title=''),
        html.Label('Click "Save" button to save at selected location(s).', className='col-12 d-block mt-4 label-l', title=''),
    ], className='col-6 d-inline mt-3'),
    html.Div([
        dcc.Input(id="opts-save-df-filename", type="text", value='', debounce=False, className='col-12 d-inline ps-2 mt-3 mb-1 smaller'),
        dcc.Dropdown(['csv', 'excel', 'txt', 'json', 'markdown', 'html', 'pickle', 'feather', 'stata'], value='csv', id='opts-save-df-format', 
            placeholder="select File format", clearable=False, maxHeight=58, optionHeight=28, className='smaller'),
    ], className='col-6 d-inline', style={'height':'125px'}), 
    dcc.Download(id="download-dataframe"),
], className='row')

data_inputs = html.Div([
    dbc.Accordion(children = [], id='edition-items', start_collapsed=False, always_open=True, flush=True, persistence=True, persistence_type='session', persisted_props=['active_item']),
    generate_pop_up_modal("modal-save-df", "btn-save-df", "Save", m_body, "Save DataFrame to your local file system", "lg")
], id='upper-panelDiv', className="resize-vertical", style={'min-height':'fit-content', 'max-height':'100vh'}) #, 'height':'fit-content'

graph_analysis = html.Div(id='graph-panelDiv')

data_outputs = html.Div(id='lower-panelDiv')

# APP-BODY Components assembly
right_panel = html.Div([
  html.Div([
    dbc.Accordion([
      dbc.AccordionItem(data_inputs, title="EDIT INPUT DATA", item_id="item-11", ), # style={'display':'none'} ## JS management
      dbc.AccordionItem(graph_analysis, title="DISPLAY INTERACTIVE GRAPHS", item_id="item-12", ), # style={'display':'none'} ## JS management
      dbc.AccordionItem(data_outputs, title="EXTRACT OUTPUT DATA", item_id="item-13", ), # style={'display':'none'} ## JS management
    ], id="accordion2", start_collapsed=True, always_open=True, flush=False), 
  ], id='app-bodyDiv')
], id='right-panelDiv', style=css_rpd)