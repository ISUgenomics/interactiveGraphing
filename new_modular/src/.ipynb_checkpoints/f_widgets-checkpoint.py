# Layout-related functions

def generate_font_options(value_list):
    options = []
    for value in value_list:
        options.append({'label':html.Span([value], style={'font-family':value}), 'value':value})
    return options


def generate_color_options(value_list):
    options = []
    for value in value_list:
        options.append({'label':html.Span([value], style={'color':value}), 'value':value})
    return options


def generate_html_label(text, cname='d-block', style=css_lab):
    return html.Label(children=str(text), className=cname, style=style)


def generate_dbc_button(text, identifier, n_clicks=0, size="sm", outline=True, color="secondary", cname="align-top w-50 h34", style={}, disabled=False):
    return dbc.Button(children=text, id=identifier, n_clicks=n_clicks, size=size, outline=outline, color=color, className=cname, style={**style})

def generate_pop_up_modal(identifier, close_id, close_text, body, title, size):
    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(title), style={'background-color':'#D6F2FA'}),
        dbc.ModalBody(children = body),
        dbc.ModalFooter(dbc.Button(close_text, id=close_id, n_clicks=0, outline=True, color="secondary", className="me-1 align-top", style={'padding':'0 5px'})),
    ], id=identifier, size=size, centered=True, is_open=False, scrollable=True)
    
    return modal
    

def get_triggered_info(ctx):
    info = []
    if len(ctx):
        tmp = ctx[0]['prop_id']
        info = ['', '', ctx[0]['value'], tmp.split('.')[-1]]
        if tmp.startswith('{'):
            prop = tmp.split('{')[1].split('}')[0].split(',')
            info[0] = prop[1].split(':')[1].replace('"', '')
            info[1] = prop[0].split(':')[1].replace('"', '')
        else:
            info[1] = tmp.split('.')[0]
    return info


def find_component_ids(component):
    ids = []
    if isinstance(component, (dcc.Graph, dcc.Input, dcc.Dropdown, dcc.Checklist, html.Button)):
        if getattr(component, 'id', None):
            ids.append(component.id)

    if hasattr(component, 'children'):
        children = component.children
        if children:
            if isinstance(children, list):
                for child in children:
                    ids.extend(find_component_ids(child))
            else:
                ids.extend(find_component_ids(children))

    return ids


def is_component_type(component_id, target_type):
    if component_id in app.layout:
        component_instance = app.layout[component_id]
        return isinstance(component_instance, target_type)
    return False