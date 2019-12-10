import re
import os
import itertools
import networkx as nx
from IPython.display import clear_output
import numpy as np
import matplotlib.pyplot as plt

pokemon_dir = "./pokemon_gen1/"
pokemon_names = sorted(os.listdir("pokemon_gen1/"))
pokemon_names.remove("[151]Mew")

def get_game_dict():
    games = {
    1: {
        "name": "Yellow"
    },
    2: {
        "name": "Crystal"
    },
    3: {
        "name": "FireRed"
    },
    4: {
        "name": "Platinum"
    }
    }

    return games


def get_gamelocations_dict(game):
    all_occurances = {}
    location_list = set()
    raw_locations = {}
    removables = ["Routes", "Route", "Evolution|Evolve"]

    for pokemon in pokemon_names:
        poke_path = pokemon_dir + pokemon
        poke_file = open(poke_path, encoding='utf-8').read()
        pokemon_text = re.findall(r"(?<=Game locations===)(.*)(?=In side games)", poke_file)
        poke_VandA = re.findall(r"(v=)(.*?)\\\\n", str(pokemon_text))
        for x in poke_VandA :
            if pokemon not in raw_locations:
                raw_locations[pokemon] = [x[1]]
            else:
                raw_locations[pokemon].append(x[1])
    for pokemon, version in raw_locations.items():
        places = set()
        for x in version:
            v1 = re.findall(r".+?(?=\|)", str(x))
            if len(v1) > 0:
                v1 = v1[0]
            else:
                v1 = re.findall(r".+?(?=\})", str(x))
                v1 = v1[0]
            if v1 == game:
                x = x.replace("[", "{")
                x = x.replace("]", "}")
                loc = re.findall(r"(?<=\{\{)(.*?)(?=\}\})", str(x))
                for place in loc:
                    if "List" in place:
                        place = "Special Event"
                    elif place[:2] == 'p|':
                        continue
                    elif "Surf" in place or "surf" in place:
                        place = "Surfing"
                    if place[:3] == 'rtn':
                        place = place.replace('rtn', 'rt', 1)
                    places.add(place)
                    location_list.add(place)
        if places == set():
            pokemon_names.remove(pokemon)
        if ('Evolution|Evolve') in places:
            pokemon_names.remove(pokemon)
            continue
        if "Route" in places:
            places.remove("Route")
        if "Routes" in places:
            places.remove("Routes")
        all_occurances[pokemon] = places
    
    for word in removables:
        if word in location_list:
            location_list.remove(word)
    
    return all_occurances, location_list


def generate_games_graph(games):
    all_occurances, location_list = get_gamelocations_dict(games["name"])

    G = nx.Graph()
    G.add_nodes_from(pokemon_names)
    G.add_nodes_from(location_list)

    for name, locations in all_occurances.items():
        for place in locations:
            G.add_edge(name, place)
    
    color_map = []
    for x in G.nodes():
        if x in location_list:
            color_map.append('rgb(0,240,0)')
        else:
            color_map.append('rgb(192, 143, 227)')

    return G, color_map


def print_graph_stats(G):
    print(f"Number of graph's nodes: {len(G.nodes)}")
    print(f"Number of graph's edges: {len(G.edges)}")
    print(f"Average node degree: {np.mean([x[1] for x in G.degree])}")
    pokemon_wo_edges = [x for x in G.nodes if G.degree(x) == 0]
    print(f"Number of Pokemon without any connections: {len(pokemon_wo_edges)}")


def draw_graph_matplotlib(generations, gen_number, G):
    plt.figure(figsize=(60,60))
    random_pos = nx.random_layout(G)
    nx.draw_networkx_nodes(G, pos=random_pos, node_size = 300, node_color="blue")
    nx.draw_networkx_edges(G, pos=random_pos, edge_color= 'grey', width = 0.25 )

def get_node_names(G):
    nodes = list(G.nodes())

    for node in range(len(nodes)):
        if (re.search(r"rt\|(\d*?)\|Kanto", nodes[node])):
            number = re.findall(r"rt\|(\d*?)\|Kanto", nodes[node])[0]
            nodes[node] = nodes[node].replace(nodes[node], f"Kanto Route {number}")
        elif (nodes[node] == 'Evolution|Evolve'):
            nodes[node] = "Evolution"
        elif (nodes[node] == 'In-game trade#Yellow|Trade'):
            nodes[node] = "Trade for"
        elif ("List" in nodes[node]):
            nodes[node] = "Special Event"
        elif (nodes[node] == 'Fishing#In the games|Super Rod'):
            nodes[node] = "Fishing"
        elif (nodes[node] == 'tt|*|immediately evolves into Machamp, but Pokédex data is entered'):
            nodes[node] = "Immediately evolves"
        elif (nodes[node] == "Diglett\\\\'s Cave"):
            nodes[node] = "Deglett's Cave"
        elif ("|" in nodes[node]):
            nodes[node] = nodes[node].replace("|", " ")  

    return nodes 