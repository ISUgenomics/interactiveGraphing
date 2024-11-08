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


pattern_state_callbacks = DjangoDash("DemoTwo")

pattern_state_callbacks.layout = html.Div([
    html.Div(id={"_id": "output-one", "_type": "divo"}),
    html.Div(id={"_id": "output-two", "_type": "div"}),
    html.Div(id={"_id": "output-three", "_type": "div"})
])


@pattern_state_callbacks.callback(
    dash.dependencies.Output({"_type": "div", "_id": MATCH}, 'children'),
    [dash.dependencies.Input({"_type": "div", "_id": MATCH}, 'n_clicks')])
def pattern_match(values):
    return str(values)


@pattern_state_callbacks.callback(
    dash.dependencies.Output({"_type": "divo", "_id": "output-one"}, 'children'),
    [dash.dependencies.Input({"_type": "div", "_id": ALL}, 'children')])
def pattern_all(values):
    return str(values)


