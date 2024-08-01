from cmu_graphics import gradient

class Theme:
    def __init__(self, bgColor, buttonColor, buttonBorderColor, textColor, hoverBorderColor, clickColor, gridColor, cellColor, activeColor, correctGuessColor, wrongGuessColor, singleGuessColor, tupleColor, titleColor):
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
        self.tupleColor = tupleColor
        self.titleColor = titleColor

lightTheme = Theme(bgColor='white', buttonColor='white', buttonBorderColor='black', textColor='black', hoverBorderColor='cyan', clickColor='darkgray', gridColor='black', cellColor='white', activeColor='lightSkyBlue', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
redTheme = Theme(bgColor='darkRed', buttonColor='darkRed', buttonBorderColor='white', textColor='white', hoverBorderColor='lightcoral', clickColor='darkRed', gridColor='black', cellColor='darkRed', activeColor='pink', correctGuessColor='lightGreen', wrongGuessColor='orange', singleGuessColor='yellow', tupleColor='orange', titleColor='white')
blueTheme = Theme(bgColor='dodgerBlue', buttonColor='dodgerBlue', buttonBorderColor='black', textColor='black', hoverBorderColor='lightblue', clickColor='navy', gridColor='black', cellColor='dodgerBlue', activeColor='skyblue', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
greenTheme = Theme(bgColor='forestGreen', buttonColor='forestGreen', buttonBorderColor='black', textColor='black', hoverBorderColor='lightgreen', clickColor='darkgreen', gridColor='black', cellColor='forestGreen', activeColor='lightgreen', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
purpleTheme = Theme(bgColor='purple', buttonColor='purple', buttonBorderColor='white', textColor='white', hoverBorderColor='violet', clickColor='indigo', gridColor='black', cellColor='purple', activeColor='violet', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='white')
orangeTheme = Theme(bgColor='orange', buttonColor='orange', buttonBorderColor='black', textColor='black', hoverBorderColor='coral', clickColor='darkorange', gridColor='black', cellColor='orange', activeColor='lightcoral', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
pinkTheme = Theme(bgColor='pink', buttonColor='pink', buttonBorderColor='black', textColor='black', hoverBorderColor='lightpink', clickColor='deeppink', gridColor='black', cellColor='pink', activeColor='lightpink', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
brownTheme = Theme(bgColor='saddleBrown', buttonColor='saddleBrown', buttonBorderColor='white', textColor='white', hoverBorderColor='tomato', clickColor='maroon', gridColor='black', cellColor='saddleBrown', activeColor='sienna', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='white')
blackTheme = Theme(bgColor='black', buttonColor='black', buttonBorderColor='white', textColor='white', hoverBorderColor='gray', clickColor='darkgray', gridColor='white', cellColor='black', activeColor='gray', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='white')
