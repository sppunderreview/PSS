import pickle
import os

import numpy as np
import pandas as pd

import random

frameworks = ["spectralA", "spectralB", "spectralSP"]


frameworksSelected = ["prototypeJaccardAnonyme","GSA_Spectral","GSA_CFG_Spectral","MutantX","GSA_GED_1","gemini","SAFEtorch","prototypeExtern","GSA_GED_1_L1","SimilarityFunctionCallGraph","spectralSP", "spectralA", "spectralB"]

frameworksSelectedInOrder = []
for f in frameworks:
    if f in frameworksSelected:
        frameworksSelectedInOrder += [f]
        
frameworks = frameworksSelectedInOrder

XPS = [("V",["BV","CV","UV"]) ,("O",["BO","CO","UO"])]
K = 1

frameworkPlot = {}

for framework in frameworks:    
    #frameworkPlot[framework] = {}

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
                        
                        if name == name2 and DS == DS2 and idS == idS2 :
                            continue
                        couples += [(name == name2,d)]
                random.shuffle(couples)
                y += [(couples,  w)]
                
        if len(y) == 0:
            continue
        

        ACC = []        
        for L, w in y :
            L.sort(key=lambda x: x[1])
            
            isIn = 0
            for i in range(K):
                if L[i][0]:
                    isIn = 1
            ACC += [isIn]
        
        successRate = sum(ACC)/len(ACC)            

        if not(framework in frameworkPlot):
            frameworkPlot[framework] = {}
        frameworkPlot[framework][nameXP] =  successRate

for f in frameworkPlot:
    frameworkPlot[f]["Average"] = (frameworkPlot[f]["V"] +  frameworkPlot[f]["O"]) / 2
    frameworkPlot[f]["V"] = "{:.2f}".format(frameworkPlot[f]["V"])
    frameworkPlot[f]["O"] = "{:.2f}".format(frameworkPlot[f]["O"])
    frameworkPlot[f]["Average"] = "{:.2f}".format(frameworkPlot[f]["Average"])
    


df = pd.DataFrame(frameworkPlot).T
df.fillna(0, inplace=True)

#print(df)

latex = df.to_latex()
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

