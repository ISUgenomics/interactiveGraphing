from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_draggable

## 2. ADJUST ANALYSIS SETTINGS
genomes = ["Genome A", "Genome B", "Genome C", "Genome D"]

synteny = [
    html.Label('select graph inputs: ', className='mb-1 label-s'),
    dcc.Dropdown(id="synteny-inputs", persistence=True, persistence_type="session"),

    html.Label('select and order genomes: ', className='mb-1 mt-3 label-s'),
    dcc.Store(id="synteny-genomes-all", data=[], storage_type='session'),
    dcc.Store(id='synteny-genomes-selected', data=[], storage_type='session'),
    dcc.Store(id='synteny-chromosomes-all', data={}, storage_type='session'),
    dcc.Store(id='synteny-chr-selected', data=[], storage_type='session'),
    # Draggable GridLayout for genome selection
    dash_draggable.GridLayout(id='genome-draggable', children=[], 
        gridCols=2, width=300, height=28, className="w-100 mt-0 pt-0 shift-up"
    ),

    html.Label('select and order chromosomes: ', className='mb-1 label-s'),
    dcc.RadioItems(['order', 'min-dist','manual'], value='order', inline=True, labelClassName="ms-0 me-3"),
    html.Div(id="synteny-chromosome-selection"),
]









# Final assembly of analysis options
opts_analysis = html.Div(id="opts-analysis")