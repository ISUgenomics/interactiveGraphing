from .synteny.callbacks import register_synteny_callbacks


def register_app_callbacks(app):
    register_synteny_callbacks(app)