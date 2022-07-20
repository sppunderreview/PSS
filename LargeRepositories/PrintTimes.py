import numpy as np
import pickle 

with open("preprocessQPSS", "rb") as f:
	preprocessQPSS = pickle.load(f)

with open("preprocessQSCG", "rb") as f:
	preprocessQSCG = pickle.load(f)

# Ajust time with preprocessing
for idS in preprocessQPSS:
	if preprocessQPSS[idS][1] > 60000:
		preprocessQPSS[idS] = [preprocessQPSS[idS][0] * 6, preprocessQPSS[idS][1]]
	elif preprocessQPSS[idS][1] > 50000:
		preprocessQPSS[idS] = [preprocessQPSS[idS][0] * 3, preprocessQPSS[idS][1]]

for idS in preprocessQSCG:
	if preprocessQSCG[idS][1] > 60000:
		preprocessQSCG[idS] = [preprocessQSCG[idS][0] * 6, preprocessQSCG[idS][1]]
	elif preprocessQSCG[idS][1] > 50000:
		preprocessQSCG[idS] = [preprocessQSCG[idS][0] * 3, preprocessQSCG[idS][1]]	

LC =  ["SHAPE","BSIZE","DSIZE","GSA","MUTANTX","PSS","FUNCTIONSET"]
for nEmb in LC:
    LATEX = ""
    for nQBI in [ "QB","QB40k", "QB20K"]:
        with open(nQBI, "rb") as f:
            E = pickle.load(f) # [Q,B,I,QNames]
            Q = E[0]    
        outputFile = "ESC/ESC_"+nQBI+"_"+nEmb
        with open(outputFile, "rb") as f:
            ESC = pickle.load(f)
            
        T = [ESC[idS] for idS in ESC]
        avgT = sum(T)/len(T)
        
        if nEmb == "PSS":
            P = []
            for idS in Q:
                P += [preprocessQPSS[idS][0]]
            PMeans = sum(P)/len(P)
        elif nEmb == "GSA":
            P = []
            for idS in Q:
                P += [preprocessQSCG[idS][0]]
            PMeans = sum(P)/len(P)
        else:
            PMeans = 0

        LATEX +=  "%.2f" % (avgT+PMeans) + " & "
        LATEX +=  "%.2f" % PMeans + " & "
        LATEX +=  "%.2f" % avgT + " & "
        
    print(nEmb)    
    print(LATEX)
    
