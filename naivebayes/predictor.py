import re
from base import Base
import operator

class Predictor(Base):
    def __init__(self, probs):
        self.name = "PREDICTOR"
        self.logFile = None
        self.probs = probs
    def persist(self, filename):
        pass
    def loadFromFile(self, filename):
        pass
    def predict(self, text):
        textwords = re.compile('\w+').findall(text)
        acc_prob = {}
        #recover all classes used
        for p in self.probs[self.probs.keys()[0]]["prob"]:
            acc_prob[p] = 1

        for word in textwords:
            try:
                for cls in acc_prob.keys():
                    acc_prob[cls] *=  self.probs[word]["prob"][cls]
            except:
                    print "Word not found : " + word
        prediction = max(acc_prob.iteritems(), key=operator.itemgetter(1))[0]
        self.__print__("value predicted is : " + prediction)
        return prediction
    def predictFile(self, filename):
        return self.predict(open(filename).read())
    def predictAll(self, data):
        for f in data.keys():
            data[f]["predicted"] = self.predictFile(f)
        return data
