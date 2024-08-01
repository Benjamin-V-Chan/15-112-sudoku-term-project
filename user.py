def saveUserInfo(username, password, theme, keybinds, muteVolume):
    keybindsSave = ""
    for key, value in keybinds.items():
        keybindsSave += f"{key}:{value}\n"
    
    with open(f"users/{username}", "w") as file:
        file.write(f"password:{password}\n")
        file.write(f"theme:{theme}\n")
        file.write(keybindsSave)
        file.write(f"muteVolume:{muteVolume}\n")

def retrieveUserInfo(username):
    with open(f"users/{username}", "r") as file:
        lines = file.readlines()
    
    password = lines[0].split(':')[1].strip()
    theme = lines[1].split(':')[1].strip()
    keybinds = {}
    for line in lines[2:-1]:
        key, value = line.strip().split(':')
        keybinds[key] = value
    muteVolume = lines[-1].split(':')[1].strip()
    
    return {
        'password': password,
        'theme': theme,
        'keybinds': keybinds,
        'muteVolume': muteVolume
    }

def passwordMatches(username, password):
    userInfo = retrieveUserInfo(username)
    return userInfo['password'] == password

class User:
    def __init__(self, username):
        self.username = username
        userInfo = retrieveUserInfo(username)
        self.password = userInfo['password']
        self.theme = userInfo['theme']
        self.keybinds = userInfo['keybinds']
        self.muteVolume = userInfo['muteVolume']
    
    def save(self):
        saveUserInfo(self.username, self.password, self.theme, self.keybinds, self.muteVolume)
