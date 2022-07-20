from tqdm import tqdm
import pickle
import requests
import sys
import json
import os.path
from os import system
from pathlib import Path


familiesByPriority = ['pnscan', 'vpnfilter', 'hajime', 'lightaidra', 'dnsamp', 'skeeyah', 'ddostf', 'tsunami', 'gafgyt', 'mirai']


"""
{'pnscan': 1, 'vpnfilter': 5, 'hajime': 6, 'lightaidra': 8, 'dnsamp': 18, 'skeeyah': 19, 'ddostf': 24, 'tsunami': 1763, 'gafgyt': 7322, 'mirai': 19541 }
"""


downloadedMalware = {}
for path in Path('../jsons').rglob('*'):
	pathString = str(path)
	idS = pathString.split("/jsons/")[1].split(".")[0]
	downloadedMalware[idS] = True


hashToFamilies = {}

with open("elf.csv", "r",encoding='utf-8') as f:
    i = -1
    for l in tqdm(f.readlines()):
        t = l.strip().split(",")
        hashS = t[1]
        if not(hashS in downloadedMalware):
            continue
        try:
			
            with open("../metadata/"+hashS+".json", "r") as f:
                l = f.readline().lower()
            
            hashToFamilies[hashS] = []
            for s in familiesByPriority:
                if s in l:
                    hashToFamilies[hashS] += [s] 
        except Exception:
            pass

with open("familiesMetaElf", "wb") as f:
	pickle.dump(hashToFamilies, f)

