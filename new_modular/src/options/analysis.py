from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_draggable

## 2. ADJUST ANALYSIS SETTINGS


# Options specific for the synteny analysis
def create_opts_analysis_synteny(tab_name):
    return [
        html.Div([
            html.Label('select graph inputs: ', className='mb-1 label-s'),
            dcc.Dropdown(id="synteny-inputs", persistence=True, persistence_type="session"),

            html.Label('select and manually sort genomes: ', className='mb-1 mt-3 label-s'),
            # Draggable GridLayout for genome selection
            dash_draggable.GridLayout(id='genome-draggable', children=[],
                gridCols=2, width=300, height=28, className="w-100 mt-0 pt-0 shift-up"
            ),

            html.Label('select and sort chromosomes: ', className='mb-1 label-s'),
            dcc.RadioItems(['original', 'length', 'connections'], value='original', inline=True, labelClassName="ms-0 me-4"),
            html.Div(id="synteny-chromosome-selection"),
        ])
    ]


# Final assembly of analysis options
def create_opts_analysis(tab_name):

    variant = tab_name.split('_')[0]
    function_name = f'create_opts_analysis_{variant}'
    if function_name in globals():
        return [html.Div(id={'id':"opts-analysis", 'tab': tab_name}, children = globals()[function_name](variant))]
    else:
        return [html.Div(id={'id':"opts-analysis", 'tab': tab_name}, children = html.Div(f"No options available for {variant}"))]