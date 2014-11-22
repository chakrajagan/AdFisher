import sys
sys.path.append("../")
import core.adfisher as adfisher
import MLfunction as myML

#log_file = "log.mentaldisorder.txt"
log_file = "log.substance.txt"

X,y = myML.getData(log_file, verbose=True)
#print(X)
#print(y)
myML.logisticRegression(X,y)
#adfisher.run_ml_analysis(log_file, verbose=True)
