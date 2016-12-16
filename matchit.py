import sys, copy
import random
from userrecorder import *
from words import *
from statwork import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MatchIt(QWidget):

    def __init__(self):
        # argv
        self.matchSize = 4
        self.pairs = int((self.matchSize * self.matchSize) / 2)
        self.answerMatrix = [0 for i in range(self.pairs * 2)]
        self.statusMatrix = [0 for i in range(self.pairs * 2)]
        self.selectedOne = False
        self.selecting = -1

        # stylesheets
        self.selectingSS = "QPushButton { background-color: #81bef7; }"
        self.rightSS = "QPushButton { background-color: #81f781; }"
        self.wrongSS = "QPushButton { background-color: #f78181; }"
        # data
        # words
        self.wd = Words()
        # user data
        self.rd = UserRecorder()
        # stat
        self.st = Stat()

        # settings
        self.filter = False
        # gui (tk)
        self.pad = 10

        # gui (qt)
        super(MatchIt, self).__init__()
        self.initUI()

        # gui after work
        self.setWindowTitle("WordMaster")

        self.loadWords()

    def initUI(self):
        # init widgets
        self.buttons = []

        btnAera = QGridLayout()
        self.buttonMatrix = []
        for i in range(0, self.matchSize):
            for j in range(0, self.matchSize):
                btn = QPushButton("BTN")
                btn.setMinimumHeight(150)
                self.buttonMatrix.append(btn)
                btnAera.addWidget(btn, i, j)


        self.rightCountLabel = QLabel(u'3')
        self.wrongCountLabel = QLabel(u'0')

        # style
        self.rightCountLabel.setStyleSheet(u'QLabel { background-color : #8f8; }')
        self.rightCountLabel.setAlignment(Qt.AlignCenter)
        self.wrongCountLabel.setStyleSheet(u'QLabel { background-color : #f88; }')
        self.wrongCountLabel.setAlignment(Qt.AlignCenter)

        # set grid
        grid = QGridLayout()

        topToolBar = QHBoxLayout()
        topToolBar.setAlignment(Qt.AlignCenter)

        statusBar = QHBoxLayout()

        quizArea = QVBoxLayout()
        quizArea.setAlignment(Qt.AlignTop)

        userdataBar = QHBoxLayout()
        userdataBar.setAlignment(Qt.AlignRight)
        userdataBar.addWidget(self.rightCountLabel)
        userdataBar.addWidget(self.wrongCountLabel)

        gridCols = 3

        grid.addLayout(topToolBar, 0, 2, 1, 1)
        grid.addLayout(btnAera, 1, 0, 1, gridCols)
        #grid.addLayout(statusBar, 4, 0, 1, 1)
        #grid.addLayout(userdataBar, 4, 1, 1, 2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("MatchIt!")

        # add links
        self.buttonMatrix[0].clicked.connect(lambda: self.onAnswerClicked(0))
        self.buttonMatrix[1].clicked.connect(lambda: self.onAnswerClicked(1))
        self.buttonMatrix[2].clicked.connect(lambda: self.onAnswerClicked(2))
        self.buttonMatrix[3].clicked.connect(lambda: self.onAnswerClicked(3))
        self.buttonMatrix[4].clicked.connect(lambda: self.onAnswerClicked(4))
        self.buttonMatrix[5].clicked.connect(lambda: self.onAnswerClicked(5))
        self.buttonMatrix[6].clicked.connect(lambda: self.onAnswerClicked(6))
        self.buttonMatrix[7].clicked.connect(lambda: self.onAnswerClicked(7))
        self.buttonMatrix[8].clicked.connect(lambda: self.onAnswerClicked(8))
        self.buttonMatrix[9].clicked.connect(lambda: self.onAnswerClicked(9))
        self.buttonMatrix[10].clicked.connect(lambda: self.onAnswerClicked(10))
        self.buttonMatrix[11].clicked.connect(lambda: self.onAnswerClicked(11))
        self.buttonMatrix[12].clicked.connect(lambda: self.onAnswerClicked(12))
        self.buttonMatrix[13].clicked.connect(lambda: self.onAnswerClicked(13))
        self.buttonMatrix[14].clicked.connect(lambda: self.onAnswerClicked(14))
        self.buttonMatrix[15].clicked.connect(lambda: self.onAnswerClicked(15))

        self.show()

    def keyPressEvent(self, e):
        pass

    def onAnswerClicked(self,buttonID):
        if not self.selectedOne:
            # first
            self.selecting = buttonID
            self.selectedOne = True
            # style
            self.buttonMatrix[buttonID].setStyleSheet(self.selectingSS)
            self.buttonMatrix[buttonID].setEnabled(False)
        else:
            # second
            # check
            if self.answerMatrix[buttonID] == self.answerMatrix[self.selecting]:
                # right
                # style
                self.buttonMatrix[buttonID].setStyleSheet(self.rightSS)
                self.buttonMatrix[buttonID].setEnabled(False)
                self.buttonMatrix[self.selecting].setStyleSheet(self.rightSS)
            else:
                # wrong
                # style
                self.buttonMatrix[buttonID].setStyleSheet(self.wrongSS)
                self.buttonMatrix[self.selecting].setStyleSheet(self.wrongSS)
                self.buttonMatrix[self.selecting].setEnabled(True)
            self.selecting = -1
            self.selectedOne = False

    def checkWord(self, data):
        # check if remembered
        if self.rd.getWordRemembered(data["oriID"], data["word"]):
            return False
        else:
            # check if below target
            if self.filter:
                quizResult = self.rd.getQuizResult(data['oriID'], data['word'])
                if quizResult[0] - quizResult[1] >= int(self.target):
                    return False
            return True

    def grabWord(self):
        data = self.wd.getWordShuffle()
        while True:
            if self.checkWord(data):
                break
            else:
                data = self.wd.getWordShuffle()
        return data

    def loadWords(self):
        self.currentWords = [self.grabWord()]
        for i in range(0, self.pairs - 1):
            newWord = self.grabWord()
            while True:
                exist = False
                for eachWord in self.currentWords:
                    if newWord["oriID"] == eachWord["oriID"] and newWord["word"] == eachWord["word"]:
                        exist = True
                if exist:
                    newWord = self.grabWord()
                else:
                    self.currentWords.append(newWord)
                    break
        self.showWords()

    def showWords(self):
        # get order
        order = []
        for i in range(0, self.pairs * 2):
            order.append(i)
        random.shuffle(order)
        # assign words
        for i in range(self.pairs * 2):
            if order[i] < self.pairs:
                # word
                wordID = order[i]
                self.buttonMatrix[i].setText(self.currentWords[wordID]["word"])
                self.answerMatrix[i] = wordID
            else:
                # equ
                wordID = order[i] - self.pairs
                self.buttonMatrix[i].setText(self.currentWords[wordID]["equ"])
                self.answerMatrix[i] = wordID


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi = MatchIt()
    sys.exit(app.exec_())
    #wm.title = "WordMaster"
    #wm.mainloop()
