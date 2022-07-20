import os
import pickle

import numpy as np

import matplotlib.pyplot as plt
from sklearn import metrics
import pandas as pd

import random

def formatTime(s):
    
    h = int(s / 3600)
    m = int((s - (h*3600))/ 60)
    s = int(s % 60)
   
    if h > 0 and m > 0:    
        return str(h)+"h"+str(m)+"m"
    if m > 0:
        return str(m)+"m"+str(s)+"s"
    return str(s)+"s"

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
    frameworksData[framework]["Clone Search avg (min,max)"] = formatTime(globalAvgCS) +  " (" + formatTime(globalMinCS) +"," + formatTime(globalMaxCS) + ")"
    frameworksData[framework]["Similarity Check avg (max)"] = formatTime(globalAvgSC) +  " (" + formatTime(globalMaxSC) + ")"


dfSIIISpeed = pd.DataFrame(frameworksData).T
dfSIIISpeed.fillna(0, inplace=True)

print(dfSIIISpeed)

latex =  dfSIIISpeed.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

latex = latex.replace("spectralSP", "\\hline\n{\\it \\SP}")
latex = latex.replace("GSA\_CFG\_Spectral ", "{\\it S CFG} (adapted)")
latex = latex.replace("GSA\_Spectral ", "{\\it S Call Graph} (adapted)")
latex = latex.replace("AMalwareAndVariantDetectionMethod", "\\hline\n{\\it ISO}")
latex = latex.replace("SimilarityFunctionCallGraph", "{\\it CGC}")
latex = latex.replace("asm2vecJ", "\\hline\n{\\it Asm2vec} (adapted)")
latex = latex.replace("SAFEtorch", "{\\it SAFE } (adapted)")
latex = latex.replace("gemini", "{\\it Gemini } (adapted)")
latex = latex.replace("GSA\_GED\_1\_L1", "{\\it GED-Labels}")
latex = latex.replace("GSA\_GED\_1", "\\hline\n{\\it GED-0}")
latex = latex.replace("MutantX", "\\hline\n{\\it MutantX}")
latex = latex.replace("SMIT", "{\\it SMIT}")
latex = latex.replace("heuristiqueJsonSize", "$D_{size}$")
latex = latex.replace("heuristiqueSampleSize", "$B_{size}$")
latex = latex.replace("prototypeExtern", "\\hline\n{\\it FunctionSet}")
latex = latex.replace("prototypeJaccardAnonyme", "{\\it Shape}")
latex = latex.replace("AD", "{\\it $\\alpha$Diff } (adapted)")

print(latex)


