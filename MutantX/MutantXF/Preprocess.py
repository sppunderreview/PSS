import time
import json
import pickle

from os import system
from os.path import isfile

from multiprocessing import Process

from random import shuffle

# 4 grams embedding
def computeEmbedding(opcodes):    
    ngrams = zip(*[opcodes[i:] for i in range(4)])    
    embedding = {}
    for ngram in ngrams:
        d = "_".join(ngram)
        if not(d in embedding):
            embedding[d] = 0        
        embedding[d] += 1   
    return embedding

# https://wiki.osdev.org/X86-64_Instruction_Encoding
# http://ref.x86asm.net/

prefixX32 = {}
for p in ["66","f2","f3","2e","9b","64","65","f0","36","3e","26"]:
    prefixX32[p] = True

def findOpcodeX32(instrBytes):
    global prefixX32
    # x32 prefix
    while(len(instrBytes) > 1 and (instrBytes[0:2] in prefixX32)):
        instrBytes = instrBytes[2:]
    
    if len(instrBytes) < 2:
        return "??"
    
    # REX x32 prefix
    if (instrBytes[0] == "4"):
        if (len(instrBytes) < 4):
            return "??"
        instrBytes = instrBytes[2:]

    # Opcode    
    # 2 bytes
    if (len(instrBytes) >= 4 and instrBytes[0:2] == "0f"):           
        return instrBytes[0:4]
    # 1 byte
    return instrBytes[0:2]


prefixX64 = {}
for p in ["f0","f2","f3","2f","36","3f","26","64","65","2e","3e","66","67"]:
    prefixX64[p] = True

def findOpcodeX64(instrBytes):
    global prefixX64
    # x64 prefix
    while(len(instrBytes) > 1 and (instrBytes[0:2] in prefixX64)):
        instrBytes = instrBytes[2:]
    
    if len(instrBytes) < 2:
        return "??"
    
    # REX x64 prefix
    if (instrBytes[0] == "4"):
        if (len(instrBytes) < 4):
            return "??"
        instrBytes = instrBytes[2:]

    # Opcode    
    # 2 bytes
    if (len(instrBytes) >= 4 and instrBytes[0:2] == "0f"):
        # 3 bytes
        if (len(instrBytes) >= 6 and instrBytes[2:4] in ["38","3a"]):
            return instrBytes[0:6]             
        return instrBytes[0:4]
    # 1 byte
    return instrBytes[0:2]

def computesEmbeddingFromBytes(idS, pathInput):
    pathOutput = "./A/"+idS
    
    opcodesTotal  = []
    with open(pathInput) as f:
        data = json.load(f)
    
    if data["architecture"]["type"] != "metapc":
        print(idS, "error not metapc",data["architecture"]["type"])
        return
    
    
    size = int(data["architecture"]["size"][1:3])
    if not(size in [32, 64]):
        print(idS, "error not 32/64",data["architecture"]["size"])
        return
    
    start = time.time()
    
    if (size == 32):
        for instrBytes in data["bytes"]:
            opcodesTotal += [findOpcodeX32(instrBytes)]
    else:    
        for instrBytes in data["bytes"]:
            opcodesTotal += [findOpcodeX64(instrBytes)]

    embedding = computeEmbedding(opcodesTotal)
    elasped = time.time()-start
    print(idS,elasped, len(opcodesTotal), len(embedding))
    data = (embedding,elasped)
    with open(pathOutput, "wb") as f:
        pickle.dump(data, f)


def extractEmbeddingFromPrograms(lP):
    for x in lP:
        idS = x[0]
        pathIntput = x[1]
        pathIdaOut = pathIntput+"_bytes.json"    
        command = "/home/?/idapro-7.5/idat64 -A -S/home/?/Documents/Travail/?/MutantXVirus/ExtractBytesViaIDA.py "+pathIntput
        system(command)     
        try:
            computesEmbeddingFromBytes(idS, pathIdaOut)
        except Exception as e:
            print(idS)
            print(e)


                            
if __name__ == '__main__':
       import sys
       sys.path.insert(0, "/home/?/Documents/Travail/?/Virus")
       from makeBenchVirus import readAllSamples as allVirus
       
       
       P = 26
       
       toDo = allVirus()
       shuffle(toDo)
       
       toDoSelected = []
       
       for x in toDo:
              idS = x[0]
              outputFile = "A/"+idS
              if isfile(outputFile) == True:
                     continue              
              toDoSelected += [x]
       toDo = toDoSelected
       
       
       print("TO DO", len(toDo))
       BS = int(len(toDo)/P) + 1       
       print("BS", BS)
       
       lP = {}
       for p in range(P):
              L = []
              i = 0
              for x in toDo:
                     L += [x]
                     i += 1
                     if i ==  BS:
                            break
                     
              if BS >= len(toDo):
                     toDo = []
              else:
                     toDo = toDo[BS:]
              lP[p] = L
       
       
       L = []
       for p in range(P):
              p1 = Process(target=extractEmbeddingFromPrograms, args=(lP[p],))
              p1.start()
              L += [p1]
              
       for p in L:
              p.join()
    
