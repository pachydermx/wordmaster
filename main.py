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
        self.currentWord = ""

    def initialize(self):
        self.grid()

        self.bind("a", self.OnPressEnter)
        self.bind("]", self.onPressNext)
        self.bind("[", self.onPressPrev)
        self.bind("d", self.onPressRemembered)

        button = Tkinter.Button(self, text="BTN", command=self.OnButtonClick)
        button.grid(column = 1, row = 0)

        # word display
        wordFont = tkFont.Font(size=24)

        self.idLabelVar = Tkinter.StringVar()
        self.idLabel = Tkinter.Label(self, textvariable=self.idLabelVar, anchor="w", padx=self.pad, pady=self.pad, width=50)
        self.idLabel.grid(column = 0, row = 2, columnspan = 2)

        self.wordLabelVar = Tkinter.StringVar()
        self.wordLabel = Tkinter.Label(self, textvariable=self.wordLabelVar, padx=self.pad, pady=self.pad, width=30, font=wordFont)
        self.wordLabel.grid(column = 0, row = 3, columnspan = 2)

        self.equLabelVar = Tkinter.StringVar()
        self.equLabel = Tkinter.Label(self, textvariable=self.equLabelVar, padx=self.pad, pady=self.pad, width=30, font=wordFont)
        self.equLabel.grid(column = 0, row = 4, columnspan = 2)

        self.desLabelVar = Tkinter.StringVar()
        self.desLabel = Tkinter.Label(self, textvariable=self.desLabelVar, padx=self.pad, pady=self.pad, width=30, font=wordFont)
        self.desLabel.grid(column = 0, row = 5, columnspan = 2)

        # quiz display
        quizFont = tkFont.Font(size=18)
        self.quizDisplay = Tkinter.Frame(self)
        self.quizDisplay.grid(column = 0, row = 6, columnspan = 2)
        self.quizDisplay.grid_columnconfigure(0, weight=1)
        quizItem1 = Tkinter.Label(self.quizDisplay, text="A", font=quizFont)
        quizItem1.grid(column = 0, row=0, sticky="W")
        quizItem2 = Tkinter.Label(self.quizDisplay, text="B", font=quizFont)
        quizItem2.grid(column = 1, row=0)
        quizItem3 = Tkinter.Label(self.quizDisplay, text="C", font=quizFont)
        quizItem3.grid(column = 2, row=0, sticky="E")

        # user display
        self.favDisplay = Tkinter.Checkbutton(text = "Delete this word")
        self.favDisplay.grid(column = 0, row = 7, sticky="W")

        self.grid_columnconfigure(0, weight = 1)

    def OnButtonClick(self):
        print "you clicked me"

    def OnPressEnter(self, event):
        self.idLabelVar.set("loaded")

    def onPressPrev(self, event):
        self.showWord(self.wd.getNextOrPrevWord(-1))

    def onPressNext(self, event):
        self.showWord(self.wd.getNextOrPrevWord(1))

    def onPressRemembered(self, event):
        self.favDisplay.select()
        self.rd.setWordRemembered(self.currentWord)

    def showWord(self, data):
        # update ui
        self.idLabelVar.set(data["oriID"])
        self.wordLabelVar.set(data["word"])
        self.equLabelVar.set(data["equ"])
        self.desLabelVar.set(data["des"])
        # get data
        if self.rd.getWordRemembered(data["word"]):
            self.favDisplay.select()
        else:
            self.favDisplay.deselect()


if __name__ == "__main__":
    wm = WordMaster(None)
    wm.title = "WordMaster"
    wm.mainloop()
