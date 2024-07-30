from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from src.pages import index, about
from src.pages.config import visualizations
from src.callbacks import register_callbacks
from src.layout.storage import storage, void, identifiers

external_stylesheets = [
    dbc.themes.BOOTSTRAP, 
#    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    '/assets/custom.css'
]

external_scripts = [
    {'src': '/assets/custom.js'}
]

app = Dash(__name__, external_stylesheets=external_stylesheets, 
                     external_scripts=external_scripts, 
                     title="SYNTENY", update_title=None,
                     suppress_callback_exceptions=False
          )

app.scripts.config.serve_locally=True
app.css.config.serve_locally=True

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
            <div class="footer row m-0">
                <div class="d-inline w-25">Copyright 2024 GIF@ISU</div>
                <div class="d-inline w-50">© <b>Interactive Graphing</b></div>
                <div class="d-inline w-25">Development: <a style="text-decoration: none;" href="https://github.com/aedawid" target="_blank">abadacz</a></div></div>
        </footer>
    </body>
</html>
'''

app.layout = dbc.Container([
    dcc.Location(id='location', refresh=False),
    void, identifiers, storage,
    dbc.Row([
        dbc.Col(dcc.Tabs(id="tabs", value='tab-home', parent_className='index-tabs', className='index-container', children=[
            dcc.Tab(label='HOME', value='tab-home', className='index-tab'),
            dcc.Tab(label='ABOUT', value='tab-about', className='index-tab'),
        ]), width=9, className="pe-0"),
        dbc.Col(dcc.Dropdown(
            id='visualizations',
            options=[{'label': viz.capitalize(), 'value': viz} for viz in visualizations],
            value='synteny',
            style={"marginTop":"2px"}
        ), width=3, className="ps-2 pb-0", style={"paddingRight":"33px"}),
    ], style={"backgroundColor":"rgb(214, 242, 250)"}),
    html.Div(id='content')
], fluid=True)


# Import all callbacks
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True, port=8085)
