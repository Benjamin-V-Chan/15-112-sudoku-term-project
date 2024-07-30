import random

numbers = list(range(1, 10))
startingNumbers = {
    'easy': 60,
    'medium': 55,
    'hard': 50,
    'expert': 45,
    'evil': 40
}

def generateBoard(difficulty):
    while True:
        board = generateCompleteBoard()
        removeNumbers(board, startingNumbers[difficulty])
        if isBoardSolvable(board):
            return board, startingNumbers[difficulty]

def generateCompleteBoard():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fillBoard(board)
    return board

def fillBoard(board):
    empty = findEmptyCell(board)
    if not empty:
        return True
    row, col = empty
    random.shuffle(numbers)
    for num in numbers:
        if isValid(board, row, col, num):
            board[row][col] = num
            if fillBoard(board):
                return True
            board[row][col] = 0
    return False

def findEmptyCell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def isValid(grid, row, col, num):
    for c in range(9):
        if grid[row][c] == num:
            return False

    for r in range(9):
        if grid[r][col] == num:
            return False

    blockRow, blockCol = 3 * (row // 3), 3 * (col // 3)
    for r in range(blockRow, blockRow + 3):
        for c in range(blockCol, blockCol + 3):
            if grid[r][c] == num:
                return False

    return True


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

def solveBoard(board):
    empty = findEmptyCell(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if isValid(board, row, col, num):
            board[row][col] = num
            if solveBoard(board):
                return True
            board[row][col] = 0
    return False

def isBoardSolvable(board):
    boardCopy = [row[:] for row in board]
    return solveBoard(boardCopy)
