from folds import Folds
from parser import Parser
from wordinfo import WordsInfo
import configs



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
    for word in words_info.get_prob().keys()[0:10]:
        print word
        print words_info.get_prob()[word]
#    print word_info.get_prob()
        
infos= {}
for cls in configs.db_dirs:
    infos[cls] = {}
    infos[cls]["folds"] = Folds(configs.db_dirs[cls])
    

print infos
for f in infos:
    infos[f]["folds"].create()
    infos[f]["folds"].load()
validation(0, infos)
