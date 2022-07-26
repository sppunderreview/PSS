import os
import pickle

jsonFinal = ""

listProgram = [ str(i) for i in range(88)]

for program in listProgram:
	command = "ida64 -A -SextractFeatures.py "+program
	os.system(command)

	f = open("fileOut","r")
	cfgs = pickle.load(f)

	for func in cfgs.raw_graph_list:
		functionName = func.funcname 
		edges = func.fun_features	
		attr = {}
		for node_id in func.old_g:
			attr[node_id] = func.retrieveVec(node_id, func.old_g)
			attr[node_id][0] = sum([ sum([ord(x) for x in s]) for s in attr[node_id][0] ])
			attr[node_id][1] = sum(attr[node_id][1])
		
		programSrc = program
		numBlocks = len(attr)
			
		
		succs = [[] for i in range(numBlocks)]
		for (u,v) in edges:
			if not(v in succs[u]):
				succs[u] += [v]
		
		features = []
		for i in range(numBlocks):
			features += [[float(x) % 10000 for x in attr[i]]]
		
		if numBlocks == 1:
			if features[0][-3] == 1.0:
				continue
		
		jsonFinal += "{\"src\": \""+programSrc+"\",";
		jsonFinal += "\"n_num\": "+str(numBlocks)+",";
		jsonFinal += "\"succs\": "+str(succs)+",";
		jsonFinal += "\"features\": "+str(features)+",";
		jsonFinal += "\"fname\": \""+functionName+"\"}\n";
	f.close()


f = open("extractedGeminiUtilsVersions.json","w")
f.write(jsonFinal)
f.close()

