import sys
sys.path.append("../")
import core.adfisher as adfisher
import MLfunction as myML

log_file = "log.mentaldisorder.txt"
#log_file = "log.substance.txt"
#log_file ="log.genjobs.may.txt"

#adfisher.run_ml_analysis(log_file, splitfrac=0.3,verbose=True)


X,y = myML.getData(log_file, verbose=True,block=False)
myML.RelaxedEnumeration(X,y,hypoSetSize=40,verbose=True,splitfrac = 0.2)
myML.enumeration(X,y,hypoSetSize=40,verbose=True,splitfrac = 0.2)
myML.MLmethod(X,y,verbose=True,splitfrac = 0.2)
#adfisher.run_ml_analysis(log_file, splitfrac=0.3,verbose=True)

"""
print(X)
print(y)

#print(feat)
myML.logisticRegression(X,y)
adfisher.run_ml_analysis(log_file, verbose=True)
"""