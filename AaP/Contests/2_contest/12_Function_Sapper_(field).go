func fill(maze [][]int) {
for x, row := range maze {
for y, v := range row {
    if v == -1 {
        for ox:=-1; ox<=1; ox++ {
        for oy:=-1; oy<=1; oy++ {
            if (x+ox >= 0) && (x+ox < len(maze)) &&
                (y+oy >= 0) && (y+oy < len(maze[x+ox])) &&
                maze[x+ox][y+oy] != -1 {
                        maze[x+ox][y+oy] += 1
            }
        } }
    }
} } }
