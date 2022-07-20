#!/usr/bin/python3

# ? ?
# 2021
# ?

import os
import time

import pickle
import numpy as np

def command(folder, id, maxId, programs):
    return "python3 computeDistances.py "+folder+ " "+str(id)+" "+str(maxId)+" "+str(programs)

toDo = [("V0","V1"),("V0","V2"),("V0","V3"),("V1","V2"),("V1","V3"),("V2","V3")]

for O0, O1 in toDo:
    dir = "./B"+O0+O1+"/"
    start = time.time()
    cores = 40
    jobT = ""
    for idL in range(cores):
        jobT += "(sleep "+str(idL*2)+" && "+command(dir, idL, cores, 84)+" ) & " 
    jobT += "wait && touch 0.txt"
    os.system(jobT)
    b = time.time()
    print(b-start)
    start = b



