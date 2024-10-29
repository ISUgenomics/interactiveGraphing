from dash import html, dcc

layout = html.Div([
    html.H2("Interactive Graphing for Bioinformatics"),
    html.P("""This application is designed to provide researchers and scientists 
        with powerful tools for analyzing and visualizing complex biological data."""),
    html.P("""Key features of this platform include:"""),
    html.Ul([
        html.Li("Comprehensive data upload and preprocessing capabilities."),
        html.Li("Flexible and customizable analysis settings."),
        html.Li("Advanced visualization options for various types of biological data."),
        html.Li("Interactive dashboards to explore and interpret results."),
        html.Li("Support for a wide range of bioinformatics pipelines."),
    ]),
    dcc.Markdown("""
        We are committed to providing a user-friendly and intuitive interface, 
        making it accessible for both beginners and experienced bioinformaticians.    
        Our goal is to facilitate the discovery process and help you achieve your research objectives 
        more efficiently.
    """),
    html.H4("""
        Happy Analyzing!
    """)
], id='info-mode', className="pt-3 px-5")
