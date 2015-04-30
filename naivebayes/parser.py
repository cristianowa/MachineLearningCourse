import re
from base import Base

class Parser(Base):
    def __init__(self, logFile = None):
        self.name = "PARSER"
        self.logFile = logFile
    def count(self, text):
        self.words = re.compile('\w+').findall(text)
        self.vocabulary = list(set(self.words))
    def getVocabulary(self):
        return self.vocabulary
    def printInfo(self):    
        self.__print__("Vocabulary size : " + str(len(self.vocabulary)))

Extractor = Parser()
