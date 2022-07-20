import pickle
from copy import deepcopy

def RunAll(L, nameXP):
    MD = {}    
    for (O, DS) in L:        
        MD[DS] = {}        
        for (idS,path,compilerOption,name, pathJson) in O:
            MD[DS][idS] = {}
            for (O2, DS2) in L: 
                if DS == DS2:
                    continue
                MD[DS][idS][DS2] = {}
                for (idS2,path2,compilerOption2,name2, pathJson2) in O2:
                    MD[DS][idS][DS2][idS2] = [name,name2,compilerOption,compilerOption2] 

    P = 40
    
    MDO = deepcopy(MD)
    
    for idP in range(P): 
        inputFile = "MD4/MD4"+nameXP+"_"+str(idP)+".txt"

        with open(inputFile, "r") as f:
            for l in f.readlines():
                # str([DS,idS,DS2,idS2,d,et])+"\n"
                l = l[1:-2]
                l = l.replace("'", "")
                l = l.replace(" ", "")
                t = l.split(",")

                DS = t[0]
                idS = int(t[1])
                DS2 = t[2]
                idS2 = int(t[3])
                d = float(t[4])
                elapsed = float(t[5])
                
                L = MD[DS][idS][DS2][idS2]+[d,elapsed]
                MD[DS][idS][DS2][idS2] = tuple(L)
    
    for idCore in range(P):
        if nameXP == "O":            
            inputFile = "MD4C/MD4C"+nameXP+"_"+str(idP)+".txt"
            with open(inputFile, "r") as f:
                for l in f.readlines():
                    # str([DS,idS,DS2,idS2,d,et])+"\n"
                    l = l[1:-2]
                    l = l.replace("'", "")
                    l = l.replace(" ", "")
                    t = l.split(",")

                    DS = t[0]
                    if DS == "BOC":
                        DS = "BO"
                    idS = int(t[1])
                    DS2 = t[2]
                    if DS2 == "BOC":
                        DS2 = "BO"
                    
                    idS2 = int(t[3])
                    d = float(t[4])
                    elapsed = float(t[5])
                    
                    L = MDO[DS][idS][DS2][idS2]+[d,elapsed]
                    MD[DS][idS][DS2][idS2] = tuple(L)    
    
    with open("MD4"+nameXP, "wb") as f:
        pickle.dump(MD, f)        


if __name__ == '__main__':
    import sys
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GBigVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GCoreutilsOptions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsVersions")
    sys.path.insert(0, "C:\\Users\\?\\Desktop\\GUtilsOptions")

    from makeBenchBO import readAllSamples as allBO
    from makeBenchBV import readAllSamples as allBV
    from makeBenchCV import readAllSamples as allCV
    from makeBenchCO import readAllSamples as allCO
    from makeBenchUO import readAllSamples as allUO
    from makeBenchUV import readAllSamples as allUV
    
    RunAll([(allBO(),"BO"),(allUO(),"UO"),(allCO(),"CO")], "O")
    RunAll([(allBV(),"BV"),(allUV(),"UV"),(allCV(),"CV")], "V")
