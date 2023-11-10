import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt
import itertools

def payoff_finder_one_dim(num_positions, num_players):
    G = nx.grid_graph([num_positions])
    distance_dict = dict(nx.all_pairs_shortest_path_length(G))
    position_list = [i for i in range(num_positions)]
    position_permutations = np.array([list(product) for product in itertools.product(position_list, repeat=num_players)])
    # going to have to create individual payoff tensors for my own sanity here
    player_tensor = np.zeros((num_positions,) * num_players)
    outcome_list = [player_tensor.copy() for i in range(num_players)]

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
        for j in range(num_players):
            outcome_list[j][tuple(player_positions)] += outcome[j]
    return outcome_list

print(payoff_finder_one_dim(3, 3)[0]) 
def get_best_response_for_players(num_positions, num_players):
    outcome_list = payoff_finder_one_dim(num_positions, num_players)
    response_list = [[] for i in range(num_players)]
    position_list = [i for i in range(num_positions)]
    # get all the permutations of other players
    position_permutations = np.array([list(product) for product in itertools.product(position_list, repeat=num_players-1)])
    for player in range(num_players):
    # this is ok for player a but for later players this is confusing -> put slice(None) where they have to be
        for position in position_permutations:
            new_list = list(position)[0:player] + [slice(None)] + list(position)[player:]
            possible_outcomes = outcome_list[player][tuple(new_list)]
            # print(possible_outcomes)
            # print(np.argwhere(possible_outcomes == np.max(possible_outcomes)))
            best_response = np.argwhere(possible_outcomes == np.max(possible_outcomes)) # TODO: this only gets one best response, of course there can be multiple
            for val in best_response:
                new_list = list(position)[0:player] + [val[0]] + list(position)[player:]
                response_list[player].append(new_list)
    return response_list

print(get_best_response_for_players(10, 2))

def get_equilibria_for_players(num_positions, num_players):
    # basically checks if the best responses intersect (if we have say [0, 1, 2] in all 3 players' best responses lists)
    response_list = get_best_response_for_players(num_positions, num_players)
    equilibrium_list = []
    for response in response_list[0]:
        add_to_list = True
        for i in range(1, len(response_list)):
            if response not in response_list[i]:
                add_to_list = False
                break
        if add_to_list:
            equilibrium_list.append(response)
    return equilibrium_list

print(get_equilibria_for_players(10, 4))