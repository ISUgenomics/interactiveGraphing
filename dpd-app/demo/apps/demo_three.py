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

# pylint: disable=no-member

import uuid
import random

from datetime import datetime

import pandas as pd

from django.core.cache import cache
from django.utils.translation import gettext, gettext_lazy

import dash
from dash import dcc, html
from dash.dependencies import MATCH, ALL

import plotly.graph_objs as go

import dpd_components as dpd

from dash.exceptions import PreventUpdate

from django_plotly_dash import DjangoDash
from django_plotly_dash.consumers import send_to_pipe_channel




a2 = DjangoDash("DemoThree",
                serve_locally=True)

a2.layout = html.Div([
    dcc.RadioItems(id="dropdown-one",
                   options=[{'label':i, 'value':j} for i, j in [("O2", "Oxygen"),
                                                                ("N2", "Nitrogen"),
                                                                ("CO2", "Carbon Dioxide")]],
                   value="Oxygen"),
    html.Div(id="output-one")
    ])

@a2.expanded_callback(
    dash.dependencies.Output('output-one', 'children'),
    [dash.dependencies.Input('dropdown-one', 'value')]
    )
def callback_c(*args, **kwargs):
    'Update the output following a change of the input selection'
    #da = kwargs['dash_app']

    session_state = kwargs['session_state']

    calls_so_far = session_state.get('calls_so_far', 0)
    session_state['calls_so_far'] = calls_so_far + 1

    user_counts = session_state.get('user_counts', None)
    user_name = str(kwargs['user'])
    if user_counts is None:
        user_counts = {user_name:1}
        session_state['user_counts'] = user_counts
    else:
        user_counts[user_name] = user_counts.get(user_name, 0) + 1

    return "Args are [%s] and kwargs are %s" %(",".join(args), str(kwargs))


