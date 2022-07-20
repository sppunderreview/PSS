import os
import pickle

import numpy as np

from sklearn import metrics
from scipy import stats
import pandas as pd

import random


frameworks = ["heuristiqueSampleSize","heuristiqueJsonSize","prototypeJaccardAnonyme","GSA_Spectral","GSA_CFG_Spectral","GSA_GED_1","GSA_GED_1_L1","SMIT","AMalwareAndVariantDetectionMethod","SimilarityFunctionCallGraph","MutantX","asm2vecJ","gemini","AD","SAFEtorch","prototypeExtern","spectralSP"]

XPS = [("CV",["CV0V1","CV0V2","CV0V3", "CV1V2", "CV1V3", "CV2V3"]),("CO",["CO0O1","CO0O2","CO0O3", "CO1O2", "CO1O3", "CO2O3"]),("UV",["UV0V1","UV0V2","UV0V3", "UV1V2", "UV1V3", "UV2V3"]),("UO",["UO0O1","UO0O2","UO0O3", "UO1O2", "UO1O3", "UO2O3"]),("BV",["BV0V1","BV0V2","BV0V3", "BV1V2", "BV1V3", "BV2V3"]),("BO",["BO0O1","BO0O2","BO0O3", "BO1O2", "BO1O3", "BO2O3"])]


dataPoints = {}

# Collect optimization information among datasets
dictidSTooptim = {}

for framework in ["spectralSP"]:    
    for (nameDS, DS_Couple) in XPS:
        print(nameDS,framework)
        dictidSTooptim[nameDS] = {}
        
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
                    name, name2, optim , optim2 , d = t
                    dictidSTooptim[nameDS][idS] = optim
                    
        
# Computes correlations
for framework in frameworks:    
    dataPoints[framework] = {}

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
                        name, name2,_,_,d = t
                    optim  = dictidSTooptim[nameDS][idS]
                    optim2 = dictidSTooptim[nameDS][idS2]
                    couples += [(optim==optim2,d)]
                random.shuffle(couples)                                                                
                y += [couples]

        if len(y) == 0:
            continue
        



        # Rank-biserial correlation
        
        rankBiserialCorr = []
        for L in y :
            L.sort(key=lambda x: x[1])
            A = []
            B = []


            for i in range(len(L)):
                if L[i][0]:
                    A += [i]
                else:
                    B += [i]
            

            total = len(A)*len(B)
            supportH = 0
            dontSupportH = 0
            for x in A:
                for y in B:
                    if   x < y:
                        supportH += 1
                    elif y < x:
                        dontSupportH += 1

            rankBiserialCorr += [(supportH-dontSupportH)/total]
            
        rankBiserialCorr = np.array(rankBiserialCorr)
        meanBC = stats.describe(rankBiserialCorr).mean
        #print(framework, nameDS, finalDistrRankBiserialCorr.skewness,finalDistrRankBiserialCorr.kurtosis)
        stdE = stats.tstd(rankBiserialCorr)
        
        if meanBC < 0.16:
            T = "\\textbf{"+"{0:.2f}".format(meanBC) + "}"
        else:
            T = "{"+"{0:.2f}".format(meanBC) + "}"
            
        dataPoints[framework][nameDS] = T # ${("+ "{0:.3f}".format(stdE) + ")}$"

df = pd.DataFrame(dataPoints).transpose()


latex =  df.to_latex().replace("\\textbackslash ","\\").replace("\\$","$").replace("\\{","{").replace("\\}","}").replace("NaN ","? ")

latex = latex.replace("spectralSP", "\\hline\n{\\it \\SP}")
latex = latex.replace("GSA\_CFG\_Spectral ", "{\\it SCFG} ")
latex = latex.replace("GSA\_Spectral ", "{\\it SCG} ")
latex = latex.replace("AMalwareAndVariantDetectionMethod", "\\hline\n{\\it ISO}")
latex = latex.replace("SimilarityFunctionCallGraph", "{\\it CGC}")
latex = latex.replace("asm2vecJ", "\\hline\n{\\it Asm2vec} ")
latex = latex.replace("SAFEtorch", "{\\it SAFE } ")
latex = latex.replace("gemini", "{\\it Gemini } ")
latex = latex.replace("GSA\_GED\_1\_L1", "{\\it GED-Labels}")
latex = latex.replace("GSA\_GED\_1", "\\hline\n{\\it GED-0}")
latex = latex.replace("MutantX", "\\hline\n{\\it MutantX}")
latex = latex.replace("SMIT", "{\\it SMIT}")
latex = latex.replace("heuristiqueJsonSize", "$D_{size}$")
latex = latex.replace("heuristiqueSampleSize", "$B_{size}$")
latex = latex.replace("prototypeExtern", "\\hline\n{\\it FunctionSet}")
latex = latex.replace("prototypeJaccardAnonyme", "{\\it Shape}")
latex = latex.replace("AD", "{\\it $\\alpha$Diff } ")

print(latex)

