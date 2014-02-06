import numpy as np
from optparse import OptionParser
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
from networkx.linalg.graphmatrix import *
import simplejson as json
#returns the edgeList/Weights of nodes for a given ingredientList and their co-occurence matrix
def createEdgeList(ingredList, recipeIngredMat):
	# get edgeList / weights for ingredients
	edgeList = {}
	
	for row in recipeIngredMat:
		for i in range(0, len(row)-1):
			source = ingredList[i]
			if row[i] > 0:
				for j in range(0, len(row)-1):
					# if source != target, row[j] > 0 and row[i] > 0
					if i!=j  and i <=j and row[j] > 0:
						dest = ingredList[j]
						key = source + "#" + dest
						revKey = dest + "#" + source
						if key in edgeList.keys():
							edgeList[key] += 1
						else:
							if revKey in edgeList.keys():
								edgeList[revKey] += 1
							else:
								edgeList[key] = 1
	return edgeList

#returns the edgeList/Weights of nodes for a given ingredientList and their co-occurence matrix
def createDirectedEdgeList(ingredList, condMat):
	# get edgeList / weights for ingredients
	edgeList = {}
	dim = condMat.shape
	print dim
	for i in range(dim[0]):
		source = ingredList[i]
		for j in range(dim[1]):
			if i!=j and condMat[i][j] >= 0.1:
				dest = ingredList[j]
				key = source + "#" + dest
				if key not in edgeList.keys():
					edgeList[key] = condMat[i][j];
				else:
					print "Problem: " + str(i) + "-" + str(j) + ":" + key
	return edgeList

#visualize a network
def visualizeNetwork(nodes, edges, isDirected):
	#visualize as graph
	B = nx.Graph()
	if isDirected:
		B = nx.DiGraph()
	B.add_nodes_from(nodes)
	for edge, weight in edges.iteritems():
		nodes=edge.split("#")
		error =0
		for node in nodes:
			if node in B:
				if not 'degree' in B.node[node]:
					B.node[node]['degree'] = 1
				else:
					B.node[node]['degree'] += 1
			else:
				print "No node found: " + node
				error = 1
				break;
		if error == 0:
			B.add_edges_from([(nodes[0], nodes[1])]) 
			B[nodes[0]][nodes[1]]['value'] = weight

	return B

if __name__ == '__main__':
	parser=OptionParser()
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="hawaiian")
        parser.add_option("-p", "--path", dest="rootPath", help="root location to store results", default="/home/vaidehi/EYB")

        options, arguments = parser.parse_args()
	print "cuisine: " + options.cuisine
	print "path: " + options.rootPath

		
	matFile = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_rlmat.txt";
 	recipeLeafMat = np.loadtxt(matFile, delimiter=",")	
	rLMat = np.matrix(recipeLeafMat)
	freqCount = rLMat.sum(axis=0)
	lfreqCount = np.array(freqCount)[0].tolist()

	ingredientList = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_ingredLeafs.txt";
	f = open(ingredientList);
	ingredLeafs = f.readlines()
	f.close()
	
	leafEdges = createEdgeList(ingredLeafs, recipeLeafMat);
	G = visualizeNetwork(ingredLeafs, leafEdges, 0)

	A = adjacency_matrix(G)
	A = A.tolist()
	
	dim = recipeLeafMat.shape
	recipeCount = dim[0]
	ingredCount = dim[1]

	print "------------------------- Generating cond probabilities -------------------------------"
	condProb = np.zeros([dim[1], dim[1]])
	for i in range(dim[1]):
		for j in range(dim[1]):
			pRecipesAB = A[i][j]/recipeCount;
			pIngredI = lfreqCount[i]/recipeCount;
			condProb[i][j] = pRecipesAB/pIngredI;

	directedEdges = createDirectedEdgeList(ingredLeafs, condProb);
	D = visualizeNetwork(ingredLeafs, directedEdges, 1)
	

	json_file = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_CP.json"
	#write network data into json
	dumps = json_graph.dumps(D)

	with open(json_file, 'w') as file:
		file.write(dumps);

	json.dump(dict(nodes=[[n, D.node[n]] for n in D.nodes()],
		edges=[[u,v,D.edge[u][v]] for u,v in D.edges()]),
	open(options.rootPath + "/network/data/" + options.cuisine + "_CP.json", 'w'), indent=2)


