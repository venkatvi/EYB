from __future__ import division
import nltk
import simplejson as json
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
from apgl.graph import SparseGraph
import numpy as np
from optparse import OptionParser
from networkx.algorithms.centrality  import *
from networkx.algorithms.vitality import *
from networkx.algorithms.assortativity import *
from networkx.algorithms.cluster import *
from networkx.algorithms.distance_measures import *
def computeNodeWiseClusteringCoefficient(A, degree):
	alist = A.tolist()
	globalClusteringCoefficient = 0
	clusteringCoefficient = []
	for i in range(0, len(alist)):
		neighbourEdges = 0
		for j in range(0, len(alist[i])):
			if alist[i][j] > 0 and i != j:
				for k in range(0, len(alist[i])):
					if alist[j][k] > 0 and alist[i][k] > 0 and i !=j and i != k and j != k:
						neighbourEdges = neighbourEdges + 1
		cc =float(neighbourEdges)/float((degree[i]+1)*degree[i]);
		clusteringCoefficient.append(cc)
		globalClusteringCoefficient += cc
	globalClusteringCoefficient = globalClusteringCoefficient / len(degree)
	return [globalClusteringCoefficient, clusteringCoefficient]

def getAssortativity(G, degree):
	degree_sq = [deg**2 for deg in degree]
	edges = G.getAllEdges()
	m = float(len(edges))
	num1, num2, den1 = 0, 0, 0
	for edge in edges:
		source = edge[0]
		target = edge[1]
		num1 += degree[source] * degree[target]
		num2 += degree[source] + degree[target]
		den1 += degree_sq[source] + degree_sq[target]
	num1 /= m
	den1 /= 2*m
	num2 = (num2 / (2*m)) ** 2
	return (num1 - num2)/(den1 - num2)

def getNeighborConnectivity(G, degree):
	knn = []
	for i in range(0, len(degree)):
		vec = []	
		for j in range(0, len(degree)):
			vec.append(0)
		knn.append(vec)

	edges = G.getAllEdges()
	for edge in edges:
		source = edge[0]
		target = edge[1]
		sdeg = degree[source]
		tdeg = degree[target]
		knn[sdeg][tdeg] += 1
		knn[tdeg][sdeg] += 1
	nn = [];
	for i in range(0, len(degree)):
		sumk = 0
		score = 0
		for j in range(0, len(degree)):
			sumk += knn[i][j]
			score += j * knn[i][j]
			
		if sumk != 0:
			nn.append(score/sumk)
		else:
			nn.append(0)

	print nn
	return nn

	
if __name__ == '__main__':
	db = ""
	itemtype = ""
	ipaddress = ""
	cuisine = ""
	parser=OptionParser()
	parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="localhost")
        parser.add_option("-t", "--itemtype", dest="itemtype", help="item type i.e. recipes/cookbooks to be parsed and added", default="recipes")
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="hawaiian")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")

        options, arguments = parser.parse_args()
        print "ipaddress: " + options.ipaddress
        print "item type: " + options.itemtype
        print "db name: " + options.db
	print "cuisine: " + options.cuisine
	
	json_file =   "data/" + options.cuisine + "_dbg.json"
	G = nx.Graph()
	d = json.load(open(json_file));
	
	edges = [el[2]['value'] for el in d['edges']];

	sortedIndices = np.argsort(edges);
	siList = sortedIndices.tolist()
	siList.reverse()
	
	toRemoveList = siList[min(10000, len(siList)):]
	toRemoveList.sort()
	toRemoveList.reverse()

	toRemoveNodes = {}
	for index in toRemoveList: # remove all other edges
		edge = d['edges'][index]
		if edge[0] not in toRemoveNodes:
			toRemoveNodes[edge[0]] = 1
		else:
			degToRemove = toRemoveNodes.get(edge[0])
			toRemoveNodes[edge[0]] = degToRemove + 1;

		if edge[1] not in toRemoveNodes:
			toRemoveNodes[edge[1]] = 1
		else:
			degToRemove = toRemoveNodes.get(edge[1])
			toRemoveNodes[edge[1]] = degToRemove + 1;

		d['edges'].pop(index)

	for node in d['nodes']:
		if node[0] in toRemoveNodes:
			node[1]['degree'] = node[1]['degree']-toRemoveNodes[node[0]]
			if node[1]['degree'] == 0:
				d['nodes'].remove(node)

	G.add_nodes_from(d['nodes'])
	G.add_edges_from(d['edges'])
	

	#Centrality Measures:
	print "Node wise metrics: "
	print "Networkx deg centrality: "
	print degree_centrality(G)

	print "closeness_centrality: " 
	print closeness_centrality(G)

	print "betweeness centrality: "
	print betweenness_centrality(G)
	#print "Edge betweeness: "
	#print edge_betweenness_centrality(G)

	print "eigen vector centrality: " 
	print eigenvector_centrality(G)

	print "communicability centrality: "
	print communicability_centrality(G)

	#print "closeness vitality: " 
	#print closeness_vitality(G)

	print "Assortativity: " 
	print degree_assortativity_coefficient(G)
	
	print "Neighbour Connectivity: " 
	print average_neighbor_degree(G)
	
	print "Avg degree connectivity: " 
	print average_degree_connectivity(G)
	
	print "Avgf degree connectivity: k nearest neighbours" 
	print k_nearest_neighbors(G)

	print "Clustering coefficient: " 
	print clustering(G)
	
	print "Graph level metrics"
	print "transitivity:"
	print transitivity(G)

	print "Average clustering coefficient: " 
	print average_clustering(G)
	
#	print "Communicability centrality: "
#	print communicability(G)

	print "Diameter"
	print diameter(G)
	
	print "Radius: " 
	print radius(G)

	print "Eccentricity: "
	print eccentricity(G)
	
	sparseGraph = SparseGraph.fromNetworkXGraph(G)

	print "Size"
	print sparseGraph.size

	#1. mean degree
	degrees = sparseGraph.degreeSequence()
	sumDegree = np.sum(degrees)
	meanDegree = sumDegree / len(degrees)
	print "Mean Degree"
	print meanDegree

	#2. diameter
	print "SG Diameter"
	print sparseGraph.diameter()


	#3. avg path length
	distances = sparseGraph.findAllDistances()
	print "Avg Path"
	totalDistance  = np.sum(distances);
	avgPath = float(totalDistance)/(float(len(degrees))*float(len(degrees)-1))
	print avgPath
	
	print "Density: "
	print sparseGraph.density()

	print "Degree Distribution: "
	print sparseGraph.degreeDistribution()


	# to compute
	print "TO COMPUTE - GRAPH CENTRALITIES"	
		
	#network statistics
	#4. clustering coefficient - node wise, graph wise
	print "Clustering Coefficient: "
	print sparseGraph.clusteringCoefficient()
	adjacencyMatrix = sparseGraph.adjacencyMatrix()
	[gc, lcc] = computeNodeWiseClusteringCoefficient(adjacencyMatrix, degrees)
	print gc

	#6. KNN
	print "Neighbor Connectivity"
	nn = getNeighborConnectivity(sparseGraph, degrees)
	print nn 

	#5. assortative coefficient
	print "Assortativity"
	r = getAssortativity(sparseGraph, degrees)
	print r

	#7. centrality 
	#7a. degree centrality - node wise, graph wise
	deg_centrality= []
	for i in range(0, len(degrees)):
		deg_centrality.append(float(degrees[i])/float(sparseGraph.getNumVertices() - 1))
	max_centrality = max(deg_centrality)
	#graph centrality
	graph_centrality = 0
	for i in range(0, len(degrees)):
 		graph_centrality += (max_centrality - deg_centrality[i])
	graph_centrality /= float(len(degrees)-1)*float(len(degrees)-2)
	print "Degree centrality: " + str(graph_centrality)
	print "Node wise degree centrality: " 
	print deg_centrality

	
	#7b. betweenness centrality - node wise, graph wise
	print "Betweenness: " 
	print sparseGraph.betweenness()	

	#7c. closeness centrality - node wise, graph wise
	closeness_centrality = []
	for i in range(0, len(degrees)):
		sumDistances = 0
		for j in range(0, len(degrees)):
			sumDistances += distances[i][j]
		closeness_centrality.append(float((len(degrees) -1)/sumDistances))
	max_centrality = max(closeness_centrality)
	graph_centrality = 0
	for i in range(0, len(degrees)):
		graph_centrality += (max_centrality - closeness_centrality[i])
	graph_centrality = ((2*len(degrees)) -3) * graph_centrality
	graph_centrality /= float(len(degrees)-1) *float(len(degrees) -2)
	print "Closeness: " + str(graph_centrality) 
	print "Node wise closeness centrality: "
	print closeness_centrality
 
	#7d. eigen vector centrality - node wise, graph wise
		
