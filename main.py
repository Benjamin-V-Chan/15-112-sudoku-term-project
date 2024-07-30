from cmu_graphics import *
from themes import *
from splash import *

def onAppStart(app):
    app.menuBarHeight = 50
    app.menuBarButtonBuffer = 10
    app.buttonWidth = 10
    app.themes = [lightTheme, redTheme, blueTheme, greenTheme, yellowTheme, purpleTheme, orangeTheme, pinkTheme, brownTheme, blackTheme]
    app.themeIndex = 0
    app.theme = app.themes[app.themeIndex]

    setActiveScreen('splash')
    setupSplashScreen(app)

def main():
    runAppWithScreens(initialScreen='splash', width=800, height=800)

main()