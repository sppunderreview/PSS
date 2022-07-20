import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import time
import pickle
import random
import numpy as np
from copy import deepcopy

from multiprocessing import Process

def distPSS(A,B):
        k  = min(len(A[0]),len(B[0]))
        k2 = min(len(A[1]),len(B[1]))
        return np.linalg.norm(A[0][:k] - B[0][:k])  + np.linalg.norm(A[1][:k2] - B[1][:k2])

def distSCG(A,B):
        k  = min(len(A),len(B))
        return np.linalg.norm(A[:k] - B[:k], ord=1)

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

def minRun(pId, maxId, Q, B, E, T, distF, nQBI, nEmb):
    outputFile = "R_"+nQBI+"_"+nEmb+"_"+str(pId)
    RESULTS = []

    for i in range(len(Q)):
        if i % maxId != pId:
            continue
        random.shuffle(B)
        idSI = Q[i]
        start = time.time()
        dMin = None
        nameI = T[idSI]
        idMinJ = 0
        for idSJ in B:
            if idSI == idSJ:
                continue
            d = distF(E[idSI],E[idSJ])
            if dMin == None or d < dMin :
                dMin = d
                idMinJ = idSJ
        elapsed = time.time() - start
        RESULTS += [idSI, nameI == T[idMinJ], elapsed]

    with open(outputFile, "wb") as f:
        pickle.dump(RESULTS, f)

if __name__ == '__main__':

    with open("QB", "rb") as f:
        QB = pickle.load(f)

    with open("QB40k", "rb") as f:
        QB40k = pickle.load(f)

    with open("QB20k", "rb") as f:
        QB20k = pickle.load(f)

    with open("idSToName", "rb") as f:
        idSToName = pickle.load(f)

    P = 40

    LQB = [(QB, "QB"), (QB40k, "QB40k"), (QB20k, "QB20K")]
    #LC =  [(distSHAPE, "SHAPE"),(distEuclid, "BSIZE"), (distEuclid, "DSIZE"), (distEuclid, "MUTANTX"),(distPSS, "PSS"), (distSCG, "GSA"),(distFS, "FUNCTIONSET"), 
    LC =  [(distRandom, "Random")]

    for (distF, nEmb) in LC:
        with open(nEmb, "rb") as f:
            E = pickle.load(f)

        for (QBI, nQBI) in LQB:
            print(nQBI, nEmb)

            Q = [idS for idS in QBI[0]]
            B = [idS for idS in QBI[1]]
            PL = []
            start = time.time()
            for pId in range(P):
                p = Process(target=minRun, args=(pId, P, Q, deepcopy(B), E, idSToName, distF, nQBI, nEmb))
                PL += [p]
                p.start()

            for p in PL:
                p.join()

            print(time.time()-start, "s")
