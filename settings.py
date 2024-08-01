from cmu_graphics import *
from button import Button
from keybinds import *
from user import *
from functions import *

def settings_onScreenActivate(app):
    setupSettingsScreen(app)

def setupSettingsScreen(app):
    app.settingButtons = []
    app.settingsTitle = 'SETTINGS'
    app.settingButtonWidth = 230
    app.settingButtonHeight = 70
    app.settingButtonBuffer = 20
    app.settingButtonX = app.width / 2 - app.settingButtonWidth / 2
    app.settingButtonY = 200
    setupSettingsScreenButtons(app)

def resetSettings(app):
    app.themeIndex = 2
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
    
    # Change the text of the mute button based on current mute status
    muteButtonText = 'Unmute Volume' if app.muteVolume else 'Mute Volume'
    app.muteVolumeButton = Button(app.settingButtonX, app.settingButtonY + 2 * (app.settingButtonHeight + app.settingButtonBuffer), app.settingButtonWidth, app.settingButtonHeight, muteButtonText, app.theme)
    
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
                setupSettingsScreenButtons(app)  # Update buttons to reflect the new theme
            elif button.text == 'Save and Exit':
                saveSettings(app)
                setActiveScreen('splash')
            elif button.text == 'Reset':
                resetSettings(app)
            elif button.text == 'Keybinds':
                setActiveScreen('keybinds')
            elif button.text == 'Mute Volume' or button.text == 'Unmute Volume':
                app.muteVolume = not app.muteVolume
                setupSettingsScreenButtons(app)  # Update buttons to reflect the mute status

def saveSettings(app):
    if app.loggedIn:
        # Update user info before saving
        app.userInfo.themeIndex = app.themeIndex
        app.userInfo.keybinds = app.keybinds
        app.userInfo.muteVolume = app.muteVolume
        app.userInfo.save()  # Use User class to save
        print(f"Settings saved for user: {app.userInfo.username}")
        updateAppWithUserInfo(app)

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
    drawLabel(app.settingsTitle.upper(), titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)
