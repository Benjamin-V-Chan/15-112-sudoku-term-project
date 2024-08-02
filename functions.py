import os

def updateAppWithUserInfo(app):
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
        'muteVolume': muteVolume == 'True'
    }

def passwordMatches(username, password):
    userInfo = retrieveUserInfo(username)
    return userInfo['password'] == password

def isValid(grid, row, col, num):
    # Check if it's valid to place a number in a specific cell.
    
    for c in range(9):
        if grid[row][c] == num:
            return False

    for r in range(9):
        if grid[r][col] == num:
            return False

    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for r in range(startRow, startRow + 3):
        for c in range(startCol, startCol + 3):
            if grid[r][c] == num:
                return False

    return True