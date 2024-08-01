from cmu_graphics import *
from themes import *
from splash import *
from audio import *
from settings import resetSettings

def onAppStart(app):
    app.menuBarHeight = 50
    app.menuBarButtonBuffer = 10
    app.buttonWidth = 10
    app.titleSize = 65
    app.gameFinished = False
    app.loggedIn = False
    app.themes = [lightTheme, redTheme, blueTheme, greenTheme]
    
    resetSettings(app)
    setupSounds(app)
    setActiveScreen('splash')

def main():
    runAppWithScreens(initialScreen='splash', width=700, height=700)

main()