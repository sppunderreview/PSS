import numpy as np
import pickle 

import matplotlib.pyplot as plt
import statsmodels.api as sm


plt.style.use('seaborn')


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

LC =  [("BSIZE","Bsize"),("DSIZE","Dsize"),("SHAPE","Shape"),("GSA","SCG"),("MUTANTX","MutantX-S"),("FUNCTIONSET","FunctionSet"),("PSS","PSS")]
for (nEmb,namePrint) in LC:
    Y = []
    for nQBI in ["QB20K","QB40k","QB"]:
        with open(nQBI, "rb") as f:
            E = pickle.load(f) # [Q,B,I,QNames]
            Q = E[0]    
        outputFile = "ESC/ESC_"+nQBI+"_"+nEmb
        with open(outputFile, "rb") as f:
            ESC = pickle.load(f)
        """
        T = [ESC[idS] for idS in ESC]
        avgSC = sum(T)/len(T)
        
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
            PMeans = 0"""
        
        T = []
        for idS in Q:
            if nEmb == "PSS":
                T += [preprocessQPSS[idS][0] + ESC[idS] ]
            elif nEmb == "GSA":
                T += [preprocessQSCG[idS][0] + ESC[idS] ]
            else:
                T += [  ESC[idS]  ]
        
        avgTotal = sum(T)/len(T)
        Y += [ avgTotal ]
        
    X = [21113, 42648, 84992]    
    
    print(nEmb,X,Y)
    if nEmb == "BSIZE":
        sc = plt.scatter(X, Y, label =namePrint, color="grey") 
    else:
        sc = plt.scatter(X, Y, label =namePrint) 
    colorNEMB = sc.get_facecolors()[0].tolist()
    
    a, b = np.polyfit(X, Y, 1)
    #labelPoly = str(a)+"n+"+str(b)
    P = np.poly1d([a,b])
    
    FAR_ENOUGH = 2000000
    X += [FAR_ENOUGH]
    Y += [P(FAR_ENOUGH)]    
    plt.scatter([FAR_ENOUGH], [P(FAR_ENOUGH)], color=colorNEMB, marker= "^")         
    XF = np.linspace(0, max(X), 1000)
    YF = P(XF) 
    regression = sm.OLS(Y, [P(x) for x in X]).fit()
    print (namePrint, regression.rsquared)    
    plt.plot(XF, YF, color=colorNEMB, alpha=0.5)

plt.ylabel('Time per clone search')
plt.xlabel('Repostory size')
plt.legend()
plt.show()
#saveFigure("NDistr", 10, 10)