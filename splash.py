from cmu_graphics import *
from button import *
from play import *
from help import *
from settings import *
from levels import *

def splash_onScreenActivate(app):
    setupSplashScreen(app)

def setupSplashScreen(app):
    app.difficulty = None
    app.colors = [rgb(255, 99, 71), rgb(255, 69, 0), rgb(255, 140, 0), rgb(255, 165, 0), rgb(255, 215, 0)]
    app.splashScreenButtonWidth = 180
    app.splashScreenButtonHeight = 60
    app.buttonSpacing = 25
    app.title = 'SUDOKU'
    app.titleSize = 65
    setupSplashScreenButtons(app)

def setupSplashScreenButtons(app):
    app.splashScreenPlayButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, 180, app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Play', app.theme)
    app.settingsButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, 180 + app.splashScreenButtonHeight + app.buttonSpacing, app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Settings', app.theme)
    app.helpButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, 180 + 2 * (app.splashScreenButtonHeight + app.buttonSpacing), app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Help', app.theme)
    
    app.splashScreenAllButtons = [app.splashScreenPlayButton, app.settingsButton, app.helpButton]

def splash_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawTitle(app)
    drawButtons(app)

def setupScreen(app, screen):
    if screen == 'play':
        setupLevelsScreen(app)
    elif screen == 'help':
        setupHelpScreen(app)
    elif screen == 'settings':
        setupSettingsScreen(app)
    elif screen == 'login':
        setupLoginScreen(app)

def splash_onMousePress(app, mouseX, mouseY):
    for button in app.splashScreenAllButtons:
        if button.checkClicked(mouseX, mouseY):
            screen = button.text.lower()
            button.onClick()
            if screen == 'play': setActiveScreen('levels')
            else: setActiveScreen(screen)
            setupScreen(app, screen)
            break

def splash_onMouseRelease(app, mouseX, mouseY):
    for button in app.splashScreenAllButtons:
        button.onRelease()

def splash_onMouseMove(app, mouseX, mouseY):
    for button in app.splashScreenAllButtons:
        button.onHover(mouseX, mouseY)

def drawTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.title, titleX, titleY, size=app.titleSize, fill=app.colors[0], bold=True, align='center', border='black', borderWidth=1)

def drawButtons(app):
    for button in app.splashScreenAllButtons:
        button.draw()