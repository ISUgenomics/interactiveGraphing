from dash import dcc, html
from dash.dependencies import Input, Output, State


def register_left_panel_callbacks(app):
    
    # color scale modal open-close
    @app.callback(Output("modal-cs", "is_open"),
                 [Input("modal-cs-btn-open", "n_clicks"), Input("modal-cs-btn-close", "n_clicks"),],
                 [State("modal-cs", "is_open")])
    def toggle_modal_cs(n_open, n_close, is_open):
        if n_open or n_close:
            return not is_open
        return is_open


    # Update graph config 
    @app.callback(Output("graph-config", "data"),
                 [Input('img-format', 'value'), Input('img-name', 'value'), 
                  Input('img-height', 'value'), Input('img-width', 'value'), Input('img-scale', 'value')],
                 [State("graph-config", "data")])
    def update_config(imgtype, name, height, width, scale, config):
        config['toImageButtonOptions'] = {'format': str(imgtype), 'filename': str(name), 'height': int(height), 'width': int(width),  'scale': float(scale)}
        return config
