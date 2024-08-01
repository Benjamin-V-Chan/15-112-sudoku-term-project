from cmu_graphics import *
from button import *
from play import *

def setupLevelsScreen(app):
    app.levels = ['easy', 'medium', 'hard', 'expert', 'evil']
    app.levelsButtonWidth = 120
    app.levelsButtonHeight = 80
    app.levelsButtonSpacing = 15
    app.levelsTitle = 'LEVELS'
    setupLevelsScreenButtons(app)

def setupLevelsScreenButtons(app):
    totalWidth = (app.levelsButtonWidth * len(app.levels)) + (app.levelsButtonSpacing * (len(app.levels) - 1))
    startX = (app.width - totalWidth) / 2
    y = 200

    app.easyButton = Button(startX, y, app.levelsButtonWidth, app.levelsButtonHeight, 'Easy', app.theme, customFill=gradient('lightgreen', 'green'))
    app.mediumButton = Button(startX + app.levelsButtonWidth + app.levelsButtonSpacing, y, app.levelsButtonWidth, app.levelsButtonHeight, 'Medium', app.theme, customFill=gradient('gold', 'orange'))
    app.hardButton = Button(startX + 2 * (app.levelsButtonWidth + app.levelsButtonSpacing), y, app.levelsButtonWidth, app.levelsButtonHeight, 'Hard', app.theme, customFill=gradient('orange', 'orangeRed'))
    app.expertButton = Button(startX + 3 * (app.levelsButtonWidth + app.levelsButtonSpacing), y, app.levelsButtonWidth, app.levelsButtonHeight, 'Expert', app.theme, customFill=gradient('orangeRed', 'red'))
    app.evilButton = Button(startX + 4 * (app.levelsButtonWidth + app.levelsButtonSpacing), y, app.levelsButtonWidth, app.levelsButtonHeight, 'Evil', app.theme, customFill=gradient('red', 'firebrick'))

    app.playButtons = [app.easyButton, app.mediumButton, app.hardButton, app.expertButton, app.evilButton]

    backButtonWidth = 100
    backButtonHeight = 50
    backButtonX = (app.width - backButtonWidth) / 2
    backButtonY = y + app.levelsButtonHeight + 50

    app.backButton = Button(backButtonX, backButtonY, backButtonWidth, backButtonHeight, 'Back', app.theme)

    app.levelsAllButtons = app.playButtons + [app.backButton]

def levels_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawLevelsTitle(app)
    drawLevelsButtons(app)

def drawLevelsTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.levelsTitle.upper(), titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def drawLevelsButtons(app):
    for button in app.levelsAllButtons:
        button.draw()

def levels_onMousePress(app, mouseX, mouseY):
    for i, button in enumerate(app.playButtons):
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            app.difficulty = app.levels[i]
            setActiveScreen('play')
            setupPlayScreen(app)
            return
    if app.backButton.checkClicked(mouseX, mouseY):
        app.difficulty = None
        setActiveScreen('splash')

def levels_onMouseRelease(app, mouseX, mouseY):
    for button in app.levelsAllButtons:
        button.onRelease()

def levels_onMouseMove(app, mouseX, mouseY):
    for button in app.levelsAllButtons:
        button.onHover(mouseX, mouseY)