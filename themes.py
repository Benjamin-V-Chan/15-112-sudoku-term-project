class Theme:
    def __init__(self, bgColor, buttonColor, buttonBorderColor, textColor, hoverBorderColor, clickColor, gridColor, cellColor, activeColor, correctGuessColor, wrongGuessColor, singleGuessColor):
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
        self.singleGuessColor = singleGuessColor

lightTheme = Theme(bgColor='white', buttonColor='lightgray', buttonBorderColor='black', textColor='black', hoverBorderColor='cyan', clickColor='darkgray', gridColor='black', cellColor='white', activeColor='lightSkyBlue', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
redTheme = Theme(bgColor='fireBrick', buttonColor='fireBrick', buttonBorderColor='black', textColor='white', hoverBorderColor='lightcoral', clickColor='maroon', gridColor='black', cellColor='fireBrick', activeColor='pink', correctGuessColor='lightGreen', wrongGuessColor='orange', singleGuessColor='yellow')
blueTheme = Theme(bgColor='dodgerBlue', buttonColor='dodgerBlue', buttonBorderColor='black', textColor='white', hoverBorderColor='lightblue', clickColor='navy', gridColor='black', cellColor='dodgerBlue', activeColor='skyblue', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
greenTheme = Theme(bgColor='forestGreen', buttonColor='forestGreen', buttonBorderColor='black', textColor='white', hoverBorderColor='lightgreen', clickColor='darkgreen', gridColor='black', cellColor='forestGreen', activeColor='lightgreen', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
yellowTheme = Theme(bgColor='gold', buttonColor='gold', buttonBorderColor='black', textColor='black', hoverBorderColor='lightyellow', clickColor='darkgoldenrod', gridColor='black', cellColor='gold', activeColor='lightyellow', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='orange')
purpleTheme = Theme(bgColor='purple', buttonColor='purple', buttonBorderColor='black', textColor='white', hoverBorderColor='violet', clickColor='indigo', gridColor='black', cellColor='purple', activeColor='violet', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
orangeTheme = Theme(bgColor='orange', buttonColor='orange', buttonBorderColor='black', textColor='black', hoverBorderColor='coral', clickColor='darkorange', gridColor='black', cellColor='orange', activeColor='lightcoral', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
pinkTheme = Theme(bgColor='pink', buttonColor='pink', buttonBorderColor='black', textColor='black', hoverBorderColor='lightpink', clickColor='deeppink', gridColor='black', cellColor='pink', activeColor='lightpink', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
brownTheme = Theme(bgColor='saddleBrown', buttonColor='saddleBrown', buttonBorderColor='black', textColor='white', hoverBorderColor='sienna', clickColor='maroon', gridColor='black', cellColor='saddleBrown', activeColor='sienna', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
blackTheme = Theme(bgColor='black', buttonColor='black', buttonBorderColor='black', textColor='white', hoverBorderColor='gray', clickColor='darkgray', gridColor='white', cellColor='black', activeColor='gray', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow')
