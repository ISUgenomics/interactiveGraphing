# interactiveGraphing
Using python, Plotly and dash to visualize informatics data.

## Download interactiveGraphing repository on your local machine

```
git clone https://github.com/ISUgenomics/interactiveGraphing.git
```

## Create conda environment

0: Activate base `conda` environemnt (on the Mac switch into condaX86 version for [Intel](https://bioinformaticsworkbook.org/100days/MacbookProInstallation#install-conda).

1: Create new virtual environment for interactiveGraphing repo and activate it :

```
conda create --name plotly python==3.9
conda activate plotly
```

2: Install dependencies from `requirements.txt` :

```
conda install --file requirements.txt
```
If the required versions are not available in the default channels, you can easily install them via `pip` :

`TIPS:` Ideally, you should use the internal pip3 in the newly created environment.

```
/path_to_your_conda_version/envs/plotly/bin/pip3 install whitenoise==5.1.0
/path_to_your_conda_version/envs/plotly/bin/pip3 install pandas==1.4.0
/path_to_your_conda_version/envs/plotly/bin/pip3 install plotly==5.6.0
/path_to_your_conda_version/envs/plotly/bin/pip3 install plotly_express==0.4.1
/path_to_your_conda_version/envs/plotly/bin/pip3 install dash==2.1.0
/path_to_your_conda_version/envs/plotly/bin/pip3 install dash_bio==1.0.1
```

3: Run local python server in your terminal:

```
python -m http.server --directory static
```

4: Run interactiveGraphing application the next terminal tab:

```
python start.py
```

5: Open your favorite web browser, paste `http://localhost:8000` or `http://[::]:8000/` on the URL bar, and enjoy the interactive analysis of your Big Data.
