from folds import Folds
from parser import Parser
from wordinfo import WordsInfo
import configs
from predictor import Predictor


def validation(fold, info):
    foldsRange = range(10)
    foldsRange.remove(fold)
    for cls in info.keys():
        info[cls]["text"] = info[cls]["folds"].merge(foldsRange)
        info[cls]["parser"] = Parser(info[cls]["text"])
        info[cls]["parser"].extract()
        info[cls]["vocab"] = info[cls]["parser"].getVocabulary()
    allvocabs = None 
    for cls in info.keys():
        if allvocabs == None:
            allvocabs = info[cls]["vocab"]
            continue
        allvocabs.merge(info[cls]["vocab"])
    for cls in info.keys():
        info[cls]["parser"].count(allvocabs.get())
        info[cls]["parser"].printInfo()
        info[cls]["count"] = info[cls]["parser"].getCount()
    words_info =  WordsInfo(info)
    words_info.count()
    words_info.calc_prob()

    predictor = Predictor(words_info.get_prob())
    results = {}
    for cls in info.keys():
        results.update(dict.fromkeys(info[cls]["folds"].listOfFiles(fold), {"oracle":cls}))
    results = predictor.predictAll(results)
infos= {}
for cls in configs.db_dirs:
    infos[cls] = {}
    infos[cls]["folds"] = Folds(configs.db_dirs[cls])
    

for cls in infos:
    infos[cls]["folds"].create()
    infos[cls]["folds"].load()
    infos[cls]["folds"].foldsInfo()
validation(0, infos)

