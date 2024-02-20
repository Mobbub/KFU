#include <iostream>
#include <queue>
#include <vector>
#include <string>
using namespace std;

struct Coordinate {
    int row;
    int col;
};
bool is_valid(const vector<string>& maze, int row, int col, vector<vector<bool>>& 
visited) 
{
    int rows = maze.size();
    int cols = maze[0].size();
    return row >= 0 && row < rows && col >= 0 && col < cols && maze[row][col] != '#' && 
!visited[row][col];
}
bool is_can_exit_from_maze(vector<string>& maze, int row, int col) 
{
    int rows = maze.size();
    int cols = maze[0].size();
    vector<vector<bool>> visited(rows, vector<bool>(cols, false));
    queue<Coordinate> queue;
    queue.push({ row, col });
    visited[row][col] = true;
    while (!queue.empty()) {
        Coordinate current = queue.front();
        queue.pop();
        if (maze[current.row][current.col] == 'E') 
        {
            return true;
        }
        int dx[] = { -1, 1, 0, 0 };
        int dy[] = { 0, 0, -1, 1 };
        for (int i = 0; i < 4; i++) 
        {
            int newRow = current.row + dx[i];
            int newCol = current.col + dy[i];

            if (is_valid(maze, newRow, newCol, visited)) 
            {
                queue.push({ newRow, newCol });
                visited[newRow][newCol] = true;
            }
        }
    }
    return false;
}
