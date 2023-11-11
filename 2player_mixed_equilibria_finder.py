import numpy as np
class MixedEquilibriumFinder:
    """
    Finds mixed equilibrium for a two player finite dimensional game.
    """

    def __init__(self,payoff,starting_strategy_0, starting_strategy_1):
        """

        :param payoff: numpy array of size R^(pure strategies 0)*(pure strategies 1)*2
        :param starting_strategy_0: numpy array of size R^(pure strategies 0)
        :param starting_strategy_1: numpy array of size R^(pure strategies 1)
        """
        self.payoff = payoff
        self.strategy = [starting_strategy_0,starting_strategy_1]
        self.game_size = [len(starting_strategy_0), len(starting_strategy_1)]

    def expected_payoff(self,player,strategy):
        """
        :param player: integer 0 or 1
        :param strategy: numpy array of size (strategy 0, strategy 1)
        :return: float
        """
        return strategy[0]@self.payoff[:,:,player]@strategy[1]

    def update_strategy(self):
        """
        updates strategy iteratively via the rule outlined by Nash
        :return: numpy array (strategy 0, strategy 1)
        """
        def basis_vector(i,n):
            e = np.zeros(n)
            e[i] = 1
            return e

        payoff_matrix_0 = np.array(
            self.expected_payoff(0,[basis_vector(i,self.game_size[0]),self.strategy[1]]) for i in range(self.game_size[0]))
        payoff_matrix_1 = np.array(
            self.expected_payoff(1, [self.strategy[0],basis_vector(i, self.game_size[1])]) for i in range(self.game_size[1]))
        x_0 = np.maximum(0, self.expected_payoff(0, self.strategy)*np.ones(self.game_size[0])-payoff_matrix_0)
        x_1 = np.maximum(0, self.expected_payoff(1, self.strategy)*np.ones(self.game_size[1])-payoff_matrix_1)
        self.strategy[0] = np.add(self.strategy[0],x_0)
        self.strategy[1] = np.add(self.strategy[1],x_1)

    def find_equilibrium(self):
        # TODO iterate the update strategy method to find equilibrium



