import numpy as np
from Prototype import computeEmbedding

import time
import os
import pickle

def distanceSP10(E1,E2):   
    k = min(E1[1],E2[1])
    k2 =  min(E1[-2],E2[-2])
    PA = np.linalg.norm(E1[0][:k] - E2[0][:k])
    PB =  np.linalg.norm(E1[2][:k2] - E2[2][:k2])    
    return PA + PB

def distanceA(E1,E2):
    k = min(E1[1],E2[1])
    PA = np.linalg.norm(E1[0][:k] - E2[0][:k])
    return PA
    
def distanceB(E1,E2):
    k2 =  min(E1[-2],E2[-2])
    PB =  np.linalg.norm(E1[2][:k2] - E2[2][:k2])
    return PB

def minRun(L, fTotal, outputFile,dist):
    MD = {}    
    for (O, DS) in L:        
        MD[DS] = {}        
        for (idS,path,compilerOption,name, pathJson) in O:
            MD[DS][idS] = {}
            
            for (O2, DS2) in L: 
                if DS == DS2:
                    continue
                MD[DS][idS][DS2] = {}
                for (idS2,path2,compilerOption2,name2, pathJson2) in O2:
                    start = time.time()
                    d = dist(fTotal[DS][str(idS)], fTotal[DS2][str(idS2)])
                    elpased = time.time()-start
                    MD[DS][idS][DS2][idS2] = (name,name2,compilerOption,compilerOption2,d,elpased)  
    with open(outputFile, "wb") as f:
        pickle.dump(MD, f)
        
def RunAll(L, nameXP):
    fTotal = {}
    for (O,DS) in L:
        with open("A_"+DS, "rb") as f:
            fTotal[DS] = pickle.load(f)    
        if DS == "BO":        
            with open("A_"+DS+"_C", "rb") as f:
                fTotalCorrect = pickle.load(f)
            for x in fTotalCorrect:
                fTotal[DS][x] = fTotalCorrect[x]
            
    minRun(L, fTotal, "../spectralSP/"+nameXP, distanceSP10)
    minRun(L, fTotal, "../spectralA/"+nameXP, distanceA)
    minRun(L, fTotal, "../spectralB/"+nameXP, distanceB)
    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")

    from makeBenchBO import readAllSamples as allBO
    from makeBenchBV import readAllSamples as allBV
    from makeBenchCV import readAllSamples as allCV
    from makeBenchCO import readAllSamples as allCO
    from makeBenchUO import readAllSamples as allUO
    from makeBenchUV import readAllSamples as allUV
    
    RunAll([(allBO(),"BO"),(allUO(),"UO"),(allCO(),"CO")], "MD4O")
    RunAll([(allBV(),"BV"),(allUV(),"UV"),(allCV(),"CV")], "MD4V")
    