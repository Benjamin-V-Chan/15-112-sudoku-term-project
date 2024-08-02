from cmu_graphics import *
from button import Button
from user import *
from functions import *
import time

def createAccount_onScreenActivate(app):
    setupCreateAccountScreen(app)
    
def setupCreateAccountScreen(app):
    app.createAccountTitle = 'CREATE ACCOUNT'
    app.createAccountButtonWidth = 230
    app.createAccountButtonHeight = 70
    app.createAccountButtonBuffer = 20
    app.createAccountButtonX = app.width / 2 - app.createAccountButtonWidth / 2
    app.createAccountButtonY = 200
    app.typingField = None
    app.messageStartTime = None
    resetCreateAccountInfo(app)
    setupCreateAccountScreenButtons(app)

def resetCreateAccountInfo(app):
    app.createAccountUsername = ''
    app.createAccountPassword = ''
    app.createAccountMessage = ''

def setupCreateAccountScreenButtons(app):
    app.usernameButton = Button(app.createAccountButtonX, app.createAccountButtonY, app.createAccountButtonWidth, app.createAccountButtonHeight, app.createAccountUsername or 'Username', app.theme)
    app.passwordButton = Button(app.createAccountButtonX, app.createAccountButtonY + app.createAccountButtonHeight + app.createAccountButtonBuffer, app.createAccountButtonWidth, app.createAccountButtonHeight, app.createAccountPassword or 'Password', app.theme)
    app.createAccountButton = Button(app.createAccountButtonX, app.createAccountButtonY + 2 * (app.createAccountButtonHeight + app.createAccountButtonBuffer), app.createAccountButtonWidth, app.createAccountButtonHeight, 'Create Account', app.theme)
    app.createAccountBackButton = Button(app.createAccountButtonX, app.createAccountButtonY + 3 * (app.createAccountButtonHeight + app.createAccountButtonBuffer), app.createAccountButtonWidth, app.createAccountButtonHeight, 'Back', app.theme)
    app.createAccountAllButtons = [app.usernameButton, app.passwordButton, app.createAccountButton, app.createAccountBackButton]

def createAccount_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawCreateAccountTitle(app)
    drawCreateAccountButtons(app)
    drawCreateAccountMessage(app)

def drawCreateAccountTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.createAccountTitle.upper(), titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def drawCreateAccountButtons(app):
    for button in app.createAccountAllButtons:
        button.draw()

def drawCreateAccountMessage(app):
    if app.createAccountMessage:
        messageX = app.width / 2
        messageY = app.createAccountButtonY - 40
        drawLabel(app.createAccountMessage, messageX, messageY, size=20, fill='red', align='center')

def createAccount_onMousePress(app, mouseX, mouseY):
    if app.messageStartTime is not None:
        return  # Disable user interaction when a message is active

    for button in app.createAccountAllButtons:
        button.isSelected = False
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Back':
                setActiveScreen('splash')
            elif button.text == 'Create Account':
                handleCreateAccount(app)
            elif button == app.usernameButton:
                button.isSelected = True
                app.typingField = 'username'
                app.createAccountUsername = ''
                app.usernameButton.text = ''
                app.createAccountMessage = 'Type your username'
            elif button == app.passwordButton:
                button.isSelected = True
                app.typingField = 'password'
                app.createAccountPassword = ''
                app.passwordButton.text = ''
                app.createAccountMessage = 'Type your password'
            break

    setupCreateAccountScreenButtons(app)

def fixEmptyCreateAccountFields(app):
    if not app.createAccountUsername.strip():
        app.createAccountUsername = ''
    if not app.createAccountPassword.strip():
        app.createAccountPassword = ''

def handleCreateAccount(app):
    username = app.createAccountUsername.strip()
    password = app.createAccountPassword.strip()

    if usernameExists(username):
        app.createAccountMessage = 'Username already exists'
    elif not username:
        app.createAccountMessage = 'Username cannot be empty'
    elif not password:
        app.createAccountMessage = 'Password cannot be empty'
    elif username.lower() == 'username':
        app.createAccountMessage = 'Invalid username'
    elif password.lower() == 'password':
        app.createAccountMessage = 'Invalid password'
    else:
        app.loggedIn = True
        saveUserInfo(username, password, app.themeIndex, app.keybinds, app.muteVolume)
        app.userInfo = User(username)
        setActiveScreen('splash')
        return 

    app.messageStartTime = time.time()

def createAccount_onStep(app):
    if app.messageStartTime is not None:
        elapsed_time = time.time() - app.messageStartTime
        if elapsed_time > 2:
            app.messageStartTime = None
            app.createAccountMessage = ''

def createAccount_onKeyPress(app, key):
    if app.messageStartTime is not None:
        return  # Disable user interaction when a message is active

    if not (len(key) == 1 and (key.isalnum() or key in ['backspace', 'enter'])):
        return

    if app.typingField is not None:
        if app.typingField == 'username':
            handleTyping(app, key, 'username')
        elif app.typingField == 'password':
            handleTyping(app, key, 'password')

    fixEmptyCreateAccountFields(app)
    setupCreateAccountScreenButtons(app)

def handleTyping(app, key, field):
    if field == 'username':
        if key == 'backspace' and app.createAccountUsername:
            app.createAccountUsername = app.createAccountUsername[:-1]
        elif key == 'enter':
            app.typingField = None
        elif key.isalnum():
            app.createAccountUsername += key
        app.usernameButton.text = app.createAccountUsername
    elif field == 'password':
        if key == 'backspace' and app.createAccountPassword:
            app.createAccountPassword = app.createAccountPassword[:-1]
        elif key == 'enter':
            app.typingField = None
        elif key.isalnum():
            app.createAccountPassword += key
        app.passwordButton.text = app.createAccountPassword

def createAccount_onMouseRelease(app, mouseX, mouseY):
    if app.messageStartTime is not None:
        return

    for button in app.createAccountAllButtons:
        button.onRelease()

def createAccount_onMouseMove(app, mouseX, mouseY):
    if app.messageStartTime is not None:
        return

    for button in app.createAccountAllButtons:
        button.onHover(mouseX, mouseY)