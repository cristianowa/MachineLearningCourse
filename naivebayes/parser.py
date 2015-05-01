import re
from base import Base


class Vocabulary:
    def __init__(self, words):
        self.vocabulary = list(set(words))
    def merge(self, vocabulary):
        self.vocabulary += vocabulary.vocabulary
        self.vocabulary = list(set(self.vocabulary))
    def get(self):
        return self.vocabulary

class Parser(Base):
    def __init__(self, textFile, logFile = None):
        self.name = "PARSER"
        self.logFile = logFile
        self.text = textFile
    def extract(self):
        self.words = re.compile('\w+').findall(self.text)
        self.vocabulary = Vocabulary(self.words)
    def count(self, words):
        self.counts = {}
        for word in words:
            self.counts[word] = self.words.count(word)
        return self.counts
    def getVocabulary(self):
        return self.vocabulary
    def getCount(self):
        return self.counts
    def printInfo(self):
        self.__print__("Vocabulary size : " + str(len(self.vocabulary)))
        
