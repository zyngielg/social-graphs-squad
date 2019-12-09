import re
import os
import itertools
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

episode_dir = "../episodes_files_raw/"
pokemon_list_file = "../pokemon list.txt"

def get_generations_dict():
    all_pokemon_names = open(pokemon_list_file, encoding='utf-8').read().split("\n")[:-1] # last element is empty line

    all_episodes = sorted(os.listdir(episode_dir))
    all_episodes_tags = [x[6:] for x in all_episodes]

    generations = {
    1: {
        "name": "The Beginning", 
        "debut_ep": "EP001", 
        "final_ep": "EP116",
        "episodes": [],
        "first_pokemon": 1,
        "last_pokemon": 151,
        "pokemons": []
    },
    2: {
        "name": "Gold and Silver", 
        "debut_ep": "EP117", 
        "final_ep": "EP274",
        "episodes": [],
        "first_pokemon": 152,
        "last_pokemon": 251,
        "pokemons": []
    },
    3: {
        "name": "Ruby and Sapphire", 
        "debut_ep": "AG001", 
        "final_ep": "AG192",
        "episodes": [],
        "first_pokemon": 252,
        "last_pokemon": 386,
        "pokemons": []
    },
    4: {
        "name": "Diamond and Pearl", 
        "debut_ep": "DP001", 
        "final_ep": "DP191",
        "episodes": [],
        "first_pokemon": 387,
        "last_pokemon": 493,
        "pokemons": []
    },
    5: {
        "name": "Black & White", 
        "debut_ep": "BW001", 
        "final_ep": "BW142",
        "episodes": [],
        "first_pokemon": 494,
        "last_pokemon": 649,
        "pokemons": []
    },
    6: {
        "name": "XY", 
        "debut_ep": "XY001", 
        "final_ep": "XY140",
        "episodes": [],
        "first_pokemon": 650,
        "last_pokemon": 721,
        "pokemons": []
    },
    7: {
        "name": "Sund & Moon", 
        "debut_ep": "SM001", 
        "final_ep": "SM146",
        "episodes": [],
        "first_pokemon": 722,
        "last_pokemon": 809,
        "pokemons": []
    },
    }

    for key, value in generations.items():
        first_poke = value["first_pokemon"] - 1
        last_poke = value["last_pokemon"]
        generations[key]["pokemons"] = all_pokemon_names[first_poke : last_poke]

        debut = value["debut_ep"]
        final = value["final_ep"]

        debut_idx = all_episodes_tags.index(debut)
        final_idx = all_episodes_tags.index(final)

        gen_episodes = all_episodes[debut_idx:final_idx+1]

        generations[key]["episodes"] = gen_episodes

    return generations


def get_episodes_dict_with_pokemon(episode_names, ignore_pikachu = False):
    episodes_with_pokemon_list = {}

    for episode_tag in episode_names:
        episode_path = episode_dir + episode_tag
        episode_file = open(episode_path, encoding='utf-8').read()
        episode_pokemons_text = re.findall(r"(?<=Pokémon==)(.*)(?=Trivia)", episode_file)
        # following episodes: [0294]AG018;[0330]AG054;[0458]AG182;[0477]DP009;[0520]DP052
        # have different text formatting, hence an if workaround
        if len(episode_pokemons_text) == 0:
            episode_pokemons_text = re.findall(r"(?<=Pokémon ==)(.*)(?=Trivia)", episode_file)

        if len(episode_pokemons_text) > 0:
            episode_pokemons_text = re.findall( r'(.*?)(?===)', episode_pokemons_text[0])
        episode_pokemons_text = episode_pokemons_text[0]

        # 1. get text between double brackets 2. remove the brackets, the first 1/2 letters and |
        # also remove examples like: "illusion"; "Charizard|Charizard X"
        # TODO: we ignore Charizard|Charizard X etc, we should increment CHarizard's friends instead
        pokemons_in_episode = list(set(re.findall("(?<=\{\{[\w+][|])([A-Z].[^|]*?)(?=\})", episode_pokemons_text)))

        if ignore_pikachu == True and "Pikachu" in pokemons_in_episode:
            pokemons_in_episode.remove("Pikachu")
        
        # some pages (20) raw text has also Pokemon word tagged. 
        # episode 0113EP111 has a Ditto, who's Transform ability is taken as a Pokemon by regex. Remove
        wrong_tokens = ["Transform", "Pokémon"]
        for wrong_token in wrong_tokens:        
            if wrong_token in pokemons_in_episode:
                pokemons_in_episode.remove(wrong_token)

        # there are entries for both Farfetch\\'d and Farfetch'd. Unifying here        
        if "Farfetch\\'d" in pokemons_in_episode:
            ind = pokemons_in_episode.index("Farfetch\\'d")
            pokemons_in_episode[ind] = pokemons_in_episode[ind].replace("\\", "")

        episodes_with_pokemon_list[episode_tag] = pokemons_in_episode
    return episodes_with_pokemon_list


def generate_edges_list(episodes_with_pokemon_list):
    all_edges = []
    for episode_tag, pokemons in episodes_with_pokemon_list.items():
        # all pokemon pairs from the episode is a binomial of len(pokemons) and 2
        list_of_nodes_from_episode = list(itertools.combinations(sorted(pokemons), 2))
        all_edges += list_of_nodes_from_episode
    return all_edges


def generate_generation_graph(generation):
    episodes_with_pokemons = get_episodes_dict_with_pokemon(generation["episodes"], True)
    edges_list = generate_edges_list(episodes_with_pokemons)
    
    G = nx.Graph()
    G.add_nodes_from(generation["pokemons"])

    for i, pokemon_edge in enumerate(edges_list):
        pokemon1 = pokemon_edge[0]
        pokemon2 = pokemon_edge[1]

        if G.has_edge(pokemon1, pokemon2):
            G[pokemon1][pokemon2]['weight'] += 1
        else:
            G.add_edge(pokemon1, pokemon2, weight=1)

    return G


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

