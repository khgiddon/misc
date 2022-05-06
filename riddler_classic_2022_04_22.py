# https://fivethirtyeight.com/features/can-you-level-up-your-armor/

import numpy as np

 # Create transition matrix between each state
matrix = np.array([
               [ 0, 1, 0, 0, 0, 0] # 0->1
              ,[.2, 0,.8, 0, 0, 0] # 1->2
              ,[ 0,.4, 0,.6, 0, 0] # 2->3
              ,[ 0, 0,.6, 0,.4, 0] # 3->4
              ,[ 0, 0, 0,.8, 0,.2] # 4->5
              ,[ 0, 0, 0, 0, 0, 1] # 5
               ])     

# Time for linear algebra
number_of_absorbing_states = 1
I = np.eye(len(matrix) - number_of_absorbing_states)
Q = matrix[:number_of_absorbing_states*-1,:number_of_absorbing_states*-1]
N = np.linalg.inv(I - Q)
o = np.ones(Q.shape[0])
tta = np.dot(N, o)
print(np.max(tta))

# 42.66666666666667
