from cmu_graphics import *

class Button:
    def __init__(self, x, y, width, height, text, theme, textSize=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textSize = textSize
        self.theme = theme
        self.isHovered = False
        self.isClicked = False

    def draw(self):
        borderColor = self.theme.hoverBorderColor if self.isHovered else self.theme.buttonBorderColor
        fillColor = self.theme.clickColor if self.isClicked else self.theme.buttonColor
        drawRect(self.x, self.y, self.width, self.height, fill=fillColor, border=borderColor)
        drawLabel(self.text, self.x + self.width / 2, self.y + self.height / 2, size=self.textSize, fill=self.theme.textColor, bold=True, align='center')

    def checkClicked(self, mouseX, mouseY):
        return self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height

    def onHover(self, mouseX, mouseY):
        self.isHovered = self.checkClicked(mouseX, mouseY)

    def onClick(self):
        self.isClicked = True

    def onRelease(self):
        self.isClicked = False
