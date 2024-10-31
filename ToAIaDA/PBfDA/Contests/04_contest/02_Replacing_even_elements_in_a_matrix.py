import numpy as np

n, m, target = map(int, input().split())
matrix = np.array([list(map(int, input().split())) for _ in range(n)])

matrix[matrix % 2 == 0] = target

for row in matrix:
    print(" ".join(map(str, row)))