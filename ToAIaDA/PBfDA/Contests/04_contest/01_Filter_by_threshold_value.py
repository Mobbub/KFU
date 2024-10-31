import numpy as np

vector = np.array([int(x) for x in input().split()])

new_vector = (vector > 127).astype(int)

print(' '.join(map(str, new_vector)))