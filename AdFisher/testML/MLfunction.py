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
	
	#validation step
	"""
	max = 0
	for i from 2^-5 to 2^15, i = i * 2
		clf = LogisticRegression(penalty='l2', dual=False, C=i)
		model = clf.fit(X_validation(80%), y_validation(80%))
		acc = model.score(X_validation(20%), y_validation(20%))
		if acc> max
			C = i
			max = acc
	"""
	
	clf = LogisticRegression(penalty='l2', dual=False, C=0.03125)
	#print(X)
	#print(y)

	#training
	model = clf.fit(X[0:20], y[0:20])
	#print(model.coef_)
	
	#testing
	acc = model.score(X[0:20], y[0:20])

	print(acc)
