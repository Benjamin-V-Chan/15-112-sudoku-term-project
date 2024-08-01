from cmu_graphics import *
from audio import *

class Button:
    def __init__(self, x, y, width, height, text, theme, textSize=25, customFill=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textSize = textSize
        self.theme = theme
        self.isHovered = False
        self.isClicked = False
        self.isSelected = False
        self.customFill = customFill

    def __eq__(self, other):
        return self.text == other.text and self.x == other.x and self.y == other.y

    def draw(self):
        borderColor = self.theme.hoverBorderColor if self.isHovered else self.theme.buttonBorderColor
        if self.isSelected or self.isClicked:
            fillColor = self.theme.clickColor
        else:
            fillColor = self.theme.buttonColor
        if self.customFill is not None:
            fillColor = self.customFill
        else:
            fillColor = self.theme.buttonColor
        drawRect(self.x, self.y, self.width, self.height, fill=fillColor, border=borderColor, borderWidth=4)
        drawLabel(self.text, self.x + self.width / 2, self.y + self.height / 2, size=self.textSize, fill=self.theme.textColor, bold=True, align='center')

    def checkClicked(self, mouseX, mouseY):
        return self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height

    def onHover(self, mouseX, mouseY):
        self.isHovered = self.checkClicked(mouseX, mouseY)

    def onClick(self):
        if not app.muteVolume:
            app.buttonClick.play(restart=True)
        self.isClicked = True

    def onRelease(self):
        self.isClicked = False
