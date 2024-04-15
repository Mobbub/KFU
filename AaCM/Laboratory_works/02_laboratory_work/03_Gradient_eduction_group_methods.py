import math

def find_error(matrix, column, solutions):
    error = []
    for i in range(len(matrix)):
        current_equation_error = 0
        for j in range(len(matrix)):
            current_equation_error += matrix[i][j] * solutions[j]
        current_equation_error -= column[i]
        error.append(current_equation_error)
    
    error_vector_sum = 0
    for element in error:
        error_vector_sum += math.pow(element, 2)
    return math.sqrt(error_vector_sum)

A = [
    [5, 2, -1],
    [3, 7, 2],
    [-2, 4, 6]
]

B = [12, 15, 10]

X = prositer(A, B, 0.0000001)

print(find_error(A, B, X))
