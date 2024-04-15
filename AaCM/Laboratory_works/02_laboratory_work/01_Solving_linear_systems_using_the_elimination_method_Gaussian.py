def gauss(matrix, column):
    matrix_size = len(matrix)
    for i in range(matrix_size):
        for j in range(i + 1, matrix_size):
            ratio = matrix[j][i] / matrix[i][i]
            for k in range(matrix_size):
                matrix[j][k] -= ratio * matrix[i][k]
            column[j] -= ratio * column[i]
    matrix_size = len(matrix)
    solutions = [0] * matrix_size
    for i in range(matrix_size - 1, -1, -1):
        solutions[i] = column[i]
        for j in range(i + 1, matrix_size):
            solutions[i] -= matrix[i][j] * solutions[j]
        solutions[i] /= matrix[i][i]
    return solutions

A = [
    [5, 2, -1],
    [3, 7, 2],
    [-2, 4, 6]
]

B = [12, 15, 10]

print(gauss(A, B))
