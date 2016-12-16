import json, io

class UserRecorder:
    def __init__(self):
        self.load()

    def load(self):
        with open('userdata.txt') as data_file:
            self.data = json.load(data_file)

    def save(self):
        with io.open("userdata.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, ensure_ascii=False))

    # make sure there is record of the word
    def checkRecord(self, oriID, word):
        id = oriID + word
        if id in self.data:
            pass
        else:
            self.data[id] = {}

    def setWordRemembered(self, oriID, word):
        self.checkRecord(oriID, word)
        self.data[oriID + word]["remembered"] = True
        self.save()

    def getWordRemembered(self, oriID, word):
        id = oriID + word
        if id in self.data:
            if "remembered" in self.data[id]:
                if self.data[id]["remembered"]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def setQuizResult(self, oriID, word, isRight):
        id = oriID + word
        self.checkRecord(oriID, word)
        if isRight:
            if "quizRight" in self.data[id]:
                self.data[id]["quizRight"] = int(self.data[id]["quizRight"]) + 1
            else:
                self.data[id]["quizRight"] = 1
        else:
            if "quizWrong" in self.data[id]:
                self.data[id]["quizWrong"] = int(self.data[id]["quizWrong"]) + 1
            else:
                self.data[id]["quizWrong"] = 1
        self.save()

    def getQuizResult(self, oriID, word):
        id = oriID + word
        result = [0, 0]
        if id in self.data:
            if "quizRight" in self.data[id]:
                result[0] = self.data[id]["quizRight"]
            if "quizWrong" in self.data[id]:
                result[1] = self.data[id]["quizWrong"]
        return result

    def getStat(self):
        sumRemembered = 0
        sumRight = 0
        sumWrong = 0
        for id in self.data:
            if "remembered" in self.data[id]:
                sumRemembered += 1
            if "quizRight" in self.data[id]:
                sumRight += int(self.data[id]["quizRight"])
            if "quizWrong" in self.data[id]:
                sumWrong += int(self.data[id]["quizWrong"])
        return [sumRemembered, sumRight, sumWrong]

if __name__ == "__main__":
    rd = UserRecorder()
