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
    def __init__(self, bgColor, buttonColor, buttonBorderColor, textColor, hoverBorderColor, clickColor):
        self.bgColor = bgColor
        self.buttonColor = buttonColor
        self.buttonBorderColor = buttonBorderColor
        self.textColor = textColor
        self.hoverBorderColor = hoverBorderColor
        self.clickColor = clickColor

# Define the themes
lightTheme = Theme(bgColor='white', buttonColor='lightgray', buttonBorderColor='black', textColor='black', hoverBorderColor='cyan', clickColor='darkgray')
darkTheme = Theme(bgColor='black', buttonColor='darkgray', buttonBorderColor='white', textColor='white', hoverBorderColor='lightcyan', clickColor='gray')

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
    app.theme = darkTheme
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

    def onMousePress(self, mouseX, mouseY):
        for i, button in enumerate(self.buttons):
            if button.checkClicked(mouseX, mouseY):
                button.onClick()
                self.app.playScreen.setDifficulty(self.messages[i])
                self.app.activeScreen = 'play'
                return

    def onMouseRelease(self, mouseX, mouseY):
        for button in self.buttons:
            button.onRelease()

    def onHover(self, mouseX, mouseY):
        for button in self.buttons:
            button.onHover(mouseX, mouseY)

    def draw(self):
        drawRect(0, 0, self.app.width, self.app.height, fill=self.app.theme.bgColor)
        self.drawTitle()
        self.drawButtons()

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
        self.app.gridColors = [['white' for _ in range(self.app.gridSize)] for _ in range(self.app.gridSize)]
        self.app.activeRow, self.app.activeCol = 0, 0
        self.app.isGuessMode = False
        self.app.activeColor = 'cyan'
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
    app.activeColor = 'lightgrey' if app.isGuessMode else 'lightSkyBlue'
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
            app.gridColors[app.activeRow][app.activeCol] = 'white'
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
    app.gridColors = [['white' for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.gridColors[app.activeRow][app.activeCol] = app.activeColor

def redrawAll(app):
    if app.activeScreen == 'splash':
        app.splashScreen.draw()
    elif app.activeScreen == 'play':
        app.playScreen.draw()

def onStep(app):
    updateGridDimensions(app)
    if not app.isIncorrect:
        app.gridColors = [['white' for _ in range(app.gridSize)] for _ in range(app.gridSize)]
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
    textY = app.height - (app.menuBarHeight / 2)
    buttonWidth = app.buttonWidth

    # Actual Menu Bar Display
    drawRect(0, app.height - app.menuBarHeight, app.width, app.menuBarHeight, fill=app.theme.bgColor, border=app.theme.buttonBorderColor)
    
    distanceBetweenLivesDisplays = app.menuBarButtonBuffer / 2

    drawLives(app, buttonY, buttonHeight, distanceBetweenLivesDisplays)

def drawLives(app, buttonY, buttonSize, distanceBetweenButtons):
    livesColor = 'tomato'
    for i in range(app.totalLives):
        if i < app.remainingLives:
            fillColor = 'lightgreen'
        else:
            fillColor = livesColor
        drawRect(app.menuBarButtonBuffer + i * (buttonSize + distanceBetweenButtons), buttonY, buttonSize, buttonSize, fill=fillColor, border='black')

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
    drawRect(app.gridPaddingX, app.gridPaddingY, app.gridWidth, app.gridHeight, fill=None, border='black', borderWidth=2 * app.cellBorderThickness)
    for i in range(1, 3):
        drawLine(app.gridPaddingX + app.gridWidth * i / 3, app.gridPaddingY, app.gridPaddingX + app.gridWidth * i / 3, app.gridPaddingY + app.gridHeight, lineWidth=4, fill='black')
        drawLine(app.gridPaddingX, app.gridPaddingY + app.gridHeight * i / 3, app.gridPaddingX + app.gridWidth, app.gridPaddingY + app.gridHeight * i / 3, lineWidth=4, fill='black')

def drawGridCell(app, row, col):
    cellLeft, cellTop = getGridCellLeftTop(app, row, col)
    cellWidth, cellHeight = calculateCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=app.gridColors[row][col], border='grey', borderWidth=app.cellBorderThickness)
    if app.grid[row][col] is not None:
        drawLabel(app.grid[row][col], cellLeft + cellWidth // 2, cellTop + cellHeight // 2, size=app.fontSize, fill='black')
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
