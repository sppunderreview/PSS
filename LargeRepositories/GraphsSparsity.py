import pickle

import matplotlib.pyplot as plt
import numpy as np

with open("QB", "rb") as f:
	E = pickle.load(f) # [Q,B,I,QNames]
	Q = E[0]
	B = E[1]
	I = E[2]
	QNames = E[3]

def saveFigure(name, w, h):
    fig = plt.gcf()
    fig.set_size_inches(w, h)
    fig.savefig(name+'.png', dpi=100)
    plt.clf()

plt.style.use('seaborn')


# Histogram of Number of functions
with open("SHAPE", "rb") as f:
	SHAPE =  pickle.load(f)
X = np.array([SHAPE[idS][0] for idS in B])
Y = np.array([SHAPE[idS][1]/SHAPE[idS][0] for idS in B])
plt.scatter(X, Y, s=0.1) 
plt.xlabel('n')
plt.ylabel('d')
saveFigure("Sparcity", 10, 10)

