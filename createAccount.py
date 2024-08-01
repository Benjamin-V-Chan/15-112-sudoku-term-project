from cmu_graphics import *
from button import *
from user import *

def setupCreateAccountScreen(app):
    app.createAccountTitle = 'CREATE ACCOUNT'
    app.createAccountButtonWidth = 230
    app.createAccountButtonHeight = 70
    app.createAccountButtonBuffer = 20
    app.createAccountButtonX = app.width / 2 - app.createAccountButtonWidth / 2
    app.createAccountButtonY = 200
    app.typingField = None
    app.createAccountUsername = ''
    app.createAccountPassword = ''
    app.createAccountMessage = ''
    setupCreateAccountScreenButtons(app)

def setupCreateAccountScreenButtons(app):
    app.usernameButton = Button(app.createAccountButtonX, app.createAccountButtonY, app.createAccountButtonWidth, app.createAccountButtonHeight, 'Username', app.theme)
    app.passwordButton = Button(app.createAccountButtonX, app.createAccountButtonY + app.createAccountButtonHeight + app.createAccountButtonBuffer, app.createAccountButtonWidth, app.createAccountButtonHeight, 'Password', app.theme)
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
    messageX = app.width / 2
    messageY = app.createAccountButtonY - 40
    drawLabel(app.createAccountMessage, messageX, messageY, size=20, fill='red', align='center')

def createAccount_onMousePress(app, mouseX, mouseY):
    for button in app.createAccountAllButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Back':
                setActiveScreen('splash')
            elif button.text == 'Create Account':
                handleCreateAccount(app)
            elif button == app.usernameButton:
                app.typingField = 'username'
                app.createAccountUsername = ''
                app.usernameButton.text = ''
                app.createAccountMessage = 'Type a username'
            elif button == app.passwordButton:
                app.typingField = 'password'
                app.createAccountPassword = ''
                app.passwordButton.text = ''
                app.createAccountMessage = 'Type a password'
            return

def handleCreateAccount(app):
    if usernameExists(app.createAccountUsername):
        app.createAccountMessage = 'Username already exists'
    elif app.createAccountUsername == '':
        app.createAccountMessage = 'Username cannot be empty'
    elif app.createAccountPassword == '':
        app.createAccountMessage = 'Password cannot be empty'
    elif app.createAccountUsername.lower() == 'username':
        app.createAccountMessage = 'Invalid username'
    elif app.createAccountPassword.lower() == 'password':
        app.createAccountMessage = 'Invalid password'
    else:
        app.loggedIn = True
        saveUserInfo(app.createAccountUsername, app.createAccountPassword, app.theme, app.keybinds, app.muteVolume)
        app.userInfo = User(app.createAccountUsername)
        setActiveScreen('splash')
    clearCreateAccountFields(app)

def clearCreateAccountFields(app):
    app.createAccountUsername = ''
    app.createAccountPassword = ''
    updateCreateAccountButtons(app)

def usernameExists(username):
    return os.path.isfile(f'users/{username}')

def createAccount_onKeyPress(app, key):
    if app.typingField is not None:
        if app.typingField == 'username':
            if key == 'backspace' and app.createAccountUsername:
                app.createAccountUsername = app.createAccountUsername[:-1]
            elif key == 'enter':
                app.typingField = None
            elif key.isalpha() or key.isdigit():
                app.createAccountUsername += key
            app.usernameButton.text = app.createAccountUsername
        elif app.typingField == 'password':
            if key == 'backspace' and app.createAccountPassword:
                app.createAccountPassword = app.createAccountPassword[:-1]
            elif key == 'enter':
                app.typingField = None
            elif key.isalpha() or key.isdigit():
                app.createAccountPassword += key
            app.passwordButton.text = app.createAccountPassword

def updateCreateAccountButtons(app):
    app.usernameButton.text = app.createAccountUsername or 'Username'
    app.passwordButton.text = app.createAccountPassword or 'Password'

def createAccount_onMouseRelease(app, mouseX, mouseY):
    for button in app.createAccountAllButtons:
        button.onRelease()

def createAccount_onMouseMove(app, mouseX, mouseY):
    for button in app.createAccountAllButtons:
        button.onHover(mouseX, mouseY)