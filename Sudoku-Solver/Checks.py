def is_valid_move(grid, row, col, num):
    
    """
    Check if placing 'num' in the specified cell is a valid move.

    Args:
        grid (list[list[int]]): The Sudoku grid.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        num (int): The number to be placed in the cell.

    Returns:
        bool: True if placing 'num' in the cell is a valid move, False otherwise.
    """

    for x in range(9):
        if grid[row][x] == num:
            return False
        
    for x in range(9):
        if grid[x][col] == num:
            return False
        
    corner_row = row - row % 3
    corner_col = col - col % 3
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == num:
                return False
    return True
