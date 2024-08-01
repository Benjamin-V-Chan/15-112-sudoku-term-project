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
            elif button == app.passwordButton:
                app.typingField = 'password'
                app.createAccountPassword = ''
                app.passwordButton.text = ''
            break
    fixEmptyCreateAccountFields(app)
    setupCreateAccountScreenButtons(app)


def login_onMousePress(app, mouseX, mouseY):
    for button in app.loginAllButtons:
        if button.checkClicked(mouseX, mouseY):
            button.onClick()
            if button.text == 'Back':
                setActiveScreen('splash')
            elif button.text == 'Create Account':
                setupCreateAccountScreen(app)
                setActiveScreen('createAccount')
            elif button.text == app.usernameButton:
                app.typingField = 'username'
                app.loginAccountUsername = ''
                app.usernameButton.text = ''
            elif button == app.passwordButton:
                app.typingField = 'password'
                app.loginAccountPassword = ''
                app.passwordButton.text = ''
            elif button.text == 'Login':
                handleLogin(app)
            break
    fixEmptyLoginFields(app)
    setupLoginScreenButtons(app)