from LoadBase import loadGraphs
import networkx as nx 

import time
import os
import pickle

def jaccardAnonyme(g1,g2):
    n1 = g1.number_of_nodes()
    n2 = g2.number_of_nodes()
    e1 = g1.number_of_edges()
    e2 = g2.number_of_edges()
    
    jaccard = (min(n1,n2)/max(n1,n2))*(min(e1,e2)/max(e1,e2))
    return 1 - jaccard

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
        fTotal[DS] = loadGraphs(O) 

    minRun(L, fTotal, nameXP, jaccardAnonyme)

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