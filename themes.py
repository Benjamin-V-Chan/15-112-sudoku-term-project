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
        self.activeColor = activeColor
        self.correctGuessColor = correctGuessColor
        self.wrongGuessColor = wrongGuessColor

# Define the themes
lightTheme = Theme(bgColor='white', buttonColor='lightgray', buttonBorderColor='black', textColor='black', hoverBorderColor='cyan', clickColor='darkgray', gridColor='black', cellColor='white', activeColor='lightSkyBlue', correctGuessColor='lightGreen', wrongGuessColor='tomato')
darkTheme = Theme(bgColor='black', buttonColor='darkgray', buttonBorderColor='white', textColor='white', hoverBorderColor='lightcyan', clickColor='gray', gridColor='white', cellColor='black', activeColor='lightgrey', correctGuessColor='darkgreen', wrongGuessColor='red')
redTheme = Theme(bgColor='darkred', buttonColor='red', buttonBorderColor='black', textColor='white', hoverBorderColor='lightcoral', clickColor='maroon', gridColor='black', cellColor='red', activeColor='pink', correctGuessColor='darkgreen', wrongGuessColor='orange')
blueTheme = Theme(bgColor='darkblue', buttonColor='blue', buttonBorderColor='black', textColor='white', hoverBorderColor='lightblue', clickColor='navy', gridColor='black', cellColor='blue', activeColor='skyblue', correctGuessColor='darkgreen', wrongGuessColor='orange')
greenTheme = Theme(bgColor='darkgreen', buttonColor='green', buttonBorderColor='black', textColor='white', hoverBorderColor='lightgreen', clickColor='forestgreen', gridColor='black', cellColor='green', activeColor='lightgreen', correctGuessColor='darkgreen', wrongGuessColor='orange')
