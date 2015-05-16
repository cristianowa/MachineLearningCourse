from folds import Folds,AllFolds
from validation import Validation
import argparse
def build(save = False):
    infos = AllFolds()
    val = Validation(infos)
    val.buildPredictors()
    if save:
        val.savePredictors()
    return val 
 
def run(run = False):  
    if run:
        val = Validation({})
        val.loadPredictors()
    else:
        val = build()
    val.testPredictors()
    val.evalPredictors()
    val.mergeAllConfusion()
    val.printPredictorsPerformance()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Naive Bayes Classifier")
    parser.add_argument("-a","-do-all", help = "Run all predictions", dest = "all", action = "store_true")
    parser.add_argument("-b","-build", help = "Only build predictors and save to files", dest = "build", action = "store_true")
    parser.add_argument("-r","-run", help = "Only run predictors saved in files", dest = "run", action = "store_true")
    args = parser.parse_args()
    if args.all:
        run()
    else:
        if args.build:
            build(True)
        if args.run:
            run(True)
