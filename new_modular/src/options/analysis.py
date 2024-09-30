from dash import html, dcc
import dash_bootstrap_components as dbc

## 2. ADJUST ANALYSIS SETTINGS

synteny = [
    html.Label('select graph inputs: ', className='mb-1 label-s'),
    dcc.Dropdown(id="synteny-inputs", persistence=True, persistence_type="session"),
    html.Label('select genomes: ', className='mb-1 mt-3 label-s'),
    dcc.Dropdown(id="synteny-genomes", multi=True, persistence=True, persistence_type="session"),
]









# Final assembly of analysis options
opts_analysis = html.Div(id="opts-analysis")