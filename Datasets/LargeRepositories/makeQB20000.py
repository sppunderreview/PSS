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
	

Q20k = []
B20k = []
I20k = []
QNames20k = deepcopy(QNames)

namesRemoved = {}
for n in nameToIdS:
	if random() < 0.75:
		namesRemoved[n] = True
		if n in QNames20k:
			del QNames20k[n]
		
for q in Q:
	if (idSToName[q] in namesRemoved) == False:
		Q20k += [q]

for b in B:
	if (idSToName[b] in namesRemoved) == False:
		B20k += [b]
		
for i in I:
	if (idSToName[i] in namesRemoved) == False:
		I20k += [i]

print(len(Q20k))
print(len(B20k))
print(len(I20k))

"""
12083
21113
9030
"""

with open("QB20k", "wb") as f:
	pickle.dump([Q20k,B20k,I20k,QNames20k],f)
