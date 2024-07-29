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

class Theme:
    def __init__(self, bgColor, buttonColor, buttonBorderColor, textColor, hoverBorderColor, clickColor, gridColor, cellColor, activeColor, correctGuessColor, wrongGuessColor):
        self.bgColor = bgColor
        self.buttonColor = buttonColor
        self.buttonBorderColor = buttonBorderColor
        self.textColor = textColor
        self.hoverBorderColor = hoverBorderColor
        self.clickColor = clickColor
        self.gridColor = gridColor
        self.cellColor = cellColor
        self.activeColor = activeColor
        self.correctGuessColor = correctGuessColor
        self.wrongGuessColor = wrongGuessColor

# Define the themes
lightTheme = Theme(bgColor='white', buttonColor='lightgray', buttonBorderColor='black', textColor='black', hoverBorderColor='cyan', clickColor='darkgray', gridColor='black', cellColor='white', activeColor='lightSkyBlue', correctGuessColor='lightGreen', wrongGuessColor='tomato')
darkTheme = Theme(bgColor='black', buttonColor='darkgray', buttonBorderColor='white', textColor='white', hoverBorderColor='lightcyan', clickColor='gray', gridColor='white', cellColor='black', activeColor='lightgrey', correctGuessColor='darkgreen', wrongGuessColor='red')
redTheme = Theme(bgColor='darkred', buttonColor='red', buttonBorderColor='black', textColor='white', hoverBorderColor='lightcoral', clickColor='maroon', gridColor='black', cellColor='red', activeColor='pink', correctGuessColor='darkgreen', wrongGuessColor='orange')
blueTheme = Theme(bgColor='darkblue', buttonColor='blue', buttonBorderColor='black', textColor='white', hoverBorderColor='lightblue', clickColor='navy', gridColor='black', cellColor='blue', activeColor='skyblue', correctGuessColor='darkgreen', wrongGuessColor='orange')
greenTheme = Theme(bgColor='darkgreen', buttonColor='green', buttonBorderColor='black', textColor='white', hoverBorderColor='lightgreen', clickColor='forestgreen', gridColor='black', cellColor='green', activeColor='lightgreen', correctGuessColor='darkgreen', wrongGuessColor='orange')

class Button:
    def __init__(self, x, y, width, height, text, theme, textSize=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textSize = textSize
        self.theme = theme
        self.isHovered = False
        self.isClicked = False

    def draw(self):
        borderColor = self.theme.hoverBorderColor if self.isHovered else self.theme.buttonBorderColor
        fillColor = self.theme.clickColor if self.isClicked else self.theme.buttonColor
        drawRect(self.x, self.y, self.width, self.height, fill=fillColor, border=borderColor)
        drawLabel(self.text, self.x + self.width / 2, self.y + self.height / 2, size=self.textSize, fill=self.theme.textColor, bold=True, align='center')

    def checkClicked(self, mouseX, mouseY):
        return self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height

    def onHover(self, mouseX, mouseY):
        self.isHovered = self.checkClicked(mouseX, mouseY)

    def onClick(self):
        self.isClicked = True

    def onRelease(self):
        self.isClicked = False

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
    app.boards, app.solutions = loadBoards()
    app.splashScreen.setup()
    app.playScreen.setup()

class SplashScreen:
    def __init__(self, app):
        self.app = app

    def setup(self):
        self.colors = [rgb(255, 99, 71), rgb(255, 69, 0), rgb(255, 140, 0), rgb(255, 165, 0), rgb(255, 215, 0)]
        self.messages = ['easy', 'medium', 'hard', 'expert', 'evil']
        self.buttonWidth = 150
        self.buttonHeight = 50
        self.buttonSpacing = 25
        self.title = 'SUDOKU'
        self.titleSize = 55
        self.buttons = [
            Button(
                self.app.width / 2 - self.buttonWidth / 2, 
                180 + i * (self.buttonHeight + self.buttonSpacing), 
                self.buttonWidth, 
                self.buttonHeight, 
                self.messages[i], 
                self.app.theme
            ) for i in range(5)
        ]
        self.changeThemeButton = Button(self.app.width - self.buttonWidth - 20, self.app.height - self.buttonHeight - 20, self.buttonWidth, self.buttonHeight, 'Change Theme', self.app.theme)

    def onMousePress(self, mouseX, mouseY):
        for i, button in enumerate(self.buttons):
            if button.checkClicked(mouseX, mouseY):
                button.onClick()
                self.app.playScreen.setDifficulty(self.messages[i])
                self.app.activeScreen = 'play'
                return
        if self.changeThemeButton.checkClicked(mouseX, mouseY):
            self.changeThemeButton.onClick()
            self.app.themeIndex = (self.app.themeIndex + 1) % len(self.app.themes)
            self.app.theme = self.app.themes[self.app.themeIndex]
            self.setup()
            self.app.playScreen.setup()

    def onMouseRelease(self, mouseX, mouseY):
        for button in self.buttons:
            button.onRelease()
        self.changeThemeButton.onRelease()

    def onHover(self, mouseX, mouseY):
        for button in self.buttons:
            button.onHover(mouseX, mouseY)
        self.changeThemeButton.onHover(mouseX, mouseY)

    def draw(self):
        drawRect(0, 0, self.app.width, self.app.height, fill=self.app.theme.bgColor)
        self.drawTitle()
        self.drawButtons()
        self.changeThemeButton.draw()

    def drawTitle(self):
        titleX = self.app.width / 2
        titleY = 100
        drawLabel(self.title, titleX, titleY, size=self.titleSize, fill=self.colors[0], bold=True, align='center', border='black', borderWidth=1)

    def drawButtons(self):
        for button in self.buttons:
            button.draw()

class PlayScreen:
    def __init__(self, app):
        self.app = app
        self.difficulty = 'easy'

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.setup()

    def setup(self):
        self.pickNewBoard()

        self.app.gridSize = 9
        self.app.gridPaddingX = 0
        self.app.gridPaddingY = 0
        self.app.cellBorderThickness = 2
        self.app.grid = [[None if cell == 0 else cell for cell in row] for row in self.app.selectedBoard]
        self.app.gridColors = [[self.app.theme.cellColor for _ in range(self.app.gridSize)] for _ in range(self.app.gridSize)]
        self.app.activeRow, self.app.activeCol = 0, 0
        self.app.isGuessMode = False
        self.app.activeColor = self.app.theme.activeColor
        self.app.cellStatus = [['normal' for _ in range(self.app.gridSize)] for _ in range(self.app.gridSize)] # 'normal', 'correct', 'incorrect'
        self.app.gridColors[self.app.activeRow][self.app.activeCol] = self.app.activeColor
        self.app.cellGuesses = [[[None for _ in range(self.app.gridSize)] for _ in range(self.app.gridSize)] for _ in range(self.app.gridSize)]
        self.app.fontSize = 22
        self.app.totalLives = 3
        self.app.remainingLives = self.app.totalLives
        self.app.isIncorrect = False
        self.app.isGameOver = False
        updateGridDimensions(self.app)
        self.setupButtons()

    def pickNewBoard(self):
        availableBoards = len(self.app.boards[self.difficulty])
        newBoardIndex = random.randint(0, availableBoards - 1)
        if hasattr(self.app, 'selectedBoardIndex'):
            while newBoardIndex == self.app.selectedBoardIndex:
                newBoardIndex = random.randint(0, availableBoards - 1)
        self.app.selectedBoardIndex = newBoardIndex
        self.app.selectedBoard = self.app.boards[self.difficulty][self.app.selectedBoardIndex]
        self.app.solutionBoard = self.app.solutions[self.difficulty][self.app.selectedBoardIndex]

    def setupButtons(self):
        buttonHeight = self.app.menuBarHeight - 2 * self.app.menuBarButtonBuffer
        buttonY = self.app.height - self.app.menuBarHeight + self.app.menuBarButtonBuffer
        buttonWidth = self.app.buttonWidth

        self.resetButton = Button(self.app.width / 2 - buttonWidth / 2, buttonY, buttonWidth, buttonHeight, 'Reset', self.app.theme)
        self.homeButton = Button(self.app.width - buttonWidth - self.app.menuBarButtonBuffer, buttonY, buttonWidth, buttonHeight, 'Home', self.app.theme)
        self.buttons = [self.resetButton, self.homeButton]

    def onMousePress(self, mouseX, mouseY):
        for button in self.buttons:
            if button.checkClicked(mouseX, mouseY):
                button.onClick()
                if button.text == 'Reset':
                    self.pickNewBoard()
                    self.setup()
                elif button.text == 'Home':
                    self.app.activeScreen = 'splash'
                return
        if not self.app.isGameOver:
            self.app.activeRow, self.app.activeCol = getGridCell(self.app, mouseX, mouseY)
            if self.app.isIncorrect:
                self.app.isIncorrect = False

    def onMouseRelease(self, mouseX, mouseY):
        for button in self.buttons:
            button.onRelease()

    def onHover(self, mouseX, mouseY):
        for button in self.buttons:
            button.onHover(mouseX, mouseY)

    def draw(self):
        drawRect(0, 0, self.app.width, self.app.height, fill=self.app.theme.bgColor)
        drawGrid(self.app)
        drawGridBorder(self.app)
        drawMenuBar(self.app)
        self.drawButtons()

    def drawButtons(self):
        for button in self.buttons:
            button.draw()

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

def onMouseRelease(app, mouseX, mouseY):
    if app.activeScreen == 'splash':
        app.splashScreen.onMouseRelease(mouseX, mouseY)
    elif app.activeScreen == 'play':
        app.playScreen.onMouseRelease(mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    if app.activeScreen == 'splash':
        app.splashScreen.onHover(mouseX, mouseY)
    elif app.activeScreen == 'play':
        app.playScreen.onHover(mouseX, mouseY)

def drawMenuBar(app):
    buttonHeight = app.menuBarHeight - 2 * app.menuBarButtonBuffer
    buttonY = app.height - app.menuBarHeight + app.menuBarButtonBuffer
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

runApp(width=600, height=600)
