from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_draggable
from src.params.styles import *


## 2. ADJUST ANALYSIS SETTINGS in Option Panel

def create_synteny_merge_data(tab_name):
    return [
        html.Div([

        ])
    ]

def create_synteny_graph_inputs(tab_name):
    return [
        html.Div([
            html.Label('select graph inputs: ', className='mb-1 label-s'),
            dcc.Dropdown(id={'id':"synteny-inputs", 'tab':tab_name}, persistence=True, persistence_type="session"),
        ])
    ]

def create_synteny_selection(tab_name):
    return [
        html.Div([
            html.Label('select and manually sort genomes: ', className='mb-1 mt-3 label-s'),
            # Draggable GridLayout for genome selection
            dash_draggable.GridLayout(id={'id':'genome-draggable', 'tab': tab_name}, children=[],
                gridCols=2, width=300, height=28, className="w-100 mt-0 pt-0 shift-up"
            ),

            html.Label('select and sort chromosomes: ', className='mb-1 label-s'),
            dcc.RadioItems(['original', 'length', 'connections'], value='original', id={'id':'chr-sort', 'tab': tab_name}, inline=True, labelClassName="ms-0 me-4"),
            html.Div(id={'id':"synteny-chromosome-selection", "tab":tab_name}),
        ])
    ]


## 4. SPECIFIC GRAPH SETTINGS in Option Panel

# Chromosome setup: spacing, hight, corner-radius
def create_synteny_chromosome(tab_name):
    return [
        html.Div([
          html.Label('position:', className='col-2 me-3 d-inline label-s', title="Choose alignment mode"),
          dcc.Dropdown(id={'id':"synteny-chr-alignment", 'tab': tab_name}, options = [{'label': value, 'value': value} for value in ['left', 'right', 'center', 'block']], value='center', className='col-6', clearable=False, style=drop50),
          html.Label('spacing:', className='col-2 me-3 d-inline label-s', style={"margin-left" : "-6em"}, title="Adjust spacing between chromosomes"),
          dcc.Input(id={'id':"synteny-chr-spacing", 'tab': tab_name}, type="number", min=0.001, max=0.5, step=0.001, placeholder="Enter spacing", value=0.01, debounce=True, className='col-3'),
          html.Label('height:', className='col-2 me-3 d-inline label-s', title="Adjust height of chromosomes"),
          dcc.Input(id={'id':"synteny-chr-height", 'tab': tab_name}, type="number", min=0.5, max=19, step=0.1, placeholder="Enter height", value=3, debounce=True, className='col-3 mt-1'),
        ], className="row align-items-center"),
    ]

# Synteny line setup: start-end position on chromosome
def create_synteny_line(tab_name):
    return [
        html.Div([
            html.Label('position:', className='col-4 d-inline label-s', title="Choose position mode for chromosomes"),
            dcc.RadioItems(['exact', 'middle'], value='exact', id={'id':"synteny-line-position", 'tab': tab_name}, inline=True, className="col-8 p-0", labelClassName="ms-0 me-3"),
        ], className="row align-items-center mt-2 pe-2 h34 w-100"),
    ]

# Synteny ribbon setup:
def create_synteny_ribbon(tab_name):
    return []


### -------------------------------------- ###

# Final assembly of the options specific for the SYNTENY analysis
def create_opts_analysis_synteny(tab_name):
    return [
        html.Div([
            dbc.Accordion([
                dbc.AccordionItem(create_synteny_merge_data(tab_name), title="MERGE DATA (optional)", item_id="graph-synteny-1"),
                dbc.AccordionItem(create_synteny_graph_inputs(tab_name), title="SELECT GRAPH INPUTS", item_id="graph-synteny-2"),
                dbc.AccordionItem(create_synteny_selection(tab_name), title="SELECT SPECIES / CHROMOSOMES", item_id="graph-synteny-3"),
            ], id={'id':"opts-analysis-synteny", 'tab': tab_name}, class_name='accordion2 p-0', start_collapsed=True, always_open=True, flush=False, className='w-100 p-0'),
        ])
    ]


# Final assembly of the options specific for the SYNTENY graph
def create_opts_graph_synteny(tab_name):
    return [
      html.Div([
        dbc.Accordion([
          dbc.AccordionItem(create_synteny_chromosome(tab_name), title="CHROMOSOMES", item_id="graph-synteny-1"),
          dbc.AccordionItem(create_synteny_line(tab_name), title="SYNTENY LINES", item_id="graph-synteny-2"),
          dbc.AccordionItem(create_synteny_ribbon(tab_name), title="SYNTENY RIBBON", item_id="graph-synteny-3"),
        ], id={'id':"graph-custom-synteny", 'tab': tab_name}, class_name='accordion2 p-0', start_collapsed=True, always_open=True, flush=False, className='w-100 p-0'),
      ], className="row align-items-center mt-1"),
    ]