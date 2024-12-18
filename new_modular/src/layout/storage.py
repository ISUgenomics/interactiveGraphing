from pathlib import Path
from dash import html, dcc

storage = html.Div([
  dcc.Store(id="add-app-tab-num", data=[], storage_type='session'),      # children of the app Tabs
  dcc.Store(id='left-panel-children', data=[], storage_type='session'),  # all options panels; visible only the one for the active tab
  dcc.Store(id='graph-panel-children', data=[], storage_type='session'), # all graph panels; visible only the one for the active tab
  dcc.Store(id='output-panel-children', data=[], storage_type='session'),# all output data panels; visible only the one for the active tab
  dcc.Store(id="data-dir", data=str(Path.cwd().parent / "data"), storage_type='session'),
  dcc.Store(id="user-files-list", data={}, storage_type='session'),      # dict of currently loaded inputs {name: base64 content}
  dcc.Store(id="user-files-status", data='', storage_type='session'),    # time_stamp triggering the emptying of the upload box
  dcc.Store(id="inputs-clicks", data={}, storage_type='session'),        # keeps in session n_clicks for each input file
  dcc.Store(id="edition-content", data={}, storage_type='session'),      # real content of input edition section (all data tables): initial dataframe, used for reset
  dcc.Store(id="edition-current", data={}, storage_type='session'),      # real content of input edition section (all data tables): current state, used for onload
  dcc.Store(id="edition-history", data={}, storage_type='session'),      # trace of changes made in (all data tables): changes only, used for undo
  dcc.Store(id='captured-name-store', data='', storage_type='session'),
  dcc.Store(id='draggable-layout', data={}, storage_type='session'), 
  dcc.Store(id="graph-config", data={'@changed':''}, storage_type='session'),  # current config of built-in interactive tools in the graph; dict with configs for all tabs
  dcc.Store(id="graph-data", data={}, storage_type='session'),           # dict that stores graph data for each plotting tab; tab-id : {subset : df_data}

# synteny
  dcc.Store(id="synteny-genomes-all", data={}, storage_type='session'),
  dcc.Store(id='synteny-genomes-selected', data={'@changed':''}, storage_type='session'),
  dcc.Store(id='synteny-chromosomes-all', data={}, storage_type='session'),
  dcc.Store(id='synteny-chr-selected', data={'@changed':''}, storage_type='session'),


  html.Button(id="edition-undo", children='', name="True", hidden=True, n_clicks=0)         # object that stores info for undo action
])

void = html.Div([
  dcc.Input(id="void0", value='', type='hidden'),    # html export
  dcc.Input(id="void1", value='', type='hidden'),    # clientside JS: CreateCloseButtons for DTs
  dcc.Input(id="void2", value='', type='hidden'),    # clientside JS: add tooltip when selecting rows
])

dummy = html.Div ([
  
])

identifiers = html.Div([
  # VALUE - dataframe
  dcc.Input(id="df-add-id", value='', type='hidden'),  # identifier of a new dataframe to add to in-memory STORAGE
  dcc.Input(id="dt-add-id", value='', type='hidden'),  # identifier of a new datatable to add into the Edition Mode
  dcc.Input(id="df-delete", value='', type='hidden'),  # identifier of a dataframe corresponding to closed DataTable
  dcc.Input(id="df-keepit", value='', type='hidden'),  # identifier of a dataframe corresponding to cached DataTable
  dcc.Input(id="df-saveit", value='', type='hidden', readOnly = False, placeholder=''),  # identifier of a dataframe selected to save: value - id_to_save (passed by 'save-'), readOnly - triggers btn-save-df, placeholder - updates df status in storage
  # VALUE - graph
  dcc.Input(id="last_trig_layout", value='', type='hidden'),            # last trigger in the graph layout
])