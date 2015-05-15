from base import Base
from parser import Parser
from wordinfo import WordsInfo
import configs
from predictor import Predictor
import configs
class Validation(Base):
    def __init__(self, info, logFile = None):
        self.logFile = None
        self.name = "VALIDATION"
        self.info = info
        self.predictors = dict.fromkeys(range(configs.folds),None)
        self.results = dict.fromkeys(range(configs.folds),None)
        self.evaluation = dict.fromkeys(range(configs.folds),None)
        self.predicted = dict.fromkeys(range(configs.folds),None)
    def buildPredictor(self,fold):
        self.__print__("Building predictor for fold " + str(fold))
        foldsRange = range(10)
        foldsRange.remove(fold)
        for cls in self.info.keys():
            self.info[cls]["text"] = self.info[cls]["folds"].merge(foldsRange)
            self.info[cls]["parser"] = Parser(self.info[cls]["text"])
            self.info[cls]["parser"].extract()
            self.info[cls]["vocab"] = self.info[cls]["parser"].getVocabulary()
        allvocabs = None 
        for cls in self.info.keys():
            if allvocabs == None:
                allvocabs = self.info[cls]["vocab"]
                continue
            allvocabs.merge(self.info[cls]["vocab"])
        for cls in self.info.keys():
            self.info[cls]["parser"].count(allvocabs.get())
            self.info[cls]["parser"].printInfo()
            self.info[cls]["count"] = self.info[cls]["parser"].getCount()
        words_info =  WordsInfo(self.info)
        words_info.count()
        words_info.calc_prob()
        predictor = Predictor(words_info.get_prob())
        self.predictors[fold] = predictor
    def savePredictor(self, fold, filename): 
        self.predictors[fold].persist(filename)
    def loadPredictor(self, fold, filename):
        self.predictors[fold] = Predictor()
        self.predictors[fold].loadFromFile(filename)
        return self.predictors[fold]
    def testPredictor(self, fold):
        self.results[fold] = {}
        for cls in self.info.keys():
            self.results[fold].update(dict.fromkeys(self.info[cls]["folds"].listOfFiles(fold), {"oracle":cls}))
        #self.results[fold] = self.predictors[fold].predictAll(self.results[fold])
        self.predicted[fold] = self.predictors[fold].predictAll(self.results[fold])
    def evalPredictor(self, fold):
        classes = self.info.keys()
        confusion = dict.fromkeys(classes,  dict.fromkeys(classes, 0))
        #print  self.results[fold]

        for f in self.results[fold]:
            correct = self.results[fold][f]["oracle"]
            predicted = self.predicted[fold][f]
            confusion[correct][predicted] += 1
        self.__print__(str(confusion))
        self.evaluation[fold] = confusion
    def loadPredictors(self):
        for i in range(configs.folds):
            self.loadPredictor(i, "predictor" + str(i) + ".pd")
    def savePredictors(self):
        for i in range(configs.folds):
            self.savePredictor(i,"predictor" + str(i) + ".pd")
    def buildPredictors(self):
        for i in range(configs.folds):
            self.buildPredictor(i)
    def testPredictors(self):
        for i in range(configs.folds):
            self.testPredictor(i) 
    def evalPredictors(self):
        for i in range(configs.folds):
            self.evalPredictor(i)
