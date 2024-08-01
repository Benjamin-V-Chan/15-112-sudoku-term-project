from cmu_graphics import *
from button import *
from play import *
from help import *
from settings import *
from levels import *
from audio import *
from login import *

def splash_onScreenActivate(app):
    setupSplashScreen(app)

def setupSplashScreen(app):
    app.difficulty = None
    app.splashTitle = 'SUDOKU'
    app.splashScreenButtonWidth = 230
    app.splashScreenButtonHeight = 70
    app.buttonSpacing = 20
    app.settingButtonX = app.width / 2 - app.splashScreenButtonWidth / 2
    app.settingButtonY = 200
    if not app.muteVolume:
        if not app.gameFinished:
            app.splashMusic.play(loop=True)
        else:
            app.splashMusic.play(restart=True, loop=True)
    else:
        app.splashMusic.pause()
    setupSplashScreenButtons(app)

def setupSplashScreenButtons(app):
    app.splashScreenPlayButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, app.settingButtonY, app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Play', app.theme)
    app.settingsButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, app.settingButtonY + app.splashScreenButtonHeight + app.buttonSpacing, app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Settings', app.theme)
    app.helpButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, app.settingButtonY + 2 * (app.splashScreenButtonHeight + app.buttonSpacing), app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Help', app.theme)
    
    if not app.loggedIn:
        app.loginButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, app.settingButtonY + 3 * (app.splashScreenButtonHeight + app.buttonSpacing), app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Login', app.theme)
    else:
        app.loginButton = Button(app.width / 2 - app.splashScreenButtonWidth / 2, app.settingButtonY + 3 * (app.splashScreenButtonHeight + app.buttonSpacing), app.splashScreenButtonWidth, app.splashScreenButtonHeight, 'Logout', app.theme)

    app.splashScreenAllButtons = [app.splashScreenPlayButton, app.settingsButton, app.helpButton, app.loginButton]

def splash_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawTitle(app)
    drawButtons(app)

def splash_onMousePress(app, mouseX, mouseY):
    for button in app.splashScreenAllButtons:
        if button.checkClicked(mouseX, mouseY):
            screen = button.text.lower()
            button.onClick()
            if screen == 'play': 
                setActiveScreen('levels')
            elif screen == 'logout': 
                app.loggedIn = False
                setActiveScreen('splash')
            elif screen == 'help':
                setActiveScreen('help')
            elif screen == 'settings':
                setActiveScreen('settings')
            else: 
                setActiveScreen(screen)
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
    drawLabel(app.splashTitle.upper(), titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def drawButtons(app):
    for button in app.splashScreenAllButtons:
        button.draw()