import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

from app import PROJECT

layout = html.Div(
    children=[
        html.Label("tab 1"),
        
        dcc.Graph(id=f'graph-{PROJECT}', responsive=True),

    ],style={"width":"100%"}
),