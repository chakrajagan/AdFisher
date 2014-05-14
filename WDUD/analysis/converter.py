import re, sys										
import numpy as np
from datetime import datetime, timedelta			# to read timestamps reloadtimes
import adVector, ad, common, interest				# common, ad ad_vector, interest classes
from nltk.corpus import stopwords 					# for removing stop-words


#------------- to convert Ad Vectors to feature vectors ---------------#

def word_vectors(list):									# returns a frequency vector of words, when input a list of adVecs
	ad_union = adVector.AdVector()
	for ads in list:
		ad_union = ad_union.union(ads)
	words = ad_union.advec_to_words()
	stemmed_words = common.stem_low_wvec(words)
	filtered_words = [w for w in stemmed_words if not w in stopwords.words('english')]
	word_v = common.unique_words(filtered_words)
	word_v = common.strip_vec(word_v)
	wv_list = []
	labels = []
	for ads in list:
		wv_list.append(ads.gen_word_vec(word_v))
		labels.append(ads.label)
	return wv_list, labels, word_v						## Returns word_v as feature

def ad_vectors(list):									# returns a frequency vector of ads, when input a list of adVecs
	ad_union = adVector.AdVector()
	for ads in list:
		ad_union = ad_union.union(ads)
	av_list = []
	labels = []
	for ads in list:
		av_list.append(ad_union.gen_ad_vec(ads))
		labels.append(ads.label)
	return av_list, labels, ad_union					## Returns entire ad as feature

def temp_ad_vectors(list):
	ad_union = adVector.AdVector()
	for ads in list:
		ad_union = ad_union.union(ads)
	tav_list = []
	labels = []
	for ads in list:
		tav_list.append(ad_union.gen_temp_ad_vec(ads))
		labels.append(ads.label)
	return tav_list, labels, ad_union

def interest_vectors(list):							# returns a frequency vector of interests, when input a list of interessts
	int_union = interest.Interests()
	for ints in list:
		int_union = int_union.union(ints)
	i_list = []
	labels = []
	for ints in list:
		i_list.append(int_union.gen_int_vec(ints))
		labels.append(ints.label)
	return i_list, labels, int_union

def get_interest_vectors(advdicts):
	list = []
	sys.stdout.write("Creating interest vectors")
 	sys.stdout.write("-->>")
 	sys.stdout.flush()
	for advdict in advdicts:
		list.extend(advdict['interests'])
	X, labels, feat = interest_vectors(list)
	if(labels[0] == ''):
		for advdict in advdicts:
			ass = advdict['ass']
			y1 = [0]*len(ass)
			for i in ass[0:len(ass)/2]:
				y1[int(i)] = 1
			y.extend(y1)
	else:
		y = [int(i) for i in labels]
	print "Complete"
	return np.array(X), np.array(y), feat

def get_feature_vectors(advdicts, feat_choice):			# returns observation vector from a list of rounds
	n = len(advdicts[0]['ass'])
	list = []
	y = []
	sys.stdout.write("Creating feature vectors")
 	sys.stdout.write("-->>")
 	sys.stdout.flush()
	for advdict in advdicts:
		list.extend(advdict['adv'])
	if(feat_choice == 'words'):
		X, labels, feat = word_vectors(list)
	elif(feat_choice == 'ads'):
		X, labels, feat = ad_vectors(list)
	if(labels[0] == ''):
		for advdict in advdicts:
			ass = advdict['ass']
			y1 = [0]*len(ass)
			for i in ass[0:len(ass)/2]:
				y1[int(i)] = 1
			y.extend(y1)
	else:
		y = [int(i) for i in labels]
	X = [X[i:i+n] for i in range(0,len(X),n)]
	y = [y[i:i+n] for i in range(0,len(y),n)]
# 	print feat[0].title, feat[0].url
	print "Complete"
	return np.array(X), np.array(y), feat
	
#------------- to read from log file into Ad Vectors ---------------#


def apply_labels_to_AdVecs(adv, ints, ass, samples, treatments):			# check
	size = samples/treatments
	for i in range(0, treatments):
		for j in range(0, size):
			adv[int(ass[i*size+j])].setLabel(i)
			ints[int(ass[i*size+j])].setLabel(i)

def get_ads_from_log(log_file):							# check
	treatnames = []
	fo = open(log_file, "r")
	line = fo.readline()
	chunks = re.split("\|\|", line)
	if(chunks[0] == 'g'):
		old = True
		gmarker = 'g'
		treatments = 2
		treatnames = ['0', '1']
		samples = len(chunks)-1
	else:
		old = False
		gmarker = 'assign'
		treatments = int(chunks[2])
		samples = int(chunks[1])
		line = fo.readline()
		chunks = re.split("\|\|", line)
		for i in range(1, len(chunks)):
			treatnames.append(chunks[i].strip())
	assert treatments == len(treatnames)
	fo.close()
	adv = []
 	ints = []
	for i in range(0, samples):
 		adv.append(adVector.AdVector())
 		ints.append(interest.Interests())
 	loadtimes = [timedelta(minutes=0)]*samples
 	reloads = [0]*samples
 	errors = [0]*samples
 	xvfbfails = []
 	breakout = False
 	par_adv = []
 	ass = []
		
	fo = open(log_file, "r")
	r = 0	
	sys.stdout.write("Scanning ads")
	for line in fo:
		chunks = re.split("\|\|", line)
		chunks[len(chunks)-1] = chunks[len(chunks)-1].rstrip()
		if(chunks[0] == gmarker and r==0):
			r += 1
			ass = chunks[2:]
			if(old):	
				ass = chunks[1:]
			assert len(ass) == samples
			apply_labels_to_AdVecs(adv, ints, ass, samples, treatments)
 			#print ass
 		elif(chunks[0] == gmarker and r >0 ):
 			r += 1
 			par_adv.append({'adv':adv, 'ass':ass, 'xf':xvfbfails, 'interests':ints, 
 						'break':breakout, 'loadtimes':loadtimes, 'reloads':reloads, 'errors':errors})
 			sys.stdout.write(".")
			sys.stdout.flush()
			adv = []
 			ints = []
			for i in range(0, samples):
 				adv.append(adVector.AdVector())
 				ints.append(interest.Interests())
 			loadtimes = [timedelta(minutes=0)]*samples
			reloads = [0]*samples
			errors = [0]*samples
 			xvfbfails = []
 			breakout = False
			ass = chunks[2:]
			if(old):	
				ass = chunks[1:]
			assert len(ass) == samples
			apply_labels_to_AdVecs(adv, ints, ass, samples, treatments)
 		elif(chunks[0] == 'Xvfbfailure'):
 			xtreat, xid = chunks[1], chunks[2]
 			xvfbfails.append(xtreat)
 		elif(chunks[1] == 'breakingout'):
 			breakout = True
 		elif(chunks[1] == 'loadtime'):
 			t = (datetime.strptime(chunks[2], "%H:%M:%S.%f"))
 			delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
 			id = int(chunks[3])
 			loadtimes[id] += delta
 		elif(chunks[1] == 'reload'):
 			id = int(chunks[2])
 			reloads[id] += 1
 		elif(chunks[1] == 'errorcollecting'):
 			id = int(chunks[2])
 			errors[id] += 1
 		elif(chunks[1] == 'pref'):
 			id = int(chunks[4])
 			int_str = chunks[3]
 			ints[id].set_from_string(int_str)
		elif(chunks[0] == 'ad'):
			ind_ad = ad.Ad({'Time':datetime.strptime(chunks[3], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[4], 
					'URL': chunks[5], 'Body': chunks[6].rstrip(), 'cat': "", 'label':chunks[2]})
			adv[int(chunks[1])].add(ind_ad)
		else:							# to analyze old log files
			try:
				ind_ad = ad.Ad({'Time':datetime.strptime(chunks[2], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[3], 
						'URL': chunks[4], 'Body': chunks[5].rstrip(), 'cat': "", 'label':chunks[1]})
# 	 			ind_ad = ad.Ad({'Time':datetime.strptime(chunks[1], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[2], 
# 	 					'URL': chunks[3], 'Body': chunks[4].rstrip(), 'cat': "", 'label':""})
				adv[int(chunks[0])].add(ind_ad)
			except:
				pass
 	
 	r += 1
 	par_adv.append({'adv':adv, 'ass':ass, 'xf':xvfbfails, 'interests':ints, 
 			'break':breakout, 'loadtimes':loadtimes, 'reloads':reloads, 'errors':errors})
 	sys.stdout.write(".Scanning complete\n")
 	sys.stdout.flush()
 	return par_adv, treatnames