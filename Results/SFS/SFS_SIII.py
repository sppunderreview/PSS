import os
import pickle

import numpy as np

from sklearn import metrics
import pandas as pd

import random
from math import sqrt

XPS = ["CV","CO","UV","UO","BV","BO"]
K = 1

frameworkPlot = {}

for nameDS in XPS:        
    outputFile = "../../spectralSP/"+nameDS+"_MD"

    if os.path.exists(outputFile) == False:
        continue

    with open(outputFile, "rb") as f:
        MD = pickle.load(f)

    with open("../../prototypeExtern/"+nameDS+"_MD", "rb") as f:
        MD2 = pickle.load(f)
    
    for alpha in range(0, 100):
        y = []
        
        for idS in MD:
            couples = []
            
            for idS2 in  MD[idS]:
                name, name2, c, c2, d, t = MD[idS][idS2]
                d /= (2*sqrt(2))                        
                d2 = MD2[idS][idS2][-2]
                d  = (alpha/100.0)*d + ((100.0-alpha)/(100.0))*d2
                
                if name == name2:
                    couples += [(True,d)]
                else:
                    couples += [(False,d)]
            random.shuffle(couples)                                                
            y += [couples]
       
        if len(y) == 0:
            continue
        
        
        ACC = []        
        for L in y :
            L.sort(key=lambda x: x[1])
            
            isIn = False
            for i in range(K):
                if L[i][0]:
                    isIn = True
            ACC += [isIn]
        
        successRate = 0
        for isIn in ACC:
            if isIn:
                successRate += 1 
        successRate /= len(ACC)
        
        
        
        if not(alpha in frameworkPlot):
            frameworkPlot[alpha] = {}
        if not(nameDS in frameworkPlot[alpha]):
            frameworkPlot[alpha][nameDS] = []
        frameworkPlot[alpha][nameDS] += [successRate] # "{:.2f}".format()

for alpha in frameworkPlot:
    for nameDS in frameworkPlot[alpha]:
        frameworkPlot[alpha][nameDS] = sum(frameworkPlot[alpha][nameDS])/len(frameworkPlot[alpha][nameDS])

alphaToScore = {}
for alpha in frameworkPlot:
    globalScore = 0
    for nameDS in frameworkPlot[alpha]:
        globalScore += frameworkPlot[alpha][nameDS]
    globalScore /= len(frameworkPlot[alpha])
    alphaToScore[alpha] = globalScore

with open("SFS_SIII_Score_Curve", "wb") as f:
    pickle.dump(alphaToScore, f)