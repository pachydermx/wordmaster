import Tkinter
import tkFont
import json
import io
from userrecorder import *
from words import *

class WordMaster(Tkinter.Tk):

    def __init__(self, parent):
        # data
        # words
        self.wd = Words()
        # user data
        self.rd = UserRecorder()
        # gui
        self.pad = 10
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        self.switchWord(1)

    def initialize(self):
        self.grid()

        self.bind("]", self.onSwitchWord)
        self.bind("[", self.onSwitchWord)
        self.bind("d", self.onPressRemembered)
        # quiz
        self.bind("1", self.onAnswerQuiz)
        self.bind("2", self.onAnswerQuiz)
        self.bind("3", self.onAnswerQuiz)
        self.bind("4", self.onAnswerQuiz)

        # settings
        button = Tkinter.Button(self, text="BTN", command=self.OnButtonClick)
        #button.grid(column = 0, row = 0)

        self.browseMode = Tkinter.StringVar()
        bMode1 = Tkinter.Radiobutton(self, command=self.onSwitchMode, text="By ID", variable=self.browseMode, value="id")
        bMode2 = Tkinter.Radiobutton(self, command=self.onSwitchMode, text="Shuffle", variable=self.browseMode, value="sf")
        bMode3 = Tkinter.Radiobutton(self, command=self.onSwitchMode, text="Incorrect Rate", variable=self.browseMode, value="ir")
        bMode1.grid(column = 0, row = 0, sticky="E")
        bMode2.grid(column = 1, row = 0, sticky="E")
        bMode3.grid(column = 2, row = 0, sticky="E")
        self.browseMode.set("id")

        # word display
        wordFont = tkFont.Font(size=24)

        self.idLabelVar = Tkinter.StringVar()
        self.idLabel = Tkinter.Label(self, textvariable=self.idLabelVar, anchor="w", padx=self.pad, pady=self.pad, width=50)
        self.idLabel.grid(column = 0, row = 2, columnspan = 3)

        self.wordLabelVar = Tkinter.StringVar()
        self.wordLabel = Tkinter.Label(self, textvariable=self.wordLabelVar, padx=self.pad, pady=self.pad, width=30, font=wordFont)
        self.wordLabel.grid(column = 0, row = 3, columnspan = 3)

        self.equLabelVar = Tkinter.StringVar()
        self.equLabel = Tkinter.Label(self, textvariable=self.equLabelVar, padx=self.pad, pady=self.pad, width=30, font=wordFont)
        self.equLabel.grid(column = 0, row = 4, columnspan = 3)

        self.desLabelVar = Tkinter.StringVar()
        self.desLabel = Tkinter.Label(self, textvariable=self.desLabelVar, padx=self.pad, pady=self.pad, width=30, font=wordFont)
        self.desLabel.grid(column = 0, row = 5, columnspan = 3)

        # quiz display
        quizFont = tkFont.Font(size=18)
        self.quizDisplay = Tkinter.Frame(self)
        self.quizDisplay.grid(column = 0, row = 6, columnspan = 3)
        self.quizDisplay.grid_columnconfigure(0, weight=1)
        self.quizVars = [Tkinter.StringVar(), Tkinter.StringVar(), Tkinter.StringVar(), Tkinter.StringVar()]
        quizItem1 = Tkinter.Label(self.quizDisplay, textvariable=self.quizVars[0], font=quizFont)
        quizItem1.grid(column = 0, row=0, sticky="W")
        quizItem2 = Tkinter.Label(self.quizDisplay, textvariable=self.quizVars[1], font=quizFont)
        quizItem2.grid(column = 0, row=1, sticky="W")
        quizItem3 = Tkinter.Label(self.quizDisplay, textvariable=self.quizVars[2], font=quizFont)
        quizItem3.grid(column = 0, row=2, sticky="W")
        quizItem4 = Tkinter.Label(self.quizDisplay, textvariable=self.quizVars[3], font=quizFont)
        quizItem4.grid(column = 0, row=3, sticky="W")
        self.quizItems = [quizItem1, quizItem2, quizItem3, quizItem4]

        # user display
        self.favDisplay = Tkinter.Checkbutton(text = "Delete this word")
        self.favDisplay.grid(column = 0, row = 7, sticky="W")
        self.quizRightVar = Tkinter.StringVar()
        self.quizWrongVar = Tkinter.StringVar()
        quizResultRight = Tkinter.Label(self, bg="#8f8", textvariable=self.quizRightVar, width=3)
        quizResultWrong = Tkinter.Label(self, bg="#f88", textvariable=self.quizWrongVar, width=3)
        quizResultRight.grid(column = 1, row = 7, sticky = "W")
        quizResultWrong.grid(column = 2, row = 7, sticky = "W")
        self.grid_columnconfigure(0, weight = 1)
        self.defaultColor = quizItem1.cget("bg")

    def OnButtonClick(self):
        print "you clicked me"

    def onSwitchWord(self, event):
        if event.char == '[':
            self.switchWord(-1)
        else:
            self.switchWord(1)

    def switchWord(self, delta):
        self.refreshAnswerItems()
        data = self.wd.getNextOrPrevWord(delta)
        while True:
            if self.checkWord(data):
                break
            else:
                data = self.wd.getNextOrPrevWord(delta)
        self.showWord(data)

    def onSwitchMode(self):
        self.wd.switchBrowsingMode(self.browseMode.get())

    def onPressRemembered(self, event):
        self.favDisplay.select()
        self.rd.setWordRemembered(self.wd.currentWord)

    def onAnswerQuiz(self, event):
        self.refreshAnswerItems()
        answer = int(event.char) - 1
        if int(self.currentQuiz["correct"]) == answer:
            # right
            self.quizItems[answer].configure(bg="#6f6")
            self.rd.setQuizResult(self.wd.currentWord, True)
        else:
            # wrong
            self.quizItems[answer].configure(bg="#f66")
            self.rd.setQuizResult(self.wd.currentWord, False)
        self.updateUserData()

    def refreshAnswerItems(self):
        for i in range(0, 4):
            self.quizItems[i].configure(bg=self.defaultColor)

    def checkWord(self, data):
        # check if remembered
        if self.rd.getWordRemembered(data["word"]):
            return False
        else:
            return True

    def showWord(self, data):
        # update ui
        self.idLabelVar.set(data["oriID"])
        self.wordLabelVar.set(data["word"])
        self.equLabelVar.set(data["equ"])
        self.desLabelVar.set(data["des"])
        # get quiz
        quiz = self.wd.getQuizItems()
        self.currentQuiz = quiz
        prefix = ["1.", "2.", "3.", "4."]
        for i in range(0, 4):
            self.quizVars[i].set(prefix[i] + quiz["set"][i])
        self.updateUserData()
        # get data
        if self.rd.getWordRemembered(data["word"]):
            self.favDisplay.select()
        else:
            self.favDisplay.deselect()

    def updateUserData(self):
        # get quiz results
        quizResult = self.rd.getQuizResult(self.wd.currentWord)
        self.quizRightVar.set(quizResult[0])
        self.quizWrongVar.set(quizResult[1])

if __name__ == "__main__":
    wm = WordMaster(None)
    wm.title = "WordMaster"
    wm.mainloop()
