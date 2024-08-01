from cmu_graphics import *
from button import *
from createAccount import *
import os

def setupLoginScreen(app):
    app.loginTitle = 'LOGIN'
    app.loginButtonWidth = 230
    app.loginButtonHeight = 70
    app.loginButtonBuffer = 20
    app.loginButtonX = app.width / 2 - app.loginButtonWidth / 2
    app.loginButtonY = 200
    app.typingField = None
    app.loginAccountUsername = 'Username'
    app.loginAccountPassword = 'Password'
    app.loginAccountMessage = ''
    setupLoginScreenButtons(app)

def setupLoginScreenButtons(app):
    app.usernameButton = Button(app.loginButtonX, app.loginButtonY, app.loginButtonWidth, app.loginButtonHeight, app.loginAccountUsername, app.theme)
    app.passwordButton = Button(app.loginButtonX, app.loginButtonY + app.loginButtonHeight + app.loginButtonBuffer, app.loginButtonWidth, app.loginButtonHeight, app.loginAccountPassword, app.theme)
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
    for button in app.loginAllButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Back':
                setActiveScreen('splash')
            elif button.text == 'Create Account':
                setupCreateAccountScreen(app)
                setActiveScreen('createAccount')
            elif button.text == app.loginAccountUsername or button.text == 'Username':
                app.typingField = 'username'
                app.loginAccountUsername = ''
                app.usernameButton.text = ''
            elif button.text == app.loginAccountPassword or button.text == 'Password':
                app.typingField = 'password'
                app.loginAccountPassword = ''
                app.passwordButton.text = ''
            elif button.text == 'Login':
                handleLogin(app)

def handleLogin(app):
    if not usernameExists(app.loginAccountUsername):
        app.loginAccountMessage = 'Username does not exist'
        clearCreateAccountFields(app)
    elif not passwordMatches(app.loginAccountUsername, app.loginAccountPassword):
        app.loginAccountMessage = 'Password is incorrect'
        clearCreateAccountFields(app)
    else:
        app.loginAccountMessage = ''
        app.loggedIn = True
        app.userInfo = retrieveUserInfo(app.loginAccountUsername)
        setActiveScreen('splash')

def login_onMouseRelease(app, mouseX, mouseY):
    for button in app.loginAllButtons:
        button.onRelease()

def login_onMouseMove(app, mouseX, mouseY):
    for button in app.loginAllButtons:
        button.onHover(mouseX, mouseY)

def login_onKeyPress(app, key):
    if app.typingField is not None:
        if app.typingField == 'username':
            if key == 'backspace' and app.loginAccountUsername:
                app.loginAccountUsername = app.loginAccountUsername[:-1]
            elif key == 'enter':
                app.typingField = None
            elif key.isalpha() or key.isdigit():
                app.loginAccountUsername += key
            app.usernameButton.text = app.loginAccountUsername
        elif app.typingField == 'password':
            if key == 'backspace' and app.loginAccountPassword:
                app.loginAccountPassword = app.loginAccountPassword[:-1]
            elif key == 'enter':
                app.typingField = None
            elif key.isalpha() or key.isdigit():
                app.loginAccountPassword += key
            app.passwordButton.text = app.loginAccountPassword
    setupLoginScreenButtons(app)

def usernameExists(username):
    return os.path.isfile(f'users/{username}')

def passwordMatches(username, password):
    if os.path.isfile(f'users/{username}'):
        with open(f'users/{username}', 'r') as file:
            savedPassword = file.readline().strip().split(':')[1]
            return savedPassword == password
    return False

def clearCreateAccountFields(app):
    app.loginAccountUsername = 'Username'
    app.loginAccountPassword = 'Password'
    setupLoginScreenButtons(app)