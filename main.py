from cmu_graphics import *
import random
import os
from themes import lightTheme, darkTheme, redTheme, blueTheme, greenTheme
from screens import SplashScreen, HelpScreen, PlayScreen

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
    app.width = 600
    app.height = 600
    app.menuBarHeight = 50
    app.menuBarButtonBuffer = 10
    app.buttonWidth = 100
    app.activeScreen = 'splash'
    app.themes = [lightTheme, darkTheme, redTheme, blueTheme, greenTheme]
    app.themeIndex = 0
    app.theme = app.themes[app.themeIndex]
    app.splashScreen = SplashScreen(app)
    app.playScreen = PlayScreen(app)
    app.helpScreen = HelpScreen(app)
    app.boards, app.solutions = loadBoards()
    app.splashScreen.setup()
    app.playScreen.setup()
    app.helpScreen.setup()

def updateGridDimensions(app):
    app.gridWidth = app.width
    app.gridHeight = app.height - app.menuBarHeight
    app.activeColor = app.theme.activeColor if app.isGuessMode else app.theme.activeColor
    app.cellWidth = app.gridWidth / app.gridSize
    app.cellHeight = app.gridHeight / app.gridSize

def isNumberValid(app, row, col, num):
    if app.grid[row][col] == num: return True
    for i in range(len(app.grid)):
        if app.grid[row][col] == num or app.grid[i][col] == num: return False
    subGrid = [app.grid[r][col//3*3:(col//3+1)*3] for r in range(row//3*3, (row//3+1)*3)]
    for line in subGrid:
        if num in line: return False
    return True

def onKeyPress(app, key):
    if not app.isGameOver and app.grid[app.activeRow][app.activeCol] is None:
        if key.isdigit() and key != '0' and not app.isGuessMode:
            app.cellGuesses[app.activeRow][app.activeCol] = [None for _ in range(app.gridSize)]
            if isNumberValid(app, app.activeRow, app.activeCol, int(key)):
                app.isIncorrect = False
                app.grid[app.activeRow][app.activeCol] = int(key)
                app.gridColors[app.activeRow][app.activeCol] = app.theme.correctGuessColor
                app.cellStatus[app.activeRow][app.activeCol] = 'correct'
                if app.grid == app.solutionBoard:
                    app.isGameOver = True
            else:
                app.remainingLives -= 1
                app.isIncorrect = True
                app.gridColors[app.activeRow][app.activeCol] = app.theme.wrongGuessColor
                app.cellStatus[app.activeRow][app.activeCol] = 'incorrect'
        elif key.isdigit() and key != '0' and app.isGuessMode and app.grid[app.activeRow][app.activeCol] is None:
            app.cellGuesses[app.activeRow][app.activeCol][int(key) - 1] = int(key)
        elif key == 'g':
            app.isGuessMode = not app.isGuessMode
        elif key == 'backspace':
            if app.cellStatus[app.activeRow][app.activeCol] != 'correct':
                app.grid[app.activeRow][app.activeCol] = None
                app.gridColors[app.activeRow][app.activeCol] = app.theme.cellColor
                app.cellStatus[app.activeRow][app.activeCol] = 'normal'
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
    app.gridColors = [[app.theme.cellColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if app.cellStatus[row][col] == 'correct':
                app.gridColors[row][col] = app.theme.correctGuessColor
    app.gridColors[app.activeRow][app.activeCol] = app.activeColor

def redrawAll(app):
    if app.activeScreen == 'splash':
        app.splashScreen.draw()
    elif app.activeScreen == 'play':
        app.playScreen.draw()
    elif app.activeScreen == 'help':
        app.helpScreen.draw()

def onStep(app):
    updateGridDimensions(app)
    if not app.isIncorrect:
        app.gridColors = [[app.theme.cellColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
        for row in range(app.gridSize):
            for col in range(app.gridSize):
                if app.cellStatus[row][col] == 'correct':
                    app.gridColors[row][col] = app.theme.correctGuessColor
        app.gridColors[app.activeRow][app.activeCol] = app.activeColor
    app.fontSize = (calculateCellSize(app)[0] + calculateCellSize(app)[0]) // 4
    if app.remainingLives == 0: app.isGameOver = True

def onMousePress(app, mouseX, mouseY):
    if app.activeScreen == 'splash':
        app.splashScreen.onMousePress(mouseX, mouseY)
    elif app.activeScreen == 'play':
        app.playScreen.onMousePress(mouseX, mouseY)
    elif app.activeScreen == 'help':
        app.helpScreen.onMousePress(mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.activeScreen == 'splash':
        app.splashScreen.onMouseRelease(mouseX, mouseY)
    elif app.activeScreen == 'play':
        app.playScreen.onMouseRelease(mouseX, mouseY)
    elif app.activeScreen == 'help':
        app.helpScreen.onMouseRelease(mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    if app.activeScreen == 'splash':
        app.splashScreen.onHover(mouseX, mouseY)
    elif app.activeScreen == 'play':
        app.playScreen.onHover(mouseX, mouseY)
    elif app.activeScreen == 'help':
        app.helpScreen.onHover(mouseX, mouseY)

def drawMenuBar(app):
    buttonHeight = app.menuBarHeight - 2 * app.menuBarButtonBuffer
    buttonY = app.height - app.menuBarButtonBuffer - buttonHeight
    buttonWidth = app.buttonWidth

    drawRect(0, app.height - app.menuBarHeight, app.width, app.menuBarHeight, fill=app.theme.bgColor, border=app.theme.buttonBorderColor)
    
    distanceBetweenLivesDisplays = app.menuBarButtonBuffer / 2

    drawLives(app, buttonY, buttonHeight, distanceBetweenLivesDisplays)

def drawLives(app, buttonY, buttonSize, distanceBetweenButtons):
    for i in range(app.totalLives):
        fillColor = 'lightgreen' if i < app.remainingLives else 'tomato'
        drawRect(app.menuBarButtonBuffer + i * (buttonSize + distanceBetweenButtons), buttonY, buttonSize, buttonSize, fill=fillColor, border=app.theme.gridColor)

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
    drawRect(app.gridPaddingX, app.gridPaddingY, app.gridWidth, app.gridHeight, fill=None, border=app.theme.gridColor, borderWidth=2 * app.cellBorderThickness)
    for i in range(1, 3):
        drawLine(app.gridPaddingX + app.gridWidth * i / 3, app.gridPaddingY, app.gridPaddingX + app.gridWidth * i / 3, app.gridPaddingY + app.gridHeight, lineWidth=4, fill=app.theme.gridColor)
        drawLine(app.gridPaddingX, app.gridPaddingY + app.gridHeight * i / 3, app.gridPaddingX + app.gridWidth, app.gridPaddingY + app.gridHeight * i / 3, lineWidth=4, fill=app.theme.gridColor)

def drawGridCell(app, row, col):
    cellLeft, cellTop = getGridCellLeftTop(app, row, col)
    cellWidth, cellHeight = calculateCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=app.gridColors[row][col], border='grey', borderWidth=app.cellBorderThickness)
    if app.grid[row][col] is not None:
        drawLabel(app.grid[row][col], cellLeft + cellWidth // 2, cellTop + cellHeight // 2, size=app.fontSize, fill=app.theme.textColor)
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

def main():
    runApp(width=600, height=600)

main()
