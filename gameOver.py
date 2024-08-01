from cmu_graphics import *
from button import Button
from splash import *

def gameOver_onScreenActivate(app):
    print('game over screen activated')
    setupGameOverScreen(app)

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
    app.gameOverHomeButton = Button(app.gameOverButtonX, app.gameOverButtonY, app.gameOverScreenButtonWidth, app.gameOverScreenButtonHeight, 'Home', app.theme)

def gameOver_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawGameOverTitle(app)
    app.gameOverHomeButton.draw()

def drawGameOverTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.gameOverTitle, titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def gameOver_mousePressed(app, mouseX, mouseY):
    print('mouse pressed')
    if app.gameOverHomeButton.checkClicked(mouseX, mouseY):
        app.gameOverHomeButton.onClick()
        setActiveScreen('splash')

def gameOver_mouseReleased(app, mouseX, mouseY):
    print('mouse released')
    app.gameOverHomeButton.onRelease()

def gameOver_mouseMoved(app, mouseX, mouseY):
    print('mouse moved')
    app.gameOverHomeButton.onHover(mouseX, mouseY)