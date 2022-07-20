import pickle

import matplotlib.pyplot as plt
import numpy as np

from math import log10

import matplotlib.font_manager as fm# Rebuild the matplotlib font cache

plt.style.use('seaborn')



with open("QB", "rb") as f:
	E = pickle.load(f) # [Q,B,I,QNames]
	Q = E[0]
	B = E[1]
	I = E[2]
	QNames = E[3]

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

# Histogram of Bsize
with open("BSIZE", "rb") as f:
	BSIZE =  pickle.load(f)
X = np.array([log10(BSIZE[idS]/1024) for idS in B])

print(sum([(BSIZE[idS]/(1024*1024*1024)) for idS in B]), "Gigabytes")

plt.hist(X, density=False, bins=FQBins(X)) 
plt.ylabel('Counts')
plt.xlabel('log10(Ko)')
#saveFigure("BSIZEDistr", 10, 10)

# Histogram of Number of functions
with open("SHAPE", "rb") as f:
	SHAPE =  pickle.load(f)
X = np.array([log10(SHAPE[idS][0]) for idS in B])
plt.hist(X, density=False, bins=FQBins(X)) 
plt.ylabel('Counts')
plt.xlabel('log10(n)')
#saveFigure("NDistr", 10, 10)


