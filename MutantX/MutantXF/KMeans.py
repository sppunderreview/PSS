import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle

import random

import numpy as np

import sklearn
from sklearn.cluster import KMeans

from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import normalized_mutual_info_score

def hashEmbedding(e):
	d = e[0]
	embed = [0 for i in range(4096)]
	
	for ngram in d:
		t = ngram.replace("??", "ff")
		t = t.split("_")
		ngramInt = [ int(s, 16) for s in t]
		hashNgram = 7		
		for x in ngramInt:
			hashNgram = 31 * hashNgram + x
		p = hashNgram % 4096
		embed[p] += d[ngram]		
	return np.array(embed)

if __name__ == '__main__':
	import sys
	sys.path.insert(0, "/home/?/Documents/Travail/?/Virus")
	from makeBenchVirus import readAllSamples as allVirus
    
	labelsDict = {}
	labelId = 0
    
	labels = []    
	embeddings = []
	for (idS,path,family,name, pathJson) in allVirus():
		try:
			with open("A/"+idS, "rb") as f:
				e = pickle.load(f)
				embeddings += [ hashEmbedding(e) ]
				
				if not(family in labelsDict):
					labelsDict[family] = labelId
					labelId += 1
					
				labels += [ labelsDict[family] ]
		except IOError:
			pass

	print("number families", len(labelsDict))
	print(len(labels))
	
	X = np.asarray(embeddings, dtype=np.float32)
	
	start = time.time()
	kmeans = KMeans(n_clusters=len(labelsDict), n_init=10, max_iter=300, algorithm="full").fit(X)	
	print("elapsed", time.time()-start)
	
	Y = kmeans.labels_
	
	scoreAMI = adjusted_mutual_info_score(labels, Y)
	scoreNMI = normalized_mutual_info_score(labels, Y)
	print("AMI",scoreAMI)
	print("NMI",scoreNMI)
