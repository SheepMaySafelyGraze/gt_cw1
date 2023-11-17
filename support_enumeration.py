import nashpy as nash
import nD_equilibria_finder as equib
#Attempt to find mixed equilibria of a 2D small political game
payoff = equib.payoff_finder(3,2,2)
deg_game = nash.Game(payoff)
eq = deg_game.support_enumeration()
for eq in eq:
    print(eq)



