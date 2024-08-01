from cmu_graphics import *
from gameOver import *
from sudokuGenerator import generateBoard
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
    app.highlightedSingles = []  # Initialize list to track singles hints
    app.highlightedTuples = []  # Initialize list to track tuples hints
    app.noHintAvailableTime = 0  # Track time for no hints available message

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

def find_obvious_singles(app):
    """Identify cells with only one legal value."""
    singles = []
    for row in range(app.gridSize):
        for col in range(app.gridSize):
            if app.grid[row][col] is None:
                legal_values = findLegalValues(app, row, col)
                if len(legal_values) == 1:
                    singles.append((row, col))
    return singles

def highlight_single(app, singles):
    """Highlight the cell with only one legal value."""
    if singles:
        row, col = singles[0]  # Take the first obvious single found
        app.highlightedSingles = [(row, col)]  # Store the highlighted single for persistent highlighting

def apply_single_hint(app, singles):
    """Apply the single hint by setting the cell's value."""
    if singles:
        row, col = singles[0]
        legal_values = findLegalValues(app, row, col)
        if legal_values:  # Ensure there are legal values available
            value = legal_values.pop()
            app.grid[row][col] = value
            app.cellStatus[row][col] = 'correct'
            return True
    return False

def find_obvious_tuples(app, region):
    """Find N cells in the region with exactly N unique legal values."""
    # Create a list of cells in the region with their legal values
    cells_with_legals = [(i, findLegalValues(app, region[i][0], region[i][1])) for i in range(len(region)) if app.grid[region[i][0]][region[i][1]] is None]
    
    # Iterate through different sizes of combinations (2 to 4 for tuples)
    for n in range(2, 5):  # We can adjust the size range based on typical Sudoku strategies
        for combo in combinations(cells_with_legals, n):
            indices, legals = zip(*combo)
            union_legals = set().union(*legals)
            if len(union_legals) == n:
                return indices, union_legals
    return None

def apply_tuple_hint(app, region, indices, union_legals):
    """Apply the tuple hint by assigning values to the grid."""
    # Iterate through each index in the indices and update grid if possible
    applied = False
    for i in indices:
        row, col = region[i]
        # Check for only legal position for the value in the union of legals
        if len(union_legals) == 1:
            value = union_legals.pop()
            app.grid[row][col] = value
            app.cellStatus[row][col] = 'correct'
            applied = True
        else:
            # Attempt to apply the value with backtracking logic
            for value in union_legals:
                # Try placing the value
                if isValid(app.grid, row, col, value):
                    app.grid[row][col] = value
                    app.cellStatus[row][col] = 'correct'
                    applied = True
                    break  # Stop trying if we found a valid placement

    return applied

def highlight_tuple(app, indices, region):
    """Highlight the cells that form an obvious tuple."""
    app.highlightedTuples = []  # Initialize or clear previous highlights
    for i in indices:
        row, col = region[i]
        app.gridColors[row][col] = app.theme.tupleColor
        app.highlightedTuples.append((row, col))  # Store the highlighted tuple for persistent highlighting

def is_board_solvable(app, grid):
    """Check if the board is solvable (basic backtracking solver)."""
    empty_pos = find_empty_position(grid)
    if not empty_pos:
        return True  # No empty positions means the board is solved
    row, col = empty_pos

    for num in range(1, 10):
        if isValid(grid, row, col, num):
            grid[row][col] = num
            if is_board_solvable(app, grid):
                return True
            grid[row][col] = None  # Backtrack

    return False

def find_empty_position(grid):
    """Find an empty position on the grid."""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] is None:
                return (row, col)
    return None

def show_hints(app):
    """Show hints by highlighting cells with singles or tuples."""
    singles = find_obvious_singles(app)
    if singles:
        highlight_single(app, singles)
    else:
        # No singles, look for tuples
        for i in range(app.gridSize):
            # Check rows
            row = [(i, j) for j in range(app.gridSize)]
            tuple_info = find_obvious_tuples(app, row)
            if tuple_info:
                indices, union_legals = tuple_info
                highlight_tuple(app, indices, row)
                return

            # Check columns
            col = [(j, i) for j in range(app.gridSize)]
            tuple_info = find_obvious_tuples(app, col)
            if tuple_info:
                indices, union_legals = tuple_info
                highlight_tuple(app, indices, col)
                return

            # Check blocks
            blockRow = (i // 3) * 3
            blockCol = (i % 3) * 3
            block = [(blockRow + r, blockCol + c) for r in range(3) for c in range(3)]
            tuple_info = find_obvious_tuples(app, block)
            if tuple_info:
                indices, union_legals = tuple_info
                highlight_tuple(app, indices, block)
                return

def fill_hints(app):
    """Fill hints by applying singles or tuples."""
    singles = find_obvious_singles(app)
    if apply_single_hint(app, singles):
        return

    # If no singles, apply obvious tuples
    hint_applied = False
    for i in range(app.gridSize):
        # Apply tuples in rows
        row = [(i, j) for j in range(app.gridSize)]
        tuple_info = find_obvious_tuples(app, row)
        if tuple_info:
            indices, union_legals = tuple_info
            if apply_tuple_hint(app, row, indices, union_legals):
                return

        # Apply tuples in columns
        col = [(j, i) for j in range(app.gridSize)]
        tuple_info = find_obvious_tuples(app, col)
        if tuple_info:
            indices, union_legals = tuple_info
            if apply_tuple_hint(app, col, indices, union_legals):
                return

        # Apply tuples in blocks
        blockRow = (i // 3) * 3
        blockCol = (i % 3) * 3
        block = [(blockRow + r, blockCol + c) for r in range(3) for c in range(3)]
        tuple_info = find_obvious_tuples(app, block)
        if tuple_info:
            indices, union_legals = tuple_info
            if apply_tuple_hint(app, block, indices, union_legals):
                return

    # If no hints applied, set the no-hint message
    if not hint_applied:
        app.noHintAvailableTime = time.time()  # Start the timer for the no-hint message

def displayNoHintsMessage(app):
    """Display a message if no hints are available."""
    if app.noHintAvailableTime > 0:
        current_time = time.time()
        if current_time - app.noHintAvailableTime < 1:  # Show the message for 1 second
            drawLabel("No available hints", app.width / 2, app.height / 2, size=24, fill='red', align='center')
        else:
            app.noHintAvailableTime = 0  # Reset the timer after 1 second

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
                fill_hints(app)  # Fill in hints automatically
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
    if key in ['up', 'down', 'left', 'right']:
        navigateGrid(app, key)
    elif key.isdigit() and key != '0' and not app.isGuessMode and (app.cellStatus[app.highlightedRow][app.highlightedCol] not in ['correct', 'starting']):
        num = int(key)
        if isValid(app.grid, app.highlightedRow, app.highlightedCol, num):
            app.grid[app.highlightedRow][app.highlightedCol] = num
            app.cellStatus[app.highlightedRow][app.highlightedCol] = 'correct'
        else:
            app.remainingLives -= 1
            app.cellStatus[app.highlightedRow][app.highlightedCol] = 'incorrect'
            app.grid[app.highlightedRow][app.highlightedCol] = None
            app.tempIncorrect[(app.highlightedRow, app.highlightedCol)] = num
        app.cellGuesses[app.highlightedRow][app.highlightedCol] = [None for _ in range(app.gridSize)]
    elif key.isdigit() and key != '0' and app.isGuessMode and (app.cellStatus[app.highlightedRow][app.highlightedCol] not in ['correct', 'starting']):
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

    # Apply persistent highlighting for singles
    for row, col in app.highlightedSingles:
        if app.cellStatus[row][col] != 'correct':  # Ensure it remains highlighted until status changes
            app.gridColors[row][col] = app.theme.singleGuessColor

    # Apply persistent highlighting for tuples
    for row, col in app.highlightedTuples:
        if app.cellStatus[row][col] != 'correct':  # Ensure it remains highlighted until status changes
            app.gridColors[row][col] = app.theme.tupleColor

    app.gridColors[app.highlightedRow][app.highlightedCol] = app.theme.highlightedColor

def play_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawGrid(app)
    drawGridBorder(app)
    drawMenuBar(app)
    displayNoHintsMessage(app)  # Draw message if no hints are available
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

def isValid(grid, row, col, num):
    """
    Check if it's valid to place a number in a specific cell.
    
    Args:
        grid (list of list of int): The Sudoku board represented as a 2D list.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        num (int): The number to be placed in the cell.
        
    Returns:
        bool: True if the number can be placed, False otherwise.
    """
    
    # Check the row
    for c in range(9):
        if grid[row][c] == num:
            return False

    # Check the column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # Check the 3x3 subgrid
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for r in range(startRow, startRow + 3):
        for c in range(startCol, startCol + 3):
            if grid[r][c] == num:
                return False

    # If no conflicts, return True
    return True
