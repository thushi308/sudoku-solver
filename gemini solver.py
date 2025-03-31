import time
start = time.time()
def solve_sudoku(board):
    """Solves a Sudoku puzzle in-place.

    Args:
        board: A 9x9 list of lists representing the Sudoku board.
               Empty cells are represented by 0.
    """

    def is_valid(row, col, num):
        """Checks if placing num at board[row][col] is valid."""
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
            if board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                return False
        return True

    def solve():
        """Recursively solves the Sudoku puzzle."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(row, col, num):
                            board[row][col] = num
                            if solve():
                                return True
                            else:
                                board[row][col] = 0  # Backtrack
                    return False  # No valid number found
        return True  # All cells filled

    solve()
    return board

def print_board(board):
    for row in board:
        print(row)

sudoku_board = [
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

# for i in range(9):
#     for j in range(9):
#         sudoku_board[i][j] = 0

solved_board = solve_sudoku(sudoku_board)
end = time.time()
print(end - start)
print_board(solved_board)