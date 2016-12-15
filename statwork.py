import json, io
import datetime

class Stat:
    def __init__(self):
        self.load()

    def load(self):
        with open('misc.txt') as data_file:
            self.data = json.load(data_file)

    def save(self):
        with io.open("misc.txt", "w", encoding="utf-8") as f:
            f.write(unicode(json.dumps(self.data, ensure_ascii=False)))

    def getDateCount(self):
        # type: () -> object
        dateStamp = datetime.date.today().isoformat()
        if dateStamp in self.data["counter"]:
            return self.data["counter"][dateStamp]
        else:
            return 0

    def dateCount(self):
        dateStamp = datetime.date.today().isoformat()
        if dateStamp in self.data["counter"]:
            self.data['counter'][dateStamp] = int(self.data['counter'][dateStamp]) + 1
        else:
            self.data['counter'][dateStamp] = 1
        self.save()

    def getTargetD(self, numOfWords, numOfRememberedWords, RightSum, WrongSum):
        activeWords = numOfWords - numOfRememberedWords
        deltaSum = RightSum - WrongSum
        return (deltaSum / float(activeWords)) + 1
