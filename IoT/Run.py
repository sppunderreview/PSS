import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np

from tqdm import tqdm
from multiprocessing import Process

def preprocessPSS(E):
	E2 = []
	for i in range(len(E)):
		CG  = np.array(E[i][:5535])
		CFG = np.array(E[i][5535:])
		sizeCG  = np.argmax(CG==0)
		sizeCFG = np.argmax(CFG==0)
		E2 += [(CG,CFG,sizeCG+1,sizeCFG+1)]
	return E2

def preprocessSCG(E):
	E2 = []
	for i in range(len(E)):
		CG  = E[i]
		sizeCG  = np.argmax(CG==0)
		E2 += [(CG,sizeCG+1)]
	return E2

def distPSS(A,B):
	k  = min(A[2],B[2])
	k2 = min(A[3],B[3])
	return np.linalg.norm(A[0][:k] - B[0][:k])  + np.linalg.norm(A[1][:k2] - B[1][:k2])

def distSCG(A,B):
	k  = min(A[1],B[1])
	return np.linalg.norm(A[0][:k] - B[0][:k], ord=1)

def distSHAPE(A,B):
	return 1 - (min(A[0],B[0])*min(A[1],B[1]))/(max(A[0],B[0])*max(A[1],B[1]))

def distEuclid(A,B):
	return np.linalg.norm(A-B)

def distFS(A, B):
    if len(A) + len(B) == 0:
        return 0
    return 1 - len(A.intersection(B))/len(A.union(B))

def distRandom(A,B):
    return random.random()

def minRun(L1, pId, L2, E, T, distF, maxId):
    for i in L1:
        if i % maxId != pId:
            continue    
        dMin = None
        minId = -1
        for j in L2:
            if i == j:
                continue
            d = distF(E[i],E[j])
            if dMin == None or d < dMin :
                dMin = d
                minId = j
        print(T[minId] == T[i])

if __name__ == '__main__':
    #LC =[(distEuclid, "DSIZE"), (distEuclid, "MUTANTX"),(distPSS, "PSS_D_5535"), (distSCG, "SCG_D_5535"), (distSHAPE, "SHAPE")]
    LC = [(distFS, "FUNCTIONSET"), (distRandom, "PSS_D_5535")]
    
    embeddingsByMethod = {}
    for (distF, nEmb) in LC:	
        with open("../EMBEDS/"+nEmb, "rb") as f:
            (E,T) = pickle.load(f)
            
        if nEmb == "PSS_D_5535":
            E = preprocessPSS(E)
        elif nEmb == "SCG_D_5535":
            E = preprocessSCG(E)
            
        ACC = []
        
        L1 = [i for i in range(len(E))]
        L2 = [i for i in range(len(E))]
        random.shuffle(L1)
        random.shuffle(L2)
        
        P = 40
        PL = []
        print(nEmb)

        start = time.time()
        for pId in range(P):
            p = Process(target=minRun, args=(L1, pId, L2, E, T, distF, P))
            PL += [p]
            p.start()
        
        for p in PL:
            p.join()
        
        print(time.time()-start,"s")

