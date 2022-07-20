import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle

import os
import random

import numpy as np
from math import sqrt

import kmedoids

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

def distanceMutantX(E1,E2):
	return np.linalg.norm(E1 - E2)
	"""d = 0
	for x in E1:
		if x in E2:
			d += (E1[x] - E2[x])**2
		else:
			d += E1[x]**2
	for y in E2:
		if not(y in E1):
			d += E2[y]**2 
	return sqrt(d)"""


if __name__ == '__main__':
	import sys
	sys.path.insert(0, "/home/?/Documents/Travail/?/Virus")
	from makeBenchVirus import readAllSamples as allVirus
    
	labelsDict = {}
	labelId = 0
    
	pointsInFamily = {}
    
	labels = []    
	points = []
	for (idS,path,family,name, pathJson) in allVirus():
		"""if not(family in ['Lollipop', 'DomaIQ', 'Agent', 'Multi', 'DLBoost', 'Inject', 'LMN', 'SoftPulse', 'StartSurf', 'BrowseFox', 'Sytro', 'iBryte', 'AutoIt', 'ScreenSaver', 'DriverUpd', 'Morstar', 'MSIL', 'KuziTui', 'Soft32', 'BitMiner', 'DealPly', 'Allaple', 'Fiseria', 'Nimnul', 'Chapak', 'AdLoad', 'BitCoinMiner', 'Miner', 'Firser', 'Ekstak', 'Parite', 'ArchSMS', 'DownloaderGuide', 'Katusha', 'OutBrowse', 'Script', 'ICLoader', 'Lamer', 'DownloAdmin', 'AntiFW', 'Sality']):
			continue"""
		try:
			with open("A/"+idS, "rb") as f:
				e = pickle.load(f)
				
				
				if not(family in labelsDict):
					labelsDict[family] = labelId
					pointsInFamily[family] = 0 
					labelId += 1
				
				"""if pointsInFamily[family] > 5:
					continue"""

				points += [hashEmbedding(e)]
				labels += [ labelsDict[family] ]
				pointsInFamily[family] += 1
				 
		except IOError:
			pass
			
	print("number families", len(labelsDict))
	print("number points", len(labels))

	start = time.time()
	
	distanceMatrix = [ [0 for i in range(len(points))] for j in range(len(points))]	
	for i in range(len(points)):
		for j in range(len(points)):
			distanceMatrix[i][j] = distanceMutantX(points[i],points[j])

	X = np.array(distanceMatrix)
	
	print("distance elapsed", time.time()-start)
	
	start = time.time()
	Y = kmedoids.fasterpam(X, len(labelsDict),100).labels
	print("medoids elapsed", time.time()-start)

	scoreAMI = adjusted_mutual_info_score(labels, Y)
	scoreNMI = normalized_mutual_info_score(labels, Y)
	print("AMI",scoreAMI)
	print("NMI",scoreNMI)
