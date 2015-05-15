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
        for f in range(len(self.folds)):
            self.__print__("Loading fold " +  str(f))
            for i in range(self.folds[f]["start"],self.folds[f]["end"]):
               fname = self.baseDir + str(i) + ".txt"
               self.folds[f]["data"] += " " + open(fname).read()
            self.folds[f]["size"] = len(self.folds[f]["data"])  
    def foldsInfo(self):
        #TODO: this can be a pretty table
        for f in range(len(self.folds)):
            self.__print__("Fold    : " + str(f))
            self.__print__("Start   : " + str(self.folds[f]["start"]))
            self.__print__("End     : " + str(self.folds[f]["end"]))
            self.__print__("Size(b) : " + str(self.folds[f]["size"]))
    def merge(self, toMerge):
        data = ""
        for f in toMerge:
            data += " " + self.folds[f]["data"]
        return data
    def listOfFiles(self, fold):
        fileList = []
        for i in range(self.folds[fold]["start"],self.folds[fold]["end"] + 1):
            fileList.append(self.baseDir + str(i) + ".txt")
        return fileList

def AllFolds():
    infos= {}
    for cls in configs.db_dirs:
        infos[cls] = {}
        infos[cls]["folds"] = Folds(configs.db_dirs[cls])
    for cls in infos:
        infos[cls]["folds"].create()
        infos[cls]["folds"].load()
        infos[cls]["folds"].foldsInfo()
    return infos

if __name__ == "__main__":
    pos = Folds(configs.db_dir_pos) 
    pos.create()
    pos.load()
    pos.foldsInfo()
