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

lightTheme = Theme(bgColor=gradient('white', 'darkgray'), buttonColor='white', buttonBorderColor='black', textColor='black', hoverBorderColor=gradient('gray', 'dimGray'), clickColor='darkgray', gridColor='black', cellColor='white', activeColor='lightSkyBlue', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
redTheme = Theme(bgColor=gradient('crimson','red','darkRed'), buttonColor='red', buttonBorderColor='black', textColor='black', hoverBorderColor=gradient('yellow', 'orange', 'orangeRed'), clickColor='darkRed', gridColor='black', cellColor='darkRed', activeColor='pink', correctGuessColor='lightGreen', wrongGuessColor='orange', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
blueTheme = Theme(bgColor=gradient('dodgerBlue', 'darkBlue'), buttonColor='dodgerBlue', buttonBorderColor='black', textColor='black', hoverBorderColor=gradient('lightblue', 'blue'), clickColor='navy', gridColor='black', cellColor='dodgerBlue', activeColor='skyblue', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')
greenTheme = Theme(bgColor=gradient('green', 'darkGreen'), buttonColor='forestGreen', buttonBorderColor='black', textColor='black', hoverBorderColor=gradient('limeGreen', 'seaGreen'), clickColor='darkgreen', gridColor='black', cellColor='forestGreen', activeColor='lightgreen', correctGuessColor='lightGreen', wrongGuessColor='tomato', singleGuessColor='yellow', tupleColor='orange', titleColor='black')