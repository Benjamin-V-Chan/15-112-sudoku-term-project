import random

# CONSTANTS
numbers = list(range(1, 10))

# Number of starting numbers based on difficulty
startingNumbers = {
    'easy': 60,
    'medium': 50,
    'hard': 40,
    'expert': 30,
    'evil': 20
}

# Generate a board based on the difficulty
def generateBoard(difficulty):
    while True:
        board = generateCompleteBoard()
        removeNumbers(board, startingNumbers[difficulty])
        if isBoardSolvable(board):
            return board

# Generate a complete board
def generateCompleteBoard():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fillBoard(board)
    return board

# Fill board with random numbers
def fillBoard(board):
    empty = findEmptyCellWithFewestOptions(board)
    if not empty:
        return True
    row, col, options = empty
    random.shuffle(options)
    for num in options:
        if isValid(board, row, col, num):
            board[row][col] = num
            if fillBoard(board):
                return True
            board[row][col] = 0
    return False

# Light Inspiration from CMU Mini Sudoku Solver HW
def findEmptyCellWithFewestOptions(board):
    min_options = 10
    best_cell = None
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                options = [num for num in numbers if isValid(board, row, col, num)]
                if len(options) < min_options:
                    min_options = len(options)
                    best_cell = (row, col, options)
                    if min_options == 1:
                        return best_cell
    return best_cell

# Light Inspiration from CMU Mini Sudoku Solver HW
# Similar function to findLegalValues in play.py
def isValid(grid, row, col, num):
    #Check if it's valid to place a number in a specific cell.
    
    # Check row
    for c in range(9):
        if grid[row][c] == num:
            return False

    # Check column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # Check 3x3 subgrid
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for r in range(startRow, startRow + 3):
        for c in range(startCol, startCol + 3):
            if grid[r][c] == num:
                return False

    return True

# Remove numbers from the board until the count is reached
def removeNumbers(board, count):
    attempts = 81 - count
    while attempts > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        backup = board[row][col]
        board[row][col] = 0
        if not isBoardSolvable(board):
            board[row][col] = backup
        else:
            attempts -= 1

# Inspiration from CMU Mini Sudoku Solver HW
def solveBoard(board):
    empty = findEmptyCellWithFewestOptions(board)
    if not empty:
        return True
    row, col, options = empty
    random.shuffle(options)
    for num in options:
        if isValid(board, row, col, num):
            board[row][col] = num
            if solveBoard(board):
                return True
            board[row][col] = 0
    return False

# Bigger function to check if the board is solvable
def isBoardSolvable(board):
    boardCopy = [row[:] for row in board]
    return solveBoard(boardCopy)