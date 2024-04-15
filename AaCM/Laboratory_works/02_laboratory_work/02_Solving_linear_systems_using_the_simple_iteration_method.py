def prositer(matrix, column, eps):
    matrix_size = len(matrix)
    solutions = [0] * matrix_size
    previous_solutions = [0] * matrix_size
    while True:
        previous_solutions = solutions.copy()
        for i in range(matrix_size):
            sum = column[i]
            for j in range(matrix_size):
                if i != j:
                    sum -= matrix[i][j] * previous_solutions[j]
            solutions[i] = sum / matrix[i][i]
        if abs(solutions[0] - previous_solutions[0]) <= eps:
            break
    return solutions

A = [
    [5, 2, -1],
    [3, 7, 2],
    [-2, 4, 6]
]

B = [12, 15, 10]

print(prositer(A, B, 0.0001))
