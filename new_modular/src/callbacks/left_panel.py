
from dash import dcc, html, callback_context, no_update
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
from src.functions.widgets import get_triggered_info, get_triggered_dict, get_triggered_index
from src.params.generic import CONFIG


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
                 [Input({'id':'img-format', 'tab':ALL}, 'value'), Input({'id':'img-name', 'tab':ALL}, 'value'), 
                  Input({'id':'img-height', 'tab':ALL}, 'value'), Input({'id':'img-width', 'tab':ALL}, 'value'), Input({'id':'img-scale', 'tab':ALL}, 'value')],
                 [State("graph-config", "data"), State('tabs', 'active_tab'), State({'id':'img-format', 'tab':ALL}, 'id')], 
                  prevent_initial_call = True)
    def update_config(imgtype, name, height, width, scale, config, active_tab, items):
        try:
            active_tab = active_tab.split('-')[-1]
            tnv = get_triggered_info(callback_context.triggered)
            key = tnv[0]
            if active_tab != key:
                raise PreventUpdate
            ix = get_triggered_index(items, value=tnv[0])
        except:
            raise PreventUpdate
        if not key in config:
            config[key] = CONFIG
        config[key]['toImageButtonOptions'] = {'format': str(imgtype[ix]), 'filename': str(name[ix]), 'height': int(height[ix]), 'width': int(width[ix]),  'scale': float(scale[ix])}
        config['@changed'] = key
        return config



    @app.callback(Output("collapse", 'is_open'),
                 [Input("close-collapse", 'n_clicks'), Input({"type":"collapse-btn", "id":ALL, 'tab': ALL}, 'n_clicks')], 
    )
    def toggle_cards(n_clicks, genome_btns):
        print("\ncallback: toggle_cards()", callback_context.triggered)                                                              ########## DEBUG
        gtd = get_triggered_dict(callback_context.triggered)
        if 'close-collapse' in {gtd.get('type'), gtd.get('id')} and n_clicks > 0:
            return False
        else:
            return True


    @app.callback(Output({"type":"collapse-card", "id":ALL, 'tab': MATCH}, 'class_name'),
                  Input({"type":"collapse-btn", "id":ALL, 'tab': MATCH}, 'n_clicks'),
                 [State({"type":"collapse-card", "id":ALL, 'tab': MATCH}, 'class_name'), State({"type":"collapse-card", "id":ALL, 'tab':MATCH}, 'id')],
    )
    def display_cards(n_clicks, styles, ids):                                                         ########## UPDATE : can be moved to universal widget_toogle module, when generalized
        print("\n callback: display_cards()")                                                         ########## DEBUG

        # Return current styles if nothing was triggered
        gtd = get_triggered_dict(callback_context.triggered)
        if not gtd:
            return styles

        # Find the index of the button clicked
        index = next((i for i, item in enumerate(ids) if gtd['id'] == item['id']), None)
        return ['d-block' if i == index else 'd-none' for i in range(len(ids))] if index is not None else styles



