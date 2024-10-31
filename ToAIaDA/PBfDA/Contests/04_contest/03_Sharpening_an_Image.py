import numpy as np

def apply_filter(matrix, filter):
    n, m = matrix.shape
    result = np.zeros((n-2, m-2), dtype=int)
    for i in range(1, n-1):
        for j in range(1, m-1):
            sub_matrix = matrix[i-1:i+2, j-1:j+2]
            value = np.sum(sub_matrix * filter)
            value = max(0, min(255, value))
            result[i-1, j-1] = value
    return result

def main():
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    matrix = np.array(matrix)
    
    filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    
    result = apply_filter(matrix, filter)
    
    for row in result:
        print(' '.join(map(str, row)))

main()