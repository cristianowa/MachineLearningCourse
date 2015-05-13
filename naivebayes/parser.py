import re
import configs
from base import Base


class Vocabulary:
    def __init__(self, words):
        if configs.load_from_file:
            self.vocabulary = open(configs.vocabulary_file).read().split("\n")
        else:
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
        self.__print__("Extracting")
        self.words = re.compile('\w+').findall(self.text)
        self.vocabulary = Vocabulary(self.words)
    def count(self, words):
        self.__print__("Counting")
        print words
        if configs.laplace_estimator:
            self.counts = dict.fromkeys(words,1)
        else:
            self.counts = dict.fromkeys(words,0)
        #this count of words in word is n^2
        #we can better this be looking at all self.words
        #and adding it to a dictionary
         
        for word in self.words:
            try:
                self.counts[word] += 1
            except:
                pass
#                self.__print__(word + " not found")
        return self.counts
    def getVocabulary(self):
        
        return self.vocabulary
    def getCount(self):
        return self.counts
    def printInfo(self):
        self.__print__("Vocabulary size : " + str(len(self.vocabulary.get())))
        self.__print__("Count size : " + str(len(self.counts)))


        
