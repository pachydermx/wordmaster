import sys
import Tkinter
import tkFont
from userrecorder import *
from words import *
from statwork import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class WordMaster(QWidget):

    def __init__(self):
        # data
        # words
        self.wd = Words()
        # user data
        self.rd = UserRecorder()
        # stat
        self.st = Stat()

        # gui (tk)
        self.pad = 10

        # gui (qt)
        super(WordMaster, self).__init__()
        self.initUI()

        # gui after work
        self.setWindowTitle("WordMaster")
        self.switchWord(1)
        self.showMeaning = False

        # get target
        rdStat = self.rd.getStat()
        self.target = self.st.getTargetD(self.wd.numOfWords, rdStat[0], rdStat[1], rdStat[2])
        self.targetLabel.setText(QString("Target: " + str(int(self.target))))

    def initUI(self):
        # init widgets
        self.oriIDLabel = QLabel(u'199.')
        self.shuffleCheck = QCheckBox(u'Shuffle')

        self.wordLabel = QLabel(u'Example Word')
        self.equLabel = QLabel(u'Example Equ')
        self.desLabel = QLabel(u'Description')

        quizItem1 = QLabel(u'1. Answer1')
        quizItem2 = QLabel(u'2. Answer2')
        quizItem3 = QLabel(u'3. Answer3')
        quizItem4 = QLabel(u'4. Answer4')
        self.quizItems = [quizItem1, quizItem2, quizItem3, quizItem4]

        self.deleteCheck = QCheckBox(u'Delete this word')

        self.targetLabel = QLabel(u'Target: 1')
        self.countLabel = QLabel(u'Count: 299')
        self.rightCountLabel = QLabel(u'3')
        self.wrongCountLabel = QLabel(u'0')

        # style
        self.oriIDLabel.setAlignment(Qt.AlignTop)
        self.oriIDLabel.setMaximumHeight(18)
        self.shuffleCheck.setMaximumWidth(60)
        wordFont = QFont("Arial", 24)
        self.wordLabel.setFont(wordFont)
        self.wordLabel.setAlignment(Qt.AlignCenter)
        desFont = QFont("Arial", 18)
        self.equLabel.setFont(desFont)
        self.equLabel.setAlignment(Qt.AlignCenter)
        self.desLabel.setFont(desFont)
        self.desLabel.setAlignment(Qt.AlignCenter)

        quizFont = QFont("Arial", 18)
        for item in self.quizItems:
            item.setAlignment(Qt.AlignCenter)
            item.setFont(quizFont)

        self.rightCountLabel.setStyleSheet(u'QLabel { background-color : #8f8; }')
        self.rightCountLabel.setAlignment(Qt.AlignCenter)
        self.wrongCountLabel.setStyleSheet(u'QLabel { background-color : #f88; }')
        self.wrongCountLabel.setAlignment(Qt.AlignCenter)

        # set grid
        grid = QGridLayout()

        statusBar = QHBoxLayout()
        statusBar.addWidget(self.deleteCheck)

        desAera = QVBoxLayout()
        desAera.addWidget(self.equLabel)
        desAera.addWidget(self.desLabel)

        quizArea = QVBoxLayout()
        for item in self.quizItems:
            quizArea.addWidget(item)

        topToolBar = QHBoxLayout()
        topToolBar.setAlignment(Qt.AlignCenter)
        topToolBar.addWidget(self.shuffleCheck)

        userdataBar = QHBoxLayout()
        userdataBar.setAlignment(Qt.AlignRight)
        userdataBar.addWidget(self.targetLabel)
        userdataBar.addWidget(self.countLabel)
        userdataBar.addWidget(self.rightCountLabel)
        userdataBar.addWidget(self.wrongCountLabel)

        gridCols = 3

        grid.addWidget(self.oriIDLabel, 0, 0, 1, 1)
        grid.addLayout(topToolBar, 0, 2, 1, 1)
        grid.addWidget(self.wordLabel, 1, 0, 1, gridCols)
        grid.addLayout(desAera, 2, 0, 1, gridCols)
        grid.addLayout(quizArea, 3, 0, 1, gridCols)
        grid.addLayout(statusBar, 4, 0, 1, 1)
        grid.addLayout(userdataBar, 4, 1, 1, 2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("WordMaster")

        # add links
        self.shuffleCheck.stateChanged.connect(self.onSwitchMode)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_BracketLeft:
            self.switchWord(-1)
        if e.key() == Qt.Key_BracketRight:
            self.switchWord(1)
        if e.key() == Qt.Key_D:
            self.onPressRemembered()
        if e.key() == Qt.Key_1:
            self.onAnswerQuiz(1)
        if e.key() == Qt.Key_2:
            self.onAnswerQuiz(2)
        if e.key() == Qt.Key_3:
            self.onAnswerQuiz(3)
        if e.key() == Qt.Key_4:
            self.onAnswerQuiz(4)
        if e.key() == Qt.Key_T:
            self.onSwitchDisplayMode()

    def switchWord(self, delta):
        self.refreshAnswerItems()
        data = self.wd.getNextOrPrevWord(delta)
        while True:
            if self.checkWord(data):
                break
            else:
                data = self.wd.getNextOrPrevWord(delta)
        self.showWord(data)

    def onSwitchDisplayMode(self):
        self.showMeaning = not self.showMeaning
        self.switchWordDisplayMode(self.showMeaning)

    def switchWordDisplayMode(self, isShowingMeanings):
        self.showMeaning = isShowingMeanings
        if self.showMeaning:
            self.equLabel.setStyleSheet(u'QLabel { color: #555; }')
            self.desLabel.setStyleSheet(u'QLabel { color: #555; }')
        else:
            self.equLabel.setStyleSheet(u'QLabel { color: transparent; }')
            self.desLabel.setStyleSheet(u'QLabel { color: transparent; }')

    def onSwitchMode(self):
        mode = "id"
        if self.shuffleCheck.isChecked():
            mode = "sf"
        self.wd.switchBrowsingMode(mode)

    def onPressRemembered(self):
        self.favDisplay.select()
        self.rd.setWordRemembered(self.wd.currentOriID, self.wd.currentWord)

    def onAnswerQuiz(self, key):
        self.refreshAnswerItems()
        answer = int(key) - 1
        if int(self.currentQuiz["correct"]) == answer:
            # right
            self.quizItems[answer].setStyleSheet(u'QLabel { background-color: #6f6; }')
            self.rd.setQuizResult(self.wd.currentOriID, self.wd.currentWord, True)
            # stat
            self.st.dateCount()
        else:
            # wrong
            self.quizItems[answer].setStyleSheet(u'QLabel { background-color: #f66; }')
            self.rd.setQuizResult(self.wd.currentOriID, self.wd.currentWord, False)
        self.switchWordDisplayMode(True)
        self.updateUserData()

    def refreshAnswerItems(self):
        for i in range(0, 4):
            self.quizItems[i].setStyleSheet(u'QLabel { background-color: transparent; }')

    def checkWord(self, data):
        # check if remembered
        if self.rd.getWordRemembered(data["oriID"], data["word"]):
            return False
        else:
            return True

    def showWord(self, data):
        # update ui
        self.oriIDLabel.setText(QString(data["oriID"]))
        self.wordLabel.setText(QString(data['word']))
        self.equLabel.setText(QString(data['equ']))
        self.desLabel.setText(QString(data['des']))
        # get quiz
        quiz = self.wd.getQuizItems()
        self.currentQuiz = quiz
        prefix = ["1.", "2.", "3.", "4."]
        for i in range(0, 4):
            self.quizItems[i].setText(QString(prefix[i] + quiz['set'][i]))
        self.updateUserData()
        # get data
        if self.rd.getWordRemembered(data["oriID"], data["word"]):
            self.deleteCheck.setChecked(True)
        else:
            self.deleteCheck.setChecked(False)
        self.switchWordDisplayMode(False)

    def updateUserData(self):
        # get quiz results
        quizResult = self.rd.getQuizResult(self.wd.currentOriID, self.wd.currentWord)
        self.rightCountLabel.setText(QString(str(quizResult[0])))
        self.wrongCountLabel.setText(QString(str(quizResult[1])))
        # load stat
        self.countLabel.setText(QString(self.st.getDateCount()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wm = WordMaster()
    sys.exit(app.exec_())
    #wm.title = "WordMaster"
    #wm.mainloop()
