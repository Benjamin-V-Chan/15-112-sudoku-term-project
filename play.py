from cmu_graphics import *
from sudokuGenerator import *
from button import Button

def setupPlayScreen(app):
    app.gridSize = 9
    app.gridPaddingX = 0
    app.gridPaddingY = 0
    app.cellBorderThickness = 2
    app.fontSize = 22
    app.highlightedRow, app.highlightedCol = 0, 0
    app.totalLives = 3
    app.remainingLives = app.totalLives
    app.isGameOver = False
    app.tempIncorrect = {}  # Track temporarily incorrect guesses
    resetPlayScreen(app)
    generateAndSetupGrid(app)

def resetPlayScreen(app):
    app.totalLives = 3
    app.remainingLives = app.totalLives
    app.isGameOver = False
    app.isGuessMode = False
    app.tempIncorrect = {}

def generateAndSetupGrid(app):
    app.grid, _ = generateBoard(app.difficulty)
    app.grid = [[None if cell == 0 else cell for cell in row] for row in app.grid]
    app.gridColors = [[app.theme.cellColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.cellStatus = [['normal' for _ in range(app.gridSize)] for _ in range(app.gridSize)]  # 'normal', 'correct', 'incorrect', 'starting', 'guess'
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if app.grid[row][col] is not None:
                app.cellStatus[row][col] = 'starting'
    app.gridColors[app.highlightedRow][app.highlightedCol] = app.theme.highlightedColor
    app.cellGuesses = [[[None for _ in range(app.gridSize)] for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    updateGridDimensions(app)
    setupPlayButtons(app)

def setupPlayButtons(app):
    buttonHeight = app.menuBarHeight - 2 * app.menuBarButtonBuffer
    buttonY = app.height - app.menuBarButtonBuffer - buttonHeight
    buttonWidth = app.buttonWidth
    app.resetButton = Button(app.width / 2 - buttonWidth / 2, buttonY, buttonWidth, buttonHeight, 'Reset', app.theme)
    app.homeButton = Button(app.width - buttonWidth - app.menuBarButtonBuffer, buttonY, buttonWidth, buttonHeight, 'Home', app.theme)
    app.playButtons = [app.resetButton, app.homeButton]

def play_onMousePress(app, mouseX, mouseY):
    for button in app.playButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Reset':
                resetPlayScreen(app)
                generateAndSetupGrid(app)
            elif button.text == 'Home':
                setActiveScreen('splash')
            return
    if not app.isGameOver:
        app.highlightedRow, app.highlightedCol = getGridCell(app, mouseX, mouseY)
        updateCellColors(app)

def play_onMouseRelease(app, mouseX, mouseY):
    for button in app.playButtons:
        button.onRelease()

def play_onMouseMove(app, mouseX, mouseY):
    for button in app.playButtons:
        button.onHover(mouseX, mouseY)

def play_onKeyPress(app, key):
    removeIncorrectGuesses(app)
    if not app.isGameOver:
        if key in ['up', 'down', 'left', 'right']:
            navigateGrid(app, key)
        elif key.isdigit() and key != '0' and not app.isGuessMode and (app.cellStatus[app.highlightedRow][app.highlightedCol] not in ['correct', 'starting']):
            app.grid[app.highlightedRow][app.highlightedCol] = int(key)
            if isValid(app.grid, app.highlightedRow, app.highlightedCol, int(key)):
                app.cellStatus[app.highlightedRow][app.highlightedCol] = 'correct'
                if all(cell is not None for row in app.grid for cell in row):
                    app.isGameOver = True
            else:
                app.remainingLives -= 1
                app.cellStatus[app.highlightedRow][app.highlightedCol] = 'incorrect'
                app.grid[app.highlightedRow][app.highlightedCol] = None
                if app.remainingLives <= 0:
                    app.isGameOver = True
                app.tempIncorrect[(app.highlightedRow, app.highlightedCol)] = int(key)
            app.cellGuesses[app.highlightedRow][app.highlightedCol] = [None for _ in range(app.gridSize)]
        elif key.isdigit() and key != '0' and app.isGuessMode and (app.cellStatus[app.highlightedRow][app.highlightedCol] not in ['correct', 'starting']):
            app.cellGuesses[app.highlightedRow][app.highlightedCol][int(key) - 1] = int(key)
        elif key == 'g':
            app.isGuessMode = not app.isGuessMode
    updateCellColors(app)

def updateGridDimensions(app):
    app.gridWidth = app.width
    app.gridHeight = app.height - app.menuBarHeight
    app.highlightedColor = app.theme.highlightedColor if app.isGuessMode else app.theme.highlightedColor
    app.cellWidth = app.gridWidth / app.gridSize
    app.cellHeight = app.gridHeight / app.gridSize

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
    elif (row, col) in app.tempIncorrect:
        drawLabel(app.tempIncorrect[(row, col)], cellLeft + cellWidth // 2, cellTop + cellHeight // 2, size=app.fontSize, fill=app.theme.wrongGuessColor)
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

def drawMenuBar(app):
    buttonHeight = app.menuBarHeight - 2 * app.menuBarButtonBuffer
    buttonY = app.height - app.menuBarButtonBuffer - buttonHeight
    drawRect(0, app.height - app.menuBarHeight, app.width, app.menuBarHeight, fill=app.theme.bgColor, border=app.theme.buttonBorderColor)
    distanceBetweenLivesDisplays = app.menuBarButtonBuffer / 2
    drawLives(app, buttonY, buttonHeight, distanceBetweenLivesDisplays)

def drawLives(app, buttonY, buttonSize, distanceBetweenButtons):
    for i in range(app.totalLives):
        fillColor = 'lightgreen' if i < app.remainingLives else 'tomato'
        drawRect(app.menuBarButtonBuffer + i * (buttonSize + distanceBetweenButtons), buttonY, buttonSize, buttonSize, fill=fillColor, border=app.theme.gridColor)

def navigateGrid(app, direction):
    if direction == 'up' and app.highlightedRow > 0:
        app.highlightedRow -= 1
    elif direction == 'down' and app.highlightedRow < app.gridSize - 1:
        app.highlightedRow += 1
    elif direction == 'left' and app.highlightedCol > 0:
        app.highlightedCol -= 1
    elif direction == 'right' and app.highlightedCol < app.gridSize - 1:
        app.highlightedCol += 1
    updateCellColors(app)

def removeIncorrectGuesses(app):
    to_remove = []
    for (row, col), value in app.tempIncorrect.items():
        if app.cellStatus[row][col] != 'incorrect':
            to_remove.append((row, col))
    for (row, col) in to_remove:
        del app.tempIncorrect[(row, col)]

def updateCellColors(app):
    app.gridColors = [[app.theme.cellColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if (row, col) in app.tempIncorrect:
                app.gridColors[row][col] = app.theme.wrongGuessColor
            elif app.cellStatus[row][col] == 'correct':
                app.gridColors[row][col] = app.theme.correctGuessColor
            elif app.cellStatus[row][col] == 'starting':
                app.gridColors[row][col] = app.theme.cellColor
            elif app.cellStatus[row][col] == 'guess':
                app.gridColors[row][col] = app.theme.cellColor
            elif app.cellStatus[row][col] == 'normal':
                app.gridColors[row][col] = app.theme.cellColor
    app.gridColors[app.highlightedRow][app.highlightedCol] = app.theme.highlightedColor

def drawEndGameScreen(app):
    if app.isGameOver:
        drawRect(0, 0, app.width, app.height, fill='black')
        drawLabel('Game Over!', app.width / 2, app.height / 2, size=40, fill='white')
        drawLabel('Press "Reset" to play again', app.width / 2, app.height / 2 + 50, size=20, fill='white')
        drawLabel('Press "Home" to go back to the main menu', app.width / 2, app.height / 2 + 80, size=20, fill='white')

def play_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawGrid(app)
    drawGridBorder(app)
    drawMenuBar(app)
    drawEndGameScreen(app)
    for button in app.playButtons:
        button.draw()
