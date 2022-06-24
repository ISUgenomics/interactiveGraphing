from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps import manager #, app_volcano #, heatmap

from whitenoise import WhiteNoise

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/apps/manager':
        return manager.layout
#    elif pathname == '/apps/app_volcano':
#        return app_volcano.layout
#    elif pathname == '/apps/heatmap':
#        return heatmap.layout
    else:
        return '404'

app.server.wsgi_app = WhiteNoise(app.server.wsgi_app, root='static/', index_file=True)

server = app.server

if __name__ == '__main__':
    app.run_server(port=8025, debug=True, dev_tools_ui=True)
