from Backtracking import sudoku_solve
import test_cases

def print_grid(grid):

    """
    Print the given Sudoku grid in a readable format.

    Args:
        grid (list[list[int]]): The Sudoku grid to be printed.
    """

    for row in grid:
        for num in row:
            print(num, end=" ")
        print()

def main(grid):

    """
    Main function to solve and print a Sudoku puzzle.
    """

    if sudoku_solve(grid):
        print_grid(grid)
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main(test_cases.test_case_1)
    print()
    main(test_cases.test_case_2)
    print()
    main(test_cases.test_case_3)
    print()
    main(test_cases.test_case_4)
    print()
