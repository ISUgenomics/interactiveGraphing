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




liveOut = DjangoDash("DemoFour")

def _get_cache_key(state_uid):
    return "demo-liveout-s6-%s" % state_uid

def generate_liveOut_layout():
    'Generate the layout per-app, generating each tine a new uuid for the state_uid argument'
    return html.Div([
        dpd.Pipe(id="named_count_pipe",
                 value=None,
                 label="named_counts",
                 channel_name="live_button_counter"),
        html.Div(id="internal_state",
                 children="No state has been computed yet",
                 style={'display':'none'}),
        dcc.Graph(id="timeseries_plot"),
        dcc.Input(value=str(uuid.uuid4()),
                  id="state_uid",
                  style={'display':'none'},
                 )
        ])

liveOut.layout = generate_liveOut_layout

#pylint: disable=unused-argument
#@liveOut.expanded_callback(
@liveOut.callback(
    dash.dependencies.Output('internal_state', 'children'),
    [dash.dependencies.Input('named_count_pipe', 'value'),
     dash.dependencies.Input('state_uid', 'value'),],
    )
def callback_liveOut_pipe_in(named_count, state_uid, **kwargs):
    'Handle something changing the value of the input pipe or the associated state uid'

    cache_key = _get_cache_key(state_uid)
    state = cache.get(cache_key)

    # If nothing in cache, prepopulate
    if not state:
        state = {}

    # Guard against missing input on startup
    if not named_count:
        named_count = {}

    # extract incoming info from the message and update the internal state
    user = named_count.get('user', None)
    click_colour = named_count.get('click_colour', None)
    click_timestamp = named_count.get('click_timestamp', 0)

    if click_colour:
        colour_set = state.get(click_colour, None)

        if not colour_set:
            colour_set = [(None, 0, 100) for i in range(5)]

        _, last_ts, prev = colour_set[-1]

        # Loop over all existing timestamps and find the latest one
        if not click_timestamp or click_timestamp < 1:
            click_timestamp = 0

            for _, the_colour_set in state.items():
                _, lts, _ = the_colour_set[-1]
                if lts > click_timestamp:
                    click_timestamp = lts

            click_timestamp = click_timestamp + 1000

        if click_timestamp > last_ts:
            colour_set.append((user, click_timestamp, prev * random.lognormvariate(0.0, 0.1)),)
            colour_set = colour_set[-100:]

        state[click_colour] = colour_set
        cache.set(cache_key, state, 3600)

    return "(%s,%s)" % (cache_key, click_timestamp)

@liveOut.callback(
    dash.dependencies.Output('timeseries_plot', 'figure'),
    [dash.dependencies.Input('internal_state', 'children'),
     dash.dependencies.Input('state_uid', 'value'),],
    )
def callback_show_timeseries(internal_state_string, state_uid, **kwargs):
    'Build a timeseries from the internal state'

    cache_key = _get_cache_key(state_uid)
    state = cache.get(cache_key)

    # If nothing in cache, prepopulate
    if not state:
        state = {}

    colour_series = {}

    colors = {'red':'#FF0000',
              'blue':'#0000FF',
              'green':'#00FF00',
              'yellow': '#FFFF00',
              'cyan': '#00FFFF',
              'magenta': '#FF00FF',
              'black' : '#000000',
             }

    for colour, values in state.items():
        timestamps = [datetime.fromtimestamp(int(0.001*ts)) for _, ts, _ in values if ts > 0]
        #users = [user for user, ts, _ in values if ts > 0]
        levels = [level for _, ts, level in values if ts > 0]
        if colour in colors:
            colour_series[colour] = pd.Series(levels, index=timestamps).groupby(level=0).first()

    df = pd.DataFrame(colour_series).fillna(method="ffill").reset_index()[-25:]

    traces = [go.Scatter(y=df[colour],
                         x=df['index'],
                         name=colour,
                         line=dict(color=colors.get(colour, '#000000')),
                        ) for colour in colour_series]

    return {'data':traces,
            #'layout': go.Layout
           }

