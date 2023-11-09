from numpy import random
import numpy as np

probs = []
N = 1000000
for q in range(2, 16, 2):
    tot = 0
    length_string = int(q / 2)
    for _ in range(N):
        str1 = "".join(random.choice(["a", "b"], length_string))
        str2 = "".join(random.choice(["c", "d"], length_string))
        if len(np.unique(list(str1+str2))) == 4:
            tot += 1

    probs.append(tot/N)

print(range(2, 16, 2))
print(probs)

