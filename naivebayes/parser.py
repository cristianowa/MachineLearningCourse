import re
from base import Base

class Vocabulary:
    def __init__(self):
        pass

class Parser(Base):
    def __init__(self, textFile, logFile = None):
        self.name = "PARSER"
        self.logFile = logFile
        self.text = textFile
    def extract(self):
        self.words = re.compile('\w+').findall(self.text)
        self.vocabulary = list(set(self.words))
    def count(self):
        self.counts = {}
        for word in self.vocabulary:
            self.counts[word] = self.words.count(word)
    def getVocabulary(self):
        return self.vocabulary
    def getCount(self):
        return self.counts
    def printInfo(self):
        self.__print__("Vocabulary size : " + str(len(self.vocabulary)))
        
