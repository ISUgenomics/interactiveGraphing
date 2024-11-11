'''
Dash bootstrap component demo app

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

import dash
import dash_bootstrap_components as dbc
from dash import html

from django_plotly_dash import DjangoDash

dd = DjangoDash("DemoSeven",
                serve_locally=True,
                add_bootstrap_links=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

dd.layout = html.Div(
    [
        dbc.Alert("This is an alert", color="primary"),
        dbc.Alert("Danger", color="danger"),
        dbc.Checklist(id='check_switch', switch=True, options=[{"label": "An example switch", "value": 1}], value=[0]),
        dbc.Checklist(id='check_check', switch=False, options=[{"label": "An example checkbox", "value": 1}], value=[0]),

        dbc.Accordion([
            dbc.AccordionItem([], title="1. UPLOAD RAW INPUTS", item_id="item-1"),
            dbc.AccordionItem([], title="2. ADJUST ANALYSIS SETTINGS", item_id="item-2"),
            dbc.AccordionItem([], title="3. GENERAL GRAPH SETTINGS", item_id="item-3"),
            dbc.AccordionItem([], title="4. SPECIFIC GRAPH SETTINGS", item_id="item-4"),
            dbc.AccordionItem([], title="5. EXPORT GRAPH", item_id="item-5", class_name=".container")
        ], id="accordion", always_open=True, flush=False, start_collapsed=False),
        ]
    )

