import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt
import itertools

def payoff_finder_one_dim(num_positions, num_players):
    G = nx.grid_graph([num_positions])
    distance_dict = dict(nx.all_pairs_shortest_path_length(G))
    outcome_list = []
    position_list = [i for i in range(num_positions)]
    position_permutations = np.array([list(product) for product in itertools.product(position_list, repeat=num_players)])
    for player_positions in position_permutations:
        outcome = np.array([0 for i in range(num_players)], dtype="float")
        for spot in position_list:
            closest_players = []
            closest_distance = num_positions + 1
            for i in range(num_players):
                if distance_dict[spot][player_positions[i]] < closest_distance:
                    closest_players = [i]
                    closest_distance = distance_dict[spot][player_positions[i]]
                elif distance_dict[spot][player_positions[i]] == closest_distance:
                    closest_players.append(i)
            outcome[closest_players] += 1/(len(closest_players) * num_players)
        outcome_list.append((player_positions, outcome))
    print(outcome_list)
        
payoff_finder_one_dim(3, 3)