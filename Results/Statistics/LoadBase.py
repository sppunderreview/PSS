import json
import networkx as nx 
 
def loadGraphs(inputs):
    
    N = []
    E = []
    M = []
    TM = []
    
    B = 0
    
    for (idS,path,compilerOption,name, pathJson) in inputs:
        with open(pathJson) as f:
          data = json.load(f)
        
        
        n = 0
        e = 0
        totalM = 0
        
        B += 1
        for f in data["functions"]:
            n += 1
            
            m = 0
            for nextF in f["call"]:
                e += 1            
            for b in f["blocks"]:                 
                 m += 1
                 totalM += 1
                 for nextB in b["call"]:
                    pass 
            
            M += [m]
        if n == 10000:
            print(idS,name, compilerOption)
        N += [n]
        E += [e]
        TM += [totalM]
    B -= 1
    return N,E,M,TM,B