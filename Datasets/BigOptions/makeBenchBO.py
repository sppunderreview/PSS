#!/usr/bin/python3

# ? ?
# 2021
# ?

def readAllSamples():
	L = []
	with open("/home/?/Documents/Travail/?/BigOptions/samples.txt", "r") as f:
		nbP = int(f.readline().strip())
		for i in range(nbP):
			idS = int(f.readline().strip()) 
			path = f.readline().strip()
			name = path.split("/")[-1]			
			pathJson = "/home/?/Documents/Travail/?/BigOptions/json/"+str(idS)+".tmp0.json"
			compilerOption = path.split("/")[-2][-2:]
			L += [(idS,path,compilerOption,name, pathJson)]
	return L
	

def selectSamples(option):
	L = readAllSamples()
	LS = []
	for (idS,p,o,n,pJ) in L:
		if o == option:
			LS += [(idS,p,o,n,pJ)]
	return LS
	
def benchmarkBO(o0,o1):	
	return (selectSamples(o0),selectSamples(o1))
