from cmu_graphics import *
from button import *
import time

def setupKeybindsScreen(app):
    app.keybindsTitle = 'Keybinds'
    app.keybindsTitleSize = 65
    app.keybindsButtonWidth = 400
    app.keybindsButtonHeight = 50
    app.keybindsButtonBuffer = 10
    app.keybindsButtonX = app.width / 2 - app.keybindsButtonWidth / 2
    app.keybindsButtonY = 180
    app.currentKeyBindCheck = None
    app.defaultKeybindsMessage = 'Press a key to change keybind'
    app.keybindsMessage = app.defaultKeybindsMessage
    app.keybindsMessageX = app.width / 2
    app.keybindsMessageY = app.height - 100
    app.keybindsMessageSize = 20
    app.keyInUseStartTime = 0
    app.keyInUse = False  # To track if a key is already in use
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
            return
        app.keybinds[app.currentKeyBindCheck.split(':')[0]] = key  # Update the keybind for the selected action
        app.currentKeyBindCheck = None
        app.keybindsMessage = app.defaultKeybindsMessage
        setupKeybindsScreenButtons(app)  # Update buttons to reflect new keybinds

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
    drawLabel(app.keybindsTitle, titleX, titleY, size=app.keybindsTitleSize, fill=app.theme.textColor, font='Arial')

def drawKeybindsButtons(app):
    for button in app.keybindsAllButtons:
        if button.text == app.currentKeyBindCheck:
            button.fillColor = 'yellow'  # Change color to indicate selection
        else:
            button.fillColor = app.theme.buttonColor  # Default button color
        button.draw()

def keybinds_onMousePress(app, mouseX, mouseY):
    if app.exitButton.checkClicked(mouseX, mouseY):
        app.exitButton.onClick()
        setActiveScreen('settings')
        return
    
    if app.keyInUse:
        return

    for button in app.keybindsAllButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            app.currentKeyBindCheck = button.text
            button.isSelected = True
            app.keybindsMessage = f'Press a key to change keybind for {app.currentKeyBindCheck.split(":")[0]}'
            return
        else:
            button.isSelected = False

def keybinds_onMouseRelease(app, mouseX, mouseY):
    for button in app.keybindsAllButtons:
        button.onRelease()

def keybinds_onMouseMove(app, mouseX, mouseY):
    for button in app.keybindsAllButtons:
        button.onHover(mouseX, mouseY)

def keybinds_onStep(app):
    if app.keyInUse and (time.time() - app.keyInUseStartTime > 2):
        app.keybindsMessage = app.defaultKeybindsMessage
        app.keyInUse = False
        app.currentKeyBindCheck = None
