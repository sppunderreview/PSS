import os
import pickle

import numpy as np

from sklearn import metrics
import pandas as pd

import random

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
    
    for L in y :
        N = len(L)
        break
    successRate = 3/N      
    frameworkPlot["Random"][nameDS] =  "{:.2f}".format(successRate)
    AVG += [successRate]

print("Scenario III",sum(AVG)/len(AVG)) # 0.02618818711195772

# (0.03511500000000004 + 0.018064999999999953 + 0.026188187111957698)/3
df = pd.DataFrame(frameworkPlot).T
df.fillna(0, inplace=True)

print(df)

latex = df.to_latex()
print(latex)