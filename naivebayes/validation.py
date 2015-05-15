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
        confusion = dict.fromkeys(classes, None)
        for k in confusion.keys():
            confusion[k] = dict.fromkeys(classes, 0)
        print confusion
        for f in self.predicted[fold].keys():
            correct = self.results[fold][f]["oracle"]
            predicted = self.predicted[fold][f]
            confusion[correct][predicted] += 1
        self.__print__(str(confusion))
        self.evaluation[fold] = {}
        self.evaluation[fold]["confusion"] = confusion
        self.evaluation[fold]["measures"] = self.Measure(confusion)
    def Measure(self, confusion):
        measures = {}
        total = 0.0
        for cls in confusion.keys():
            for cls2 in confusion[cls].keys():
                total += confusion[cls][cls2]
        correct = 0.0
        for cls in confusion.keys():
            correct += confusion[cls][cls]
        measures["accuracy"] = correct * 1.0 / total
        measures["error"]    = (total - correct) * 1.0 /total
        measures["recall"] = confusion["pos"]["pos"]*1.0 / ( confusion["pos"]["pos"] + confusion["pos"]["neg"] )
        measures["specificity"] = confusion["neg"]["neg"]*1.0 / ( confusion["neg"]["neg"] + confusion["neg"]["pos"] )
        measures["false positive"] = confusion["neg"]["pos"]*1.0/ ( confusion["neg"]["pos"] + confusion["neg"]["neg"] )
        measures["false negative"] = confusion["pos"]["neg"]*1.0/ ( confusion["pos"]["neg"] + confusion["pos"]["pos"] )
        print measures
        return measures
    def printPredictorPerformance(self, fold):
        if fold == "all":
            matrix = {}
            matrix["confusion"] = self.combinedConfusion
            matrix["measures"] = self.combinedConfusionMeasure
        else:
            matrix = self.evaluation[fold]
        #TODO: this should be extended for multiple classes
        template =  "CONFUSION MATRIX : " + str(fold) + "\n"
        template += " *----------------------------------------------*\n"
        template += " |        | Predicted values                    |\n"
        template += " +----------------------------------------------+\n"
        template += " | Real   |           | Positive   | Negative   |\n"
        template += " | values | Positive  | C1XC1      | C1XC2      |\n"
        template += " |        | Negative  | C2XC1      | C2XC2      |\n"
        template += " +----------------------------------------------+\n"
        for m in matrix["measures"].keys():
            template+= " | " + m.rjust(17) + "  | " + str(round(matrix["measures"][m],3)).rjust(5) + "                   |\n"
        template += " *----------------------------------------------*"
        template = template.replace("C1XC1", str(matrix["confusion"]["pos"]["pos"]).rjust(5))
        template = template.replace("C2XC1", str(matrix["confusion"]["pos"]["neg"]).rjust(5))
        template = template.replace("C2XC2", str(matrix["confusion"]["neg"]["neg"]).rjust(5))
        template = template.replace("C1XC2", str(matrix["confusion"]["neg"]["pos"]).rjust(5))
        print template
    def mergeAllConfusion(self):
        self.combinedConfusion = dict.fromkeys(self.evaluation[0]["confusion"], None)
        for k in self.combinedConfusion.keys():
            self.combinedConfusion[k] = dict.fromkeys(self.combinedConfusion.keys(), 0)
        for i in range(configs.folds):
            for j in self.evaluation[i]["confusion"].keys():
               for k in self.evaluation[i]["confusion"][j].keys():
                    self.combinedConfusion[j][k] += self.evaluation[i]["confusion"][j][k]
        self.combinedConfusionMeasure = self.Measure(self.combinedConfusion)
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
    def printPredictorsPerformance(self):        
        for i in range(configs.folds):
            self.printPredictorPerformance(i)
        self.printPredictorPerformance("all")    
