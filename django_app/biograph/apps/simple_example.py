'''
Dash apps for the demonstration of functionality

Copyright (c) 2018 Gibbs Consulting and others - see CONTRIBUTIONS.md

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import uuid
import random
from datetime import datetime

from django.core.cache import cache
from django.utils.translation import gettext, gettext_lazy

import dash
from dash import dcc, html
from dash.dependencies import MATCH, ALL
from dash.exceptions import PreventUpdate


from django_plotly_dash import DjangoDash
import requests
import json


#pylint: disable=too-many-arguments, unused-argument, unused-variable

app = DjangoDash('SimpleExample')


# Function to fetch the saved state from the server
def fetch_app_state():
    # Replace 'DemoApp' and 'instance-1' with your app name and instance ID
    try:
        response = requests.get('/load_state/SimpleExample/instance-1/')
        if response.status_code == 200:
            state_data = response.json().get('state', {})
            return state_data
        return {}
    except requests.exceptions.RequestException:
        return {}

# Load the state on app initialization
saved_state = fetch_app_state()

# Set initial values based on saved state, fallback to default if state not found
initial_color = saved_state.get('dropdown_color', 'red')
initial_size = saved_state.get('dropdown_size', 'medium')




app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value=initial_color
    ),
    html.Div(id='output-color'),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i, 'value': j} for i, j in [('L', gettext('large')),
                                                       ('M', gettext_lazy('medium')),
                                                       ('S', 'small')]],
        value=initial_size
    ),
    html.Div(id='output-size')

])

# Callback to update the color display
@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')]
)
def callback_color(dropdown_value):
    'Change output message'
    # Save the state whenever the user changes the color
    save_app_state('SimpleExample', 'instance-1', {'dropdown_color': dropdown_value})
    return f"The selected color is {dropdown_value}."

# Callback to update the size display and save the state
@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')]
)
def callback_size(dropdown_color, dropdown_size):
    'Change output message'
    # Save the state whenever the user changes the size or color
    save_app_state('SimpleExample', 'instance-1', {
        'dropdown_color': dropdown_color,
        'dropdown_size': dropdown_size
    })
    return f"The chosen T-shirt is a {dropdown_size} {dropdown_color} one."

# Function to save the state to the server
def save_app_state(app_name, instance_id, state_data):
    try:
        requests.post('/save_state/SimpleExample/instance-1/', data={
            'state': json.dumps(state_data)  # Convert to JSON
        })
    except requests.exceptions.RequestException:
        pass  # Handle exceptions (e.g., logging)



