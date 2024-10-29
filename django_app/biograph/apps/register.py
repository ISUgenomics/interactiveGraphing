# Global list to track registered Dash apps
REGISTERED_DASH_APPS = []

# Function to register and track Dash apps
def register_dash_app(name, **kwargs):
    from django_plotly_dash import DjangoDash
    app = DjangoDash(name, **kwargs)
    REGISTERED_DASH_APPS.append(name)  # Track the app name
    print(f"Registered Dash app: {name}") 
    return app