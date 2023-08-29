import numpy as np

List = [3.24, 3.24, 3.26, 3.27, 3.25]
Y = 0

for i in List:
    Y += np.power((i - 3.252), 2)

print(np.sqrt(Y / 4))
