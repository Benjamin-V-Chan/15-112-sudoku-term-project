from cmu_graphics import *
from buttons import Button
from themes import lightTheme, darkTheme, redTheme, blueTheme, greenTheme

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
        self.helpButton = Button(self.app.width - self.buttonWidth - 20, self.app.height - 2 * self.buttonHeight - 40, self.buttonWidth, self.buttonHeight, 'Help', self.app.theme)

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
            self.app.helpScreen.setup()
        if self.helpButton.checkClicked(mouseX, mouseY):
            self.helpButton.onClick()
            self.app.activeScreen = 'help'

    def onMouseRelease(self, mouseX, mouseY):
        for button in self.buttons:
            button.onRelease()
        self.changeThemeButton.onRelease()
        self.helpButton.onRelease()

    def onHover(self, mouseX, mouseY):
        for button in self.buttons:
            button.onHover(mouseX, mouseY)
        self.changeThemeButton.onHover(mouseX, mouseY)
        self.helpButton.onHover(mouseX, mouseY)

    def draw(self):
        drawRect(0, 0, self.app.width, self.app.height, fill=self.app.theme.bgColor)
        self.drawTitle()
        self.drawButtons()
        self.changeThemeButton.draw()
        self.helpButton.draw()

    def drawTitle(self):
        titleX = self.app.width / 2
        titleY = 100
        drawLabel(self.title, titleX, titleY, size=self.titleSize, fill=self.colors[0], bold=True, align='center', border='black', borderWidth=1)

    def drawButtons(self):
        for button in self.buttons:
            button.draw()

class HelpScreen:
    def __init__(self, app):
        self.app = app
        self.currentPage = 0
        self.pages = [HelpPage(app, i, self.drawPageContent) for i in range(5)]
        self.prevButton = Button(20, self.app.height - self.app.menuBarHeight - 20, 100, 50, '< Prev', self.app.theme)
        self.nextButton = Button(self.app.width - 120, self.app.height - self.app.menuBarHeight - 20, 100, 50, 'Next >', self.app.theme)
        self.homeButton = Button(self.app.width / 2 - 50, self.app.height - self.app.menuBarHeight - 20, 100, 50, 'Home', self.app.theme)

    def setup(self):
        for page in self.pages:
            page.setup()

    def onMousePress(self, mouseX, mouseY):
        if self.prevButton.checkClicked(mouseX, mouseY):
            self.prevButton.onClick()
            if self.currentPage > 0:
                self.currentPage -= 1
        elif self.nextButton.checkClicked(mouseX, mouseY):
            self.nextButton.onClick()
            if self.currentPage < len(self.pages) - 1:
                self.currentPage += 1
        elif self.homeButton.checkClicked(mouseX, mouseY):
            self.homeButton.onClick()
            self.app.activeScreen = 'splash'

    def onMouseRelease(self, mouseX, mouseY):
        self.prevButton.onRelease()
        self.nextButton.onRelease()
        self.homeButton.onRelease()

    def onHover(self, mouseX, mouseY):
        self.prevButton.onHover(mouseX, mouseY)
        self.nextButton.onHover(mouseX, mouseY)
        self.homeButton.onHover(mouseX, mouseY)

    def draw(self):
        drawRect(0, 0, self.app.width, self.app.height, fill=self.app.theme.bgColor)
        self.pages[self.currentPage].draw()
        self.prevButton.draw()
        self.nextButton.draw()
        self.homeButton.draw()

    def drawPageContent(self, pageIndex):
        topBoxHeight = self.app.height // 4
        lineDistance = 30
        line1Y = topBoxHeight + 60
        line2Y = line1Y + lineDistance
        line3Y = line2Y + lineDistance
        line4Y = line3Y + lineDistance
        drawRect(0, 0, self.app.width, topBoxHeight, fill=self.app.theme.buttonColor, border=self.app.theme.buttonBorderColor)
        if pageIndex == 0:
            drawLabel('Welcome to Sudoku!', self.app.width / 2, topBoxHeight / 2, size=24, fill=self.app.theme.textColor, align='center')
            drawLabel('In this game, you need to fill the grid so that each row,', self.app.width / 2, line1Y, size=18, fill=self.app.theme.textColor, align='center')
            drawLabel('column, and 3x3 box contains the numbers 1 to 9', self.app.width / 2, line2Y, size=18, fill=self.app.theme.textColor, align='center')
            drawLabel('without repeating.', self.app.width / 2, line3Y, size=18, fill=self.app.theme.textColor, align='center')        
        elif pageIndex == 1:
            drawLabel('How to Start a Game', self.app.width / 2, topBoxHeight / 2, size=24, fill=self.app.theme.textColor, align='center')
            drawLabel('On the home screen, select a difficulty level', self.app.width / 2, line1Y, size=18, fill=self.app.theme.textColor, align='center')
            drawLabel('to start a new game.', self.app.width / 2, line2Y, size=18, fill=self.app.theme.textColor, align='center')
        elif pageIndex == 2:
            drawLabel('Gameplay Instructions', self.app.width / 2, topBoxHeight / 2, size=24, fill=self.app.theme.textColor, align='center')
            drawLabel('Use the arrow keys to navigate the grid and', self.app.width / 2, line1Y, size=18, fill=self.app.theme.textColor, align='center')
            drawLabel('the number keys to fill in the cells.', self.app.width / 2, line2Y, size=18, fill=self.app.theme.textColor, align='center')
        elif pageIndex == 3:
            drawLabel('Guess Mode', self.app.width / 2, topBoxHeight / 2, size=24, fill=self.app.theme.textColor, align='center')
            drawLabel('Press "G" to toggle guess mode. In guess mode,', self.app.width / 2, line1Y, size=18, fill=self.app.theme.textColor, align='center')
            drawLabel('your guesses will be highlighted differently.', self.app.width / 2, line2Y, size=18, fill=self.app.theme.textColor, align='center')
        elif pageIndex == 4:
            drawLabel('Hints and Tips', self.app.width / 2, topBoxHeight / 2, size=24, fill=self.app.theme.textColor, align='center')
            drawLabel('If you are stuck, try to find the numbers that can', self.app.width / 2, line1Y, size=18, fill=self.app.theme.textColor, align='center')
            drawLabel('only fit in one place. Use logic to deduce the', self.app.width / 2, line2Y, size=18, fill=self.app.theme.textColor, align='center')
            drawLabel('placement of numbers.', self.app.width / 2, line3Y, size=18, fill=self.app.theme.textColor, align='center')

class HelpPage:
    def __init__(self, app, pageIndex, drawContentFunc):
        self.app = app
        self.pageIndex = pageIndex
        self.drawContentFunc = drawContentFunc

    def setup(self):
        pass

    def draw(self):
        self.drawContentFunc(self.pageIndex)

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
        buttonY = self.app.height - self.app.menuBarButtonBuffer - buttonHeight
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
