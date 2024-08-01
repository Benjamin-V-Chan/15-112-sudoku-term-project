import os

def updateAppWithUserInfo(app):
    print(f"Updating app with user info: ThemeIndex: {app.userInfo.themeIndex}, Keybinds: {app.userInfo.keybinds}, MuteVolume: {app.userInfo.muteVolume}")
    app.theme = app.themes[app.userInfo.themeIndex]
    app.keybinds = app.userInfo.keybinds
    app.muteVolume = app.userInfo.muteVolume

def usernameExists(username):
    return os.path.isfile(f'users/{username}')

def saveUserInfo(username, password, themeIndex, keybinds, muteVolume):
    keybindsSave = ""
    for key, value in keybinds.items():
        keybindsSave += f"{key}:{value}\n"
    
    with open(f"users/{username}", "w") as file:
        file.write(f"password:{password}\n")
        file.write(f"themeIndex:{themeIndex}\n")
        file.write(keybindsSave)
        file.write(f"muteVolume:{muteVolume}\n")

def retrieveUserInfo(username):
    with open(f"users/{username}", "r") as file:
        lines = file.readlines()
    
    password = lines[0].split(':')[1].strip()
    themeIndex = lines[1].split(':')[1].strip()
    keybinds = {}
    for line in lines[2:-1]:
        key, value = line.strip().split(':')
        keybinds[key] = value
    muteVolume = lines[-1].split(':')[1].strip()
    
    return {
        'password': password,
        'themeIndex': int(themeIndex),
        'keybinds': keybinds,
        'muteVolume': muteVolume == 'True'  # Ensure muteVolume is a boolean
    }

def passwordMatches(username, password):
    userInfo = retrieveUserInfo(username)
    return userInfo['password'] == password
