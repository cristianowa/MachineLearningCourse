from base import Base

class WordsInfo(Base):
    def __init__(self, baseinfo):
        self.name = "WORDINFO"
        self.logFile = None
        self.info = {}
        self.baseinfo = baseinfo
    def count(self):
        for cls in self.baseinfo.keys():
            self.__print__("Count " +cls )
            for word in self.baseinfo[cls]["count"].keys():
#                if word not in self.info.keys():
                try:
                    x = self.info[word]
                except:
                    self.info[word] = {}
                    self.info[word]["count"] = 0
                    self.info[word]["prob"] = {}

                self.info[word]["count"] += self.baseinfo[cls]["count"][word]

    def calc_prob(self):
        self.__print__("Calc Prob")
        for word in self.info.keys():
            for cls in self.baseinfo.keys():
                self.info[word]["prob"][cls] = float(self.baseinfo[cls]["count"][word]) / self.info[word]["count"]
    def get_prob(self, word = None):
        if word == None:
            return self.info
        else:
            return self.info[word]
