# https://fivethirtyeight.com/features/can-you-crawl-around-the-cone/
# Riddler Expres

import numpy as np
from scipy.stats import binom
from scipy.stats import hypergeom

# Find probability of k successes in n trials and fill out matrix with results
M = np.zeros((3,4)) # 3 different trials, 4 different outcomes (0,1,2,3 successes) for each
n = 3

# Coins
p = .5
for k in range(n+1):
    M[0,k] = binom.pmf(k, n, p, loc = 0)

# Dice
p = 1/3
for k in range(n+1):
    M[1,k] = binom.pmf(k, n, p, loc = 0)

# Cards: Use hypergeometric (not binomial distribution) b/c is without replacement
[a,b,c] = [52, 13, 3] # 52 cards, 13 hearts, 3 trials
for k in range(n+1):
    M[2,k] = hypergeom(a,b,c).pmf(k)

# Vertically multiply for probability of each k
p = np.prod(M,axis=0)

# Sum for total probability
total_p = np.sum(p)
print(total_p)

# 0.09949346405228743
