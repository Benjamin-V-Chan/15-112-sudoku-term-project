from cmu_graphics import *
from button import *
from play import *
from help import *

def setupSplashScreen(app):
    app.difficulty = None
    app.colors = [rgb(255, 99, 71), rgb(255, 69, 0), rgb(255, 140, 0), rgb(255, 165, 0), rgb(255, 215, 0)]
    app.messages = ['easy', 'medium', 'hard', 'expert', 'evil']
    app.buttonWidth = 150
    app.buttonHeight = 50
    app.buttonSpacing = 25
    app.title = 'SUDOKU'
    app.titleSize = 55
    app.playButtons = [
        Button(
            app.width / 2 - app.buttonWidth / 2, 
            180 + i * (app.buttonHeight + app.buttonSpacing), 
            app.buttonWidth, 
            app.buttonHeight, 
            app.messages[i], 
            app.theme
        ) for i in range(5)
    ]
    app.changeThemeButton = Button(app.width - app.buttonWidth - 20, app.height - app.buttonHeight - 20, app.buttonWidth, app.buttonHeight, 'Change Theme', app.theme)
    app.helpButton = Button(app.width - app.buttonWidth - 20, app.height - 2 * app.buttonHeight - 40, app.buttonWidth, app.buttonHeight, 'Help', app.theme)

def splash_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawTitle(app)
    drawButtons(app)

def splash_onScreenActivate(app):
    setupSplashScreen(app)

def splash_onMousePress(app, mouseX, mouseY):
    for i, button in enumerate(app.playButtons):
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            app.difficulty = app.messages[i]
            setActiveScreen('play')
            setupPlayScreen(app)
            return
    if app.changeThemeButton.checkClicked(mouseX, mouseY):
        app.changeThemeButton.onClick()
        app.themeIndex = (app.themeIndex + 1) % len(app.themes)
        app.theme = app.themes[app.themeIndex]
        setupSplashScreen(app)
    if app.helpButton.checkClicked(mouseX, mouseY):
        app.helpButton.onClick()
        setActiveScreen('help')
        setupHelpScreen(app)

def splash_onMouseRelease(app, mouseX, mouseY):
    for button in app.playButtons:
        button.onRelease()
    app.changeThemeButton.onRelease()
    app.helpButton.onRelease()

def splash_onMouseMove(app, mouseX, mouseY):
    for button in app.playButtons:
        button.onHover(mouseX, mouseY)
    app.changeThemeButton.onHover(mouseX, mouseY)
    app.helpButton.onHover(mouseX, mouseY)

def drawTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.title, titleX, titleY, size=app.titleSize, fill=app.colors[0], bold=True, align='center', border='black', borderWidth=1)

def drawButtons(app):
    for button in app.playButtons:
        button.draw()
    app.changeThemeButton.draw()
    app.helpButton.draw()