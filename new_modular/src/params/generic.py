import plotly.express as px
from src.functions.widgets import generate_font_options, generate_color_options

# GENERIC DASH VARIABLES

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


