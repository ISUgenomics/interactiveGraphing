# IMPORTS
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


# CONSTANTS, DEFAULT VARIABLES AND GLOBAL SETTINGS
from generic import fruits, amounts

# APP LAYOUT
app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='fruit-dropdown',
        options=[{'label': fruit, 'value': fruit} for fruit in fruits],
        value=fruits[0]
    ),
    dcc.Graph(id='example-graph')
])

# APP CALLBACKS
@app.callback(
    Output('example-graph', 'figure'),
    Input('fruit-dropdown', 'value')
)
def update_graph(selected_fruit):
    colors = ['blue' if fruit == selected_fruit else 'grey' for fruit in fruits]
    fig = px.bar(x=fruits, y=amounts, color=colors, color_discrete_map={"blue": "blue", "grey": "grey"}, category_orders={"x": fruits})
    return fig


# DEPLOY ON LOCAL PYTHON SERVER
if __name__ == '__main__':
    app.run(debug=True, port=8051)