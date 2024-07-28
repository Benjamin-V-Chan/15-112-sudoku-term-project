from cmu_graphics import *
import random
import os

def loadBoards():
    difficulties = ['easy', 'medium', 'hard', 'expert', 'evil']
    boards = {difficulty: [] for difficulty in difficulties}
    solutions = {difficulty: [] for difficulty in difficulties}

    for difficulty in difficulties:
        board_files = [f for f in os.listdir('boards') if f.startswith(difficulty)]
        board_files = board_files[:3]
        for file in board_files:
            with open(f'boards/{file}', 'r') as f:
                board = [list(map(int, line.strip().split())) for line in f]
                boards[difficulty].append(board)
            solution_file = file.replace('.png.txt', '-solution.png-solution.txt')
            with open(f'solutions/{solution_file}', 'r') as f:
                solution = [list(map(int, line.strip().split())) for line in f]
                solutions[difficulty].append(solution)
    
    return boards, solutions

def onAppStart(app):
    app.difficulty = 'easy'
    app.boards, app.solutions = loadBoards()
    app.selectedBoardIndex = random.randint(0, len(app.boards[app.difficulty]) - 1)
    app.selectedBoard = app.boards[app.difficulty][app.selectedBoardIndex]
    app.solutionBoard = app.solutions[app.difficulty][app.selectedBoardIndex]

    app.gridSize = 9
    app.gridPaddingX = 0
    app.gridPaddingY = 0
    app.windowWidth, app.windowHeight = 600, 700
    app.cellBorderThickness = 2
    app.grid = [[None if cell == 0 else cell for cell in row] for row in app.selectedBoard]
    app.gridColors = [['white' for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.activeRow, app.activeCol = 0, 0
    app.isGuessMode = False
    app.activeColor = 'cyan'
    app.gridColors[app.activeRow][app.activeCol] = app.activeColor
    app.cellGuesses = [[[None for _ in range(app.gridSize)] for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.fontSize = 22
    app.remainingLives = 3
    app.isIncorrect = False
    app.isGameOver = False
    app.theme = 'light'
    updateGridDimensions(app)
    updateTheme(app)

def updateGridDimensions(app):
    app.gridWidth = app.windowWidth
    app.gridHeight = 0.85 * app.windowHeight
    app.activeColor = 'lightgrey' if app.isGuessMode else 'cyan'
    app.cellWidth = app.gridWidth / app.gridSize
    app.cellHeight = app.gridHeight / app.gridSize

def updateTheme(app):
    if app.theme == 'light':
        app.bgColor = 'white'
        app.fgColor = 'black'
    else:
        app.bgColor = 'black'
        app.fgColor = 'white'

def isNumberValid(app, row, col, num):
    if app.grid[row][col] == num: return True
    for i in range(len(app.grid)):
        if app.grid[row][col] == num or app.grid[i][col] == num: return False
    subGrid = [app.grid[r][col//3*3:(col//3+1)*3] for r in range(row//3*3, (row//3+1)*3)]
    for line in subGrid:
        if num in line: return False
    return True

def onKeyPress(app, key):
    if not app.isGameOver:
        if key.isdigit() and key != '0' and not app.isGuessMode:
            app.cellGuesses[app.activeRow][app.activeCol] = [None for _ in range(app.gridSize)]
            if isNumberValid(app, app.activeRow, app.activeCol, int(key)):
                app.isIncorrect = False
                app.grid[app.activeRow][app.activeCol] = int(key)
                app.gridColors[app.activeRow][app.activeCol] = 'lightGreen'
                if app.grid == app.solutionBoard:
                    app.isGameOver = True
            else:
                app.remainingLives -= 1
                app.isIncorrect = True
                app.gridColors[app.activeRow][app.activeCol] = 'tomato'
        elif key.isdigit() and key != '0' and app.isGuessMode and app.grid[app.activeRow][app.activeCol] is None:
            app.cellGuesses[app.activeRow][app.activeCol][int(key) - 1] = int(key)
        elif key == 'g':
            app.isGuessMode = not app.isGuessMode
        elif key == 'backspace':
            app.grid[app.activeRow][app.activeCol] = None
            app.gridColors[app.activeRow][app.activeCol] = app.bgColor
        elif key in ['up', 'down', 'left', 'right']:
            navigateGrid(app, key)

def navigateGrid(app, direction):
    if direction == 'up' and app.activeRow > 0:
        app.activeRow -= 1
    elif direction == 'down' and app.activeRow < app.gridSize - 1:
        app.activeRow += 1
    elif direction == 'left' and app.activeCol > 0:
        app.activeCol -= 1
    elif direction == 'right' and app.activeCol < app.gridSize - 1:
        app.activeCol += 1
    app.gridColors = [[app.bgColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.gridColors[app.activeRow][app.activeCol] = app.activeColor

def redrawAll(app):
    drawRect(0, 0, app.windowWidth, app.windowHeight, fill=app.bgColor)
    drawGrid(app)
    drawGridBorder(app)
    drawMenuBar(app)

def onStep(app):
    updateGridDimensions(app)
    if not app.isIncorrect:
        app.gridColors = [[app.bgColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
        app.gridColors[app.activeRow][app.activeCol] = app.activeColor
    app.fontSize = (calculateCellSize(app)[0] + calculateCellSize(app)[0]) // 4
    if app.remainingLives == 0: app.isGameOver = True

def onMousePress(app, mouseX, mouseY):
    if 10 <= mouseX <= 10 + 3 * 30 and app.windowHeight - 40 <= mouseY <= app.windowHeight - 20:
        pass
    elif app.windowWidth / 2 - 50 <= mouseX <= app.windowWidth / 2 + 50 and app.windowHeight - 40 <= mouseY <= app.windowHeight - 10:
        resetBoard(app)
    elif app.windowWidth - 120 <= mouseX <= app.windowWidth - 20 and app.windowHeight - 40 <= mouseY <= app.windowHeight - 10:
        changeTheme(app)
    else:
        if not app.isGameOver:
            app.activeRow, app.activeCol = getGridCell(app, mouseX, mouseY)
            if app.isIncorrect:
                app.isIncorrect = False

def resetBoard(app):
    app.selectedBoardIndex = random.randint(0, len(app.boards[app.difficulty]) - 1)
    app.selectedBoard = app.boards[app.difficulty][app.selectedBoardIndex]
    app.solutionBoard = app.solutions[app.difficulty][app.selectedBoardIndex]
    app.grid = [[None if cell == 0 else cell for cell in row] for row in app.selectedBoard]
    app.gridColors = [[app.bgColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.cellGuesses = [[[None for _ in range(app.gridSize)] for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.activeRow, app.activeCol = 0, 0
    app.remainingLives = 3
    app.isIncorrect = False
    app.isGameOver = False

def changeTheme(app):
    app.theme = 'dark' if app.theme == 'light' else 'light'
    updateTheme(app)
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            app.gridColors[row][col] = app.bgColor
    app.gridColors[app.activeRow][app.activeCol] = app.activeColor

def drawMenuBar(app):
    drawRect(0, 0.85 * app.windowHeight, app.windowWidth, 0.15 * app.windowHeight, fill=app.bgColor, border=app.fgColor)
    drawLivesBar(app)
    drawRect(app.windowWidth / 2 - 50, app.windowHeight - 40, 100, 30, fill=app.fgColor, border=app.fgColor)
    drawLabel('Reset', app.windowWidth / 2, app.windowHeight - 25, size=15, fill=app.bgColor)
    drawRect(app.windowWidth - 120, app.windowHeight - 40, 100, 30, fill=app.fgColor, border=app.fgColor)
    drawLabel('Change Theme', app.windowWidth - 70, app.windowHeight - 25, size=15, fill=app.bgColor)

def drawLivesBar(app):
    livesColor = 'red'
    for i in range(3):
        if i < app.remainingLives:
            fillColor = 'lightgreen'
        else:
            fillColor = livesColor
        drawRect(10 + i*30, app.windowHeight - 40, 20, 20, fill=fillColor, border=app.fgColor)

def getGridCell(app, x, y):
    cellWidth, cellHeight = calculateCellSize(app)
    row, col = int(y // cellHeight), int(x // cellWidth)
    if row >= app.gridSize: row = app.gridSize - 1
    if col >= app.gridSize: col = app.gridSize - 1
    return row, col

def drawGrid(app):
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            drawGridCell(app, row, col)

def drawGridBorder(app):
    drawRect(app.gridPaddingX, app.gridPaddingY, app.gridWidth, app.gridHeight, fill=None, border=app.fgColor, borderWidth=2 * app.cellBorderThickness)
    for i in range(1, 3):
        drawLine(app.gridPaddingX + app.gridWidth * i / 3, app.gridPaddingY, app.gridPaddingX + app.gridWidth * i / 3, app.gridPaddingY + app.gridHeight, lineWidth=4, fill=app.fgColor)
        drawLine(app.gridPaddingX, app.gridPaddingY + app.gridHeight * i / 3, app.gridPaddingX + app.gridWidth, app.gridPaddingY + app.gridHeight * i / 3, lineWidth=4, fill=app.fgColor)

def drawGridCell(app, row, col):
    cellLeft, cellTop = getGridCellLeftTop(app, row, col)
    cellWidth, cellHeight = calculateCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=app.gridColors[row][col], border='grey', borderWidth=app.cellBorderThickness)
    if app.grid[row][col] is not None:
        drawLabel(app.grid[row][col], cellLeft + cellWidth // 2, cellTop + cellHeight // 2, size=app.fontSize, fill=app.fgColor)
    for i in range(9):
        if app.cellGuesses[row][col][i] is not None:
            num = app.cellGuesses[row][col][i]
            xPos = cellWidth / 3 * (i % 3 + 1) - (cellWidth // 3) * 0.5
            yPos = cellHeight / 3 * (i // 3 + 1) - (cellHeight // 3) * 0.5
            drawLabel(str(num), cellLeft + xPos, cellTop + yPos, size=app.fontSize // 2.5, fill='grey')

def getGridCellLeftTop(app, row, col):
    cellWidth, cellHeight = calculateCellSize(app)
    cellLeft = app.gridPaddingX + col * cellWidth
    cellTop = app.gridPaddingY + row * cellHeight
    return cellLeft, cellTop

def calculateCellSize(app):
    cellWidth = app.gridWidth / app.gridSize
    cellHeight = app.gridHeight / app.gridSize
    return cellWidth, cellHeight

runApp(width=600, height=700)