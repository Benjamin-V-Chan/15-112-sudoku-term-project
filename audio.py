from cmu_graphics import *
import os, pathlib

# TP Recourses Documentation - SoundDemo File
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def setupSounds(app):
    # Pixabay - 'Game Music' from DeepMusicEveryDay
    app.playMusic = loadSound('audio/play.mp3')

    # Pixabay - Button from UNIVERSFIELD
    app.buttonClick = loadSound('audio/buttonClick.mp3')

    # Pixabay - Glass Of Winem from Monument_Music
    app.splashMusic = loadSound('audio/splash.mp3')


    # Pixabay - 'Correct' from chrisiex1
    app.correctSound = loadSound('audio/correct.mp3')

    # Pixabay - 'Error #4' from UNIVERSFIELD
    app.incorrectSound = loadSound('audio/incorrect.mp3')