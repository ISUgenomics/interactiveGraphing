# Folder and File Descriptions

- `run_app.py` (file): The main entry point to run the Dash application.
- `requirements.txt` (file): Lists the dependencies required for the project.

## assets/
Contains custom CSS and JS files that are automatically included by Dash.

`custom.css`: Custom styles for the Dash application.

## static/
Holds static files such as additional CSS, data files, fonts, images, and JavaScript plugins.

## src/
The main source code of the Dash application, organized into several subdirectories for clarity and modularity.

### pages/
Contains the main page layout files and configurations.

- `__init__.py`: Initializes the pages module.
- `about.py`: Layout and content for the About page.
- `index.py`: Layout and content for the Home page.
- `config.py`: Configuration for available visualization types.
  - `synteny.py`: Layout and content for the Synteny visualization page.

### params/
Stores constant and customizable parameters for the application.

- `generic.py`: Constant options that do not change.
- `variables.py`: Custom options and tooltips that can be added and modified.

### layout/
Contains assembled layouts for different sections of the application.

- `options.py`: Assembled layout for the options section. (left panel of the app)
- `graphing.py`: Assembled layout for the graphing section. (right panel of the app)

### options/
Contains components for different sections under the options menu.

- 01. `uploads.py`: Components for input file uploads.
- 02. `analysis.py`: Components for preprocessing and analytical options applied to raw data.
- 03. `graph_general.py`: General graph-related options. (applicable to any graph type)
- 04. `graph_custom.py`: Custom graph-related options. (specific to the selected grap type)
- 05. `export.py`: Components related to exporting data or plots.

### functions/
Contains utility functions for dynamic creation of widgets and other calculations.

- `io.py`: Python functions for managing and processing inputs and outputs.
- `widgets.py`: Python functions for dynamic generation of Dash components/widgets.

### callbacks/
Contains dash-type functions that handle app interactivity and callbacks.

- `basic.py`: Functions to register and manage callbacks for interactivity.

### analyses/
Contains specialized Python functions for data analysis and statistics.

- `statistics.py`: Functions for statistical analysis on data.


# How to Use This Project

**0.** Git clone the repo:
```
git clone https://github.com/ISUgenomics/interactiveGraphing.git
```

**1.** Create conda env:
```
conda create -n graphing python=3.12
```

**2.**  **Setup:** Install the required dependencies listed in `requirements.txt`.
```
pip install -r requirements.txt
```

**3.** **Run the App:** start the Dash server in a terminal and run the application
```
python run_app.py
``` 

3. **Explore the App:** Open any web browser and navigate to URL: `http://127.0.0.1:8085/`.