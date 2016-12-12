import Tkinter
import json
import io

class WordMaster(Tkinter.Tk):
    data = None
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entry = Tkinter.Entry(self)
        self.entry.grid(column = 0, row = 0, sticky = "EW")
        self.entry.bind("a", self.OnPressEnter)

        button = Tkinter.Button(self, text="Click me", command=self.OnButtonClick)
        button.grid(column = 1, row = 0)

        label = Tkinter.Label(self, anchor="w", fg="white", bg="blue")
        label.grid(column = 0, row = 1, columnspan=2, sticky = "EW")

        self.grid_columnconfigure(0, weight = 1)

    def OnButtonClick(self):
        print "you clicked me"

    def OnPressEnter(self, event):
        print "you pressed enter"

if __name__ == "__main__":
    wm = WordMaster(None)
    wm.title = "WordMaster"
    wm.mainloop()
    data = [["a", "equ", "des"], ["b", "equb", "desb"]]
    with io.open("data.txt", "w", encoding="utf-8") as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))