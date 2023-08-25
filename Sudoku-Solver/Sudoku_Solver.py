def is_valid_move(grid, row, col, num):

    for x in range(9):
        if grid[row][x] == num:
            return False
        
    for x in range(9):
        if grid[x][col] == num:
            return False
        
    # LOGIC 1 for BLOCK NUMBER CHECK
    corner_row = row - row % 3
    corner_col = col - col % 3
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == num:
                return False
    return True
        
def sudoku_solve(grid, row, col):

    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if grid[row][col] > 0:
        return sudoku_solve(grid, row, col + 1)
    
    for num in range (1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
        
            if sudoku_solve(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False


grid = [
    [0, 0, 0, 0, 0, 0, 6, 8, 0],
    [0, 0, 0, 0, 7, 3, 0, 0, 9],
    [3, 0, 9, 0, 0, 0, 0, 4, 5],
    [4, 9, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 3, 0, 5, 0, 9, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 3, 6],
    [9, 6, 0, 0, 0, 0, 3, 0, 8],
    [7, 0, 0, 6, 8, 0, 0, 0, 0],
    [0, 2, 8, 0, 0, 0, 0, 0, 0]
]

if sudoku_solve(grid, 0, 0):
    for x in range(9):
        for y in range(9):
            print(grid[x][y], end = " ")
        print()
else:
    print("No solution exists.")