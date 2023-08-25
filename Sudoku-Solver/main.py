from flask import Flask, render_template
from Backtracking import sudoku_solve
import test_cases

app = Flask(__name__)

def format_grid(grid):
    """
    Format the given Sudoku grid as a list of lists of strings for rendering.

    Args:
        grid (list[list[int]]): The Sudoku grid to be formatted.

    Returns:
        list[list[str]]: Formatted grid as strings.
    """
    formatted_grid = []
    for row in grid:
        formatted_row = [str(num) if num != 0 else '' for num in row]
        formatted_grid.append(formatted_row)
    return formatted_grid

@app.route('/')
def index():
    results = []

    for test_case in [test_cases.test_case_1, test_cases.test_case_2, test_cases.test_case_3, test_cases.test_case_4]:
        grid_copy = [row[:] for row in test_case]  # Create a copy of the grid
        if sudoku_solve(grid_copy):
            formatted_grid = format_grid(grid_copy)
            results.append(formatted_grid)
        else:
            results.append("No solution exists.")

    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
