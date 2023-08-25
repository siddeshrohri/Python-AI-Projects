from Checks import is_valid_move

def sudoku_solve(grid):

    """
    Solve the given Sudoku puzzle using backtracking.

    Args:
        grid (list[list[int]]): The initial Sudoku grid.

    Returns:
        bool: True if a solution exists, False otherwise.
    """

    return _sudoku_solve(grid, 0, 0)

def _sudoku_solve(grid, row, col):

    """
    Recursive function to solve the Sudoku puzzle using backtracking.

    Args:
        grid (list[list[int]]): The Sudoku grid.
        row (int): The current row index.
        col (int): The current column index.

    Returns:
        bool: True if a solution exists, False otherwise.
    """
    
    if col == 9:
        if row == 8:
            return True
        row += 1
        col = 0

    if grid[row][col] > 0:
        return _sudoku_solve(grid, row, col + 1)
    
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
        
            if _sudoku_solve(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False
