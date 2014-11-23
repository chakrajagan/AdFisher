import sys
sys.path.append("../")
import core.adfisher as adfisher

import core.analysis.converter as converter
import core.analysis.ml as ml
import core.analysis.stat as stat

import numpy as np
import math
import random

from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RandomizedLogisticRegression

def getData(log_file="log.txt", splitfrac=0.1, nfolds=10, 
		feat_choice="ads", nfeat=5, verbose=False,block=False):
	if(feat_choice != "ads" and feat_choice != "words"):
		print "Illegal feat_choice", feat_choice
		return
	collection, names = converter.get_ads_from_log(log_file)	

	if len(collection) < nfolds:
		print "Too few blocks (%s). Analysis requires at least as many blocks as nfolds (%s)." % (len(collection), nfolds)
		return

	s = datetime.now()
	X,y,feat = converter.get_feature_vectors(collection, feat_choice='ads')

	if(block==True):
		X_oneLine = np.array([item for sublist in X for item in sublist])
		y_oneLine = np.array([item for sublist in y for item in sublist])
	else:
		X_oneLine = X
		y_oneLine = y
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
	X_oneLine = np.array([item for sublist in X for item in sublist])
	y_oneLine = np.array([item for sublist in y for item in sublist])
	model = clf.fit(X_oneLine, y_oneLine )
	#print(model.coef_)
	
	#testing
	#acc = model.score(X[0:20], y[0:20])

	#print(acc)
	getPValue(X,y,model)

def getPValue(X,y,cls):
	pvalue = stat.block_p_test(X, y, cls,iterations=10000)
	print(pvalue)

def listCmp(list1, list2):
    for val in list1:
        if val in list2:
            return True
    return False

def genHypoSet(hypoSetSize,X_train,y_train,isRandom=True):
	isRandom=False
	minC = 0.03125
	multiple = pow( 2 ,float(1)/math.log( ((float)(hypoSetSize)/10.0),2) )

	hypoSet = []
	for i in range(0,hypoSetSize):
		randomNum = random.uniform(-5,15);
		#print(randomNum)
		
			#iterative
		if(isRandom!=True):
			C = minC * pow(multiple,i)
		else:
			#random
			C = pow(2,randomNum)

		clf = LogisticRegression(penalty='l2', dual=False, C=C)
		#clf = RandomizedLogisticRegression( C=C)
		model = clf.fit((X_train), y_train )
		hypoSet.append(model)
	return hypoSet

def getAbstainAccuracy(X_test,y_test,model, abstainSet):
	match = 0
	total = 0
	dontknow =0
	for i in range(0,len(X_test)):
		if(i in abstainSet):
			dontknow += 1
		if (model.predict(X_test[i])==y_test[i]):
			match += 1
		total += 1

	return(float(match)/float(total)), (float(dontknow)/float(total))

def getHypoSetAccuracy(X_train,y_train,X_test,y_test,hypoSet):
	maxAcc = 0
	maxCls = hypoSet[0]
	for cls in hypoSet:
		acc = cls.score(X_train,y_train)
		if(acc > maxAcc):
			acc = maxAcc
			maxCls = cls

	return maxCls.score(X_test,y_test)

def enumeration(X,y,hypoSetSize=20,verbose=True,splitfrac = 0.1,splittype = 'timed'):
	
	X_train, y_train, X_test, y_test = ml.split_data(X, y, splittype, splitfrac, verbose)

	X_train = np.array([item for sublist in X_train for item in sublist])
	y_train = np.array([item for sublist in y_train for item in sublist])
	
	X_test = np.array([item for sublist in X_test for item in sublist])
	y_test = np.array([item for sublist in y_test for item in sublist])

	hypoSet = genHypoSet(hypoSetSize,X_train,y_train)
	
	#print(getHypoSetAccuracy(X_train,y_train,X_test,y_test,hypoSet))

	dontKnowData = set()
	keep_hypo = []
	for i in range(0,len(X_test)):
		oneX = X_test[i]
		oneY = y_test[i]
		
		allSame = True
		predictFirst = hypoSet[0].predict(oneX)
		for j in range(1,len(hypoSet)):
			predictVal = hypoSet[j].predict(oneX)
			if(predictFirst!=predictVal):
				allSame = False
				break
		
		if(allSame == True):
			a=1
			#print(str(i)+": "+str(predictFirst)+" real:"+str(oneY))
		else:
			dontKnowData.add(i)
			#print(str(i)+": dont' know")
			"""
			print(len(hypoSet))
			print(oneY)
			print(hypoSet[0].predict(oneX))
			print(hypoSet[1].predict(oneX))
			"""
			deleteHypoAry = []
			for j in range(0,len(hypoSet)):
				if(hypoSet[j].predict(oneX) != oneY):
					#print(hypoSet[j])
					deleteHypoAry.append(hypoSet[j])

			for j in range(0,len(deleteHypoAry)):
				#print(deleteHypoAry[j])
				hypoSet.remove(deleteHypoAry[j])
				if(len(hypoSet)==1):
					break
		if(len(hypoSet)==1):
			keep_hypo.append(hypoSet[0])
			break
	
	#print(len(hypoSet))
	if(len(keep_hypo)==0):
		keep_hypo.append(hypoSet[0])

	acc , dontknow = getAbstainAccuracy(X_test,y_test,keep_hypo[0],dontKnowData)
	print("acc: "+str(acc) +", don't know: " + str(dontknow))

def RelaxedEnumeration(X,y,hypoSetSize=20,verbose=True,errRatio=0.1,splitfrac = 0.1,splittype = 'timed'):
	
	
	X_train, y_train, X_test, y_test = ml.split_data(X, y, splittype, splitfrac, verbose)

	X_train = np.array([item for sublist in X_train for item in sublist])
	y_train = np.array([item for sublist in y_train for item in sublist])
	
	X_test = np.array([item for sublist in X_test for item in sublist])
	y_test = np.array([item for sublist in y_test for item in sublist])

	hypoSet = genHypoSet(hypoSetSize,X_train,y_train)
	
	#print(getHypoSetAccuracy(X_train,y_train,X_test,y_test,hypoSet))

	k = hypoSetSize * errRatio
	s = pow(hypoSetSize,(float)(k)/(float)(k+1) )
	m = 0

	keep_hypo = []
	dontKnowData = set()
	
	for i in range(0,len(X_test)):
		oneX = X_test[i]
		oneY = y_test[i]

		predictP=0
		predictN=0
		for cls in hypoSet:
			if(cls.predict(oneX)[0]==1):
				#print(cls.predict(oneX)[0])
				predictP += 1
			else:
				#print(cls.predict(oneX)[0])
				predictN += 1

		#print str(predictP) + " " + str(predictN)
		u = min(predictP,predictN)

		if(u <= s):
			if(u==predictP):
				prefictY = 0
				#print(0)
			else:
				predictY = 1
				#print(1)
		else:
			dontKnowData.add(i)
			#print("don't know")

		deleteHypoAry = []
		for cls in hypoSet:
			if(cls.predict(oneX)[0] != oneY):
				#print str(cls.predict(oneX)[0]) + " " + str(oneY)
				deleteHypoAry.append(cls)
		for j in range(0,len(deleteHypoAry)):
			hypoSet.remove(deleteHypoAry[j])
			if(len(hypoSet)==1):
				break

		#print str(u)+" "+str(s)+" set size:"+str(len(hypoSet))

		if( (u>s) and (predictY != oneY)):
			m += 1
			s = pow(hypoSetSize,(float)(k-m)/(float)(k+1-m))

		if(len(hypoSet)==1):
			keep_hypo.append(hypoSet[0])
			break



	#print(len(hypoSet))
	if(len(keep_hypo)==0):
		keep_hypo.append(hypoSet[0])

	acc , dontknow = getAbstainAccuracy(X_test,y_test,keep_hypo[0],dontKnowData)
	print("acc: "+str(acc) +", don't know: " + str(dontknow))

def MLmethod(X,y,verbose=True,splitfrac = 0.1,splittype = 'timed'):
	algos = {	
				'logit':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'penalty':['l2']},
# 				'svc':{'C':np.logspace(-5.0, 15.0, num=21, base=2)}	
# 				'kNN':{'k':np.arange(1,20,2), 'p':[1,2,3]}, 
# 				'polySVM':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'degree':[1,2,3,4]},
# 				'rbfSVM':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'gamma':np.logspace(-15.0, 3.0, num=19, base=2)}			
			}

	X_train, y_train, X_test, y_test = ml.split_data(X, y, splittype, splitfrac, verbose)

	if(verbose):
		print "Training Set size: ", len(y_train), "blocks"
		print "Testing Set size: ", len(y_test), "blocks"

	clf, CVscore = ml.select_and_fit_classifier(10, algos, X_train, y_train, splittype, splitfrac, 1, verbose)

	print "CVscore: ", CVscore
	print "Test accuracy: ", ml.test_accuracy(clf, X_test, y_test, 1)
