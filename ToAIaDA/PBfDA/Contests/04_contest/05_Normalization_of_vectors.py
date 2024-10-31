import numpy as np

k, m = map(int, input().split())
matrix = []
for _ in range(k):
    row = list(map(float, input().split()))
    matrix.append(row)

matrix = np.array(matrix)

normalized_matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
normalized_matrix = np.round(normalized_matrix, 2)

for row in normalized_matrix:
    print(' '.join(map(str, row)))