from cmu_graphics import *
from button import *
from keybinds import *

def settings_onScreenActivate(app):
    setupSettingsScreen(app)

def setupSettingsScreen(app):
    app.settingButtons = []
    app.settingsTitle = 'Settings'
    app.settingButtonWidth = 200
    app.settingButtonHeight = 50
    app.settingButtonBuffer = 10
    app.settingButtonX = app.width / 2 - app.settingButtonWidth / 2
    app.settingButtonY = 180
    setupSettingsScreenButtons(app)
    
def resetSettings(app):
    app.themeIndex = 0
    app.theme = app.themes[app.themeIndex]
    app.keybinds = {
        'Up': 'up',
        'Down': 'down',
        'Left': 'left',
        'Right': 'right',
        'Toggle Manual Guess Mode': 'g',
        'Toggle Auto Guess Mode': 'a'
    }
    app.muteVolume = False

def setupSettingsScreenButtons(app):
    app.changeThemeButton = Button(app.settingButtonX, app.settingButtonY, app.settingButtonWidth, app.settingButtonHeight, 'Change Theme', app.theme)
    app.keybindsButton = Button(app.settingButtonX, app.settingButtonY + app.settingButtonHeight + app.settingButtonBuffer, app.settingButtonWidth, app.settingButtonHeight, 'Keybinds', app.theme)
    app.muteVolumeButton = Button(app.settingButtonX, app.settingButtonY + 2 * (app.settingButtonHeight + app.settingButtonBuffer), app.settingButtonWidth, app.settingButtonHeight, 'Mute Volume', app.theme)
    app.resetButton = Button(app.settingButtonX, app.settingButtonY + 3 * (app.settingButtonHeight + app.settingButtonBuffer), app.settingButtonWidth, app.settingButtonHeight, 'Reset', app.theme)
    app.exitButton = Button(app.settingButtonX, app.settingButtonY + 4 * (app.settingButtonHeight + app.settingButtonBuffer), app.settingButtonWidth, app.settingButtonHeight, 'Save and Exit', app.theme)

    app.settingsAllButtons = [app.changeThemeButton, app.keybindsButton, app.muteVolumeButton, app.resetButton, app.exitButton]

def settings_onMousePress(app, mouseX, mouseY):
    for button in app.settingsAllButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Change Theme':
                app.themeIndex = (app.themeIndex + 1) % len(app.themes)
                app.theme = app.themes[app.themeIndex]
                setupSettingsScreenButtons(app)
            elif button.text == 'Save and Exit':
                setActiveScreen('splash')
            elif button.text == 'Reset':
                resetSettings(app)
                setupSettingsScreenButtons(app)
            elif button.text == 'Keybinds':
                setActiveScreen('keybinds')
                setupKeybindsScreen(app)


def settings_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawTitle(app)
    drawSettingsButtons(app)

def drawSettingsButtons(app):
    for button in app.settingsAllButtons:
        button.draw()

def settings_onMouseMove(app, mouseX, mouseY):
    for button in app.settingsAllButtons:
        button.onHover(mouseX, mouseY)

def settings_onMouseRelease(app, mouseX, mouseY):
    for button in app.settingsAllButtons:
        button.onRelease()

def drawTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.settingsTitle, titleX, titleY, size=app.titleSize, fill=app.colors[0], bold=True, align='center', border='black', borderWidth=1)