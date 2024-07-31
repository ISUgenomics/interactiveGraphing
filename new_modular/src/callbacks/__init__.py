from .basic import register_basic_callbacks
from .storage import register_storage_callbacks
from .data_table import register_datatable_callbacks
from .clientside import register_clientside_callbacks
from .left_panel import register_left_panel_callbacks
from .right_panel import register_right_panel_callbacks
from .graph import register_graph_callbacks

def register_callbacks(app):
    register_basic_callbacks(app)
    register_storage_callbacks(app)
    register_datatable_callbacks(app)
    register_clientside_callbacks(app)
    register_left_panel_callbacks(app)
    register_right_panel_callbacks(app)
    register_graph_callbacks(app)
