import pickle
from copy import deepcopy
from random import random

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
	
Q40k = []
B40k = []
I40k = []
QNames40k = deepcopy(QNames)

namesRemoved = {}
for n in nameToIdS:
	if random() < 0.5:
		namesRemoved[n] = True
		if n in QNames40k:
			del QNames40k[n]
		
for q in Q:
	if (idSToName[q] in namesRemoved) == False:
		Q40k += [q]

for b in B:
	if (idSToName[b] in namesRemoved) == False:
		B40k += [b]
		
for i in I:
	if (idSToName[i] in namesRemoved) == False:
		I40k += [i]

print(len(Q40k))
print(len(B40k))
print(len(I40k))

"""
24983
42646
17663
"""

with open("QB40k", "wb") as f:
	pickle.dump([Q40k,B40k,I40k,QNames40k],f)
