from base import Base

class WordsInfo(Base):
    def __init__(self, baseinfo):
        self.info = {}
        self.baseinfo = baseinfo
    def count(self):
        for cls in self.baseinfo.keys():
            for word in self.baseinfo[cls]["count"].keys():
                if word not in self.info.keys():
                    self.info[word] = {}
                    self.info[word]["count"] = 0
                    if word == "Sugar":
                        print "SUGAR IS DONE ! "
                        print self.baseinfo[cls]["count"][word]
                self.info[word]["count"] += self.baseinfo[cls]["count"][word]

    def calc_prob(self):
       for word in self.info.keys():
            for cls in self.baseinfo.keys():
                self.info[word][cls] = float(self.baseinfo[cls]["count"][word]) / self.info[word]["count"]
    def get_prob(self, word = None):
        if word == None:
            return self.info
        else:
            return self.info[word]
