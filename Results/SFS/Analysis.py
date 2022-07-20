import os
import pickle

import numpy as np
import matplotlib.pyplot as plt

with open("SFS_SI_Score_Curve", "rb") as f:
    alphaToScoreSI = pickle.load(f)

with open("SFS_SII_Score_Curve", "rb") as f:
    alphaToScoreSII = pickle.load(f)

with open("SFS_SIII_Score_Curve", "rb") as f:
    alphaToScoreSIII = pickle.load(f)

plt.style.use('seaborn')

Y_SI = []
Y_SII = []
Y_SIII = []

for alpha in range(0, 100):
    Y_SI    +=   [alphaToScoreSI[alpha]]
    Y_SII   +=   [alphaToScoreSII[alpha]]
    Y_SIII  +=   [alphaToScoreSIII[alpha]]


X = np.array([alpha/100.0 for alpha in range(0,100)])

Y_SI = np.array(Y_SI)
Y_SII = np.array(Y_SII)
Y_SIII = np.array(Y_SIII)

plt.plot(X, Y_SI, label='Scenario I')
plt.plot(X, Y_SII, label='Scenario II')
plt.plot(X, Y_SIII, label='Scenario III')


plt.ylabel('Score')
plt.xlabel(r'$\alpha$')
plt.legend()
plt.show()