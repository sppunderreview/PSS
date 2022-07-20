import numpy as np
import time

from Prototype import extractCallGraphs, functionCallSimilarity

from multiprocessing import Process
import pickle

import random

def similarityAll(functionsData, graphPPreds, graphPSuccs, programsNE, DS, DS2, pS, pT):
    return functionCallSimilarity(functionsData[DS][str(pS)], graphPPreds[DS][str(pS)], graphPSuccs[DS][str(pS)], programsNE[DS][str(pS)], functionsData[DS2][str(pT)], graphPPreds[DS2][str(pT)], graphPSuccs[DS2][str(pT)], programsNE[DS2][str(pT)])


def loadEverything(L):

    fDTotal = {}
    gPPresdTotal = {}
    gPSuccsTotal = {}
    pNETotal = {}

    for (O,DS) in L:
        functionsDataS, graphPPredsS, graphPSuccsS, programsSNE = extractCallGraphs(O)
        fDTotal[DS] = functionsDataS
        gPPresdTotal[DS] = graphPPredsS
        gPSuccsTotal[DS] = graphPSuccsS
        pNETotal[DS] = programsSNE

    return fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal


def run(nameXP, L, idP, maxID,fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal):
    random.seed(10)

    outputFile = "MD4C"+nameXP+"_"+str(idP)+".txt"

    tasks = []
    for (O, DS) in L:
        for (idS,path,compilerOption,name, pathJson) in O:
            for (O2, DS2) in L:
                if DS == DS2:
                    continue
                if not("BO" in [DS,DS2]):
                    continue
                for (idS2,path2,compilerOption2,name2, pathJson2) in O2:
                    tasks += [(DS,idS,DS2,idS2,name,name2,compilerOption,compilerOption2)]


    random.shuffle(tasks)

    i = 0
    for (DS,idS,DS2,idS2,name,name2,compilerOption,compilerOption2) in tasks:
        if i % maxID == idP:
            print(idP, idS,idS2,DS,DS2)
            start = time.time()
            d = 1 - similarityAll(fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal, DS, DS2, idS, idS2)
            el = time.time()-start
            with open(outputFile, "a") as f:
                f.write(str([DS,idS,DS2,idS2,name,name2,compilerOption,compilerOption2,d,el])+"\n")
        i += 1

if __name__ == '__main__':
    import sys
    sys.path.insert(0, "/home/?/GCoreutilsOptions")
    sys.path.insert(0, "/home/?/GUtilsOptions")
    sys.path.insert(0, "/home/?/GBigOptions")

    from correctBenchBO import readToCorrect
    from makeBenchCO import readAllSamples as allCO
    from makeBenchUO import readAllSamples as allUO

    L = [(readToCorrect(),"BO"),(allUO(),"UO"),(allCO(),"CO")]
    fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal =  loadEverything(L)

    P = 40
    PL = []
    for i in range(P):
        p = Process(target=run, args=("O",L,i,P,fDTotal, gPPresdTotal, gPSuccsTotal, pNETotal))
        PL += [p]
        p.start()

    for i in range(P):
        PL[i].join()

