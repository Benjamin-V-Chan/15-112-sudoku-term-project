from cmu_graphics import *
from button import Button
from splash import *

def gameOver_onScreenActivate(app):
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

def gameOver_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawGameOverTitle(app)

def drawGameOverTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.gameOverTitle, titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)
    drawLabel('Press "h" to return to the home screen', titleX, titleY + 250, size=20, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def gameOver_onKeyPress(app, key):
    if key == 'h':
        app.playMusic.pause()
        setActiveScreen('splash')