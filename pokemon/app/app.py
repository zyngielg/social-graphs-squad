import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import networkx as nx
from pokemon_episodes_graph import generate_generation_graph, get_generations_dict
from dash.dependencies import Input, Output
from textwrap import dedent as d
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

def random_graph(no_nodes = 200, edge_percent = 0.125):
    return nx.random_geometric_graph(no_nodes, edge_percent)


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
        #edge_trace['x']+=(x_tuple)
        #edge_trace['y']+=(y_tuple)
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
            #xaxis=dict(range=[0, 1]),
            #yaxis=dict(range=[0, 1])
        )
    )
    return fig


def get_graph_figure(gen_number):
    generations = get_generations_dict()
    G = generate_generation_graph(generations[gen_number])
    positions = nx.random_layout(G)
    #for item in positions.values():
        #item[0] *= 5
        #item[1] *= 5
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
    g, f = get_graph_figure(i+1)
    graphs.append(g)
    figures.append(f)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(dcc.Graph(id='Graph')),
    #html.Div(
    #    className='row',
    #    children=[
    #        html.Div([
    #            html.H2('Overall Data'),
    #            html.P('Num of nodes: ' + str(len(g1.nodes))),
    #            html.P('Num of edges: ' + str(len(g2.edges)))
    #        ],
    #        className='three columns'),
    #        html.Div([
    #            html.H2('Selected Data'),
    #            html.Div(id='selected-data'),
    #        ],
    #        className='six columns')
    #    ]
    #),
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
    html.Div([
        dcc.Markdown(d("""
            **Click Data**

            Click on points in the graph.
        """)),
        html.Pre(id='click-data', style=styles['pre']),
    ], className='three columns'),
])

@app.callback(
    Output('Graph', 'figure'),
    [Input('season-slider', 'value')])
def update_figure(selected_season):
    return figures[selected_season-1]

@app.callback(
    Output('click-data', 'children'),
    [Input('Graph', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)