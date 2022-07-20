import os
import pickle

import numpy as np

from sklearn import metrics
import pandas as pd

import random
from math import sqrt

XPS = [("CV",["CV0V1","CV0V2","CV0V3", "CV1V2", "CV1V3", "CV2V3"]),("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UV",["UV0V1","UV0V2","UV0V3", "UV1V2", "UV1V3", "UV2V3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BV",["BV0V1","BV0V2","BV0V3", "BV1V2", "BV1V3", "BV2V3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]

K = 1

frameworkPlot = {}

for (nameDS, DS_Couple) in XPS:        
    for nameXP  in DS_Couple:
        outputFile = "../../spectralSP/"+nameXP+"_MD"

        if os.path.exists(outputFile) == False:
            continue

        with open(outputFile, "rb") as f:
            MD = pickle.load(f)

        with open("../../prototypeExtern/"+nameXP+"_MD", "rb") as f:
            MD2 = pickle.load(f)
        
        for alpha in range(0, 100):
            y = []
            
            for idS in MD["->"]:
                couples = []
                
                for idS2 in  MD["<>"][idS]:
                    t = MD["<>"][idS][idS2]
                    if len(t) == 3:
                        name,name2,d = t 
                    else:
                        name, name2, _ ,_ , d = t
                    d /= (2*sqrt(2))
                    d2 = MD2["<>"][idS][idS2][-1]
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

with open("SFS_SII_Score_Curve", "wb") as f:
    pickle.dump(alphaToScore, f)