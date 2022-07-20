import numpy as np
import pickle 

LC =  ["BSIZE","DSIZE","SHAPE","GSA","MUTANTX","PSS","FUNCTIONSET", "Random"]
for nEmb in LC:
    LATEX = ""
    for nQBI in [ "QB","QB40k", "QB20K"]:
        RESULTS = []
        for pId in range(40):
            inputFile = "R/R_"+nQBI+"_"+nEmb+"_"+str(pId)                
            with open(inputFile, "rb") as f:
                RESULTS += pickle.load(f)
        ACC = []
        for i in range(1,len(RESULTS), 3):
            ACC += [RESULTS[i]]
        score = sum(ACC)/len(ACC)
        
        print(len(ACC))

        LATEX +=  "%.5f" % (score) + " & "

    print(nEmb)    
    print(LATEX)
    
