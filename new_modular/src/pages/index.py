from dash import html, dcc
import dash_bootstrap_components as dbc
from src.pages.config import visualizations
from src.functions.widgets import generate_dbc_button


layout = html.Div([
    html.H2("Home Page"),
    html.P("Welcome to the home page!"),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='visualizations',
            options=[{'label': viz, 'value': viz} for viz in visualizations],
            value='synteny',
            style={"marginTop":"2px"}
        ), width=3, className="ps-2 me-2"),
        dbc.Col(generate_dbc_button('Add Tab', 'add-app-tab'), width=2, className="ps-2 me-2 mt-1")
    ]),
], id='home-mode', className="pt-3 px-5")
