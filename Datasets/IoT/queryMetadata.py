from tqdm import tqdm
import pickle
import requests
import sys
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'API-KEY': ''}

def getJson(hashS):
    r = requests.post('https://mb-api.abuse.ch/api/v1/', data={"query": "get_info", "hash": hashS}, verify=False, headers=headers)
    r.raise_for_status()
    dataJson = r.json()
    return dataJson

with open("elf.csv", "r",encoding='utf-8') as f:
    i = -1
    for l in tqdm(f.readlines()):
        t = l.strip().split(",")
        
        try:
            dataJson = getJson(t[1])
            with open("../metadata/"+t[1]+".json", "w") as f:
                f.write(str(dataJson))
        except Exception:
            pass



