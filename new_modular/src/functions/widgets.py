import pandas as pd
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from src.params.styles import *
from src.params.defaults import tooltip


COL_PROPS={'renamable':True, 'editable':True, 'hideable':True, 'selectable':True, 'clearable':True, 'deletable':True}

# Layout-related functions

def generate_font_options(value_list):
    options = []
    for value in value_list:
        options.append({'label':html.Span([value], style={'font-family':value}), 'value':value})
    return options


def generate_color_options(value_list):
    options = []
    for value in value_list:
        options.append({'label':html.Span([value], style={'color':value}), 'value':value})
    return options


def generate_html_label(text, cname='d-block', style=css_lab):
    return html.Label(children=str(text), className=cname, style=style)


def generate_dcc_input_scroll(text, cname=''):
    return dcc.Input(value=str(text), className=cname, type='text', disabled=True, persistence=True, persistence_type='session')


def generate_dbc_button(text, identifier, n_clicks=0, size="sm", outline=True, color="secondary", cname="align-top w-50 h34", style=None, disabled=False):
    if style is None:
        style = {}
    return dbc.Button(children=text, id=identifier, n_clicks=n_clicks, size=size, outline=outline, color=color, className=cname, style={**style}, disabled=disabled)

def generate_dash_table(identifier, dataframe, col_props={}, other_props={}):
    id_dtbl = {'type':"dtbl-",'id': identifier}
    id_save = {'type':"save-",'id': identifier}
    id_cache = {'type':"cache-",'id': identifier}
    id_close = {'type':"close-",'id': identifier}
    id_status = {'type':"status-",'id': identifier}
    id_tooltip = {'type':"tooltip-",'id': identifier}
    id_item = {'type':"item-", 'id': identifier}
    id_ncol = {'type':"ncol-", 'id': identifier}
    id_nrow = {'type':"nrow-", 'id': identifier}
    id_input = {'type':"ninp-", 'id': identifier}
    id_prune = {'type':"prune-", 'id': identifier}
    id_check = {'type':"ifany-", 'id': identifier}
    id_lview = {'type':"listview-", 'id': identifier}
    id_prows = {'type':"pagerows-", 'id': identifier}
    id_psize = {'type':"pagesize-", 'id': identifier}
    id_format = {'type':"exformat-", 'id': identifier}
    id_reset = {'type':"reset-", 'id': identifier}
    id_undo = {'type':"undo-", 'id': identifier}
    id_row_counter = {'type':"rcount-", 'id': identifier}
    id_out = {'type':"dtout-", 'id': identifier}
    
    if not len(col_props):
        col_props=COL_PROPS
    
    if isinstance(dataframe, list) and len(dataframe) == 2:
        data = dataframe[0]
        columns = dataframe[1]
        cols = [col['name'] for col in (columns if columns else [])]

    else:
        df = pd.DataFrame(dataframe)
        df['id'] = range(0, len(df))
        data = df.to_dict('records')
        cols = df.columns
        columns=[{"name": i, "id": i, **col_props} for i in cols if i != 'id']
#        columns=[{"name": i, "id": i, **col_props} for i in cols if i != 'row_id'] + [{"name": "Row ID", "id": "row_id", "hidden": True}]

    dt = dash_table.DataTable(id=id_dtbl, data=data, columns=columns, 
        persistence=True, persistence_type='session', persisted_props=[ 'columns.name', 'filter_query', 'hidden_columns', 'page_current', 'selected_columns', 'selected_rows', 'sort_by', 'data'],
        style_as_list_view=False,                                                           # table without cell borders
        page_action='native', page_size=25,  #virtualization=True,                          # pagination settings
        fixed_rows={'headers': True}, include_headers_on_copy_paste=True,                   # header settings
        filter_action='native',                                                             # filtering options
        sort_action='native', sort_mode='multi',                                            # sorting options
        editable=True, cell_selectable=True, column_selectable='multi', row_selectable='multi', row_deletable=True,   # edit and select options
        export_columns='visible', export_format='csv', export_headers='names', merge_duplicate_headers=False,          # export current state of the DT
        style_table={**css_dt_table}, style_cell={**css_dt_cell}, style_header={**css_dt_header}, style_data={**css_dt_data},
        tooltip_header={i: i for i in cols},
        tooltip_data=[{column: {'value': str(value), 'type': 'markdown'} for column, value in row.items()} for row in data],
    )
    
    buttonsItem = html.Div([
        generate_dbc_button(['save ', html.I(className="fa fa-floppy-o"), dbc.Tooltip(children=tooltip['save-'], target=id_save, id=id_tooltip, placement='bottom-start', style={'width': '400px'})], id_save, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline mt-2 ms-2 me-0 h34", style={'width':'80px'}),
        generate_dbc_button(['cache ', html.I(className="fa fa-database"), dbc.Tooltip(children=tooltip['cache-'], target=id_cache, id=id_tooltip, placement='bottom-start', style={'width': '400px'})], id_cache, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline mt-2 ms-2 me-0 h34", style={'width':'80px'}), 
        generate_dbc_button([html.I(className="fa fa-times"), dbc.Tooltip(children=tooltip['close-'], target=id_close, id=id_tooltip,  placement='bottom-start', style={'width': '400px'})], id_close, n_clicks=0, size="sm", outline=True, color="danger", cname="d-inline mt-2 ms-2 me-2 h34", style={'width':'22px'}),
        dcc.Input(id=id_status, type="text", placeholder="status:", value='status: edit', disabled=True, className='ps-2 disabled'),
    ], id='my-buttons', className='d-inline', style={'width':'50%'})
    
    buttonsDT = html.Div([
        generate_dbc_button(['reset', dbc.Tooltip(children=tooltip['reset-'], target=id_reset, id=id_tooltip, placement='top-start', style={'width': '400px'})], id_reset, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline me-2 h28", style={'width':'80px'}),
        generate_dbc_button(['undo', dbc.Tooltip(children=tooltip['undo-'], target=id_undo, id=id_tooltip, placement='top-start', style={'width': '400px'}), dcc.Input(id=id_row_counter, value='', type='hidden', persistence=True, persistence_type="session")], id_undo, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline me-2 h28", style={'width':'80px'}, disabled=True),
        html.Div([
          generate_dbc_button(['list view', dbc.Tooltip(children=tooltip['listview-'], target=id_lview, id=id_tooltip, placement='top-start', style={'width': '400px'})], id_lview, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline me-2 h28", style={'width':'80px'}),
          dcc.Input(id=id_prows, type="number", placeholder="rows/page", value=25, debounce=False, persistence=True, persisted_props=['value'], persistence_type='session', className='d-inline ps-2 me-2 smaller h28', style={'width':'80px'}),
          dcc.Input(id=id_psize, type="number", placeholder="table H px", value=280, debounce=False, persistence=True, persisted_props=['value'], persistence_type='session', className='d-inline ps-2 me-2 smaller h28', style={'width':'80px'}),
        ], className='vertical-line-left vertical-line-right ps-2 me-2 pe-1'),
        dcc.Input(id=id_input, type="text", placeholder="enter new column name", value=None, debounce=False, className='d-inline ms-1 ps-2 me-2 smaller h28', style={'width':'200px'}),
        generate_dbc_button(['+ column', dbc.Tooltip(children=tooltip['ncol-'], target=id_ncol, id=id_tooltip, placement='top-start', style={'width': '400px'})], id_ncol, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline me-2 h28", style={'width':'80px'}),
        generate_dbc_button(['+ row', dbc.Tooltip(children=tooltip['nrow-'], target=id_nrow, id=id_tooltip, placement='top-start', style={'width': '400px'})], id_nrow, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline me-2 h28", style={'width':'80px'}), 
        dcc.Checklist(id=id_check, options=[{'label': 'any', 'value': True}], value=[], inline=True, className='d-inline me-1 vertical-line-left ps-3 ms-2 h28', labelClassName='checkbox-label', labelStyle={'top':'0'}),
        generate_dbc_button(['del empty', dbc.Tooltip(children=tooltip['prune-'], target=id_prune, id=id_tooltip, placement='top-start', style={'width': '400px'})], id_prune, n_clicks=0, size="sm", outline=True, color="secondary", cname="d-inline me-2 h28", style={'width':'80px'}), 
        dcc.Dropdown(['csv', 'xlsx'], id=id_format, placeholder="format", value='csv', className="export-format ms-1", optionHeight=28, clearable=False, searchable=False),
    ], id='dt-buttons', className='dt-buttons')
    
    output = html.Div(children=[], id=id_out)

    return dbc.AccordionItem([buttonsItem, dt, buttonsDT, output], title=identifier, id=id_item, class_name='visible')


def generate_pop_up_modal(identifier, close_id, close_text, body, title, size):
    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(title), style={'background-color':'#D6F2FA'}),
        dbc.ModalBody(children = body),
        dbc.ModalFooter(dbc.Button(close_text, id=close_id, n_clicks=0, outline=True, color="secondary", className="me-1 align-top", style={'padding':'0 5px'})),
    ], id=identifier, size=size, centered=True, is_open=False, scrollable=True)
    
    return modal
    

def get_triggered_info(ctx):
    info = []
    if len(ctx):
        tmp = ctx[0]['prop_id']
        info = ['', '', ctx[0]['value'], tmp.split('.')[-1]]
        if tmp.startswith('{'):
            prop = tmp.split('{')[1].split('}')[0].split(',')
            info[0] = prop[1].split(':')[1].replace('"', '')
            info[1] = prop[0].split(':')[1].replace('"', '')
        else:
            info[1] = tmp.split('.')[0]
    return info


def find_component_ids(component):
    ids = []
    if isinstance(component, (dcc.Graph, dcc.Input, dcc.Dropdown, dcc.Checklist, html.Button)):
        if getattr(component, 'id', None):
            ids.append(component.id)

    if hasattr(component, 'children'):
        children = component.children
        if children:
            if isinstance(children, list):
                for child in children:
                    ids.extend(find_component_ids(child))
            else:
                ids.extend(find_component_ids(children))

    return ids


