import re
from base import Base

class Parser(Base):
    def __init__(self):
        self.name = "PARSER"
    def count(self, text):
        self.words = re.compile('\w+').findall(text)
        self.vocabulary = list(set(word))
    def getVocabulary():
        return self.vocabulary
    def printInfo(self):    
        self.__print__("Vocabulary size : " + str(len(self.vocabulary)))   
