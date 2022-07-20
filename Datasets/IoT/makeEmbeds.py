import os
from os.path import isfile
from pathlib import Path

import pickle
import json

import random
import time

import numpy as np
import networkx as nx

# PSS
# [SL, len(SL), traceF, len(traceF), elapsed]
def embeddingPSS(idS, D):	
	with open("../PSS/A_PSS/"+idS, "rb") as f:
		E = pickle.load(f)
	l = []		
	for i in range(D):
		if i >= E[1]:
			l += [0]
			continue
		l += [ E[0][i] ]

	for i in range(D):
		if i >= E[-2]:
			l += [0]
			continue
		l += [ E[2][i] ]

	return np.array(l)

# SCG
# [spectrum, elapsed]
def embeddingSCG(idS, D):	
	with open("../GSA/A_GSA/"+idS, "rb") as f:
		E = pickle.load(f)
	l = []		
	for i in range(D):
		if i >= len(E[0]):
			l += [0]
			continue
		l += [ E[0][i] ]
	return np.array(l)

# Mutant-X
# {4-gram -> freq}
def embeddingMUTANTX(idS):	
	with open("../MutantX/A_MUTANTX/"+idS, "rb") as f:
		D = pickle.load(f)[0]

	embed = [0 for i in range(4096)]	
	for ngram in D:
		t = ngram.replace("??", "ff")
		
		isBinary = True
		for c in t:
			if not(c in ["0","1", " "]):
				isBinary = False
				break
		t = t.split("_")
		t = [x for x in t if x != "" ]
		
		if isBinary:
			ngramInt = [ int(s, 2) for s in t]
		else:
			ngramInt = [ int(s, 16) for s in t]
		hashNgram = 7		
		for x in ngramInt:
			hashNgram = 31 * hashNgram + x
		p = hashNgram % 4096

		embed[p] += D[ngram]	
	return np.array(embed)

# Function Set
def embeddingFS(idS):
	pathJson = "../jsons/"+idS+".tmp.json"
	with open(pathJson, "r") as f:
	  data = json.load(f)
	
	externCalls = set()
	for f in data["functions"]:
		for nameCall in f["api"]:
			externCalls.add(nameCall)
	return externCalls
	
# Shape
def embeddingSHAPE(idS):
	pathJson = "../jsons/"+idS+".tmp.json"
   
	with open(pathJson, "r") as f:
	  data = json.load(f)

	functionName = {}
	graphP = {}
	
	for f in data["functions"]:
		idFunction = "F_"+str(f["id"])
		functionName[idFunction] = f["name"]
		graphP[idFunction] = []
		
		for nextF in f["call"]:
			idNF = "F_"+str(nextF)
			graphP[idFunction] += [idNF]
	
	G = nx.Graph()
	for x in graphP:
		for y in graphP[x]:
			nameX = functionName[x]
			if not(y in functionName):
				continue
			nameY = functionName[y]
			if nameX == nameY:
				continue
			G.add_edge(nameX, nameY)
	
	N = G.number_of_nodes()
	E = G.number_of_edges()
	return np.array([N,E])

# BSize
def embeddingBSIZE(idS):		
	return np.array([os.path.getsize("../samples/"+idS)])

#DSize
def embeddingDSIZE(idS):		
	return np.array([os.path.getsize("../jsons/"+idS+".tmp.json")])

	
with open("../make/familiesMetaElf", "rb") as f:
	hashToFamilies = pickle.load(f)

familiesByPriority = ['pnscan', 'vpnfilter', 'hajime', 'lightaidra', 'dnsamp', 'skeeyah', 'ddostf', 'tsunami', 'gafgyt', 'mirai']
"""
{'pnscan': 1, 'vpnfilter': 5, 'hajime': 6, 'lightaidra': 8, 'dnsamp': 18, 'skeeyah': 19, 'ddostf': 24, 'tsunami': 1763, 'gafgyt': 7322, 'mirai': 19541 }
"""
# {9: 12357, 7: 1760, 8: 5842, 0: 1, 6: 23, 4: 17, 2: 6, 5: 19, 1: 5, 3: 8}

labelsAssigned = {}

IoT = []
for path in Path('../jsons').rglob('*'):
	pathJson = str(path)
	idS = pathJson.split(".tmp.json")[0].split("jsons/")[1]
	outputFile = "../PSS/A_PSS/"+idS
	if isfile(outputFile) == False:
		continue
	hashS = idS.replace(".elf","")
	if hashToFamilies[hashS] == None:
		continue
	trueLabel = len(familiesByPriority) - 1
	for i in range(len(familiesByPriority)):
		
		if familiesByPriority[i] in hashToFamilies[hashS]:
			trueLabel = i
			break
	
	if not(trueLabel in labelsAssigned):
		labelsAssigned[trueLabel] = 0
	labelsAssigned[trueLabel] += 1
	
	
	if trueLabel in [7,8,9]:
		IoT += [(idS, trueLabel-7)]	

# PSS
for D in [5535]:
	E = []
	T = []
	for (idS, trueLabel) in IoT:
		try:
			E += [ embeddingPSS(idS, D) ]
			T += [trueLabel]
		except Exception:
			pass	
	X = np.asarray(E, dtype=np.float64)			
	Y = np.asarray(T)
	FE = (X,Y)
	
	with open("PSS_D_"+str(D),"wb") as f:
		pickle.dump(FE, f)

# SCG
for D in [5535]:
	E = []
	T = []
	for (idS, trueLabel) in IoT:
		try:
			E += [ embeddingSCG(idS, D) ]
			T += [trueLabel]
		except Exception:
			pass	
	X = np.asarray(E, dtype=np.float64)			
	Y = np.asarray(T)
	FE = (X,Y)
	
	with open("SCG_D_"+str(D),"wb") as f:
		pickle.dump(FE, f)


# OTHERS

for (fEmb, nEmb) in  [(embeddingFS, "FUNCTIONSET"),(embeddingMUTANTX, "MUTANTX"),(embeddingSHAPE, "SHAPE"),(embeddingBSIZE, "BSIZE"), (embeddingDSIZE, "DSIZE")]:
	print(nEmb)
	E = []
	T = []
	for (idS, trueLabel) in IoT:
		try:
			E += [fEmb(idS)]
			T += [trueLabel]
		except Exception as e:
			print(e)

	if nEmb != "FUNCTIONSET":
		X = np.asarray(E, dtype=np.float64)
	else:
		X = E
	Y = np.asarray(T)
	FE = (X,Y)	
	with open(nEmb,"wb") as f:
		pickle.dump(FE, f)


