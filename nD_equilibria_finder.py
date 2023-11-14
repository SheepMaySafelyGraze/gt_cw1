# political compass payoff optimiser

import networkx as nx
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import itertools
import copy


# TODO:
#   - functions to compute payoffs and equilibria in multiplayer case
#   - functions to compute payoffs and equilibria in 2d political compass case
#


def payoff_finder(num_positions, dimensions=1, num_players=2):
    """
    :param num_positions: number of positions along each
    :param dimensions: number of dimensions
    :param num_players: number of players
    :return:
    """
    square_weight = 1/(num_positions**dimensions)
    # grid object describing positions on political hypercube
    G = nx.grid_graph([num_positions for _ in range(dimensions)])
    distance_dict = dict(nx.all_pairs_shortest_path_length(G))
    position_list = list(itertools.product(list(range(num_positions)), repeat=dimensions))
    position_dict = {}
    for i, pos in enumerate(position_list):  # code for accessing positions
        position_dict[pos] = i

    payoff_tensor = np.zeros((num_positions**dimensions,) * num_players)
    # loop over positions of n-1 players, computing payoff for final player
    # this gives entire list as game is symmetric
    for play in itertools.product(position_list, repeat=num_players-1):
        print(play)
        i, j = [position_dict[x] for x in play]
        for player_spot in position_list:  # for each playable position by nth player
            pos = copy.deepcopy(list(play))  # list of all positions
            pos.append(player_spot)
            # number of players on player_spot
            player_overlap = sum([int(b == player_spot) for b in pos])
            for space in position_list:  # for each space in grid
                distances = distance_dict[space]  # distances to each position from space
                player_distances = [distances[loc] for loc in pos]  # the distance of each player from space
                minimum = min(player_distances)
                if distances[player_spot] > minimum:  # if player is not closest to space
                    continue
                else:  # player is closest, compute and give payoff
                    # finding number of occupied positions which are equidistant
                    pos_closest = [b for b in pos if distances[b] == minimum]
                    closest_unique = len(list(set(pos_closest)))
                    payoff_tensor[i, j, position_dict[player_spot]] += square_weight/(max(1, closest_unique) * max(1, player_overlap))
    return payoff_tensor


def find_best_responses(player_positions, payoff_tensor, num_positions, dimensions):
    """
    accepts a list of players positions as tuples, as well as a payoff tensor
    returns the best responses for a player against the positions given
    it is assumed that all player positions but one are given,
    i.e. if payoff_tensor is n-dimensional, then n-1 player positions are provided

    :param player_positions: list of player positions as tuples
    :param payoff_tensor: payoff tensor giving payoffs for each strategy combination
    :param num_positions: number of positions in game
    :param dimensions: number of dimensions
    :return: list of the best responses as tuples
    """
    # form position dictionary
    position_list = list(itertools.product(list(range(num_positions)), repeat=dimensions))
    position_dict = {}
    for i, pos in enumerate(position_list):  # code for accessing positions
        position_dict[pos] = i

    payoffs = copy.deepcopy(payoff_tensor)
    for i in player_positions:
        payoffs = payoffs[position_dict[i]]

    max_payoff = np.max(payoffs)
    best_response_keys = np.argwhere(np.isclose(payoffs, max_payoff, 1e-12))
    best_response = []
    for k in best_response_keys:
        best_response.append(position_list[k[0]])

    return best_response


def find_equilibria(num_positions, dimensions, num_players, payoff_tensor=None, debug=False):
    """
    loops over possible positions, checks whether each is an equilibrium
    returns all equilibria found
    :param num_positions: number of positions
    :param dimensions: number of dimensions
    :param num_players: number of players
    :param payoff_tensor: payoff tensor given payoffs for each possible set of plays
    :param debug:
    :return:
    """
    if payoff_tensor is None:  # computing payoffs if none given (costly for all but small input)
        if debug:
            print("Computing payoff tensor...")
        payoff_tensor = payoff_finder(num_positions, dimensions, num_players)

    position_list = list(itertools.product(list(range(num_positions)), repeat=dimensions))
    equilibria = []

    for pos in itertools.product(position_list, repeat=num_players):  # for each possible arrangement
        equilibrium_found = True
        for i, spot in enumerate(pos):  # for each position, check it is a best response
            other_plays = [pos[j] for j in range(num_players) if j != i]  # all other plays
            if spot in find_best_responses(other_plays, payoff_tensor, num_positions, dimensions):
                pass
            else:
                equilibrium_found = False
                break
        if equilibrium_found:
            equilibria.append(pos)

    return equilibria









