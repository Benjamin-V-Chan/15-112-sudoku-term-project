import random
import copy

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
        boardCopy = copy.deepcopy(board)
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

def isValid(board, row, col, num):
    board = noneToZero(board)
    for i in range(9):
        if (board[row][i] == num and i != col) or (board[i][col] == num and i != row):
            return False
    boxRow, boxCol = row // 3 * 3, col // 3 * 3
    for i in range(boxRow, boxRow + 3):
        for j in range(boxCol, boxCol + 3):
            if board[i][j] == num and (i, j) != (row, col):
                return False
    return True

def noneToZero(board):
    boardCopy = copy.deepcopy(board)
    for row in range(9):
        for col in range(9):
            if boardCopy[row][col] is None:
                boardCopy[row][col] = 0
    return boardCopy

def removeNumbers(board, count):
    attempts = 81 - count
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        backup = board[row][col]
        board[row][col] = 0
        boardCopy = copy.deepcopy(board)
        if not solveBoard(boardCopy):
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
    boardCopy = copy.deepcopy(board)
    return solveBoard(boardCopy)