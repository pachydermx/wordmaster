import json, io
import random

class Words:
    def __init__(self):
        self.loadWords()
        self.currentID = 0
        self.currentWord = ""
        self.numOfWords = len(self.data)

    def loadWords(self):
        with open('data.txt') as data_file:
            self.data = json.load(data_file)

    def readWord(self, id):
        self.currentWord = self.data[id][1]
        return {
            "oriID": self.data[id][0],
            "word": self.data[id][1],
            "equ": self.data[id][2],
            "des": self.data[id][3]
        }

    def getNextOrPrevWord(self, delta):
        self.currentID += delta
        return self.readWord(self.currentID)

    def getQuizItems(self):
        result = []
        correct = random.randint(0, 3)
        for i in range(0, 4):
            if i == correct:
                result.append(self.data[self.currentID][2])
            else:
                randomID = random.randint(0, self.numOfWords)
                randomEqu = self.data[randomID][2]
                result.append(randomEqu)
        return {"correct": correct, "set": result}


if __name__ == "__main__":
    wd = Words()
    print wd.getQuizItems()
