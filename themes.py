class Theme:
    def __init__(self, bgColor, buttonColor, buttonBorderColor, textColor, hoverBorderColor, clickColor, gridColor, cellColor, activeColor, correctGuessColor, wrongGuessColor):
        self.bgColor = bgColor
        self.buttonColor = buttonColor
        self.buttonBorderColor = buttonBorderColor
        self.textColor = textColor
        self.hoverBorderColor = hoverBorderColor
        self.clickColor = clickColor
        self.gridColor = gridColor
        self.cellColor = cellColor
        self.highlightedColor = activeColor
        self.correctGuessColor = correctGuessColor
        self.wrongGuessColor = wrongGuessColor

lightTheme = Theme(bgColor='white', buttonColor='lightgray', buttonBorderColor='black', textColor='black', hoverBorderColor='cyan', clickColor='darkgray', gridColor='black', cellColor='white', activeColor='lightSkyBlue', correctGuessColor='lightGreen', wrongGuessColor='tomato')
redTheme = Theme(bgColor='fireBrick', buttonColor='fireBrick', buttonBorderColor='black', textColor='white', hoverBorderColor='lightcoral', clickColor='maroon', gridColor='black', cellColor='fireBrick', activeColor='pink', correctGuessColor='lightGreen', wrongGuessColor='orange')
blueTheme = Theme(bgColor='dodgerBlue', buttonColor='dodgerBlue', buttonBorderColor='black', textColor='white', hoverBorderColor='lightblue', clickColor='navy', gridColor='black', cellColor='dodgerBlue', activeColor='skyblue', correctGuessColor='lightGreen', wrongGuessColor='tomato')
