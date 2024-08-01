from cmu_graphics import *
from user import User
from createAccount import *
from button import Button
from functions import *

def setupLoginScreen(app):
    app.loginTitle = 'LOGIN'
    app.loginButtonWidth = 230
    app.loginButtonHeight = 70
    app.loginButtonBuffer = 20
    app.loginButtonX = app.width / 2 - app.loginButtonWidth / 2
    app.loginButtonY = 200
    app.typingField = None
    app.loginAccountUsername = ''
    app.loginAccountPassword = ''
    app.loginAccountMessage = ''
    app.loggedIn = False
    app.messageTimer = 0
    setupLoginScreenButtons(app)

def setupLoginScreenButtons(app):
    app.usernameButton = Button(app.loginButtonX, app.loginButtonY, app.loginButtonWidth, app.loginButtonHeight, app.loginAccountUsername or 'Username', app.theme)
    app.passwordButton = Button(app.loginButtonX, app.loginButtonY + app.loginButtonHeight + app.loginButtonBuffer, app.loginButtonWidth, app.loginButtonHeight, app.loginAccountPassword or 'Password', app.theme)
    app.loginButton = Button(app.loginButtonX, app.loginButtonY + 2 * (app.loginButtonHeight + app.loginButtonBuffer), app.loginButtonWidth, app.loginButtonHeight, 'Login', app.theme)
    app.createAccountButton = Button(app.loginButtonX, app.loginButtonY + 3 * (app.loginButtonHeight + app.loginButtonBuffer), app.loginButtonWidth, app.loginButtonHeight, 'Create Account', app.theme)
    app.loginBackButton = Button(app.loginButtonX, app.loginButtonY + 4 * (app.loginButtonHeight + app.loginButtonBuffer), app.loginButtonWidth, app.loginButtonHeight, 'Back', app.theme)
    app.loginAllButtons = [app.usernameButton, app.passwordButton, app.loginButton, app.createAccountButton, app.loginBackButton]

def login_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.theme.bgColor)
    drawLoginTitle(app)
    drawLoginButtons(app)
    drawLoginMessage(app)

def drawLoginTitle(app):
    titleX = app.width / 2
    titleY = 100
    drawLabel(app.loginTitle.upper(), titleX, titleY, size=app.titleSize, fill=app.theme.titleColor, bold=True, align='center', border='black', borderWidth=1)

def drawLoginButtons(app):
    for button in app.loginAllButtons:
        button.draw()

def drawLoginMessage(app):
    messageX = app.width / 2
    messageY = app.loginButtonY - 40
    drawLabel(app.loginAccountMessage, messageX, messageY, size=20, fill='red', align='center')

def login_onMousePress(app, mouseX, mouseY):
    if app.messageTimer > 0:
        return  # Disable user interaction when a message is active

    for button in app.loginAllButtons:
        if button.checkClicked(mouseX, mouseY) or button.isClicked:
            button.onClick()
            if button.text == 'Back':
                setActiveScreen('splash')
            elif button.text == 'Create Account':
                setupCreateAccountScreen(app)
                setActiveScreen('createAccount')
            elif button == app.usernameButton:
                app.typingField = 'username'
                app.loginAccountUsername = ''
                app.usernameButton.text = ''
                app.loginAccountMessage = 'Type your username'
            elif button == app.passwordButton:
                app.typingField = 'password'
                app.loginAccountPassword = ''
                app.passwordButton.text = ''
                app.loginAccountMessage = 'Type your password'
            elif button.text == 'Login':
                handleLogin(app)

    setupLoginScreenButtons(app)  # Ensure the buttons are updated after input

def fixEmptyLoginFields(app):
    if not app.loginAccountUsername.strip():
        app.loginAccountUsername = ''
    if not app.loginAccountPassword.strip():
        app.loginAccountPassword = ''

def handleLogin(app):
    username = app.loginAccountUsername.strip()
    password = app.loginAccountPassword.strip()

    if not username:
        app.loginAccountMessage = 'Please enter a username'
    elif not password:
        app.loginAccountMessage = 'Please enter a password'
    elif not usernameExists(username):
        app.loginAccountMessage = 'Username does not exist'
    elif not passwordMatches(username, password):
        app.loginAccountMessage = 'Password is incorrect'
    else:
        app.loggedIn = True
        app.userInfo = User(username)
        updateAppWithUserInfo(app)
        setActiveScreen('splash')
        return  # Exit early since no error occurred

    # Set message timer if there was an error
    app.messageTimer = 120  # 120 steps for 2 seconds at 60 FPS

def login_onStep(app):
    if app.messageTimer > 0:
        app.messageTimer -= 1

def login_onMouseRelease(app, mouseX, mouseY):
    if app.messageTimer > 0:
        return  # Disable user interaction when a message is active

    for button in app.loginAllButtons:
        button.onRelease()

def login_onMouseMove(app, mouseX, mouseY):
    if app.messageTimer > 0:
        return  # Disable user interaction when a message is active

    for button in app.loginAllButtons:
        button.onHover(mouseX, mouseY)

def login_onKeyPress(app, key):
    if app.messageTimer > 0:
        return  # Disable user interaction when a message is active

    if not (len(key) == 1 and (key.isalnum() or key in ['backspace', 'enter'])):
        return

    if app.typingField is not None:
        if app.typingField == 'username':
            handleTyping(app, key, 'username')
        elif app.typingField == 'password':
            handleTyping(app, key, 'password')

    fixEmptyLoginFields(app)
    setupLoginScreenButtons(app)

def handleTyping(app, key, field):
    if field == 'username':
        if key == 'backspace' and app.loginAccountUsername:
            app.loginAccountUsername = app.loginAccountUsername[:-1]
        elif key == 'enter':
            app.typingField = None
        elif key.isalnum():
            app.loginAccountUsername += key
        app.usernameButton.text = app.loginAccountUsername
    elif field == 'password':
        if key == 'backspace' and app.loginAccountPassword:
            app.loginAccountPassword = app.loginAccountPassword[:-1]
        elif key == 'enter':
            app.typingField = None
        elif key.isalnum():
            app.loginAccountPassword += key
        app.passwordButton.text = app.loginAccountPassword

def clearCreateAccountFields(app):
    app.loginAccountUsername = ''
    app.loginAccountPassword = ''
    setupLoginScreenButtons(app)
