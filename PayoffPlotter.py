import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

# code for plotting payoff space of a 2-player game via monte carlo methods

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or counterclockwise


def graham_scan(points):
    points = sorted(set(points))  # Remove duplicate points and sort by x-coordinate
    if len(points) <= 1:
        return points

    lower_hull = []
    for point in points:
        while len(lower_hull) >= 2 and orientation(lower_hull[-2], lower_hull[-1], point) != 2:
            lower_hull.pop()
        lower_hull.append(point)

    upper_hull = []
    for point in reversed(points):
        while len(upper_hull) >= 2 and orientation(upper_hull[-2], upper_hull[-1], point) != 2:
            upper_hull.pop()
        upper_hull.append(point)

    return lower_hull[:-1] + upper_hull[:-1]


def is_convex_combination(x, vertices):
    # Ensure there are at least 3 vertices to form a convex combination
    if len(vertices) < 3:
        return False

    convex_hull = graham_scan(vertices)

    # Check if x is inside the convex hull by checking its orientation with each adjacent pair of vertices
    for i in range(len(convex_hull)):
        p1, p2 = convex_hull[i], convex_hull[(i + 1) % len(convex_hull)]
        if orientation(p1, p2, x) != 2:
            return False

    return True


class PayoffSampler:
    def __init__(self, payoffs, n_A=None, seed=1):
        """
        initialise a naive payoff sampler
        :param payoffs: list of payoffs, n_A * n_B in length, assumed listed row-wise from table
        :param n_A: number of pure strategies for player A
        :param seed: seed for rng
        """
        # extract number of strategies, with error catching
        if not n_A:  # if no n_A given, assume equal number of strategies for each player
            try:
                self.n_A = int(np.sqrt(len(payoffs)))
                self.n_B = self.n_A
                assert n_A - np.sqrt(len(payoffs)) < 1e-8  # check number was indeed square
            except AssertionError:
                raise ValueError("Number of pure strategies not provided and payoffs not square, please specify n_A.")
        else:  # if number of pure strategies provided
            self.n_A = n_A
            try:  # check that number of payoffs divisible by number of pure strategies provided, else error
                self.n_B = int(len(payoffs)/n_A)
                assert self.n_B - len(payoffs)/n_A < 1e-8  # check number of payoffs was indeed divisible by n_A
            except AssertionError:
                raise ValueError("Invalid input table: number of payoffs not divisible by number of strategies.")

        self.payoffs = payoffs
        # payoffs for A, B as list of tuples
        self.payoffs_A = np.array([p[0] for p in payoffs]).reshape((self.n_A, self.n_B))
        self.payoffs_B = np.array([p[1] for p in payoffs]).reshape((self.n_A, self.n_B))
        # list of pure strats
        self.pureStrats = range(len(payoffs))
        # sampler using given seed
        self.rng = np.random.default_rng(seed)

    def sample_naive(self, N):
        """
        draw N samples and return expected payoffs as list of tuples of length N
        :param N: number of samples to draw
        :return: samples as list of tuples
        """
        samples = []  # list of tuples giving expected payoffs from playing random strategies
        for i in range(N):
            # sample random probabilities of each strategy
            bStratProbs = self.rng.uniform(low=0, high=1, size=self.n_B)
            bStratProbs = bStratProbs/sum(bStratProbs)  # normalise to give probabilities
            aStratProbs = self.rng.uniform(low=0, high=1, size=self.n_A)
            aStratProbs = aStratProbs/sum(aStratProbs)  # normalise to give probabilities

            # forming expected strategies by law of total expectation
            A_payoff, B_payoff = 0, 0
            for k, pA in enumerate(aStratProbs):
                for l, pB in enumerate(bStratProbs):
                    A_payoff += pA*pB*self.payoffs_A[k, l]
                    B_payoff += pA*pB*self.payoffs_B[k, l]

            samples.append((A_payoff, B_payoff))

        return samples

    def sample_rejection(self, N):
        """
        uses rejection sampling to sample uniformly from convex hull
        this should constitute a speedup to sample_naive, which is not uniform so fills area very slowly
        :param N: number of samples to draw
        :return: samples as list of tuples
        """
        print("The sample_rejection method will NOT sample from payoff set... It will be fixed at some point.")
        # obtaining bounds of box within which to sample
        max_x, min_x = np.max(self.payoffs_A), np.min(self.payoffs_A)
        max_y, min_y = np.max(self.payoffs_B), np.min(self.payoffs_B)

        samples = []
        nits = 0  # iteration counter
        while len(samples) < N and nits <= 10*N:
            x = self.rng.uniform(low=min_x, high=max_x, size=1)
            y = self.rng.uniform(low=min_y, high=max_y, size=1)

            proposal = (x, y)

            if is_convex_combination(proposal, self.payoffs):
                samples.append(proposal)

        return samples


# function to generate payoffs for 1d election game
def get_election_payoffs(n):

    payoffs = []
    # loop of possible strategies of each of candidates A and B
    for i, aStrat in enumerate(range(n)):
        for j, bStrat in enumerate(range(n)):
            aPay = 0
            bPay = 0
            # for each point on the political spectrum
            for k in range(n):
                aDist = abs(aStrat-k)
                bDist = abs(bStrat-k)
                if aDist < bDist:
                    bPay += 1/n
                elif bDist < aDist:
                    aPay += 1/n
                else:  # equidistant cast, half payoff
                    aPay += 1/(2*n)
                    bPay += 1/(2*n)

            payoffs.append((aPay, bPay))

    return payoffs


v = 2
c = 3

payoffs = [((v-c)/2, -(v-c)/2), (v, 0), (0, 0), (v + 5, v/2)]
sampler = PayoffSampler(payoffs, n_A=2, seed=1)
convex_hull = sampler.sample_naive(1000)
plt.scatter([t[0] for t in convex_hull], [t[1] for t in convex_hull], s=0.5, color="red")
plt.show()

