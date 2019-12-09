import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps import home, pokemon_episode, pokemon_routes, sentiment_analysis

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Pokemon-episode graph", href="/pokemon_episode")),
        dbc.NavItem(dbc.NavLink("Sentiment analysis", href="/apps/pokemon_routes")),
        dbc.NavItem(dbc.NavLink("Sentiment analysis", href="/apps/sentiment_analysis"))
    ],
    brand="Pokemon graphs and analysis",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return home.layout
    if pathname == '/pokemon_episode':
        return pokemon_episode.layout
    elif pathname == '/apps/pokemon_routes':
        return pokemon_routes.layout
    elif pathname == '/apps/sentiment_analysis':
        return sentiment_analysis.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)