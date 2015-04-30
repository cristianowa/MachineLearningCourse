from folds import Folds
from parser import Extractor
import configs



def validation(fold, folds):
    foldsRange = range(10)
    foldsRange.remove(fold)
    postext = folds["pos"].merge(foldsRange)
    negtext = folds["neg"].merge(foldsRange)
    Extractor.count(postext)
    posvoc = Extractor.getVocabulary()
    Extractor.printInfo()
    Extractor.count(negtext)
    negvoc = Extractor.getVocabulary()
    Extractor.printInfo()
allfolds = {}

allfolds["pos"] = Folds(configs.db_dir_pos)
allfolds["neg"] = Folds(configs.db_dir_neg)
for f in allfolds:
    allfolds[f].create()
    allfolds[f].load()
validation(0, allfolds)
