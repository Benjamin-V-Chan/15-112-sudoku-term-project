from cmu_graphics import *
from button import Button

def help_onScreenActivate(app):
    setupHelpScreen(app)

def setupHelpScreen(app):
    app.currentPage = 0
    app.pages = [HelpPage(app, i, drawPageContent) for i in range(9)]
    app.prevButton = Button(20, app.height - app.menuBarHeight - 20, 100, 50, '< Prev', app.theme)
    app.nextButton = Button(app.width - 120, app.height - app.menuBarHeight - 20, 100, 50, 'Next >', app.theme)
    app.homeButton = Button(app.width / 2 - 50, app.height - app.menuBarHeight - 20, 100, 50, 'Home', app.theme)

def help_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    app.pages[app.currentPage].draw()
    app.prevButton.draw()
    app.nextButton.draw()
    app.homeButton.draw()

def help_onMousePress(app, mouseX, mouseY):
    if app.prevButton.checkClicked(mouseX, mouseY):
        app.prevButton.onClick()
        if app.currentPage > 0:
            app.currentPage -= 1
    elif app.nextButton.checkClicked(mouseX, mouseY):
        app.nextButton.onClick()
        if app.currentPage < len(app.pages) - 1:
            app.currentPage += 1
    elif app.homeButton.checkClicked(mouseX, mouseY):
        app.homeButton.onClick()
        setActiveScreen('splash')

def help_onMouseRelease(app, mouseX, mouseY):
    app.prevButton.onRelease()
    app.nextButton.onRelease()
    app.homeButton.onRelease()

def help_onMouseMove(app, mouseX, mouseY):
    app.prevButton.onHover(mouseX, mouseY)
    app.nextButton.onHover(mouseX, mouseY)
    app.homeButton.onHover(mouseX, mouseY)

def drawPageContent(app, pageIndex):
    topBoxHeight = app.height // 4
    lineDistance = 30
    line1Y = topBoxHeight + 60
    drawRect(0, 0, app.width, topBoxHeight, fill=app.theme.buttonColor, border=app.theme.buttonBorderColor)

    # Strings for each page with colon separators for titles
    pageContents = [
        "Welcome to Sudoku!: In this game, you need to fill the grid so that each row, column, and 3x3 box contains the numbers 1 to 9 without repeating.",
        "How to Start a Game: On the home screen, press play, then select a difficulty level to start a new game.",
        "Gameplay Instructions: Use the arrow keys or mouse to navigate the grid and the number keys to fill in the cells.",
        "Guess Mode: Press 'G' to toggle manual guess mode, or 'A' to automatically fill guesses. Use this to map out potential values for that cell.",
        "Hints and Tips: If you are stuck, try to find the numbers that can only fit in one place. Use logic to deduce the placement of numbers.",
        "Keybinds: To view all keybinds and customize them to your liking, navigate to settings > keybinds.",
        "Customization: You can also customize other aspects of your game like themes and volume within the settings menu.",
        "Save User Info: You can save your custom settings by creating an account and logging in.",
        "Good luck and have fun!: Enjoy the game and challenge yourself!"
    ]

    maxCharsPerLine = 50
    content = pageContents[pageIndex]

    # Split title and text by the first occurrence of ':'
    if ':' in content:
        title, text = content.split(':', 1)
    else:
        # Default behavior if no colon is found
        title, text = content.split(' ', 1)

    drawLabel(title.strip(), app.width / 2, topBoxHeight / 2, size=24, fill=app.theme.textColor, align='center')

    # Split remaining text into lines based on maxCharsPerLine
    lines = splitIntoLines(text.strip(), maxCharsPerLine)

    for i, line in enumerate(lines, start=0):
        y = line1Y + i * lineDistance
        drawLabel(line, app.width / 2, y, size=18, fill=app.theme.textColor, align='center')

def splitIntoLines(text, maxChars):
    """Split text into lines, each with a maximum number of characters."""
    words = text.split()
    lines = []
    currentLine = ""

    for word in words:
        if len(currentLine) + len(word) + 1 <= maxChars:
            currentLine += (word + " ")
        else:
            lines.append(currentLine.strip())
            currentLine = word + " "

    # Add the last line if there's remaining text
    if currentLine:
        lines.append(currentLine.strip())

    return lines

class HelpPage:
    def __init__(self, app, pageIndex, drawContentFunc):
        self.app = app
        self.pageIndex = pageIndex
        self.drawContentFunc = drawContentFunc

    def draw(self):
        self.drawContentFunc(self.app, self.pageIndex)