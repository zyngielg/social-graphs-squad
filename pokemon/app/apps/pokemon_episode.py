import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import networkx as nx
from pokemon_episodes_graph import generate_generation_graph, get_generations_dict
from dash.dependencies import Input, Output
from textwrap import dedent as d
import re
import pandas as pd
from . import *
from app import app

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'overflowY': 'scroll'

    },
    'img': {
        'border': '10px solid',
        'padding': '15px',
        'textAlign': 'center',
        'display': 'block'
    },
    'centeredMarkdown': {
        'textAlign': 'center',
    }
}

df = pd.read_csv("../pokemon_data.csv")

'''
def create_edge_trace(G):
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    a = []
    b = []
    for i, edge in enumerate(G.edges()):
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        a.append(x0)
        a.append(x1)
        a.append(None)
        b.append(y0)
        b.append(y1)
        b.append(None)
        # edge_trace['x']+=(x_tuple)
        # edge_trace['y']+=(y_tuple)
    edge_trace['x'] = tuple(a)
    edge_trace['y'] = tuple(b)
    return edge_trace


def create_node_trace(G):
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))
    for i, node in enumerate(G.nodes()):
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    return node_trace


def add_color_and_hover_text(G, node_trace):
    # add color to node points
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = 'Name: ' + str(adjacencies[0]) + '<br># of connections: ' + str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])


def create_figure(node_trace, edge_trace):
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            height=1000,
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            # xaxis=dict(range=[0, 1]),
            # yaxis=dict(range=[0, 1])
        )
    )
    return fig


def get_graph_figure(gen_number):
    generations = get_generations_dict()
    G = generate_generation_graph(generations[gen_number])
    positions = nx.random_layout(G)
    # for item in positions.values():
    # item[0] *= 5
    # item[1] *= 5
    nx.set_node_attributes(G, positions, 'pos')
    node_trace = create_node_trace(G)
    edge_trace = create_edge_trace(G)
    add_color_and_hover_text(G, node_trace)
    fig = create_figure(node_trace, edge_trace)

    return G, fig

seasons = get_generations_dict()
graphs = []
figures = []
for i in range(len(seasons)):
    g, f = get_graph_figure(i + 1)
    graphs.append(g)
    figures.append(f)
'''

layout = html.Div([
    dcc.Markdown(d("""
        # Pokemon-episode graph
        
        Here we write some generic description of this graph (and other stuff).
        
        - using bullet points
        - and stuff
        
        Writing like *this* or **this** or like `this`.
        
        or
        ```py
        def like_this():
            print("Guys use this")
        ```
        
        # HOWEVER
        for layout purposes we also might be using HTML tags instead.
    """), style={'padding': '20px'}),
    html.Div(dcc.Graph(id='Graph')),
    dcc.Slider(
        id='season-slider',
        min=1,
        max=7,
        value=1,
        marks=
        {
            key: seasons[key]["name"] for key in seasons.keys()
        },
        step=None
    ),
    html.Div(className='row', children=[

        html.Div([
            dcc.Markdown(d("""
            **Click Data**

            Click on points in the graph.
        """), style=styles['centeredMarkdown']),
            html.Pre(id='click-data', style=styles['pre']),

        ], className='four columns'),
        html.Div([
            dcc.Markdown(d("""
                **Click Data Image**

                Displays image of the clicked node's pokemon
            """)),
            html.Img(id='image', style=styles['img'])
        ], className='four columns'),
        html.Div([
            dcc.Markdown(d("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.
            """)),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='four columns')
    ])
])

@app.callback(
    Output('Graph', 'figure'),
    [Input('season-slider', 'value')])
def update_figure(selected_season):
    return figures[selected_season - 1]


@app.callback(
    Output('image', 'src'),
    [Input('Graph', 'clickData')]
)
def display_img(clickData):
    name = ""
    if clickData is not None:
        text = clickData["points"][0]["text"]
        name = re.search(r"(?<=Name: )(.*)(?=<br>)", text)[0]
    url = f"https://img.pokemondb.net/artwork/{name.lower()}.jpg"
    return url


@app.callback(
    Output('click-data', 'children'),
    [Input('Graph', 'clickData')])
def display_click_data(clickData):
    result = ""
    if clickData is not None:
        text = clickData["points"][0]["text"]
        name = re.search(r"(?<=Name: )(.*)(?=<br>)", text)[0]
        sentiment = df[df["Pokémon"] == name]["Sentiment_stemmed"].values[0]
        generation = df[df["Pokémon"] == name]["Generation"].values[0]
        type = df[df["Pokémon"] == name]["Type"].values[0]
        result = f"""
Name: {name}
  Type: {type}
  Generation: {generation}
  Sentiment: {sentiment}
        """

        # no_connections = re.search(r"(?<=connections: )(.*)", text)[0]
    # return json.dumps(clickData, indent=2)
    return result


@app.callback(
    Output('selected-data', 'children'),
    [Input('Graph', 'selectedData')])
def display_selected_data(selectedData):
    result = ""
    if selectedData is not None:
        for point in selectedData["points"]:
            text = point["text"]
            name = re.search(r"(?<=Name: )(.*)(?=<br>)", text)[0]
            sentiment = df[df["Pokémon"] == name]["Sentiment_stemmed"].values[0]
            generation = df[df["Pokémon"] == name]["Generation"].values[0]
            type = df[df["Pokémon"] == name]["Type"].values[0]
            result += f"""
Name: {name}
  Type: {type}
  Generation: {generation}
  Sentiment: {sentiment}
            """

    return result

