from folds import Folds
from parser import Parser
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
    #consilidate all vocabs
#    for 
    #Another FOR
    for cls in info.keys():
        info[cls]["parser"].count(allvocabs.get())
        info[cls]["parser"].printInfo()
        info[cls]["count"] = info[cls]["parser"].getCount()

    info["__total__words__"] = {}
    for cls in info.keys():
        if cls == "__total__words__":
            continue
        for word in  info[cls]["count"].keys():
            if word not in info["__total__words__"].keys():
                info["__total__words__"][word] = info[cls]["count"][word]
            else:
                info["__total__words__"][word] += info[cls]["count"][word]
    for word in info["__total__words__"].keys():
        for cls in info.keys():
            if cls == "__total__words__":
                continue
            
infos= {}
for cls in configs.db_dirs:
    infos[cls] = {}
    infos[cls]["folds"] = Folds(configs.db_dirs[cls])
    

print infos
for f in infos:
    infos[f]["folds"].create()
    infos[f]["folds"].load()
validation(0, infos)
