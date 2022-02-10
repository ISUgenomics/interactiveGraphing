# -*- coding: utf-8 -*-
import os
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

from app import app

#colorscales
cs_seq = [[0, "#c6ff1a"], [0.05, "#c6ff1a"], [0.05, "#ffff00"], [0.1, "#ffff00"], [0.1, "#ffcc00"], [0.15, "#ffcc00"], [0.15, "#ff944d"], [0.2, "#ff944d"], [0.2,"#ff6600"], [0.25,"#ff6600"], [0.25, "#e62e00"], [0.3, "#e62e00"], [0.3, "#cc0000"], [0.35, "#cc0000"], [0.35, "#b30059"], [0.4, "#b30059"], [0.4, "#ff0080"], [0.45, "#ff0080"], [0.45, "#ff00ff"], [0.5, "#ff00ff"], [0.5, "#bf00ff"], [0.55, "#bf00ff"], [0.55, "#8000ff"], [0.6, "#8000ff"], [0.6, "#262673"], [0.65, "#262673"], [0.65, "#4000ff"], [0.7, "#4000ff"], [0.7, "#0080ff"], [0.75, "#0080ff"], [0.75, "#00bfff"], [0.8, "#00bfff"], [0.8, "#00ffff"], [0.85, "#00ffff"], [0.85, "#00e6ac"], [0.9, "#00e6ac"], [0.9, "#009900"], [0.95, "#009900"], [0.95, "#004d00"], [0.999, "#004d00"], [1, "#cccccc"]]	#20AA: A, C, D, E, 
cs_blues = [[0, "#ffffff"], [0.05, "#f6fdff"], [0.10, "#e6f9ff"], [0.20, "#b4e6f4"], [0.3, "#82d2ea"], [0.4, "#1DACD6"], [0.5, "#1680ba"], [0.6, "#1060a5"], [0.7, "#0b4090"], [0.8, "#000066"], [0.9, "#000029"], [1, "rgb(0,0,0)"]]

#colorhash
acids={'-': 1, 'X': 1, 'W': 0, 'F': 0.05, 'Y': 0.1, 'N': 0.15, 'Q': 0.2, 'D': 0.25, 'E': 0.3, 'S': 0.35, 'T': 0.4, 'H': 0.45, 'K': 0.5, 'R': 0.55, 'L': 0.6, 'I': 0.65, 'V': 0.7, 'A': 0.75, 'G': 0.8, 'M': 0.85, 'C': 0.9, 'P': 0.95}

#descriptionhash
amino={'-': 'deletion', 'X': 'X', 'A': "ALA", 'C': "CYS", 'D': "ASP", 'E': "GLU", 'F': "PHE", 'G': "GLY", 'H': "HIS", 'I': "ILE", 'K': "LYS", 'L': "LEU", 'M': "MET", 'N': "ASN", 'P': "PRO", 'Q': "GLN", 'R': "ARG", 'S': "SER", 'T': "THR", 'V': "VAL", 'W': "TRP", 'Y': "TYR"}
d_ter={'-': 'deletion', 'X': 'any','0': 'ordered', '1': 'disorder < 0.75', '2': 'disorder > 0.75'}
d_bin={'-': 'deletion', 'X': 'any', '0': 'ordered', '1': 'disordered'}

tool_dict = {'spot': 'SPOTCON', 'raptor': 'RAPTOR', 'respre.SP': 'RESPRE (SwissProt)', 'respre.50': 'RESPRE (UniProt50)', 'respre.90': 'RESPRE (UniProt90)'}
AA=['W', 'F', 'Y', 'N', 'Q', 'D', 'E', 'S', 'T', 'H', 'K', 'R', 'L', 'I', 'V', 'A', 'G', 'M', 'C', 'P']
uniprot_ids = []
tool_db = {}
path=os.getcwd()+'/static/data/heatmap/contacts/'

with open(path+'uniprot_ids','r') as f:
  for row in f:
    uniprot_ids.append(row.strip())
with open(path+'files', 'r') as f2:
  for row in f2:
    tokens = row.split('.')
    if not tokens[0] in tool_db.keys():
      tool_db[tokens[0]] = []
    if len(tokens) == 3:
      tool_db[tokens[0]].append(str(tokens[1]))
    else:
      tool_db[tokens[0]].append(str(tokens[1])+'.'+str(tokens[2]))

layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Select UniProt ID', className="labs"),
            dcc.Dropdown(id='uniprot_id', placeholder="Select UniProt ID", clearable=False, className="drops",
                options=[{'label': i, 'value': i} for i in uniprot_ids], value='A0A0G2UHG9')], className="drops1",),
        html.Div([
            html.Label('Select Contact Prediction Tool', className="labs labs2"),
            dcc.Dropdown(id='tool_con', placeholder="Select prediction method", clearable=False, className="drops",
                options=list({'label': tool_dict[i], 'value': i} for i in tool_db['A0A0G2UHG9']), value='raptor')], className="drops2",),
    ]),
    html.Div([
        dcc.Loading(id='loading-composition', children=[html.Div(dcc.Graph(id='graph6', className="graph", 
            config={'toImageButtonOptions': {'format':'png', 'width':1400, 'height':800, 'scale':1.5}, 'responsive': True,},))], type='circle'),
    ], className="graph-parent"),
])

@app.callback(Output('tool_con', 'options'), [Input('uniprot_id', 'value')])
def update_contact_options(uniprot_id):
    return list({'label': tool_dict[i], 'value': i} for i in tool_db[uniprot_id])

@app.callback(Output('tool_con', 'value'), [Input('uniprot_id', 'value'), Input('tool_con', 'options')])
def update_val_con(uniprot_id, tools):
    return tools[0]['value']

@app.callback(Output('graph6', 'figure'), [Input('uniprot_id', 'value'), Input('tool_con', 'value')])
def update_graph_con(uniprot_id, tool):

    data_con = pd.read_csv(path+str(uniprot_id)+"."+tool+".csv")
    data_con = data_con[data_con.value >= 0.01]
    p=''
    if tool.split('.')[0] == 'respre':
      p=str(path+str(uniprot_id)+"."+tool+".seq")
    else:
      p=str(path+str(uniprot_id)+".seq")
    seq=pd.read_csv(p)

    data_seq = list(acids[str(i).upper()] for i in seq['res'])
    desc_seq = list(str(str(num+1)+", deletion") if str(i)=='-' else (str(amino[str(i).upper()]+" "+str(num+1)+", deletion") if str(i).islower() else str(amino[i]+" "+str(num+1))) for num,i in enumerate(seq['res']))
    trace3 = go.Bar(x=seq['id'], y=[2]*len(seq['id']), text=desc_seq, name='amino acid', hoverinfo="text+name", marker=dict(cmin=0.00, cmax=0.99, color=data_seq, colorscale=cs_seq,
        colorbar=dict(title='SEQ', len=0.9, x=0.57, y=0.44, tickvals=[0.02, 0.07, 0.12, 0.17, 0.22, 0.27, 0.32, 0.37, 0.42, 0.47, 0.52, 0.57, 0.62, 0.67, 0.72, 0.77, 0.82, 0.87, 0.92, 0.97],
            ticktext=AA), showscale=True), showlegend=False, yaxis='y3', xaxis='x1')
    trace4 = go.Bar(x=[-1]*len(seq['id']), y=seq['id'], orientation='h', base=0, text=desc_seq, name='amino acid', hoverinfo="text+name", marker=dict(cmin=0.00, cmax=0.99, color=data_seq, 
        colorscale=cs_seq, showscale=False), showlegend=False, yaxis='y1', xaxis='x2')
    desc=list('contact: '+str(i)[0:4] for num,i in enumerate(data_con['value']))
    desc.extend(desc)
    trace1=go.Heatmap(x=data_con['id1'].append(data_con['id2']), y=data_con['id2'].append(data_con['id1']), z=data_con['value'].append(data_con['value']), text=desc, name=tool, hoverinfo="x+y+text+name", colorscale=cs_blues, zmin=0, zmax=1, yaxis='y1', xaxis='x1',
        colorbar=dict(title='CONTACTS', len=0.9, x=0.65, y=0.44, tickvals=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]))
    dataset = [trace4, trace3, trace1]
    return {
        'data': dataset,
        'layout': go.Layout(
            autosize=True,
            hovermode='closest',
            xaxis1=dict(tickfont = dict(size = 18), title = dict(text = '',), automargin = True, scaleanchor="y", scaleratio=1, domain=[0, 0.5], showline=True),
            xaxis2=dict(tickfont = dict(size = 18), automargin = True, domain=[0.5, 0.55], tickvals=[0], ticktext=[''], showticklabels=False),
            yaxis1=dict(tickfont = dict(size = 18), title = dict(text = 'position in a sequence', font=dict(color="black", size=24)), scaleanchor="x", scaleratio=1, domain=[0, 0.85], showline=True),
            yaxis3=dict(tickfont = dict(size = 18), tickmode='array', tickvals=[1], ticktext=[' SEQUENCE'], domain=[0.885, 0.96], showline=False, automargin = True),
            margin=dict(t=0,r=100),
            annotations=[dict(x=0.25, y=0, align="center", arrowcolor="rgba(0, 0, 0, 0)", arrowhead=0, arrowsize=0.3, ax=-0, ay=40, 
              bgcolor="rgba(0, 0, 0, 0)", font=dict(color="black", size=24), text="position in a sequence", yref='paper', xref='paper',)],
         )
    }

