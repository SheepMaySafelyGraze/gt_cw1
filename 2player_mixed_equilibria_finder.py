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
        self.strategy = np.array([starting_strategy_0,starting_strategy_1])
        self.game_size = np.array([len(starting_strategy_0), len(starting_strategy_1)])

    def expected_payoff(self,player,strategy):
        """
        :param player: integer 0 or 1
        :param strategy: numpy array of size (strategy 0, strategy 1)
        :return: float
        """
        return strategy[0]@self.payoff[player,:,:]@strategy[1]

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
            [self.expected_payoff(0,[basis_vector(i,self.game_size[0]),self.strategy[1]]) for i in range(self.game_size[0])])
        payoff_matrix_1 = np.array(
            [self.expected_payoff(1, [self.strategy[0],basis_vector(i, self.game_size[1])]) for i in range(self.game_size[1])])
        x_0 = np.maximum(0, payoff_matrix_0 - self.expected_payoff(0, self.strategy)*np.ones(self.game_size[0]))
        p_0 = np.add(self.strategy[0], x_0) / (1+np.sum(x_0))
        x_1 = np.maximum(0, payoff_matrix_1 - self.expected_payoff(1, self.strategy)*np.ones(self.game_size[1]))
        p_1 = np.add(self.strategy[1], x_1) / (1 + np.sum(x_1))
        self.strategy[0] = p_0
        self.strategy[1] = p_1

    def find_equilibrium(self, thresh, max_iterations):
        """
        Attempts to find equilibrium stopping when difference between two consecutive updates is below the threshold or
        when the maximum number of iterations is reached. The 'difference' is just the 1-norm of the strategy.
        :param error: float
        :param iterations: integer
        :return: numpy array [strategy_0, strategy_1]
        """
        # TODO iterate the update strategy method to find equilibrium
        iterations = 0
        error = 10000
        while iterations<max_iterations and thresh<error:
            starting_strategy = self.strategy.copy()
            self.update_strategy()
            end_strategy = self.strategy
            error = np.sum(np.abs(np.subtract(end_strategy,starting_strategy)))
            iterations += 1
            if iterations %1000 ==0:
                print(self.strategy)

        return self.strategy



#some preliminary tests
payoff = np.array([[[1,2],[-1,3]],[[-2,1],[1,-1]]])
starting_strategy_0 = np.array([2/5-0.001,3/5+0.001])
starting_strategy_1 = np.array([1/3+0.001,2/3-0.001])
ef = MixedEquilibriumFinder(payoff,starting_strategy_0,starting_strategy_1)
print(ef.strategy)
print(ef.payoff)
print(ef.expected_payoff(0, ef.strategy))
print(ef.find_equilibrium(0.0001,100000))
