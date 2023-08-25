def is_valid_move(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
    for x in range(9):
        if grid[x][col] == num:
            return False
        
    # LOGIC 1 for BLOCK NUMBER CHECK
    # corner_row = row - row % 3
    # corner_col = col - col % 3
    # for x in range(3):
    #     for y in range(3):
    #         if grid[corner_row + x][corner_col + y] == num:
    #             return False

    # LOGIC 2 for BLOCK NUMBER CHECK
    for x in range(9):
        if grid[3*(row//3)+x//3][3*(col//3)+x%3] == num:
            return False

grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]