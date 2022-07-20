import os
import pickle

import numpy as np

from sklearn import metrics
import pandas as pd

import random

dictSimulation = {}

def simulation(N):
    global dictSimulation
    if N in dictSimulation:
        return dictSimulation[N]
    """
    M = 1000000
    D = [False for i in range(N-1)]
    D += [True]    
    total = 0
    for i in range(M):    
        random.shuffle(D)        
        if D[0]:
            total += 1"""
    dictSimulation[N] = 1/N
    return dictSimulation[N]

AVG = [] 

XPS = [("CV",["CV0V1","CV0V2","CV0V3", "CV1V2", "CV1V3", "CV2V3"]),("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UV",["UV0V1","UV0V2","UV0V3", "UV1V2", "UV1V3", "UV2V3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BV",["BV0V1","BV0V2","BV0V3", "BV1V2", "BV1V3", "BV2V3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]

frameworkPlot  = {}
frameworkPlot["Random"]  = {}

for (nameDS, DS_Couple) in XPS:
    y = []


    for nameXP  in DS_Couple:
        outputFile = "../../../spectralSP/"+nameXP+"_MD"

        if os.path.exists(outputFile) == False:
            continue

        with open(outputFile, "rb") as f:
            MD = pickle.load(f)

        for idS in MD["<>"]:
            couples = []
            
            for idS2 in  MD["<>"][idS]:
                t = MD["<>"][idS][idS2]
                
                if len(t) == 3:
                    name,name2,d = t 
                else:
                    name, name2, _ ,_ , d = t

                if name == name2:
                    couples += [(True,0)]
                else:
                    couples += [(False,0)]
            random.shuffle(couples)                                                
            y += [couples]

    if len(y) == 0:
        continue
    
    
    ACC = []        
    for L in y :
        N = len(L)
        ACC += [simulation(N)]

    successRate = sum(ACC)/len(ACC)        
    frameworkPlot["Random"][nameDS] =  "{:.2f}".format(successRate)
    AVG += [successRate]

print("Scenario II",sum(AVG)/len(AVG)) # 0.018064999999999953

df = pd.DataFrame(frameworkPlot).T
df.fillna(0, inplace=True)

print(df)

latex = df.to_latex()
print(latex)
