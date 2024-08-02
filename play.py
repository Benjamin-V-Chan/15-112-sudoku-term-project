from cmu_graphics import *
from gameOver import *
from sudokuGenerator import *
from button import Button
from itertools import combinations
import time

def play_onScreenActivate(app):
    setupPlayScreen(app)

def setupPlayScreen(app):
    app.gridSize = 9
    app.gridPaddingX = 0
    app.gridPaddingY = 0
    app.cellBorderThickness = 2
    app.fontSize = 22
    app.playScreenButtonWidth = 135
    app.highlightedRow, app.highlightedCol = 0, 0
    app.splashMusic.pause()
    if not app.muteVolume:
        app.playMusic.play(loop=True, restart=True)
    resetPlayScreen(app)
    generateAndSetupGrid(app)

def resetPlayScreen(app):
    app.totalLives = 3
    app.remainingLives = app.totalLives
    app.isManualGuessMode = False
    app.isGuessMode = False
    app.tempIncorrect = {}
    app.wonGame = False
    app.highlightedSingles = []
    app.highlightedTuples = []
    app.noHintAvailableTime = 0

def generateAndSetupGrid(app):
    app.grid = generateBoard(app.difficulty)
    app.grid = [[None if cell == 0 else cell for cell in row] for row in app.grid]
    app.gridColors = [[app.theme.cellColor for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.cellStatus = [['normal' for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if app.grid[row][col] is not None:
                app.cellStatus[row][col] = 'starting'
    app.gridColors[app.highlightedRow][app.highlightedCol] = app.theme.highlightedColor
    app.cellGuesses = [[[None for _ in range(app.gridSize)] for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    app.autoCellGuesses = [[[] for _ in range(app.gridSize)] for _ in range(app.gridSize)]
    updateGridDimensions(app)
    setupPlayButtons(app)

def setupPlayButtons(app):
    buttonHeight = app.menuBarHeight - 2 * app.menuBarButtonBuffer
    buttonY = app.height - app.menuBarButtonBuffer - buttonHeight
    buttonWidth = app.playScreenButtonWidth
    app.resetButton = Button(125, buttonY, buttonWidth, buttonHeight, 'Reset', app.theme)
    app.homeButton = Button(app.resetButton.x + app.menuBarButtonBuffer + buttonWidth, buttonY, buttonWidth, buttonHeight, 'Home', app.theme)
    app.hintShowButton = Button(app.homeButton.x + app.menuBarButtonBuffer + buttonWidth, buttonY, buttonWidth, buttonHeight, 'Hint Show', app.theme)
    app.hintFillButton = Button(app.hintShowButton.x + app.menuBarButtonBuffer + buttonWidth, buttonY, buttonWidth, buttonHeight, 'Hint Fill', app.theme)
    app.playButtons = [app.resetButton, app.homeButton, app.hintShowButton, app.hintFillButton]

# Import necessary modules
from itertools import combinations

# Find cells with only one legal value
def findObviousSingles(app):
    """Identify cells with only one legal value."""
    singles = []
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if app.grid[row][col] is None:
                legalValues = findLegalValues(app, row, col)
                if len(legalValues) == 1:
                    singles.append((row, col))
    return singles

# Highlight single value cells
def highlightSingle(app, singles):
    """Highlight the first obvious single cell found."""
    if singles:
        row, col = singles[0]
        app.highlightedSingles = [(row, col)]

# Apply the single hint by setting the cell's value
def applySingleHint(app, singles):
    """Apply the single hint by setting the cell's value."""
    if singles:
        row, col = singles[0]
        legalValues = findLegalValues(app, row, col)
        if legalValues:
            value = legalValues.pop()

            # Create a temporary grid to test the hint application
            tempGrid = [row[:] for row in app.grid]
            tempGrid[row][col] = value

            # Check if the board is solvable and legal with the applied hint
            if isBoardSolvable(tempGrid) and isBoardLegal(tempGrid):
                # If solvable and legal, apply the changes to the actual grid
                app.grid[row][col] = value
                app.cellStatus[row][col] = 'correct'
                return True
    return False

# Find N cells in the region with exactly N unique legal values
def findObviousTuples(app, region):
    """Find N cells in the region with exactly N unique legal values."""
    cellsWithLegals = [(i, findLegalValues(app, region[i][0], region[i][1])) for i in range(len(region)) if app.grid[region[i][0]][region[i][1]] is None]
    
    for n in range(2, 5):
        for combo in combinations(cellsWithLegals, n):
            indices, legals = zip(*combo)
            unionLegals = set().union(*legals)
            if len(unionLegals) == n:
                return indices, unionLegals
    return None

def applyTupleHint(app, region, indices, unionLegals):
    """Apply the tuple hint by assigning values to the grid if it keeps the board solvable."""
    applied = False
    unionLegalsList = list(unionLegals)  # Convert the set to a list for indexing

    # Create a temporary grid to test the hint application
    tempGrid = [row[:] for row in app.grid]

    # Try assigning each legal value to one of the cells in the indices
    for idx, i in enumerate(indices):
        row, col = region[i]
        tempGrid[row][col] = unionLegalsList[idx]  # Assign one of the possible values

    # Check if the board is solvable and legal with the applied hints
    if isBoardSolvable(tempGrid) and isBoardLegal(tempGrid):
        # If solvable and legal, apply the changes to the actual grid
        for idx, i in enumerate(indices):
            row, col = region[i]
            app.grid[row][col] = unionLegalsList[idx]
            app.cellStatus[row][col] = 'correct'
            applied = True

    return applied

def highlightTuple(app, indices, region):
    """Highlight the cells that form an obvious tuple."""
    app.highlightedTuples = []
    for i in indices:
        row, col = region[i]
        app.gridColors[row][col] = app.theme.tupleColor
        app.highlightedTuples.append((row, col))

def show_hints(app):
    """Show hints by highlighting cells with singles or tuples."""
    singles = findObviousSingles(app)
    if singles:
        highlightSingle(app, singles)
    else:
        # No singles, look for tuples
        for i in range(app.gridSize):
            # Check rows
            row = [(i, j) for j in range(app.gridSize)]
            tuple_info = findObviousTuples(app, row)
            if tuple_info:
                indices, unionLegals = tuple_info
                highlightTuple(app, indices, row)
                return

            # Check columns
            col = [(j, i) for j in range(app.gridSize)]
            tuple_info = findObviousTuples(app, col)
            if tuple_info:
                indices, unionLegals = tuple_info
                highlightTuple(app, indices, col)
                return

            # Check blocks
            blockRow = (i // 3) * 3
            blockCol = (i % 3) * 3
            block = [(blockRow + r, blockCol + c) for r in range(3) for c in range(3)]
            tuple_info = findObviousTuples(app, block)
            if tuple_info:
                indices, unionLegals = tuple_info
                highlightTuple(app, indices, block)
                return

# Fill hints by applying singles or tuples
def fillHints(app):
    """Fill hints by applying singles or tuples."""
    singles = findObviousSingles(app)
    if applySingleHint(app, singles):
        return

    # If no singles, apply obvious tuples
    hint_applied = False
    for i in range(app.gridSize):

        # Apply tuples in rows
        row = [(i, j) for j in range(app.gridSize)]
        tuple_info = findObviousTuples(app, row)
        if tuple_info:
            indices, unionLegals = tuple_info
            if applyTupleHint(app, row, indices, unionLegals):
                return

        # Apply tuples in columns
        col = [(j, i) for j in range(app.gridSize)]
        tuple_info = findObviousTuples(app, col)
        if tuple_info:
            indices, unionLegals = tuple_info
            if applyTupleHint(app, col, indices, unionLegals):
                return 

        # Apply tuples in blocks
        blockRow = (i // 3) * 3
        blockCol = (i % 3) * 3
        block = [(blockRow + r, blockCol + c) for r in range(3) for c in range(3)]
        tuple_info = findObviousTuples(app, block)
        if tuple_info:
            indices, unionLegals = tuple_info
            if applyTupleHint(app, block, indices, unionLegals):
                return  # Exit after applying to one region

    if not hint_applied:
        app.noHintAvailableTime = time.time()

# Function to check if the board is legal
def isBoardLegal(grid):
    """Check if the given grid is legal."""
    # Check rows for duplicates
    for row in grid:
        if not isUnique(row):
            return False
    
    # Check columns for duplicates
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if not isUnique(column):
            return False

    # Check 3x3 blocks for duplicates
    for blockRow in range(0, 9, 3):
        for blockCol in range(0, 9, 3):
            block = [grid[row][col] for row in range(blockRow, blockRow + 3) for col in range(blockCol, blockCol + 3)]
            if not isUnique(block):
                return False

    return True

def isUnique(values):
    """Check if values contain duplicates, ignoring None."""
    seen = set()
    for value in values:
        if value is not None:
            if value in seen:
                return False
            seen.add(value)
    return True

def displayNoHintsMessage(app):
    """Display a message if no hints are available."""
    if app.noHintAvailableTime > 0:
        current_time = time.time()
        if current_time - app.noHintAvailableTime < 1:
            drawLabel("No available hints", app.width / 2, app.height / 2, size=24, fill='red', align='center')

def play_onStep(app):
    if time.time() - app.noHintAvailableTime > 1:
        app.noHintAvailableTime = 0

def checkForGameWon(app):
    if app.remainingLives == 0:
        app.wonGame = False
        setActiveScreen('gameOver')
        return
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if app.grid[row][col] is None:
                return
    app.wonGame = True
    setActiveScreen('gameOver')
    return

def play_onMousePress(app, mouseX, mouseY):
    for button in app.playButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Reset':
                resetPlayScreen(app)
                generateAndSetupGrid(app)
            elif button.text == 'Home':
                app.playMusic.pause()
                app.gameFinished = True
                setActiveScreen('splash')
            elif button.text == 'Hint Show':
                show_hints(app)  # Highlight possible hints
            elif button.text == 'Hint Fill':
                fillHints(app)  # Fill in hints automatically
            return
    app.highlightedRow, app.highlightedCol = getGridCell(app, mouseX, mouseY)

def play_onMouseRelease(app, mouseX, mouseY):
    for button in app.playButtons:
        button.onRelease()

def play_onMouseMove(app, mouseX, mouseY):
    for button in app.playButtons:
        button.onHover(mouseX, mouseY)

def play_onKeyPress(app, key):
    removeIncorrectGuesses(app)

    # Check if logged in and use custom keybinds
    if app.loggedIn and hasattr(app, 'userInfo') and hasattr(app.userInfo, 'keybinds'):
        keybinds = app.userInfo.keybinds

        # Use keybinds for navigation
        if key == keybinds.get('up', 'up'):
            navigateGrid(app, 'up')
        elif key == keybinds.get('down', 'down'):
            navigateGrid(app, 'down')
        elif key == keybinds.get('left', 'left'):
            navigateGrid(app, 'left')
        elif key == keybinds.get('right', 'right'):
            navigateGrid(app, 'right')
    else:
        # Default navigation keys
        if key == 'up':
            navigateGrid(app, 'up')
        elif key == 'down':
            navigateGrid(app, 'down')
        elif key == 'left':
            navigateGrid(app, 'left')
        elif key == 'right':
            navigateGrid(app, 'right')

    # Handle number input for setting values
    if key.isdigit() and key != '0':
        num = int(key)
        if not app.isGuessMode and app.cellStatus[app.highlightedRow][app.highlightedCol] not in ['correct', 'starting']:
            if isValid(app.grid, app.highlightedRow, app.highlightedCol, num):
                app.grid[app.highlightedRow][app.highlightedCol] = num
                app.cellStatus[app.highlightedRow][app.highlightedCol] = 'correct'
            else:
                app.remainingLives -= 1
                app.cellStatus[app.highlightedRow][app.highlightedCol] = 'incorrect'
                app.grid[app.highlightedRow][app.highlightedCol] = None
                app.tempIncorrect[(app.highlightedRow, app.highlightedCol)] = num
            app.cellGuesses[app.highlightedRow][app.highlightedCol] = [None for _ in range(app.gridSize)]
        elif app.isGuessMode and app.cellStatus[app.highlightedRow][app.highlightedCol] not in ['correct', 'starting']:
            app.cellGuesses[app.highlightedRow][app.highlightedCol][int(key) - 1] = int(key)

    elif key == 'g':
        app.isGuessMode = not app.isGuessMode
        app.isManualGuessMode = False
    elif key == 'a':
        app.isManualGuessMode = not app.isManualGuessMode
        app.isGuessMode = False

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
    for i in range(app.gridSize):
        if app.cellGuesses[row][col][i] is not None and app.isGuessMode:
            num = app.cellGuesses[row][col][i]
            xPos = cellWidth / 3 * (i % 3 + 1) - (cellWidth // 3) * 0.5
            yPos = cellHeight / 3 * (i // 3 + 1) - (cellHeight // 3) * 0.5
            drawLabel(str(num), cellLeft + xPos, cellTop + yPos, size=app.fontSize // 1.5, fill='grey')
        elif app.autoCellGuesses[row][col] and i < len(app.autoCellGuesses[row][col]) and app.autoCellGuesses[row][col][i] is not None and app.isManualGuessMode:
            num = app.autoCellGuesses[row][col][i]
            xPos = cellWidth / 3 * (i % 3 + 1) - (cellWidth // 3) * 0.5
            yPos = cellHeight / 3 * (i // 3 + 1) - (cellHeight // 3) * 0.5
            drawLabel(str(num), cellLeft + xPos, cellTop + yPos, size=app.fontSize // 1.5, fill='grey')

def play_onStep(app):
    updateAutoCellGuesses(app)
    updateCellColors(app)
    checkForGameWon(app)

def updateAutoCellGuesses(app):
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if app.grid[row][col] is None:
                app.autoCellGuesses[row][col] = []
                for i in range(1, app.gridSize + 1):
                    if isValid(app.grid, row, col, i):
                        app.autoCellGuesses[row][col].append(i)

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
            elif app.cellStatus[row][col] == 'single':
                app.gridColors[row][col] = app.theme.singleGuessColor
            elif app.cellStatus[row][col] == 'tuple':
                app.gridColors[row][col] = app.theme.tupleColor

    for row, col in app.highlightedSingles:
        if app.cellStatus[row][col] != 'correct':
            app.gridColors[row][col] = app.theme.singleGuessColor

    for row, col in app.highlightedTuples:
        if app.cellStatus[row][col] != 'correct':
            app.gridColors[row][col] = app.theme.tupleColor

    app.gridColors[app.highlightedRow][app.highlightedCol] = app.theme.highlightedColor

def play_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawGrid(app)
    drawGridBorder(app)
    drawMenuBar(app)
    displayNoHintsMessage(app)
    for button in app.playButtons:
        button.draw()

def findLegalValues(app, row, col):
    """Find all legal values for a cell at (row, col)."""
    if app.grid[row][col] is not None:
        return set()

    legalValues = set(range(1, 10))
    for i in range(9):
        if app.grid[row][i] is not None:
            legalValues.discard(app.grid[row][i])
        if app.grid[i][col] is not None:
            legalValues.discard(app.grid[i][col])

    blockRow, blockCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(blockRow, blockRow + 3):
        for j in range(blockCol, blockCol + 3):
            if app.grid[i][j] is not None:
                legalValues.discard(app.grid[i][j])

    return legalValues