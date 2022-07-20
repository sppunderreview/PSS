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

# RESULTS += [idSI, nameI == T[idMinJ], elapsed]
if __name__ == '__main__':
    P = 40
    LQB = ["QB", "QB40k","QB20K"]
    LC =  [(distSHAPE, "SHAPE"),(distEuclid, "BSIZE"), (distEuclid, "DSIZE"), (distEuclid, "MUTANTX"),(distPSS, "PSS"), (distSCG, "GSA"),(distFS, "FUNCTIONSET"), (distRandom, "Random")]

    for (distF, nEmb) in LC:
        for nQBI in LQB:
            RESULTS = []
            for pId in range(P):
                inputFile = "R/R_"+nQBI+"_"+nEmb+"_"+str(pId)                
                with open(inputFile, "rb") as f:
                    RESULTS += pickle.load(f)
            ACC = []
            for i in range(1,len(RESULTS), 3):
                ACC += [RESULTS[i]]
            S = sum(ACC)
            print(nEmb, nQBI, S, len(ACC), S/len(ACC))
            

"""
SHAPE QB 19148 49443 0.387274234977651
SHAPE QB40k 11259 24983 0.45066645318816795
SHAPE QB20K 5810 12083 0.48084085078209055
BSIZE QB 9668 49443 0.19553829662439576
BSIZE QB40k 6478 24983 0.2592963214986191
BSIZE QB20K 3772 12083 0.31217412894148805
DSIZE QB 21995 49443 0.4448556924134862
DSIZE QB40k 11790 24983 0.471920906216227
DSIZE QB20K 5577 12083 0.4615575602085575
MUTANTX QB 23390 49443 0.4730699997977469
MUTANTX QB40k 13282 24983 0.5316415162310371
MUTANTX QB20K 6671 12083 0.5520979889100389
PSS QB 23416 49443 0.47359585785652164
PSS QB40k 13507 24983 0.5406476403954689
PSS QB20K 6893 12083 0.5704709095423321
GSA QB 21842 49443 0.44176121999069634
GSA QB40k 12418 24983 0.4970579994396189
GSA QB20K 6153 12083 0.5092278407680212
FUNCTIONSET QB 21036 49443 0.4254596201686791
FUNCTIONSET QB40k 12438 24983 0.49785854380979067
FUNCTIONSET QB20K 6671 12083 0.5520979889100389
Random QB 6 49443 0.00012135185971725017
Random QB40k 4 24983 0.00016010887403434336
Random QB20K 2 12083 0.00016552180749813787
"""