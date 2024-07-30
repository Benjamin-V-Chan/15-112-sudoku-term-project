from cmu_graphics import *
from themes import lightTheme, redTheme, blueTheme
from splash import *

def onAppStart(app):
    app.menuBarHeight = 50
    app.menuBarButtonBuffer = 10
    app.buttonWidth = 100
    app.themes = [lightTheme, redTheme, blueTheme]
    app.themeIndex = 0
    app.theme = app.themes[app.themeIndex]

    setActiveScreen('splash')
    setupSplashScreen(app)

def main():
    runAppWithScreens(initialScreen='splash', width=600, height=600)

main()