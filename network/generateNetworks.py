import numpy as np
from optparse import OptionParser
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
from networkx.linalg.graphmatrix import *
import simplejson as json
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

if __name__ == '__main__':
	parser=OptionParser()
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="hawaiian")
        parser.add_option("-p", "--path", dest="rootPath", help="root location to store results", default="/home/hduser/EYB")

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

	# write co-occurrence of this network  as cuisine_cooc.json
	A = adjacency_matrix(G)
	A = A.tolist()
	coocFile = options.rootPath + "/network/data/" + options.cuisine + "_cooc.csv"
	dim = recipeLeafMat.shape
	recipeCount = dim[0]
	ingredCount = dim[1]

	# compute conditional prob
	CP = np.zeros([dim[1], dim[1]+1])
	cpFile = options.rootPath + "/network/data/" + options.cuisine + "_CP.csv"
	# compute PMI 
	PMI = np.zeros([dim[1], dim[1]+1])
	pmiFile = options.rootPath + "/network/data/" + options.cuisine + "_PMI.csv"
	# compute correlation coefficient mat
	CCF = np.corrcoef(recipeLeafMat, rowvar=0);
	ccfFile = options.rootPath + "/network/data/" + options.cuisine + "_CCF.csv"
	
	ingredIds = np.zeros([dim[1], 1])
	for i in range(0, dim[1]-1):
		ingredIds[i] = i;
		for j in range(0, dim[1]-2):
			pRecipesAB = A[i][j]/recipeCount;
			pIngredI = lfreqCount[i]/recipeCount;
			CP[i][j] = pRecipesAB/pIngredI;
			if i!=j and i<=j:
				pIngredJ = lfreqCount[j]/recipeCount;
				PMI[i][j] = pRecipesAB/(pIngredI * pIngredJ)
				PMI[j][i] = pRecipesAB/(pIngredI * pIngredJ)
	
	np.savetxt(coocFile, A, fmt='%10.5f', delimiter=",")

	print 	PMI.shape
	print ingredIds.shape
	PMI = np.append(PMI, ingredIds, axis = 1);
	np.savetxt(pmiFile, PMI, fmt='%10.5f', delimiter=",")
	
	CCF = np.append(CCF, ingredIds, axis = 1);
	np.savetxt(ccfFile, CCF, fmt='%10.5f', delimiter=",")
	
	CP = np.append(CP, ingredIds, axis = 1);
	np.savetxt(cpFile, CP, fmt='%10.5f', delimiter=",")
