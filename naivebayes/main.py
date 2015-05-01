from folds import Folds
from parser import Parser
import configs



def validation(fold, info):
    foldsRange = range(10)
    foldsRange.remove(fold)
    info["pos"]["text"] = info["pos"]["folds"].merge(foldsRange)
    info["neg"]["text"] = info["neg"]["folds"].merge(foldsRange)
    # TODO: this MUST improve ! 
    info["neg"]["parser"] = Parser( info["neg"]["text"])
    info["neg"]["parser"].extract()
    info["neg"]["vocab"] = info["neg"]["parser"].getVocabulary()
    
    #consilidate all vocabs
    #Another FOR
    info["neg"]["parser"].count(allVocabs)
    info["neg"]["parser"].printInfo()
    info["neg"]["count"] =  info["neg"]["parser"].getCount()

infos= {}

infos["pos"] = {}
infos["pos"]["folds"] = Folds(configs.db_dir_pos)
infos["neg"] = {}
infos["neg"]["folds"] = Folds(configs.db_dir_neg)

for f in infos:
    infos[f]["folds"].create()
    infos[f]["folds"].load()
validation(0, infos)
