#!/usr/bin/env python
import sys
import networkx as nx
from networkx.readwrite import json_graph
import simplejson as json
def getCuisineStr(cuisineId):
	cuisineId = int(float(cuisineId))
	if cuisineId == 1:
		return 'french'
	elif cuisineId == 2:
		return 'italian'
	elif cuisineId == 3:
		return 'indian'
	elif cuisineId == 4:
		return 'chinese'
	else:
		return 'temp'
def getNetworkType(matType):
	matType = int(float(matType))
	if matType == 1:
		return 'cooc'
	elif matType == 2:
		return 'pmi'
	elif matType == 3:
		return 'cp'
	elif matType == 4:
		return 'ccf'
	else:
		return 'none' 
def initGraph(cuisineId, matType,networksMap, ingredListMap):
	cuisine = getCuisineStr(cuisineId);
	netType = getNetworkType(matType);
	if (cuisine == 'temp'):
		print 'initGraph'
		print cuisineId
		print matType
		return networksMap
	if netType == 'none':
		print 'initGraph netType'
		print cuisineId
		print matType
		return networksMap
	key = cuisine + "_" + netType
	if netType == 'ccf': #mapping to corceff mat
		# add pos and neg to the key
		tkey = key + "_pos";	
		networksMap = addKey(networksMap, ingredListMap, cuisine, tkey)
		tkey = key + "_neg";
		networksMap = addKey(networksMap, ingredListMap, cuisine, tkey)
		tkey = key + "_uncr";
		networksMap = addKey(networksMap, ingredListMap, cuisine, tkey)
	else:
		networksMap = addKey(networksMap, ingredListMap, cuisine, key)
	return networksMap

def addKey(networksMap, ingredListMap, cuisine, key):
	if key not in networksMap.keys():
		if 'cp' in key: # mapping to conditional prob matrix
			B = nx.DiGraph()
			B.add_nodes_from(ingredListMap[cuisine])
			networksMap[key] = B
		else:
			B = nx.Graph()
			B.add_nodes_from(ingredListMap[cuisine])
			networksMap[key] = B
	return networksMap
def addEdge(edge, weight, cuisineId, matType, networksMap):
	cuisine = getCuisineStr(cuisineId);
	netType = getNetworkType(matType);
	if cuisine == 'temp':
		print "addEdge"
		print cuisineId
		print matType
		return networksMap
	if netType == 'none':
		print "addEdge nettype"
		print cuisineId
		print matType
		return networksMap
	key = cuisine + "_" + netType
	if netType == 'ccf':
		if weight > 0:
			key = key + "_pos"
		elif weight < 0:
			key = key + "_neg"
		else:
			key = key + "_uncor"
	B = networksMap[key]
	# add edge to these nodes
	nodes=edge.split("#")
	error =0
	for node in nodes:
		node = node.strip()
		if node:
			if node in B:
				if not 'degree' in B.node[node]:
					B.node[node]['degree'] = 1
				else:
					B.node[node]['degree'] += 1
			else:
				print node + " not found. error"
				error = 1
				break;
	if error == 0:
		B.add_edges_from([(nodes[0], nodes[1])]) 
		B[nodes[0]][nodes[1]]['value'] = weight
	networksMap[key] = B
	return networksMap
def getIngredList(cuisine):
	ingredListFile = "/home/hduser/EYB/coquere/ingredientNets/data/" + cuisine + "_ingredLeafs.txt";
	f = open(ingredListFile);
	ingredList = f.readlines()
	ingredList = map(str.strip,ingredList);
	f.close()
	return ingredList

if __name__ == '__main__':
	ingredListMap = {};
	ingredListMap['french'] = getIngredList('french');
	ingredListMap['italian'] = getIngredList('italian');
	ingredListMap['indian'] = getIngredList('indian');
	ingredListMap['chinese'] = getIngredList('chinese');

	networksMap = {};	
	last_key = None
	last_value = 0
	
	for input_line in sys.stdin:
		input_line = input_line.strip().strip(" ")
		if input_line:
			cuisineId, matType, this_key, this_value = input_line.split("\t", 3)
			networksMap = initGraph(cuisineId, matType, networksMap, ingredListMap)
			value = float(this_value)
			if last_key == this_key:
				if this_value != last_value:
					networksMap = addEdge(this_key, this_value, cuisineId, matType, networksMap);
			else:
				# add edge to these nodes
				last_key = this_key
				last_value = this_value
				networksMap = addEdge(this_key, this_value, cuisineId, matType, networksMap);

	for key in networksMap.keys():
		B = networksMap[key];
		#write network data into json
		dumps = json_graph.dumps(B)

		json_file = "/home/hduser/EYB/coquere/ingredientNets/data/" + key + ".json";
		with open(json_file, 'w') as file:
			file.write(dumps);

		json.dump(dict(nodes=[[n, B.node[n]] for n in B.nodes()],
			edges=[[u,v,B.edge[u][v]] for u,v in B.edges()]),
		open("/home/hduser/EYB/network/data/" + key + ".json", 'w'), indent=2)

