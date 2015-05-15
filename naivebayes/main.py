from folds import Folds,AllFolds
from validation import Validation

  
infos = AllFolds()
val = Validation(infos)
val.buildPredictors()
val.testPredictors()
val.evalPredictors()
val.mergeAllConfusion()
val.printPredictorsPerformance()
