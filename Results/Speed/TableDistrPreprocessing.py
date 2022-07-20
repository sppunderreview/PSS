import os
import pickle

import numpy as np

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

frameworks = ["GSA_Spectral","GSA_CFG_Spectral","prototypeSpectral9"]
XPS = ["CV","CO","UV","UO","BV","BO"]

frameworksPlot = {}

for framework in frameworks:
    frameworksPlot[framework] = {}    
    for nameDS in XPS:
        y = []
        
        outputFile = "../../"+framework+"/A_"+nameDS
        if os.path.exists(outputFile) == False:
            continue

        with open(outputFile, "rb") as f:
            D = pickle.load(f)

        if os.path.exists(outputFile+"_C"):
            with open(outputFile+"_C", "rb") as f:
                DC = pickle.load(f)
                for x in DC:
                    D[x] = DC[x]
            
        for idS in D:
            y += [D[idS][-1]]
        frameworksPlot[framework][nameDS] = y
        

table = {}
for framework in frameworksPlot:
    table[framework] = {}
    AVG = []
    totalY = []
    for nameDS in frameworksPlot[framework]:
        totalY += frameworksPlot[framework][nameDS]
        AVG += [sum(frameworksPlot[framework][nameDS])/len(frameworksPlot[framework][nameDS])]
    
    print(len(totalY))
    minF = min(totalY)
    maxF = max(totalY)
    totalF = sum(totalY)
    avgF = sum(AVG)/len(AVG)
    
    table[framework]["Total"] = totalF#formatTime(totalF)
    table[framework]["Maximum"] = formatTime(maxF)
    table[framework]["Weighted Average"] = formatTime(avgF)
    

df = pd.DataFrame(table).T
df.fillna(0, inplace=True)

print(df)

latex =  df.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

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

