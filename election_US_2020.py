import numpy as np
import nD_equilibria_finder as nD
donald_trump = [(18, 18)]
joe_biden = [(16, 17)]
payoffs = np.load("gt_cw1\payoffs_20_2_2.npy")

joe_biden_best_response = nD.find_best_responses(donald_trump, payoffs, 20, 2)
print(joe_biden_best_response)

donald_trump_best_response = nD.find_best_responses(joe_biden, payoffs, 20, 2)
print(donald_trump_best_response)