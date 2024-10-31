from collections import deque

class Coordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col

def is_valid(maze, row, col, visited):
    rows = len(maze)
    cols = len(maze[0])
    return 0 <= row < rows and 0 <= col < cols and maze[row][col] != '#' and not visited[row][col]

def is_can_exit_from_maze(maze, row, col):
    rows = len(maze)
    cols = len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque()
    queue.append(Coordinate(row, col))
    visited[row][col] = True
    
    while queue:
        current = queue.popleft()
        if maze[current.row][current.col] == 'E':
            return True
        
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        
        for i in range(4):
            new_row = current.row + dx[i]
            new_col = current.col + dy[i]

            if is_valid(maze, new_row, new_col, visited):
                queue.append(Coordinate(new_row, new_col))
                visited[new_row][new_col] = True
                
    return False