from folds import Folds
from parser import Parser
import configs



def validation(fold, folds):
    foldsRange = range(10)
    foldsRange.remove(fold)
    postext = folds["pos"].merge(foldsRange)
    negtext = folds["neg"].merge(foldsRange)
    posparser = Parser(postext)
    negparser = Parser(negtext)
    posparser.extract()
    posparser.count()
    posparser.printInfo()
    print posparser.getCount()
    negparser.extract()
    negparser.count()
    negparser.printInfo()
    
allfolds = {}

allfolds["pos"] = Folds(configs.db_dir_pos)
allfolds["neg"] = Folds(configs.db_dir_neg)
for f in allfolds:
    allfolds[f].create()
    allfolds[f].load()
validation(0, allfolds)
