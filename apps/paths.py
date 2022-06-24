import os
import shutil
import datetime as dt
import pathlib as path

#-- PATHS
path_repo = path.Path.cwd().absolute()  # .as_posix() to get string
path_apps = path.Path.joinpath(path_repo, 'apps').absolute()
path_data = path.Path.joinpath(path_repo, 'static/data').absolute()
path_examples = path.Path.joinpath(path_data, 'examples').absolute()
path_downloads = path.Path.joinpath(path_data, 'downloads').absolute()
path_projects = path.Path.joinpath(path_data, 'projects').absolute()