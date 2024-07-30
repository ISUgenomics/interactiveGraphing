
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


# TEMPORARY INLINE CSS STYLES

css_lpd = {'display':'inline-block', 'background-color':'#D6F2FA', 'border-right': '1px solid #008CBA', 'overflow-y':'auto', 'overflow-x':'hidden', 'height':'95vh', 'padding':'5px'}
css_rpd = {'display':'inline-block', 'background-color':'ghostwhite', 'padding':'20px', 'overflow-y':'auto', 'overflow-x':'hidden', 'height':'95vh', 'flex-grow': '1', 'width':'0'}
css_btn = {'font-size':'20px', 'background-color':'#008CBA', 'color':'white', 'border':'1px solid #006B88', 'border-radius':'8px', 'marginBottom':'10px'}

css_lab = {'font-style':'italic', 'padding-right':'0', 'font-size':'16px', 'color':'#008CBA'}
drop50 = {'display':'inline-block', 'height':'34px', 'width':'50%'}
drop33 = {'display':'inline-block', 'height':'34px', 'width':'33%'}