import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_table
import random
import pandas as pd
import numpy as np

from app import app, sample_datasets, DF, PROJECT, PROJECTS, server

colorscale={ 6: '#ff0000', 5: '#fb1b1b', 4: '#f93333', 3: "#f95b5b", 2: '#f98080', 1: "#ffc4c4" }
colors = ["#396AB1", "#DA7C30", "#3E9651","#CC2529","#535154","#6B4C9A","#922428","#948B3D"]

GRAPH_TYPES = ["scatter","bar"]

for project in PROJECTS:
    @app.callback(Output(f"table-{project}-inside-table-div", 'data'), [
    Input(f"dropdown-{project}-inside-table-div", 'value'),
    Input(f"table-{project}-inside-table-div", 'page_current'),
    Input(f"table-{project}-inside-table-div", 'page_size'),
    Input(f"table-{project}-inside-table-div", 'sort_by'),
    ])
    def select_rows(rows, page_current, page_size, sort_by):
        # get data from global DF
        df_new = DF if rows=="ALL" else  DF.iloc[ int(rows.split(":")[0]) : int(rows.split(":")[1]) , :]
        dff = df_new if not len(sort_by) else df_new.sort_values( sort_by[0]['column_id'],ascending=sort_by[0]['direction'] == 'asc', inplace=False )
        return  dff.iloc[ page_current*page_size:(page_current+ 1)*page_size ].to_dict('records')

for project in PROJECTS:
    @app.callback(Output(f"graph-{project}", 'figure'), [
    Input(f"dropdown-graph-range-{project}-inside-table-div", 'value'),
    Input(f"dropdown-graph-y-{project}-inside-table-div", 'value'),
    Input(f"dropdown-graph-x-{project}-inside-table-div", 'value'),
    Input( f"dropdown-graph-type-{project}-inside-table-div", 'value'),
    ])
    def draw_graph(rows, y, x, graph_type):
        df_new = DF if rows=="ALL" else  DF.iloc[ int(rows.split(":")[0]) : int(rows.split(":")[1]) , :]
        traces = []
        if graph_type=="scatter":
            traces.append(
                go.Scatter(
                    line = {"color": random.choice(colors),},
                    mode = "markers",
                    name = f" {x} vs {y} ",
                    type = "scatter",
                    x = df_new[x],
                    y = df_new[y],
                    xaxis = "x",
                    yaxis = "y",
                    # showlegend=True,
                    marker_color=df_new[y],
                    marker=dict(
                            # size=16,
                            # color=np.random.randn(500), #set color equal to a variable
                            colorscale='Bluered_r',#Inferno Viridis Bluered_r# one of plotly colorscales
                            showscale=True
                        ),
                    )
                )
        elif graph_type=="bar":
            traces.append(
                go.Bar(
                    name = f" {x} vs {y} ",
                    x = df_new[x],
                    y = df_new[y],
                    xaxis = "x",
                    yaxis = "y",
                    width=1,
                    hoverinfo="y",
                    showlegend=True,
                    # marker_color=df_new[y],
                    # marker=dict(
                    #         colorscale='Bluered_r',#Inferno Viridis Bluered_r# one of plotly colorscales
                    #         showscale=True
                    #     ),
                    )
                )
        return {"data": traces,
            "layout": dict(
                title=f" {x} vs {y} ",
                titlefont=dict(color="#ff7f0e"),
                colorway=['#fdae61', '#abd9e9', '#2c7bb6',],
                yaxis=dict(showgrid =False, title = y),
                xaxis=dict(showgrid=False,title =x),
                # font = dict(color="#7FDBFF"),
                )
            }

#====================
#Main Layout
#====================
app.layout = html.Div( children=[

    html.H3(
        children='DASH - PLOTLY',
        style={'textAlign': 'center'},
        className = 'dashboard-title',
        ),

    html.Div([
        dbc.Row([
            dbc.Col([
                    html.Label('Select Dataset'),
                    dcc.Dropdown(
                        id="dropdown-projectidentifier",
                        value = PROJECTS[10],
                        options = [{"label":i, "value": i} for i in PROJECTS ]
                        ),
                    ],width=3, style={"width":"25%",},
                ),
            ],style={"width":"100%",},
            ),

    ], style={'width':"100%"}),

    html.Div([ ],id="table-div" , style={'width':"100%"}),

    # # =====================
    # #         Tabs
    # # =====================
    # html.H3(children='TABS',style={ 'textAlign': 'center', }),
    # dcc.Tabs(id="tabs", value='tab1', children=[
    #     dcc.Tab(label='TAB1', value='tab1',
    #         className = 'main_tab'),
    #     dcc.Tab(label='TAB2', value='tab2',
    #         className = 'main_tab'),
    #     dcc.Tab(label='TAB2', value='tab3',
    #         className = 'main_tab'),
    # ],),
    # html.Div(id='tabs-content'),

], style={"padding":"1%", "background":"aliceblue"})


@app.callback(
    Output('table-div', 'children'),
    [Input('dropdown-projectidentifier', 'value'),
    ])
def select_project(project):
    global DF , PROJECT
    PROJECT = project
    DF = pd.read_csv(sample_datasets.get(project))

    optionlist =[{"label":"ALL","value":"ALL"}]+[{"label":str(i+1)+" to "+str(i+50), "value": str(i)+":"+str(i+50) } for i in range(0,DF.shape[0],50) ]
    optioncolslist = [{"label":str(i).upper(), "value": str(i) } for i in DF.columns ]
    optionrangelist = [{"label":"ALL","value":"ALL"}]+[{"label":str(i+1)+" to "+str(i+500), "value": str(i)+":"+str(i+500) } for i in range(0,DF.shape[0],500) ]
    optiongraphtypelist = [{"label":str(i).upper(), "value": str(i) } for i in GRAPH_TYPES ]
    return [
            html.H3(
                children=f'Loaded Dataset : {project}',
                style={'textAlign': 'center'},
                className = 'sub-title',
            ),
            dbc.Row([
                dbc.Col([
                        html.Label('Filter Rows '),
                ],width=3,),

                dbc.Col([
                    dcc.Dropdown(
                        id=f"dropdown-{project}-inside-table-div",
                        value=optionlist[0]["value"],
                        options = optionlist
                        ),
                ],width=3, style={"width":"25%",},),

            ],style={"width":"100%","display":"flex","justify-content":"flex-end", "text-align":"center","align-items":"center"},
            ),

            dash_table.DataTable(
                id=f"table-{project}-inside-table-div",
                columns=[{"name": i.upper(), "id": i} for i in DF.columns],
                data=DF.head().to_dict('records'),
                # style_as_list_view=True,
                sort_action='custom',
                sort_mode='single',
                sort_by=[],
                page_current=0,
                page_size=10,
                page_action='custom',
                style_table={'overflowX': 'scroll'},
                style_header={'backgroundColor': 'rgb(30, 30, 30)', "text-align":"center"},
                style_cell={
                    'backgroundColor': 'rgb(100, 100, 100)',
                    'color': 'white',
                    "text-align":"center"
                },
            ),

        dbc.Row([
        html.H3(
                children=f'Sample Graph for features of : {project}',
                style={'textAlign': 'center'},
                className = 'sub-title',
            ),
        ], style={"margin-top":"5%"}),

        dbc.Row([
                dbc.Col([
                    html.Label('GraphType'),
                    dcc.Dropdown(
                        id=f"dropdown-graph-type-{project}-inside-table-div",
                        value="scatter",
                        options = optiongraphtypelist
                        ),
                ],width=6,
                style={"width":"100%",},
                ),
                dbc.Col([
                    html.Label('Range'),
                    dcc.Dropdown(
                        id=f"dropdown-graph-range-{project}-inside-table-div",
                        value=optionrangelist[0]["value"],
                        options = optionrangelist
                        ),
                ],width=6,
                style={"width":"100%",},
                ),
                dbc.Col([
                    html.Label('X : '),
                    dcc.Dropdown(
                        id=f"dropdown-graph-x-{project}-inside-table-div",
                        value=optioncolslist[0]["value"],
                        options = optioncolslist
                        ),
                ],width=6,
                style={"width":"100%",},
                ),
                dbc.Col([
                    html.Label('Y : '),
                    dcc.Dropdown(
                        id=f"dropdown-graph-y-{project}-inside-table-div",
                        value=optioncolslist[2]["value"],
                        options = optioncolslist
                        ),
                ],width=6, 
                style={"width":"100%",},
                ),

            ],style={"width":"100%","display":"flex","justify-content":"flex-end", "text-align":"center","align-items":"center"},
            ),
        dcc.Graph(id=f'graph-{project}', responsive=True),

    ]

# @app.callback(Output('tabs-content', 'children'),
#     [Input('tabs', 'value')])
# def render_content(tab):
#     if tab == 'tab1':
#         return html.Div(
#                 children=[
#                     html.Label("tab 1"),
#                     html.Div([ ],id="table-div" , style={'width':"100%"}),
#                 ],style={"width":"100%"}
#             ),
#     elif tab == 'tab3':
#         optioncolslist = [{"label":str(i).upper(), "value": str(i) } for i in DF.columns ]
#         optionrangelist = [{"label":"ALL","value":"ALL"}]+[{"label":str(i+1)+" to "+str(i+500), "value": str(i)+":"+str(i+500) } for i in range(0,DF.shape[0],500) ]
#         return html.Div(
#                 children=[
#                     html.Label("tab 2"),
#                     dbc.Row([
#                 dbc.Col([
#                     html.Label('Range'),
#                     dcc.Dropdown(
#                         id=f"dropdown-graph-range-{project}-inside-table-div",
#                         value=optionrangelist[0]["value"],
#                         options = optionrangelist
#                         ),
#                 ],width=6,
#                 style={"width":"100%",},
#                 ),
#                 dbc.Col([
#                     html.Label('X : '),
#                     dcc.Dropdown(
#                         id=f"dropdown-graph-x-{project}-inside-table-div",
#                         value=optioncolslist[0]["value"],
#                         options = optioncolslist
#                         ),
#                 ],width=6,
#                 style={"width":"100%",},
#                 ),

#                 dbc.Col([
#                     html.Label('Y : '),
#                     dcc.Dropdown(
#                         id=f"dropdown-graph-y-{project}-inside-table-div",
#                         value=optioncolslist[2]["value"],
#                         options = optioncolslist
#                         ),
#                 ],width=6, 
#                 style={"width":"100%",},
#                 ),

#             ],style={"width":"100%","display":"flex","justify-content":"flex-end", "text-align":"center","align-items":"center"},
#             ),
#         dcc.Graph(id=f'graph-{project}', responsive=True),
#                 ],style={"width":"100%"}
#             ),
#     elif tab == 'tab2':
#         return html.Div(
#                 children=[
#                     html.Label("tab 1"),
#                     html.Div([ ],id="table-div" , style={'width':"100%"}),
#                 ],style={"width":"100%"}
#             ),
# #====================
#LAUNCH APP
#====================
if __name__ == '__main__':
    app.run_server(debug=False,port=5000,host='0.0.0.0')
