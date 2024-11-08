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


liveIn = DjangoDash("DemoFive",
                    serve_locally=True,
                    add_bootstrap_links=True)

liveIn.layout = html.Div([
    html.Div([html.Button('Choose red. Press me!',
                          id="red-button",
                          className="btn btn-danger"),
              html.Button('Blue is best. Pick me!',
                          id="blue-button",
                          className="btn btn-primary"),
              html.Button('Time to go green!',
                          id="green-button",
                          className="btn btn-success"),
             ], className="btn-group"),
    html.Div(id='button_local_counter', children="Press any button to start"),
    ], className="")

#pylint: disable=too-many-arguments
@liveIn.expanded_callback(
    dash.dependencies.Output('button_local_counter', 'children'),
    [dash.dependencies.Input('red-button', 'n_clicks'),
     dash.dependencies.Input('blue-button', 'n_clicks'),
     dash.dependencies.Input('green-button', 'n_clicks'),
     dash.dependencies.Input('red-button', 'n_clicks_timestamp'),
     dash.dependencies.Input('blue-button', 'n_clicks_timestamp'),
     dash.dependencies.Input('green-button', 'n_clicks_timestamp'),
    ],
    )
def callback_liveIn_button_press(red_clicks, blue_clicks, green_clicks,
                                 rc_timestamp, bc_timestamp, gc_timestamp, **kwargs): # pylint: disable=unused-argument
    'Input app button pressed, so do something interesting'

    if not rc_timestamp:
        rc_timestamp = 0
    if not bc_timestamp:
        bc_timestamp = 0
    if not gc_timestamp:
        gc_timestamp = 0

    if (rc_timestamp + bc_timestamp + gc_timestamp) < 1:
        change_col = None
        timestamp = 0
    else:
        if rc_timestamp > bc_timestamp:
            change_col = "red"
            timestamp = rc_timestamp
        else:
            change_col = "blue"
            timestamp = bc_timestamp

        if gc_timestamp > timestamp:
            timestamp = gc_timestamp
            change_col = "green"

        value = {'red_clicks':red_clicks,
                 'blue_clicks':blue_clicks,
                 'green_clicks':green_clicks,
                 'click_colour':change_col,
                 'click_timestamp':timestamp,
                 'user':str(kwargs.get('user', 'UNKNOWN'))}

        send_to_pipe_channel(channel_name="live_button_counter",
                             label="named_counts",
                             value=value)
    return "Number of local clicks so far is %s red and %s blue; last change is %s at %s" % (red_clicks,
                                                                                             blue_clicks,
                                                                                             change_col,
                                                                                             datetime.fromtimestamp(0.001*timestamp))

