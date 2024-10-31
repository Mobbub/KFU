def is_valid_sudoku(matrix):
    for row in matrix:
        if not is_valid_row(row):
            return False

    for col in range(9):
        if not is_valid_row([matrix[i][col] for i in range(9)]):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            square = [matrix[x][y] for x in range(i, i+3) for y in range(j, j+3)]
            if not is_valid_row(square):
                return False

    return True

def is_valid_row(row):
    seen = set()
    for num in row:
        if num == 0:
            continue
        if num in seen:
            return False
        seen.add(num)
    return True