from dash import html


tooltip = {
    'img-format':'select format of exported static image: png, svg, jpeg, webp, pdf, eps',
    'img-filename':'provide custom filename for exported static image',
    'img-height':'enter the expected height (in px) of exported static image ',
    'img-width':'enter the expected width (in px) of exported static image',
    'img-scale':'enter the expected scale ratio of exported static image ',
    
    'graph-title':'provide custom text for the graph title',
    'title-font':'customize title font: \n1) select font family, \n2) select font color, \n3) select font size',
    'title-position':'customize title position: \n1) graph title horizontal position, \n2) graph title vertical position',
    'graph-size':'provide size of an interactive graph in px: \n1) height, \n2) width',
    'graph-legend':'legend settings: \n1) if True the legend is visible, if False the legend is hidden, \n2) legend X position, \n3) legend Y position',
    'X-title':'provide custom text for the X-axis title',
    'Y-title':'provide custom text for the Y-axis title',
    'margin':'values (in px) for graph margins in order [left, top, right, bottom] \ntype "d" for the defaults',
    'bg-colors':'background colors: \n1) background color in the plottiong area, \n2) background color of the drawing area',
    'X-axis-font':'customize X-axis font: \n1) select font family, \n2) select font color, \n3) select font size',
    'X-line':'X-axis line: \n1) if True the X axis is visible, if False X axis is hidden, \n2) X line width in px, \n3) X line color',
    'X-mirror':'if True the X axis complementary mirror axis is visible [on the top/bottom of the graph]',
    'X-ticks':'X axis ticks (marks): \n1) position of X axis ticks: "outside", "inside", "" (not visible), \n2) color of X axis ticks, \n3) width (in px) of X axis ticks, \n4) length (in px) of X axis ticks',
    'X-tick-labels':'X axis ticks (labels): \n1) if True the labels of X axis ticks are visible, \n2) font color of ticks labels for X axis, \n3) font size of ticks labels for X axis, \n4) side of the graph where the ticks and labels will apear; enter "top" or "bottom", \n5) angle of X axis ticks in range 0 - 360, \n6) list of strings with tick labels for X axis; should match the number of data columns in the input file; if empty list, the keys (column names) from the header will be used',
    'Y-axis-font':'customize Y-axis font: \n1) select font family, \n2) select font color, \n3) select font size',
    'Y-title-pos':'position of the Y-axis title: \n1) Y axis title horizontal position; balow 0 - left side of the graph, above 1 - right side of the graph, \n2) Y axis title vertical position; usually value around 0.5 center title with the heatmap, \n3) the angle of the text: 0 is horizontal; -90 is vertical-left; 90 is vertical-right',
    'Y-line':'Y-axis line: \n1) if True the Y axis is visible, if False Y axis is hidden, \n2) Y line width in px, \n3) Y line color',
    'Y-mirror':'if True the Y axis complementary mirror axis is visible [on the top/bottom of the graph]',
    'Y-ticks':'Y axis ticks (marks): \n1) position of Y axis ticks: "outside", "inside", "" (not visible), \n2) color of Y axis ticks, \n3) width (in px) of Y axis ticks, \n4) length (in px) of Y axis ticks',
    'Y-tick-labels':'Y axis ticks (labels): \n1) if True the labels of Y axis ticks are visible, \n2) font color of ticks labels for Y axis, \n3) font size of ticks labels for Y axis, \n4) side of the graph where the ticks and labels will apear; enter "left" or "right", \n5) angle of Y axis ticks in range 0 - 360',
    'Y-labels-data':'custom Y-axis ticks: \n1) if True, text labels for the Y axis in the heatmap section can be dispalyed; otherwise an automatic numerical (data index) values will be dispalyed; \n2) name of the column in the input used for labeling ticks on the Y-axis for the heatmap section, \n3) number of ticks on the zoomed Y axis with text tick labels, \n4) specify the zoomed fragment along normalized Y axis; 0 - bottom, 1 - top; text labels switches off the interactive Y axis zooming - this variable can zoom the Y axis though;',

    'center-vals':'if True, center the values of the heatmap about zero',
    'display-cutoff':'standardized values below the negative of this value will be colored with one shade, and the values that are above this value will be colored with another',
    'color-scale':'colorscale for the heatmap: \nselect built-in Plotly color scale \n*use button to preview rendering of available color scales)',
    'colorbar':'heatmap colorbar settings: \n1) if True, the colorbar (heatmap colorscale) will be displayed, \n2) vertical length of the colorbar; default = 1 - dendro_ratio[0], means that the colorbar height matches the heatmap height, \n3) horizontal position of the colorbar; value above 1 places colorbar on the right margin of the plotting area, 4) vertical position of the center of the colorbar; default = 0.5*(1-dendro_ratio[0]), means that the colorbar will be aligned vertically with the heatmap',
    'label-name':'custom name displayed on the interactive labels for the heatmap points',
    'label-X':'label for X data displayed on the interactive label; \nby default the ticks of X axis will be used as data; \n"none" will switch off the option',
    'label-Y':'label for Y data displayed on the interactive label; \nby default the ticks of Y axis will be used as data; \n"none" will switch off the option',
    'label-Z':'label for Z data displayed on the interactive label; \nby default the heatmap (Z) values will be used as data; \n"none" will switch off the option',
    'label-custom':'name of the custom label; \nlabel element is any string;',
    'label-dimension':'dimension options are: "x", "y", "z"; \ndimension specifies the data structure;',
    'label-file':'filename with data for custom label; \nselect filename from the list of pre-loaded files; \n load additional files in the inputs section, if needed;',
    'label-data':'data is an array (1D for "x" or "y", 2D for "z") provided explicitly or as a string of the column name from the input file;',
    'label-font-size':'font size of interactive labels',
    'label-align':'horizontal alignment of the text content within on-hover label box; \nselect option: "left", "right", "auto"',
    
    'row-prefix':'custom name of the dendrogram clusters in rows',
    'col-prefix':'custom name of the dendrogram clusters in columns',
    'dendro-line':'line width [row, column] for the dendrograms',
    'dendro-linkage':'maximum linkage value [row, column] for which unique colors are assigned to clusters',
    'dendro-colors':'list of colors to use for different clusters in the dendrogram that have a root under the threshold for each dimension',
    'leaf-order':'determine leaf order that maximizes similarity between neighboring leaves',
    'scale-ratio':'proportions of dendrogram vs. cluster-bars and heatmap vs. dendrogram: \n1) scale ratio between dendrogram and cluster-bar sections, \n2) scale ratio between heatmap and X axis dendrogram, \n3) scale ratio between heatmap and Y axis dendrogram',
    'dendro-labels':'Interactive labels for dendrograms: \n1) whether to list all cluster elements on interactive labels for Y dendrogram, \n2) number of elements names listed per single line on interactive labels (prevents overly wide labels)',

    'export-html':'if True the generated interactive HTML graph will be automatically saved to file',
    
    'edit-': ['Initiates editing mode for a selected file:',html.Br(),'- Allows for interactive modifications to the files data within the app.',html.Br(),'- Each editing session is saved as a separate DataTable state, enabling multiple versions (e.g., #1, #2, etc.).'],
    'remove-': ['Removes a selected file from the applications memory:',html.Br(),'- Frees up memory space by discarding files that are no longer needed.',html.Br(),'- Once removed, the file must be re-uploaded for further use, as this action cannot be undone.'],
    'save-': ['Saving modified dataframe to files on disk:',html.Br(),'- Reduced memory usage, as data is offloaded to disk.',html.Br(),'- Persistent storage, which survives app restarts or crashes.',html.Br(),'- Slower to access data due to I/O operations.'],
    'cache-': ['Caching modified dataframe in session memory:',html.Br(),'- Fast access to data for analysis.',html.Br(),'- Modified dataframe retained in session after closing edit mode.',html.Br(),'- Higher memory usage with large datasets or many edited states.'],
    'close-': ['Closing edited DataTables to release memory:',html.Br(),'- Manually manage the data you no longer need.',html.Br(),'- Removes the edited DataTable state from memory.',html.Br(),'- This is essential for managing the apps memory footprint.'],
    'ncol-': ['Add new column:',html.Br(),'- Type a custom column name.',html.Br(),'- Click "+ column" to add it at the table start.'],
    'nrow-': ['Add new row:',html.Br(),'- Click "+ row" to insert it at the top of the table.'],
    'prune-': ['Remove rows with empty cells:',html.Br(),'- Click "prune" to delete rows with completely empty cells.',html.Br(),'- Select "any" then "prune" to delete rows with any empty cell.',html.Br(),'- Select columns and "any," then click "prune" to remove rows with empty cells in those columns.'],
    'listview-': ['The table will be styled like a list view and not have borders between the columns.'],
    'reset-': ['Reset the DataTable to the original state.'],
    'undo-': ['Reverse last change.'],
    
}


default_headers = {
    '.PAF' : ['query_name', 'query_length', 'query_start', 'query_end', 'target_name', 'target_length', 'target_start', 'target_end', 'target_strand', 'num_matching', 'alignment_block_length', 'mapping_quality'],     # synteny app, minimap2 output
}