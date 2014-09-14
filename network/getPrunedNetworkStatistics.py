from optparse import OptionParser
import numpy as np
import simplejson as json
import networkx as nx
import csv
import os.path
if __name__ == '__main__':
	cuisine = ""
	netType = "";
	parser	= OptionParser()
	parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="indian")
	parser.add_option("-l", "--linkthreshold", dest="edgethreshold", help="link threshold", default=100)
	options, arguments = parser.parse_args()
	print "cuisine:" + options.cuisine
	print "link threshold:" + str(options.edgethreshold)
	
	maxLinks = int(options.edgethreshold);
		
	json_file = "data/" + options.cuisine + "_dbg.json"
	d = json.load(open(json_file))
	edges = d['edges'];
	
	edgeWts = [];
	for edge in edges:
		edgeWts.append(edge[2]['value']);
	orderedIndices = np.argsort(edgeWts);
	orderedIndices = orderedIndices.tolist();
	# descending order
	orderedIndices.reverse();

	print "-------------------------------------"
	print "Compute pruned network"
	print "-------------------------------------"

	prunedEdges = [];
	nodes = {};
	for linkIndex in orderedIndices[1:maxLinks]:
		prunedEdges.append(edges[linkIndex]);
		srcNode = edges[linkIndex][0];
		destNode = edges[linkIndex][1];
		if srcNode not in nodes.keys():
			nodes[srcNode] = 1;
		else:
			nodes[srcNode] = nodes[srcNode] + 1;

		if destNode not in nodes.keys():
			nodes[destNode] = 1;
		else:
			nodes[destNode] = nodes[destNode] + 1;
	prunedNodes = [];
	prunedNodeDegrees = [];
	for nodeName in nodes.keys():
		degree = nodes[nodeName]
		prunedNodeDegrees.append(degree);
		prunedNode = [nodeName, {'degree': degree}]
		prunedNodes.append(prunedNode)

	orderedDegreeIndices = np.argsort(prunedNodeDegrees);
	orderedDegreeIndices = orderedDegreeIndices.tolist();
	orderedDegreeIndices.reverse();

	G = nx.Graph()
	G.add_nodes_from(prunedNodes)
	G.add_edges_from(prunedEdges)

	print "-------------------------------------"
	print "Find cliques of the graph"
	print "-------------------------------------"
	cliques = list(nx.find_cliques(G))
	print cliques

	print "-------------------------------------"
	print "Compute clique number - size of the largest clique"
	print "-------------------------------------"
	graphCliqueNumber = nx.graph_clique_number(G, cliques)
	print graphCliqueNumber

	print "-------------------------------------"
	print "Compute number of maximal ciiques"
	print "-------------------------------------"
	graphNumberOfCliques = nx.graph_number_of_cliques(G, cliques)
	print graphNumberOfCliques


	print "-------------------------------------"
	print "Compute size of largest maximal clique containing a given node"
	print "-------------------------------------"
	maximalCliqueSizePerNode = nx.node_clique_number(G)
	print maximalCliqueSizePerNode

	print "-------------------------------------"
	print "Compute number of maximal cliques for each node"
	print "-------------------------------------"
	noOfMaximalCliquesPerNode = nx.number_of_cliques(G)
	print noOfMaximalCliquesPerNode

	print "-------------------------------------"
	print "Compute list of cliques containing  a given node"
	print "-------------------------------------"
	lcliques = nx.cliques_containing_node(G)
	print lcliques

	print "-------------------------------------"
	print "Writing data into global file"
	print "-------------------------------------"

	globalCliqueFile = 'data/globalCliqueFile.csv'
	mode = '';
	if os.path.isfile(globalCliqueFile):
		mode = 'a';
	else:
		mode = 'wb';
		with open(globalCliqueFile, mode) as csvfile:
			sw = csv.writer(csvfile, delimiter=',')
			data = ['cuisine', 'edgeWtThreshold', 'NumberOfCliques', 'Size of Largest Maximal Clique'];
			sw.writerow(data)
		mode = 'a';
		
	with open(globalCliqueFile, mode) as csvfile:
		sw = csv.writer(csvfile, delimiter=',')
		data = [options.cuisine, str(options.edgethreshold), str(len(cliques)), str(graphCliqueNumber)]
		sw.writerow(data)


	print "-------------------------------------"
	print "Writing data into per cuisine per edge threshold file"
	print "-------------------------------------"

	perCuisineEdgeThCliqueFile = 'data/' + options.cuisine + '_' + str(options.edgethreshold) + '_cliqueInfo.csv'
	mode = '';
	if os.path.isfile(perCuisineEdgeThCliqueFile):
		mode = 'a';
	else:
		mode = 'wb';
		with open(perCuisineEdgeThCliqueFile, mode) as csvfile:
			sw = csv.writer(csvfile, delimiter=',')
			data = ['Ingredient', 'Rank', 'Degree', 'NumberOfCliques', 'Size of Largest Maximal Clique'];
			sw.writerow(data);
		mode = 'a';

	with open(perCuisineEdgeThCliqueFile, mode) as csvfile:
		sw = csv.writer(csvfile, delimiter=',')
		i=0;
		data = [];
		for index in orderedDegreeIndices:
			node = prunedNodes[index];
			nodeName = node[0];
			nodeDegree = prunedNodeDegrees[index]

			rank = i;
			i=i+1;
			print nodeName
			cliquesForGivenNode = lcliques[nodeName]		
			numberOfCliquesForGivenNode = len(cliquesForGivenNode)
			maxCliqueSizeForGivenNode = maximalCliqueSizePerNode[nodeName]
			noOfMaximalCliquesForGivenNode = noOfMaximalCliquesPerNode[nodeName]

			data.append([nodeName, str(rank), str(nodeDegree), str(numberOfCliquesForGivenNode), str(maxCliqueSizeForGivenNode)])
		sw.writerows(data);

	print "-------------------------------------"
	print "Writing cliques per cuisine per link threshold "
	print "-------------------------------------"

	perCuisineEdgeThCliquesList = 'data/' + options.cuisine + '_' + str(options.edgethreshold) + '_cliqueList.csv'
	with open(perCuisineEdgeThCliquesList, 'wb') as csvfile:
		sw = csv.writer(csvfile, delimiter=',')
		for clique in cliques:
			sw.writerow(clique);

	
