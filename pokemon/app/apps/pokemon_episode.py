import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import re
from . import *
from app import app

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

