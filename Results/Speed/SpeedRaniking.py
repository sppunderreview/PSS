import os
import pickle

import numpy as np

import matplotlib.pyplot as plt
from sklearn import metrics
import pandas as pd

import random

def formatTime(s):
    return str(int(s))

frameworks = ["heuristiqueSampleSize","heuristiqueJsonSize","prototypeJaccardAnonyme","GSA_Spectral","GSA_CFG_Spectral","GSA_GED_1","GSA_GED_1_L1","SMIT","AMalwareAndVariantDetectionMethod","SimilarityFunctionCallGraph","MutantX","asm2vecJ","gemini","AD","SAFEtorch","prototypeExtern","spectralSP"]
XPS = ["CV","CO","UV","UO","BV","BO"]

frameworksData = {}

for framework in frameworks:
    frameworksData[framework] = {}

    globalAvgCS = 0
    globalAvgSC = 0
    globalTotal = 0
    globalMinCS = 100000
    globalMinSC = 100000
    globalMaxCS = 0
    globalMaxSC = 0
        
    for nameDS in XPS:
        y = []
        
        outputFile = "../../"+framework+"/"+nameDS+"_MD"

        if os.path.exists(outputFile) == False:
            continue

        with open(outputFile, "rb") as f:
            MD = pickle.load(f)

        for idS in MD:
            couples = []
            
            for idS2 in  MD[idS]:
                name, name2, c, c2, d, t = MD[idS][idS2]                
                couples += [t]
            y += [couples]
        
        avgCS = 0
        for l in y:
            avgCS += sum(l)
        avgCS /= len(y)
        
        avgSC = 0
        n = 0
        for l in y:
            avgSC += sum(l)
            n += len(l)
        avgSC /= n 
        
        total = 0
        minCS = 100000
        minSC = 100000
        maxCS = 0
        maxSC = 0
        for l in y:
            total += sum(l)            
            minCS = min(sum(l),minCS)
            maxCS = max(sum(l), maxCS)
            for x in l:
                minSC = min(x,minSC)
                maxSC = max(x, maxSC)
                
                
        

        globalAvgCS += avgCS
        globalAvgSC += avgSC
        globalTotal += total
        globalMinCS = min(globalMinCS, minCS)
        globalMinSC = min(globalMinSC, minSC)
        globalMaxCS = max(globalMaxCS, maxCS)
        globalMaxSC = max(globalMaxSC, maxSC)
    
    globalAvgCS /= 6
    globalAvgSC /= 6

    frameworksData[framework]["Total"] = formatTime(globalTotal)
    
dfSIIISpeed = pd.DataFrame(frameworksData).T
dfSIIISpeed.fillna(0, inplace=True)

print(dfSIIISpeed)

"""
                                      Total
heuristiqueSampleSize                     7
heuristiqueJsonSize                       6
prototypeJaccardAnonyme                 107
GSA_Spectral                              2
GSA_CFG_Spectral                          3
GSA_GED_1                            386457
GSA_GED_1_L1                         222674
SMIT                               16250282
AMalwareAndVariantDetectionMethod         0
SimilarityFunctionCallGraph          807595
MutantX                                   4
asm2vecJ                             315544
gemini                               485790
AD                                  3024514
SAFEtorch                           3095329
prototypeExtern                           3
spectralSP                                3
"""

"""
heuristiqueSampleSize                     7
heuristiqueJsonSize                       6
prototypeJaccardAnonyme                 107
GSA_Spectral                           2199
GSA_CFG_Spectral                     153443
GSA_GED_1                            386457
GSA_GED_1_L1                         222674
SMIT                               16250282
AMalwareAndVariantDetectionMethod         0
SimilarityFunctionCallGraph          807595
MutantX                                   4
asm2vecJ                             315544
gemini                               485790
AD                                  3024514
SAFEtorch                           3095329
prototypeExtern                           3
spectralSP                             2849
"""

