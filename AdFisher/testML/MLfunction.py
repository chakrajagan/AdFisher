import sys
sys.path.append("../")
import core.adfisher as adfisher

import core.analysis.converter as converter
import core.analysis.ml as ml
import numpy as np

import stat
from datetime import datetime
from sklearn.linear_model import LogisticRegression

def getData(log_file="log.txt", splitfrac=0.1, nfolds=10, 
		feat_choice="ads", nfeat=5, verbose=False):
	if(feat_choice != "ads" and feat_choice != "words"):
		print "Illegal feat_choice", feat_choice
		return
	collection, names = converter.get_ads_from_log(log_file)	

	if len(collection) < nfolds:
		print "Too few blocks (%s). Analysis requires at least as many blocks as nfolds (%s)." % (len(collection), nfolds)
		return

	s = datetime.now()
	X,y,feat = converter.get_feature_vectors(collection, feat_choice='ads')

	X_oneLine = np.array([item for sublist in X for item in sublist])
	y_oneLine = np.array([item for sublist in y for item in sublist])

	return X_oneLine, y_oneLine
	
def logisticRegression(X,y):
	clf = LogisticRegression(penalty='l2', dual=False, C=np.logspace(-5.0, 15.0, num=21, base=2))
	model = clf.fit(X, y)
	print(model.score(X, y))
