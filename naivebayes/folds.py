import configs
from commands import getstatusoutput as cmd
import time
from base import Base

class Folds(Base):
    def __init__(self, baseDir ,logFile = None, start_file = configs.start_file, end_file = configs.end_file):
        self.logFile = logFile
        self.baseDir = baseDir
        self.start_file = start_file
        self.end_file = end_file
        self.name = "FOLDS"
    def create(self):
        self.__print__("Creating")
        self.folds = []
        current_file = self.start_file
        step = (self.end_file - self.start_file)/configs.folds
        for i in range(configs.folds):
            idx = "fold" + str(i)
            fold = {}
            fold["start"] = current_file
            current_file += step + 1
            fold["end"] = current_file -1
            fold["data"] = ""
            fold["size"] = 0
            self.folds.append(fold)
    def load(self):
        start = time.time()
        for f in range(len(self.folds)):
            self.__print__("Loading fold " +  str(f))
            for i in range(self.folds[f]["start"],self.folds[f]["end"]):
               fname = self.baseDir + str(i) + ".txt"
               self.folds[f]["data"] += " " + open(fname).read()
            self.folds[f]["size"] = len(self.folds[f]["data"])  
        self.__print__("Loading folds took " + 
            str(round(time.time() - start,4)) + "s")
    def foldsInfo(self):
        #TODO: this can be a pretty table
        for f in range(len(self.folds)):
            self.__print__("Fold  : " + str(f))
            self.__print__("Start : " + str(self.folds[f]["start"]))
            self.__print__("End   : " + str(self.folds[f]["end"]))
            self.__print__("Size  : " + str(self.folds[f]["size"]))
    def merge(self, toMerge):
        data = ""
        for f in toMerge:
            data += " " + self.folds[f]["data"]
        return data


if __name__ == "__main__":
    pos = Folds(configs.db_dir_pos) 
    pos.create()
    pos.load()
    pos.foldsInfo()
