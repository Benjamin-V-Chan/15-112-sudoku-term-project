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
        'muteVolume': muteVolume == 'True'  # Ensure muteVolume is a boolean
    }

def passwordMatches(username, password):
    userInfo = retrieveUserInfo(username)
    return userInfo['password'] == password

def isValid(grid, row, col, num):
    """
    Check if it's valid to place a number in a specific cell.
    
    Args:
        grid (list of list of int): The Sudoku board represented as a 2D list.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        num (int): The number to be placed in the cell.
        
    Returns:
        bool: True if the number can be placed, False otherwise.
    """
    
    # Check the row
    for c in range(9):
        if grid[row][c] == num:
            return False

    # Check the column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # Check the 3x3 subgrid
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for r in range(startRow, startRow + 3):
        for c in range(startCol, startCol + 3):
            if grid[r][c] == num:
                return False

    # If no conflicts, return True
    return True