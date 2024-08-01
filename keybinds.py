from cmu_graphics import *
from button import *
import time

def setupKeybindsScreen(app):
    app.keybindsTitle = 'KEYBINDS'
    app.keybindsButtonWidth = 400
    app.keybindsButtonHeight = 55
    app.keybindsButtonBuffer = 15
    app.keybindsButtonX = app.width / 2 - app.keybindsButtonWidth / 2
    app.keybindsButtonY = 160
    app.currentKeyBindCheck = None
    app.defaultKeybindsMessage = 'Press a key to change keybind'
    app.keybindsMessage = app.defaultKeybindsMessage
    app.keybindsMessageX = app.width / 2
    app.keybindsMessageY = app.height - 35
    app.keybindsMessageSize = 25
    app.keyInUseStartTime = 0
    app.keyInUse = False
    setupKeybindsScreenButtons(app)

def setupKeybindsScreenButtons(app):
    app.upButton = Button(app.keybindsButtonX, app.keybindsButtonY, app.keybindsButtonWidth, app.keybindsButtonHeight, f'Up: {app.keybinds["Up"]}', app.theme)
    app.downButton = Button(app.keybindsButtonX, app.keybindsButtonY + app.keybindsButtonHeight + app.keybindsButtonBuffer, app.keybindsButtonWidth, app.keybindsButtonHeight, f'Down: {app.keybinds["Down"]}', app.theme)
    app.leftButton = Button(app.keybindsButtonX, app.keybindsButtonY + 2 * (app.keybindsButtonHeight + app.keybindsButtonBuffer), app.keybindsButtonWidth, app.keybindsButtonHeight, f'Left: {app.keybinds["Left"]}', app.theme)
    app.rightButton = Button(app.keybindsButtonX, app.keybindsButtonY + 3 * (app.keybindsButtonHeight + app.keybindsButtonBuffer), app.keybindsButtonWidth, app.keybindsButtonHeight, f'Right: {app.keybinds["Right"]}', app.theme)
    app.toggleManualGuessModeButton = Button(app.keybindsButtonX, app.keybindsButtonY + 4 * (app.keybindsButtonHeight + app.keybindsButtonBuffer), app.keybindsButtonWidth, app.keybindsButtonHeight, f'Toggle Manual Guess Mode: {app.keybinds["Toggle Manual Guess Mode"]}', app.theme)
    app.toggleAutoGuessModeButton = Button(app.keybindsButtonX, app.keybindsButtonY + 5 * (app.keybindsButtonHeight + app.keybindsButtonBuffer), app.keybindsButtonWidth, app.keybindsButtonHeight, f'Toggle Auto Guess Mode: {app.keybinds["Toggle Auto Guess Mode"]}', app.theme)
    app.exitButton = Button(app.keybindsButtonX, app.keybindsButtonY + 6 * (app.keybindsButtonHeight + app.keybindsButtonBuffer), app.keybindsButtonWidth, app.keybindsButtonHeight, 'Save and Exit', app.theme)
    app.keybindsAllButtons = [app.upButton, app.downButton, app.leftButton, app.rightButton, app.toggleManualGuessModeButton, app.toggleAutoGuessModeButton]

def keybinds_onKeyPress(app, key):
    if app.keyInUse:
        return

    if app.currentKeyBindCheck is not None:
        if key in app.keybinds.values():
            app.keybindsMessage = 'Key already in use'
            app.keyInUseStartTime = time.time()
            app.keyInUse = True
            app.currentKeyBindCheck = None
            return
        app.keybinds[app.currentKeyBindCheck] = key
        app.currentKeyBindCheck = None
        app.keybindsMessage = app.defaultKeybindsMessage
        setupKeybindsScreenButtons(app)

def keybinds_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawKeybindsTitle(app)
    drawKeybindsButtons(app)
    drawKeyBindsMessage(app)

def drawKeyBindsMessage(app):
    drawLabel(app.keybindsMessage, app.keybindsMessageX, app.keybindsMessageY, size=app.keybindsMessageSize, fill=app.theme.textColor, align='center')

def drawKeybindsTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.keybindsTitle.upper(), titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def drawKeybindsButtons(app):
    app.exitButton.draw()
    for button in app.keybindsAllButtons:
        if button.text.split(':')[0] == app.currentKeyBindCheck:
            button.fillColor = 'yellow'
        else:
            button.fillColor = app.theme.buttonColor
        button.draw()

def keybinds_onMousePress(app, mouseX, mouseY):
    if app.exitButton.checkClicked(mouseX, mouseY):
        app.exitButton.onClick()
        setActiveScreen('settings')
        return

    if app.keyInUse:
        return

    if app.exitButton.checkClicked(mouseX, mouseY):
        app.exitButton.onClick()
        setActiveScreen('settings')
        return

    for button in app.keybindsAllButtons:
        button.isSelected = False

    for button in app.keybindsAllButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            app.currentKeyBindCheck = button.text.split(':')[0]
            button.isSelected = True
            app.keybindsMessage = f'Press a key to change keybind for {app.currentKeyBindCheck}'
            return
        else:
            app.keybindsMessage = app.defaultKeybindsMessage

def keybinds_onMouseRelease(app, mouseX, mouseY):
    app.exitButton.onRelease()
    for button in app.keybindsAllButtons:
        button.onRelease()

def keybinds_onMouseMove(app, mouseX, mouseY):
    app.exitButton.onHover(mouseX, mouseY)
    for button in app.keybindsAllButtons:
        button.onHover(mouseX, mouseY)

def keybinds_onStep(app):
    if app.keyInUse and (time.time() - app.keyInUseStartTime > 2):
        app.keybindsMessage = app.defaultKeybindsMessage
        app.keyInUse = False
        app.currentKeyBindCheck = None
