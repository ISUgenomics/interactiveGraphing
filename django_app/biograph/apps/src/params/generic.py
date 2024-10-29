import plotly.express as px
from src.functions.widgets import generate_font_options, generate_color_options

# GENERIC DASH VARIABLES
PARAMS = {'graph-title':'layout.title.text', 'graph-height':'layout.height', 'graph-width':'layout.width',
          'X-title': 'layout.xaxis.title.text', 'Y-title': 'layout.annotations.0.text',
          'graph-legend': 'layout.showlegend', 'legend-X': 'layout.legend.x', 'legend-Y': 'layout.legend.y',
          'margin-l': 'layout.margin.l', 'margin-t': 'layout.margin.t', 'margin-r': 'layout.margin.r', 'margin-b': 'layout.margin.b',
          'plotting-c': 'layout.plot_bgcolor', 'drawing-c': 'layout.paper_bgcolor',
          'title-size': 'layout.title.font.size', 'title-font': 'layout.title.font.family', 'title-color': 'layout.title.font.color',
          'title-posX': 'layout.title.x', 'title-posY': 'layout.title.y',
          'X-axis-font': 'layout.xaxis.title.font.family', 'X-axis-color': 'layout.xaxis.title.font.color', 'X-axis-size': 'layout.xaxis.title.font.size',
          'X-line': 'layout.xaxis.showline', 'X-line-color': 'layout.xaxis.linecolor', 'X-line-width': 'layout.xaxis.linewidth', 'X-mirror': 'layout.xaxis.mirror',
          'X-ticks': 'layout.xaxis.ticks', 'X-ticks-color': 'layout.xaxis.tickcolor', 'X-ticks-width': 'layout.xaxis.tickwidth', 'X-ticks-len': 'layout.xaxis.ticklen',
          'X-tick-labels': 'layout.xaxis.showticklabels', 'X-tick-font-color': 'layout.xaxis.tickfont.color', 'X-tick-font-size': 'layout.xaxis.tickfont.size',
          'X-tick-font-pos': 'layout.xaxis.side','X-tick-font-angle': 'layout.xaxis.tickangle', 'X-tick-labels-list': 'layout.xaxis.ticktext',
          'Y-axis-font': 'layout.annotations.customY.font.family', 'Y-axis-color': 'layout.annotations.customY.font.color', 'Y-axis-size': 'layout.annotations.customY.font.size',
          'Y-axis-angle': 'layout.annotations.customY.textangle', 'Y-axis-posX': 'layout.annotations.customY.x', 'Y-axis-posY': 'layout.annotations.customY.y',
          'Y-line': 'layout.yaxis.showline', 'Y-line-color': 'layout.yaxis.linecolor', 'Y-line-width': 'layout.yaxis.linewidth', 'Y-mirror': 'layout.yaxis.mirror',
          'Y-ticks': 'layout.yaxis.ticks', 'Y-ticks-color': 'layout.yaxis.tickcolor', 'Y-ticks-width': 'layout.yaxis.tickwidth', 'Y-ticks-len': 'layout.yaxis.ticklen',
          'Y-tick-labels': 'layout.yaxis.showticklabels', 'Y-tick-font-color': 'layout.yaxis.tickfont.color', 'Y-tick-font-size': 'layout.yaxis.tickfont.size',
          'Y-tick-font-pos': 'layout.yaxis.side','Y-tick-font-angle': 'layout.yaxis.tickangle'}
# 'Y-labels-data', 'Y-labels-col', 'Y-labels-number', 'Y-labels-zoom-from', 'Y-labels-zoom-to'


COLORS = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 
          'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 
          'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 
          'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 
          'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 
          'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 
          'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 
          'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 
          'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 
          'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 
          'magenta', 'maroon', 'mediumaquamarine', 'ediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 
          'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 
          'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 
          'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 
          'rebeccapurple', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 
          'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 
          'white', 'whitesmoke', 'yellow', 'yellowgreen']


COL_PROPS={'renamable':True, 'editable':True, 'hideable':True, 'selectable':True, 'clearable':True, 'deletable':True}


FONTS = ["Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", 
         "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"]


CHECK = [{'label': 'YES', 'value': True}]


TICKS = [{'label': 'outside', 'value': 'outside'}, {'label': 'inside', 'value': 'inside'}, {'label': '(not visible)', 'value': ''}]

CONFIG = {'responsive': True, 'showTips': True, 
          'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape', 'resetViews', 'toggleHover', 'toggleSpikelines'],
          'toImageButtonOptions': {'format': 'svg', 'filename': 'clustergram', 'height': 1100, 'width': 1100, 'scale': 2}}


# Function-generated variables

FONT_OPTS = generate_font_options(FONTS)
COLOR_OPTS = generate_color_options(COLORS)

CS_OPTS = px.colors.named_colorscales()
CS_SEQ = px.colors.sequential.swatches_continuous().update_layout(width=350)
CS_DIV = px.colors.diverging.swatches_continuous().update_layout(width=350)
CS_CYC = px.colors.cyclical.swatches_continuous().update_layout(width=350)




