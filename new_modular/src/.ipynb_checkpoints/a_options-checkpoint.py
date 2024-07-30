# C. OPTIONS Components assembly

opts = html.Div([
  dbc.Accordion([
    dbc.AccordionItem(opts_inputs, title="1. UPLOAD INPUTS", item_id="item-1"),
    dbc.AccordionItem(opts_analysis, title="2. ADJUST ANALYSIS SETTINGS", item_id="item-2"),
    dbc.AccordionItem(opts_graph, title="3. GENERAL GRAPH SETTINGS", item_id="item-3"),
    dbc.AccordionItem(opts_heatmap, title="A. CUSTOMIZE HEATMAP", item_id="item-4"),
    dbc.AccordionItem(opts_dendro, title="B. CUSTOMIZE DENDROGRAMS", item_id="item-5"),
    dbc.AccordionItem(opts_bars, title="C. CUSTOMIZE CLUSTER BARS", item_id="item-6"),
    dbc.AccordionItem(opts_config, title="D. EXPORT GRAPH", item_id="item-7", class_name=".container"),
  ], id="accordion", start_collapsed=True, always_open=True, flush=False, style={'width':'25vw'}),
  html.Div(id="accordion-contents", className="mt-3"),
], id='optionsDiv')