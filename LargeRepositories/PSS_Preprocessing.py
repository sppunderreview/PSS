import pickle

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

from math import log10

plt.style.use('seaborn')


with open("idSToName", "rb") as f:
	idSToName = pickle.load(f)

with open("nameToIdS", "rb") as f:
	nameToIdS = pickle.load(f)

with open("QB", "rb") as f:
	E = pickle.load(f) # [Q,B,I,QNames]
	Q = E[0]
	B = E[1]
	I = E[2]
	QNames = E[3]
	
with open("preprocessQPSS", "rb") as f:
	preprocessQPSS = pickle.load(f)

with open("preprocessQSCG", "rb") as f:
	preprocessQSCG = pickle.load(f)
	
# Ajust time with preprocessing
for idS in Q:
	if preprocessQPSS[idS][1] > 60000:
		preprocessQPSS[idS] = [preprocessQPSS[idS][0] * 6, preprocessQPSS[idS][1]]
	elif preprocessQPSS[idS][1] > 50000:
		preprocessQPSS[idS] = [preprocessQPSS[idS][0] * 3, preprocessQPSS[idS][1]]

for idS in Q:
	if preprocessQSCG[idS][1] > 60000:
		preprocessQSCG[idS] = [preprocessQSCG[idS][0] * 6, preprocessQSCG[idS][1]]
	elif preprocessQSCG[idS][1] > 50000:
		preprocessQSCG[idS] = [preprocessQSCG[idS][0] * 3, preprocessQSCG[idS][1]]
		

def FQBins(X):
	q25, q75 = np.percentile(X, [25, 75])
	bin_width = 2 * (q75 - q25) * len(X) ** (-1/3)
	if bin_width == 0 or (bin_width < 1 and type(X[0]) == int):
		return  round(X.max() - X.min())
	return round((X.max() - X.min()) / bin_width) # Freedman–Diaconis number of bins
    
def saveFigure(name, w, h):
    fig = plt.gcf()
    fig.set_size_inches(w, h)
    fig.savefig(name+'.png', dpi=100)
    plt.clf()

X = np.array([preprocessQPSS[idS][1] for idS in Q])
Y = np.array([preprocessQSCG[idS][0] for idS in Q])

a, b, c = np.polyfit(X, Y, 2)
labelPoly = str(a)+"n²+"+str(b)+"n+"+str(c)
P = np.poly1d([a,b,c])
XF = np.linspace(min(X), max(X), 1000)
YF = P(XF) 

regression = sm.OLS(Y, [P(x) for x in X]).fit()
print(regression.summary())
labelPoly = "r^2=%.3f" % (regression.rsquared) 


plt.plot(XF, YF, color='r', alpha=0.1, label=labelPoly)
plt.scatter(X, Y, s=0.2)
plt.ylabel('seconds')
plt.xlabel('n')
plt.legend()
plt.show()


# Total PSS Q
print("PSS", sum ([preprocessQPSS[idS][1] for idS in Q]), "s")
print("SCG", sum ([preprocessQSCG[idS][1] for idS in Q]), "s")

# Total PSS B
print("PSS", sum ([preprocessQPSS[idS][1] for idS in B]), "s")
print("SCG", sum ([preprocessQSCG[idS][1] for idS in B]), "s")

