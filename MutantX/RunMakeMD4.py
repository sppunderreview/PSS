import numpy as np
import time
import os
import pickle

def distanceE(E1,E2):
    return np.linalg.norm(E1 - E2)       
    
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
        fTotal[DS] = {}
        for idS in range(len(O)):
            with open( "./A/"+DS+"/"+str(idS), "rb") as f:
                embed, elapsed = pickle.load(f)
            fTotal[DS][str(idS)] = embed

    minRun(L, fTotal, nameXP, distanceE)
    
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