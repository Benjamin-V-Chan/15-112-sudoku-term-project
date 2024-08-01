from button import Button
from splash import *
from levels import *

def setupGameOverScreen(app):
    if app.wonGame:
        app.gameOverTitle = 'Level Complete!'
    else:
        app.gameOverTitle = 'Level Lost!'
    app.gameOverScreenButtonWidth = 200
    app.gameOverScreenButtonHeight = 50
    app.gameOverScreenButtonSpacing = 20
    app.gameOverButtonX = app.width / 2 - app.gameOverScreenButtonWidth / 2
    app.gameOverButtonY = app.height / 2 + 50
    setupGameOverButtons(app)

def setupGameOverButtons(app):
    app.gameOverHomeButton = Button(app.gameOverButtonX, app.gameOverButtonY, app.gameOverScreenButtonWidth, app.gameOverScreenButtonHeight, 'Home', app.theme)
    app.gameOverPlayAgainButton = Button(app.gameOverButtonX, app.gameOverButtonY + app.gameOverScreenButtonHeight + app.gameOverScreenButtonSpacing, app.gameOverScreenButtonWidth, app.gameOverScreenButtonHeight, 'Play Again', app.theme)
    app.gameOverAllButtons = [app.gameOverHomeButton, app.gameOverPlayAgainButton]

def gameOver_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawGameOverTitle(app)
    drawGameOverButtons(app)

def drawGameOverTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.gameOverTitle, titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def drawGameOverButtons(app):
    for button in app.gameOverAllButtons:
        button.draw()

def gameOver_mousePressed(app, mouseX, mouseY):
    for button in app.gameOverAllButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Home':
                setActiveScreen('splash')
            elif button.text == 'Play Again':
                setupLevelsScreen(app)
                setActiveScreen('levels')
            break

def gameOver_mouseReleased(app, mouseX, mouseY):
    for button in app.gameOverAllButtons:
        button.onRelease()

def gameOver_mouseMoved(app, mouseX, mouseY):
    for button in app.gameOverAllButtons:
        button.onHover(mouseX, mouseY)