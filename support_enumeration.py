import nashpy as nash
import nD_equilibria_finder as equib
import numpy as np
#Attempt to find mixed equilibria of a 2D small political game
num_positions = 3
payoff = equib.payoff_finder(num_positions,2,2)
deg_game = nash.Game(payoff.transpose(), (np.ones([num_positions**2,num_positions**2])-payoff).transpose())
eq = deg_game.support_enumeration()
for eq in eq:
    print(eq)
print(equib.find_equilibria(3,2,2))




