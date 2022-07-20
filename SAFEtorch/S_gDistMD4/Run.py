#!/usr/bin/python3

# ? ?
# 2022
# ?

import os
import sys

import time
import numpy as np

import random
from multiprocessing import Process
import pickle


def computesDistance(vectorsP1,vectorsP2):
    start = time.time()
    dL = 0
    for v in vectorsP1:
        dLM = 1000
        for v2 in vectorsP2:
            d =  np.linalg.norm(v2[1]-v[1], ord=2)
            if d < dLM:
                dLM = d
        dL += dLM
    et = time.time() - start
    return dL, et

def run(vecById, L_DS, myId, maxID):
    outputFile = "MD4"+L_DS[0][1]+"_"+str(myId)+".txt"
    
    done = {}
    try:
        with open(outputFile, "r") as f:
            for l in f.readlines():                
                t = l.split(",")
                s = ",".join(t[0:4])
                done[s] = True
    except (Exception):
        pass
    
    print(len(done))
    
    tasks = []

    for DS in L_DS:
        for idS in range(len(vecById[DS])):
            for DS2 in L_DS:
                if DS == DS2:
                    continue
                for idS2 in range(len(vecById[DS2])):
                    tasks += [(DS,idS,DS2,idS2)]

    random.seed(10)    
    random.shuffle(tasks)
    batchSize = int((1/maxID) * len(tasks)) + 1
    
    startT = batchSize * myId
    if myId == maxID - 1:
        endT = len(tasks)
    else:
        endT = batchSize * (myId+1)

    for i in range(startT, endT):
        DS = tasks[i][0]
        idS = tasks[i][1]
        DS2 = tasks[i][2]
        idS2 = tasks[i][3]
        
        l = str([DS,idS,DS2,idS2,0,0])+"\n"
        t = l.split(",")
        s = ",".join(t[0:4])
        if s in done:
            continue
        
        d, et = computesDistance(vecById[DS][idS],vecById[DS2][idS2])
        with open(outputFile, "a") as f:
            f.write(str([DS,idS,DS2,idS2,d,et])+"\n")

if __name__ == '__main__':
    P = 40

    TODO = [["BV","UV","CV"]]
        
    for L_DS in TODO:
        vecById = {}
        for DS in L_DS:
            with open(DS+"/vecById", 'rb') as f:
                vecById[DS] = pickle.load(f)
        PL = []
        for idL in range(P):
            p = Process(target=run, args=(vecById, L_DS, idL, P))
            PL += [p]
            p.start()

        for i in range(P):
            PL[i].join()

