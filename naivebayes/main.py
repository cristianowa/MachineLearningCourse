from folds import Folds,AllFolds
from validation import Validation

  
infos = AllFolds()
val = Validation(infos)
val.buildPredictor(0)
val.savePredictor(0, "zero.pl")
val.testPredictor(0)
val.evalPredictor(0)
