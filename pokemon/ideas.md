# Ideas for analysis

1. Analyse which pokemon met the most of other pokemon throughout the anime episodes.
  - Nodes: pokemon
  - Edges: there is an edge between two pokemon if they both played role in the same episode   
    - Weight: number of common episodes       
  - Do the community detection. 
    - Will it divide pokemon into the Generations?
  - What is type % in each detected group?
    - Check the handshake theorem 
    - Check the friendship paradox 
2. Check which type combo is the most common / the strongest.
  - Nodes: pokemon with 2 types
    - Weight: stats sum
  - Edges: if they at least 1 common type out of two between two pokemon
3. Idea: See which pokemon are most commonly found together in the games (in the same areas) (**Riley**)
  - Nodes: pokemon
  - Edges: two pokemon are connected if they both appear in the same area
    - Weight: how many areas they appeared in together throughout all the games
4. Grouping them by episodes and finding out which episode is the most dangerous to walk around based on the average sentiment of pokemon in the episodes.
5. The aim would be to find 6 type combinations which would counter all possible types:
  - Graph type: directed
  - Nodes: pokemon
  - Edges: 
    - Weight: 1/2, 2, 4
6. Word-cloud for each Pokemon type.
  - How about multi-type pokemon? We combine both types' tokens?
7. 