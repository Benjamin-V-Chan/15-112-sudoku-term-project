from functions import retrieveUserInfo, saveUserInfo

class User:
    def __init__(self, username):
        userInfo = retrieveUserInfo(username)
        self.username = username
        self.password = userInfo['password']
        self.themeIndex = userInfo['themeIndex']
        self.keybinds = userInfo['keybinds']
        self.muteVolume = userInfo['muteVolume']
    
    def save(self):
        saveUserInfo(self.username, self.password, self.themeIndex, self.keybinds, self.muteVolume)
