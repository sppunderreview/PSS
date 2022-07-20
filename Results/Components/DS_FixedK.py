import os
import pickle

import numpy as np

from sklearn import metrics
import pandas as pd

import random

frameworks = ["spectralA", "spectralB", "spectralSP"]

XPS = [("CV",["CV0V1","CV0V2","CV0V3", "CV1V2", "CV1V3", "CV2V3"]),("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UV",["UV0V1","UV0V2","UV0V3", "UV1V2", "UV1V3", "UV2V3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BV",["BV0V1","BV0V2","BV0V3", "BV1V2", "BV1V3", "BV2V3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]

K = 1

frameworkPlot = {}


for framework in frameworks:    

    for (nameDS, DS_Couple) in XPS:
        y = []
        
        for nameXP  in DS_Couple:
            outputFile = "../../"+framework+"/"+nameXP+"_MD"

            if os.path.exists(outputFile) == False:
                continue

            with open(outputFile, "rb") as f:
                MD = pickle.load(f)

            for idS in MD["->"]:
                couples = []
                
                for idS2 in  MD["->"][idS]:
                    t = MD["->"][idS][idS2]
                    
                    if len(t) == 3:
                        name,name2,d = t 
                    else:
                        name, name2, _ ,_ , d = t

                    if name == name2:
                        couples += [(True,d)]
                    else:
                        couples += [(False,d)]
                random.shuffle(couples)
                y += [couples]
                
            for idS in MD["<-"]:
                couples = []
                
                for idS2 in  MD["<-"][idS]:
                    t = MD["<-"][idS][idS2]
                    
                    if len(t) == 3:
                        name,name2,d = t 
                    else:
                        name, name2, _ ,_ , d = t

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
       
        
        if not(framework in frameworkPlot):
            frameworkPlot[framework] = {}
        frameworkPlot[framework][nameDS] =  successRate # "{:.2f}".format()


dfSI = pd.DataFrame(frameworkPlot).T
dfSI.fillna(0, inplace=True)

frameworkPlot = {}


for framework in frameworks:    
    for (nameDS, DS_Couple) in XPS:
        y = []
        
        for nameXP  in DS_Couple:
            outputFile = "../../"+framework+"/"+nameXP+"_MD"

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
            
        if not(framework in frameworkPlot):
            frameworkPlot[framework] = {}
        frameworkPlot[framework][nameDS] =  successRate


dfSII = pd.DataFrame(frameworkPlot).T
dfSII.fillna(0, inplace=True)

frameworkPlot = {}
XPS = ["CV","CO","UV","UO","BV","BO"]

for framework in frameworks:    
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
                
                if name == name2:
                    couples += [(True,d)]
                else:
                    couples += [(False,d)]
            y += [couples]
                
        if len(y) == 0:
            continue
        
        ACC = []        
        for L in y :
            random.shuffle(L)
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
                    
        if not(framework in frameworkPlot):
            frameworkPlot[framework] = {}
        frameworkPlot[framework][nameDS] =  successRate # "{:.2f}".format(successRate)


dfSIII = pd.DataFrame(frameworkPlot).T
dfSIII.fillna(0, inplace=True)

dataTable = {}

for framework in frameworkPlot:
    dataTable[framework] = {}
    
    
    successRateByDS = {}
    for nameDS in XPS:
        if not (nameDS in successRateByDS):
            successRateByDS[nameDS] = {}
        successRateByDS[nameDS] = dfSI._get_value(framework, nameDS)   + dfSII._get_value(framework, nameDS)  + dfSIII._get_value(framework, nameDS)  
        dataTable[framework][nameDS] = "{0:.2f}".format(successRateByDS[nameDS]/3)        
        
dfScenario = pd.DataFrame(dataTable).T
dfScenario.fillna(0, inplace=True)

print(dfScenario)

latex =  dfScenario.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

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


