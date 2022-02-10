# -*- coding: utf-8 -*-
import os
import pandas as pd
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bio as dashbio

from app import app


path = os.getcwd()+'/static/data/volcano/'
df = pd.read_csv(path+"volcano.csv")
uniprot_ids = df.GENE.tolist()

layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Some options 1', className="labs"),
            dcc.Dropdown(id='variable_1', placeholder="Select option", clearable=False, className="drops",
                options=[{'label': i, 'value': i} for i in uniprot_ids], value=uniprot_ids[0])], className="drops1",),
        html.Div([
            html.Label('Select point size', className="labs labs2"),
            dcc.Dropdown(id='variable_2', placeholder="Select option", clearable=False, className="drops",
                options=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], value=8)], className="drops2",),
    ], style={'display': 'inline-block'}),
    html.Div([
        html.Label('Select range', className="labs labs2"),
        dcc.RangeSlider(
            id='volcano-input',
            min=-3,
            max=3,
            step=0.05,
            marks={i: {'label': str(i)} for i in range(-3, 3)},
            value=[-0.5, 1], 
        ),
    ], style={'width':'40vw', 'display':'inline-block', 'vertical-align': 'middle', 'margin-left':'5px'}),
    html.Div([
        dcc.Loading(id='loading-volcano', children=[html.Div(dcc.Graph(id='graph-volcano', className="graph", 
            config={'toImageButtonOptions': {'format':'png', 'width':1400, 'height':800, 'scale':1.5}, 'responsive': True,},))], type='circle'),
    ], className="graph-parent"),
])


@app.callback(Output('graph-volcano', 'figure'),
              [Input('variable_1', 'value'), Input('variable_2', 'value'), Input('volcano-input', 'value')])
def plot_volcano(var1, var2, effects):


    fig = dashbio.VolcanoPlot(
        dataframe=df,
        genomewideline_value=2.5,
        effect_size_line=effects,
        effect_size="log2(FC)",
        p="raw.pval",
        snp="GENE",
        gene="GENE",
        logp=True,
        xlabel="effect size",
        ylabel="-log10(p)",
        point_size=var2,
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(255, 255, 255, 1)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
        font_color="rgba(0,0,0,1)",
        title=dict(text='',),
        margin=dict(t=0),
        autosize=True,
    )
    
    return fig
