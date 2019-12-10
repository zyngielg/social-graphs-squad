import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d

from app import app

layout = html.Div([
    #html.H1('Home'),
    dcc.Markdown(d("""
        # Pokemon social graph and analysis
        
        ## Aim
        
        The aim of this project was to create social graphs associated with data fetched from the Bulbapedia website,
        use the graph analysis and NLP techniques learnt during the class and come up with some meaningful, interesting
        analysis of it.
        
        ## Dataset
        The dataset consists of X pokemon files, Y episode files, Z MB combined
        
        ## Workflow description
        The following list describes the worflow for this project:
        
        1. Fetch the data from Bulbapedia.
        2. Create three sections for the analysis:
            - pokemon-episodes graph
            - pokemon-routes graph
            - sentiment analysis of pokemons belonging to the same **Type** category
        3. Create a website using **Plotly Dash**.
        
        ## Page navigation
        
        To display each section of the report, please select the corresponding title on the navigation bar, on the top
        of the website.
        
        To navigate back to this Home page, please select the navigation bar title (left part).
        
        ## Graphs traits
        
        The generated graphs are **interactive** graphs. It is possible to:
        - display more information about the single/multiple nodes by:
            - hovering over single node
            - clicking on the single node
            - selecting multiple nodes with the lasso/box tools (top right corner of the graph)
        - zoom in and zoom out by:
            - pressing + and - buttons in the graph tools
            - double clicking on the graph (default zoom in, followed by zoom out)
            - selecting an area with a mouse to zoom in
        - move throughout the graph by holding Shift, left mouse button and by hovering the mouse
        multiple nodes with the 
        
        ## Group members
        * Riley Goodling
        * Ali Saleem
        * Gustaw Żyngiel
    """))
])