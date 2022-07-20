import pickle

import numpy as np
import pandas as pd

import random


XPS = [("V",["BV","CV","UV"]) ,("O",["BO","CO","UO"])]
K = 1

for (nameXP, LDS) in XPS:
    y = []
    
    with open("../../../spectralSP/MD4"+nameXP, "rb") as f:
        MDT = pickle.load(f)
    
    totalS = 0
    for DS in LDS:
        with open("../../../spectralSP/"+DS+"_MD", "rb") as f:
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
        areClones = 0
        for (l,d) in L:
            if l:
                areClones += 1

        ACC += [areClones/len(L)]
    
    successRate = sum(ACC)/len(ACC)            

    print(nameXP, successRate)



