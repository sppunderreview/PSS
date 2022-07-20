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
    M = 100000
    D = [False for i in range(N-3)]
    for i in range(3):
        D += [True]
    
    total = 0
    for i in range(M):    
        random.shuffle(D)        
        if D[0] or D[1] or D[2]:
            total += 1
    dictSimulation[N] = total/M
    return dictSimulation[N]

AVG = [] 

XPS = ["CV","CO","UV","UO","BV","BO"]

frameworkPlot  = {}
frameworkPlot["Random"]  = {}


for nameDS in XPS:
    y = []
    
    outputFile = "../../../spectralSP/"+nameDS+"_MD"

    if os.path.exists(outputFile) == False:
        continue

    with open(outputFile, "rb") as f:
        MD = pickle.load(f)

    for idS in MD:
        couples = []
        
        for idS2 in  MD[idS]:
            name, name2, c, c2, d, t = MD[idS][idS2]
            if idS == idS2:
                print("ALERT")
            if name == name2:
                couples += [(True,0)]
            else:
                couples += [(False,0)]
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

print("Scenario III",sum(AVG)/len(AVG)) # 0.07609166666666667

# (0.07609166666666667 + 0.05326833333333328 + 0.10368333333333347)/3
df = pd.DataFrame(frameworkPlot).T
df.fillna(0, inplace=True)

print(df)

latex = df.to_latex()
print(latex)