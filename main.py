import Tkinter
import json
import io

class WordMaster(Tkinter.Tk):

    def __init__(self, parent):
        # var
        self.id = 0
        # gui
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.loadWords()
        self.initialize()

    def initialize(self):
        self.grid()


        #self.entry = Tkinter.Entry(self)
        #self.entry.grid(column = 0, row = 0, sticky = "EW")
        self.bind("a", self.OnPressEnter)
        self.bind("]", self.onPressNext)
        self.bind("[", self.onPressPrev)

        button = Tkinter.Button(self, text="BTN", command=self.OnButtonClick)
        button.grid(column = 1, row = 0)

        self.idLabelVar = Tkinter.StringVar()
        self.idLabel = Tkinter.Label(self, textvariable=self.idLabelVar, anchor="w")
        self.idLabel.grid(column = 0, row = 2, columnspan = 2, sticky = "W")

        self.wordLabelVar = Tkinter.StringVar()
        self.wordLabel = Tkinter.Label(self, textvariable=self.wordLabelVar, anchor="w")
        self.wordLabel.grid(column = 0, row = 3, columnspan = 2, sticky = "W")

        self.equLabelVar = Tkinter.StringVar()
        self.equLabel = Tkinter.Label(self, textvariable=self.equLabelVar, anchor="w")
        self.equLabel.grid(column = 0, row = 4, columnspan = 2, sticky = "W")

        self.desLabelVar = Tkinter.StringVar()
        self.desLabel = Tkinter.Label(self, textvariable=self.desLabelVar, anchor="w")
        self.desLabel.grid(column = 0, row = 5, columnspan = 2, sticky = "W")

        self.grid_columnconfigure(0, weight = 1)

    def OnButtonClick(self):
        print "you clicked me"

    def OnPressEnter(self, event):
        self.idLabelVar.set("loaded")

    def onPressPrev(self, event):
        self.id -= 1
        self.showWord()

    def onPressNext(self, event):
        self.id += 1
        self.showWord()

    def showWord(self):
        self.idLabelVar.set(self.data[self.id][0])
        self.wordLabelVar.set(self.data[self.id][1])
        self.equLabelVar.set(self.data[self.id][2])
        self.desLabelVar.set(self.data[self.id][3])

    def loadWords(self):
        with open('data.txt') as data_file:
            self.data = json.load(data_file)
        print self.data

if __name__ == "__main__":
    wm = WordMaster(None)
    wm.title = "WordMaster"
    wm.mainloop()
