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


frameworksSelected = ["prototypeJaccardAnonyme","GSA_Spectral","GSA_CFG_Spectral","MutantX","GSA_GED_1","gemini","SAFEtorch","prototypeExtern","GSA_GED_1_L1","SimilarityFunctionCallGraph","spectralSP"]

frameworksSelectedInOrder = []
for f in frameworks:
    if f in frameworksSelected:
        frameworksSelectedInOrder += [f]
        
frameworks = frameworksSelectedInOrder

XPS = [("V",["BV","CV","UV"]) ,("O",["BO","CO","UO"])]

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
    
    for (nameXP, LDS) in XPS:
        y = []
        
        with open("../../"+framework+"/MD4"+nameXP, "rb") as f:
            MDT = pickle.load(f)
        
        totalS = 0
        for DS in LDS:
            with open("../../"+framework+"/"+DS+"_MD", "rb") as f:
                MD3 = pickle.load(f)
                for idS in MD3:
                    totalS += 1
                    MDT[DS][idS][DS] =  {}            
                    for idS2 in MD3[idS]:                
                            MDT[DS][idS][DS][idS2] =  MD3[idS][idS2]

        for DS in MDT:
            w = totalS/(len(MDT[DS])*3)
            for idS in MDT[DS]:
                couples = []
                for DS2 in MDT[DS][idS]:
                    for idS2 in MDT[DS][idS][DS2]:
                        name, name2, c, c2, d, t = MDT[DS][idS][DS2][idS2]
                        
                        if name == name2 and DS == DS2 and idS == idS2:
                            continue
                        couples += [t]
                y += [(couples,  w)]
                
        if len(y) == 0:
            continue
            
        
        avgCS = 0
        for (l,w) in y:
            avgCS += sum(l)
        avgCS /= len(y)
        
        avgSC = 0
        n = 0
        for (l,w) in y:
            avgSC += sum(l)
            n += len(l)
        avgSC /= n 
        
        total = 0
        minCS = 100000
        minSC = 100000
        maxCS = 0
        maxSC = 0
        for (l,w) in y:            
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
    
    globalAvgCS /= 2
    globalAvgSC /= 2

    frameworksData[framework]["Total"] = formatTime(globalTotal)
    frameworksData[framework]["Clone Search (min,max)"] = "(" + formatTime(globalMinCS) +"," + formatTime(globalMaxCS) + ")"
    frameworksData[framework]["Similarity Check max)"] = "(" + formatTime(globalMinSC) +"," + formatTime(globalMaxSC) + ")"


dfSIVSpeed = pd.DataFrame(frameworksData).T
dfSIVSpeed.fillna(0, inplace=True)

print(dfSIVSpeed)

latex =  dfSIVSpeed.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

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


