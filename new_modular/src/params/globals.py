import os

# ------ GLOBAL VARIABLES ------ #

# Path to the src of the codebase
src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
opts_db = os.path.join(src, 'params', 'options_dynamic.db')