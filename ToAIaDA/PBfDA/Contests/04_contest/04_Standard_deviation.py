import numpy as np

k, m = map(int, input().split())
matrix1 = [list(map(float, input().split())) for _ in range(k)]
matrix2 = [list(map(float, input().split())) for _ in range(k)]

matrix1 = np.array(matrix1)
matrix2 = np.array(matrix2)

n = k * m
msd = np.sum((matrix1 - matrix2) ** 2) / n

print(f"{msd:.2f}")