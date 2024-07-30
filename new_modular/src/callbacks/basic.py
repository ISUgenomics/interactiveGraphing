from dash import dcc, html
from dash.dependencies import Input, Output
from src.pages import index, about
from src.pages.apps import synteny

def register_basic_callbacks(app):
    @app.callback(
        Output('content', 'children'),
        [Input('tabs', 'value'), Input('visualizations', 'value')]
    )
    def render_content(tab, visualization):
        if tab == 'tab-home':
            if visualization == 'synteny':
                return synteny.layout
            else:
                return index.layout
        elif tab == 'tab-about':
            return about.layout

