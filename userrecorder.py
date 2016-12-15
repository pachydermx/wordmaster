import json, io

class UserRecorder:
    def __init__(self):
        self.load()

    def load(self):
        with open('userdata.txt') as data_file:
            self.data = json.load(data_file)

    def save(self):
        with io.open("userdata.txt", "w", encoding="utf-8") as f:
            f.write(unicode(json.dumps(self.data, ensure_ascii=False)))

    # make sure there is record of the word
    def checkRecord(self, word):
        if word in self.data:
            pass
        else:
            self.data[word] = {}

    def setWordRemembered(self, word):
        self.checkRecord(word)
        self.data[word]["remembered"] = True
        self.save()

    def getWordRemembered(self, word):
        if word in self.data:
            if "remembered" in self.data[word]:
                if self.data[word]["remembered"]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

if __name__ == "__main__":
    rd = UserRecorder()
    print rd.getWordRemembered(" a solicitation of ")