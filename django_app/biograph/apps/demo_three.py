import dash
from dash import dcc, html
from django_plotly_dash import DjangoDash
from .register import register_dash_app

# Register the Dash app with the exact name "demo-three"
#a3 = DjangoDash("Demo3", serve_locally=True)
a3 = register_dash_app("Ex2", serve_locally=True)

a3.layout = html.Div([
    dcc.RadioItems(
        id="dropdown-one",
        options=[
            {'label': 'Oxygen', 'value': 'O2'},
            {'label': 'Nitrogen', 'value': 'N2'},
            {'label': 'Carbon Dioxide', 'value': 'CO2'}
        ],
        value="Oxygen"
    ),
    html.Div(id="output-one")
])

@a3.expanded_callback(
    dash.dependencies.Output('output-one', 'children'),
    [dash.dependencies.Input('dropdown-one', 'value')]
)
def callback_c(value, **kwargs):
    session_state = kwargs['session_state']
    session_state['last_value'] = value
    return f"Selected value is: {value}"