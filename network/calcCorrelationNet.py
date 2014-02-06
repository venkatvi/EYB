import numpy as np
import networkx as nx
from networkx.readwrite import json_graph
from optparse import OptionParser
import simplejson as json
#returns the edgeList/Weights of nodes for a given ingredientList and their co-occurence matrix
def createEdgeList(ingredList, corrMat):
	# get edgeList / weights for ingredients
	posEdgeList = {}
	negEdgeList = {}
	dim = corrMat.shape
	print dim
	for i in range(dim[0]):
		source = ingredList[i]
		for j in range(dim[1]):
			if i <=j and i!=j:
				dest = ingredList[j]
				key = source + "#" + dest
				revKey = dest + "#" + source
				if corrMat[i][j] > 0 and corrMat[i][j] > 0.1:
					if key in posEdgeList.keys():
						posEdgeList[key] += 1
					else:
						if revKey in posEdgeList.keys():
							posEdgeList[revKey] += 1
						else:
							posEdgeList[key] = 1
				if (corrMat[i][j] < 0 and corrMat[i][j] < -0.1):
					if key in negEdgeList.keys():
						negEdgeList[key] += 1
					else:
						if revKey in negEdgeList.keys():
							negEdgeList[revKey] += 1
						else:
							negEdgeList[key] = 1
	return [posEdgeList, negEdgeList]
#visualize a network
def visualizeNetwork(nodes, edges, json_file):
	#visualize as graph
	B = nx.Graph()
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
				#print "No node found: " + node
				error = 1
				break;
		if error == 0:
			B.add_edges_from([(nodes[0], nodes[1])]) 
			B[nodes[0]][nodes[1]]['value'] = weight

	#write network data into json
	dumps = json_graph.dumps(B)

	with open(json_file, 'w') as file:
		file.write(dumps);

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

	print "------------------------Calculating correlation coefficient--------------------------------------"
	#calculating correlation coefficient network
	dim = recipeLeafMat.shape
	corrMat = np.corrcoef(recipeLeafMat, rowvar=0);

	ingredientList = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_ingredLeafs.txt";
	f = open(ingredientList);
	ingredLeafs = f.readlines()
	for i in range(len(ingredLeafs)):
		ingredLeafs[i] = ingredLeafs[i].strip("\n")
	f.close()

	[posleafEdges, negleafEdges] = createEdgeList(ingredLeafs, corrMat);

	posFilename = options.rootPath + "/coquere/ingredientNets/data/" +  options.cuisine + "_posNet.json"
	negFilename = options.rootPath + "/coquere/ingredientNets/data/" +  options.cuisine + "_negNet.json"


	Gpos = visualizeNetwork(ingredLeafs, posleafEdges, posFilename)
	Gneg = visualizeNetwork(ingredLeafs, negleafEdges, negFilename)

	json.dump(dict(nodes=[[n, Gpos.node[n]] for n in Gpos.nodes()],
		edges=[[u,v,Gpos.edge[u][v]] for u,v in Gpos.edges()]),
	open(options.rootPath + "/network/data/" + options.cuisine + "_posNet.json", 'w'), indent=2)

	json.dump(dict(nodes=[[n, Gneg.node[n]] for n in Gneg.nodes()],
		edges=[[u,v,Gneg.edge[u][v]] for u,v in Gneg.edges()]),
	open(options.rootPath + "/network/data/" + options.cuisine + "_negNet.json", 'w'), indent=2)




