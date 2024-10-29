import os
from src.params.globals import src

def get_visualizations():
    apps_path = os.path.join(src, 'apps')
    all_dirs = [d for d in os.listdir(apps_path) if os.path.isdir(os.path.join(apps_path, d))]
    visualizations = [d for d in all_dirs if not (d.startswith('_') or d.startswith('.'))]  # skip apps under development
    
    return visualizations


# Dynamically generate the list of available apps
visualizations = get_visualizations()