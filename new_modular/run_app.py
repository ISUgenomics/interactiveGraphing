from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from src.pages import index, about
from src.callbacks import register_callbacks
from src.params.generic import PARAMS                                          # DEBUG ############
from src.layout.storage import storage, void, identifiers
from src.layout.options import left_panel
from src.layout.graphing import right_panel
from src.functions.widgets import find_component_ids                           # DEBUG ############

external_stylesheets = [
    dbc.themes.BOOTSTRAP, 
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    '/assets/custom.css', 'font-awesome.min.css'
]

external_scripts = [
    {'src': '/assets/custom.js'}
]

app = Dash(__name__, external_stylesheets=external_stylesheets, 
                     external_scripts=external_scripts, 
                     title="ActiGraph", update_title=None,
                     prevent_initial_callbacks='initial_duplicate',
                     suppress_callback_exceptions=True
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
        dbc.Col(dcc.Tabs(id="tabs", value='tab-home', parent_className='index-tabs', className='index-container',
                    children=[
                        dcc.Tab(label='HOME', value='tab-home', className='index-tab'),
                        dcc.Tab(label='ABOUT', value='tab-about', className='index-tab'),]), 
                width=12, className="pe-0"),
    ], style={"backgroundColor":"rgb(214, 242, 250)"}),
    html.Div(id='info-mode'),
    html.Div(id='app-mode', children=[
        left_panel,
        right_panel
    ], style={'width':'100%', 'height':'100%', 'overflowY':'hidden', "display": "flex"}, hidden=True)
], fluid=True)



#### ------- DEBUG SECTION  ------------------- ####
# [OPTIONAL - DEBUG] Get all component IDs                                                      # DEBUG ############
def is_component_type(component_id, target_type):
    if component_id in app.layout:
        component_instance = app.layout[component_id]
        return isinstance(component_instance, target_type)
    return False

all_ids = find_component_ids(app.layout)                                                        # DEBUG ############
print(all_ids, '\n')                                                                            # DEBUG #########
missing_keys = set(PARAMS.keys()) - set(all_ids)                                                # DEBUG ############
print("The following keys from PARAMS are missing in the all_ids list:", missing_keys, '\n')    # DEBUG ############
#### ------- DEBUG SECTION  ------------------- ####



# Import all callbacks
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True, port=8085)
