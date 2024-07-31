from cmu_graphics import *
from button import Button

def setupHelpScreen(app):
    app.currentPage = 0
    app.pages = [HelpPage(app, i, drawPageContent) for i in range(5)]
    app.prevButton = Button(20, app.height - app.menuBarHeight - 20, 100, 50, '< Prev', app.theme)
    app.nextButton = Button(app.width - 120, app.height - app.menuBarHeight - 20, 100, 50, 'Next >', app.theme)
    app.homeButton = Button(app.width / 2 - 50, app.height - app.menuBarHeight - 20, 100, 50, 'Home', app.theme)

def help_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    app.pages[app.currentPage].draw()
    app.prevButton.draw()
    app.nextButton.draw()
    app.homeButton.draw()

def help_onScreenActivate(app):
    setupHelpScreen(app)

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
    line2Y = line1Y + lineDistance
    line3Y = line2Y + lineDistance
    line4Y = line3Y + lineDistance
    drawRect(0, 0, app.width, topBoxHeight, fill=app.theme.buttonColor, border=app.theme.buttonBorderColor)
    if pageIndex == 0:
        drawLabel('Welcome to Sudoku!', app.width / 2, topBoxHeight / 2, size=24, fill=app.theme.textColor, align='center')
        drawLabel('In this game, you need to fill the grid so that each row,', app.width / 2, line1Y, size=18, fill=app.theme.textColor, align='center')
        drawLabel('column, and 3x3 box contains the numbers 1 to 9', app.width / 2, line2Y, size=18, fill=app.theme.textColor, align='center')
        drawLabel('without repeating.', app.width / 2, line3Y, size=18, fill=app.theme.textColor, align='center')        
    elif pageIndex == 1:
        drawLabel('How to Start a Game', app.width / 2, topBoxHeight / 2, size=24, fill=app.theme.textColor, align='center')
        drawLabel('On the home screen, select a difficulty level', app.width / 2, line1Y, size=18, fill=app.theme.textColor, align='center')
        drawLabel('to start a new game.', app.width / 2, line2Y, size=18, fill=app.theme.textColor, align='center')
    elif pageIndex == 2:
        drawLabel('Gameplay Instructions', app.width / 2, topBoxHeight / 2, size=24, fill=app.theme.textColor, align='center')
        drawLabel('Use the arrow keys or mouse to navigate the grid and', app.width / 2, line1Y, size=18, fill=app.theme.textColor, align='center')
        drawLabel('the number keys to fill in the cells.', app.width / 2, line2Y, size=18, fill=app.theme.textColor, align='center')
    elif pageIndex == 3:
        drawLabel('Guess Mode', app.width / 2, topBoxHeight / 2, size=24, fill=app.theme.textColor, align='center')
        drawLabel('Press "G" to toggle manual guess mode.', app.width / 2, line1Y, size=18, fill=app.theme.textColor, align='center')
        drawLabel('Use this to map out potential values for that cell', app.width / 2, line2Y, size=18, fill=app.theme.textColor, align='center')
    elif pageIndex == 4:
        drawLabel('Hints and Tips', app.width / 2, topBoxHeight / 2, size=24, fill=app.theme.textColor, align='center')
        drawLabel('If you are stuck, try to find the numbers that can', app.width / 2, line1Y, size=18, fill=app.theme.textColor, align='center')
        drawLabel('only fit in one place. Use logic to deduce the', app.width / 2, line2Y, size=18, fill=app.theme.textColor, align='center')
        drawLabel('placement of numbers.', app.width / 2, line3Y, size=18, fill=app.theme.textColor, align='center')

class HelpPage:
    def __init__(self, app, pageIndex, drawContentFunc):
        self.app = app
        self.pageIndex = pageIndex
        self.drawContentFunc = drawContentFunc

    def setup(self):
        pass

    def draw(self):
        self.drawContentFunc(self.app, self.pageIndex)
