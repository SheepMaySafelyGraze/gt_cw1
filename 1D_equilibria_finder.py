import networkx as nx
import numpy as np
import itertools


def payoff_finder_one_dim(num_positions, num_players):
    """
    Find an individual payoff tensor for each player on the num_positions
    election grid.
    """
    # creating a graph that represents the positions and distance between them
    G = nx.grid_graph([num_positions])
    distance_dict = dict(nx.all_pairs_shortest_path_length(G))
    position_list = [i for i in range(num_positions)]
    # obtaining all permutations for the player positions
    position_permutations = np.array([list(product) for product in itertools.product(position_list, repeat=num_players)])

    # creating an individual tensor per player
    player_tensor = np.zeros((num_positions,) * num_players)
    outcome_list = [player_tensor.copy() for i in range(num_players)]

    for player_positions in position_permutations:
        outcome = np.array([0 for i in range(num_players)], dtype="float")
        for spot in position_list:
            closest_players = {}
            closest_distance = num_positions + 1
            for i in range(num_players):
                if distance_dict[spot][player_positions[i]] < closest_distance:
                    closest_players = {}
                    closest_players[player_positions[i]] = [i]
                    closest_distance = distance_dict[spot][player_positions[i]]
                elif distance_dict[spot][player_positions[i]] == closest_distance:
                    if player_positions[i] in closest_players.keys():
                        closest_players[player_positions[i]].append(i)
                    else:
                        closest_players[player_positions[i]] = [i]
            for key in closest_players.keys():
                # spltting the outcome so that if we have 2 left and 1 right, the left gets 2.5% each and the right 5%
                outcome[closest_players[key]] += 1/(len(closest_players.keys()) * len(closest_players[key]) * num_positions)
        for j in range(num_players):
            outcome_list[j][tuple(player_positions)] += outcome[j]
    return outcome_list


def get_best_response_for_players(num_positions, num_players):
    """
    Find the best response for a player, for each permutation of all other
    players' positions
    """
    outcome_list = payoff_finder_one_dim(num_positions, num_players)
    response_list = [[] for i in range(num_players)]
    position_list = [i for i in range(num_positions)]
    # get all the permutations of other players
    position_permutations = np.array([list(product) for product in itertools.product(position_list, repeat=num_players-1)])
    for player in range(num_players):
        for position in position_permutations:
            # slice(None) takes the entire column
            new_list = list(position)[0:player] + [slice(None)] + list(position)[player:]
            possible_outcomes = outcome_list[player][tuple(new_list)]
            # gets all best responses possible, had to use isclose due to floating point errors
            best_response = np.argwhere(np.isclose(possible_outcomes, np.max(possible_outcomes), 1e-6))
            for val in best_response:
                new_list = list(position)[0:player] + [val[0]] + list(position)[player:]
                response_list[player].append(new_list)
    return response_list


def get_equilibria_for_players(num_positions, num_players):
    """
    Obtain the equilibria for the game, given the number of players and
    positions available.
    """
    # this checks if the best responses intersect
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
    equilibrium_count = len(equilibrium_list)
    return [equilibrium for equilibrium in equilibrium_list], equilibrium_count


# obtaining values for the table seen in the report
player_list = [2, 3, 4, 5]
num_spaces = [10, 11]
for player in player_list:
    for spaces in num_spaces:
        print(f"Equilibria for {player} players and {spaces} spaces")
        eq, eq_count = get_equilibria_for_players(spaces, player)
        print(eq)
        print(eq_count)
        eq_set = []
        # obtains the unique equilibria (permutations discarded)
        for equilibrium in eq:
            x = np.sort(equilibrium)
            if list(x) in eq_set:
                pass
            else:
                eq_set.append(list(x))
        print(eq_set)
        np.save(f"{player}-{spaces}", eq)
