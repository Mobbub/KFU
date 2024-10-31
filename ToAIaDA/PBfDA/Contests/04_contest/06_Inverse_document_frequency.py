import math
import numpy as np

def calculate_idf(matrix):
    num_docs = len(matrix)  # Количество документов
    num_words = len(matrix[0])  # Количество слов
    idf_matrix = [[0 for _ in range(num_words)] for _ in range(num_docs)]
    
    for j in range(num_words):
        n = 0
        for i in range(num_docs):
            if matrix[i][j] > 0:
                n += 1
        idf = math.log(num_docs / (1 + n)) + 1
        for i in range(num_docs):
            idf_matrix[i][j] = idf
    
    return idf_matrix

k, m = map(int, input().split())

matrix = []

for _ in range(k):
    row = list(map(float, input().split()))
    matrix.append(row)

matrix = np.array(matrix)

idf_matrix = calculate_idf(matrix)

for row in idf_matrix:
    formatted_row = ' '.join(f'{num:.2f}' for num in row)
    print(formatted_row)
    break