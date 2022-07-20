import pickle

P = 40

for nameXP in ["O","V"]:
    MD = {}
    for idP in range(P): 
        inputFile = "MD4/MD4"+nameXP+"_"+str(idP)+".txt"

        with open(inputFile, "r") as f:
            for l in f.readlines():
                # str([DS,idS,DS2,idS2,name,name2,compilerOption,compilerOption2,d,el])+"\n"
                l = l[1:-2]
                l = l.replace("'", "")
                l = l.replace(" ", "")
                t = l.split(",")

                DS = t[0]
                idS = int(t[1])
                DS2 = t[2]
                idS2 = int(t[3])
                name = t[4]
                name2 = t[5]
                compilerOption = t[6]
                compilerOption2 = t[7]
                d = float(t[8])
                elapsed = float(t[9])
                
                if not(DS in MD):
                    MD[DS] = {}
                if not(idS in MD[DS]):
                    MD[DS][idS] = {}
                if not(DS2 in MD[DS][idS]):
                    MD[DS][idS][DS2] = {}
                
                MD[DS][idS][DS2][idS2] = (name,name2,compilerOption,compilerOption2,d,elapsed)
                
    for idP in range(P): 
        if nameXP == "O":
            inputFile = "MD4C/MD4C"+nameXP+"_"+str(idP)+".txt"

            with open(inputFile, "r") as f:
                for l in f.readlines():
                    # str([DS,idS,DS2,idS2,name,name2,compilerOption,compilerOption2,d,el])+"\n"
                    l = l[1:-2]
                    l = l.replace("'", "")
                    l = l.replace(" ", "")
                    t = l.split(",")

                    DS = t[0]
                    idS = int(t[1])
                    DS2 = t[2]
                    idS2 = int(t[3])
                    name = t[4]
                    name2 = t[5]
                    compilerOption = t[6]
                    compilerOption2 = t[7]
                    d = float(t[8])
                    elapsed = float(t[9])
                    
                    if not(DS in MD):
                        MD[DS] = {}
                    if not(idS in MD[DS]):
                        MD[DS][idS] = {}
                    if not(DS2 in MD[DS][idS]):
                        MD[DS][idS][DS2] = {}
                    
                    MD[DS][idS][DS2][idS2] = (name,name2,compilerOption,compilerOption2,d,elapsed)
    with open("MD4"+nameXP, "wb") as f:
        pickle.dump(MD, f)        



