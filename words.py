import json, io

class Words:
    def __init__(self):
        self.loadWords()
        self.currentID = 0

    def loadWords(self):
        with open('data.txt') as data_file:
            self.data = json.load(data_file)

    def readWord(self, id):
        return {
            "oriID": self.data[id][0],
            "word": self.data[id][1],
            "equ": self.data[id][2],
            "des": self.data[id][3]
        }

    def getNextOrPrevWord(self, delta):
        self.currentID += delta
        print self.readWord(self.currentID)
        return self.readWord(self.currentID)
