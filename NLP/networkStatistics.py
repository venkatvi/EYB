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
	
	json_file =   options.cuisine + ".json"
	G = nx.Graph()
	d = json.load(open(json_file));
	G.add_nodes_from(d['nodes'])
	G.add_edges_from(d['edges'])
	
	
	sparseGraph = SparseGraph.fromNetworkXGraph(G)

	#todo:
	#0. size 
	print "Size"
	print sparseGraph.size

	#1. mean degree
	degrees = sparseGraph.degreeSequence()
	sumDegree = np.sum(degrees)
	meanDegree = sumDegree / len(degrees)
	print "Mean Degree"
	print meanDegree

	#2. diameter
	print "Diameter"
	print sparseGraph.diameter()


	#3. avg path length
	distances = sparseGraph.findAllDistances()
	print "Avg Path"
	totalDistance  = np.sum(distances);
	avgPath = float(totalDistance)/(float(len(degrees))*float(len(degrees)-1))
	print avgPath
			
	#network statistics
	#4. clustering coefficient - node wise, graph wise
	print "Clustering Coefficient: "
	print sparseGraph.clusteringCoefficient()
	adjacencyMatrix = sparseGraph.adjacencyMatrix()
	[gc, lcc] = computeNodeWiseClusteringCoefficient(adjacencyMatrix, degrees)
	print gc

	#5. assortative coefficient
	print "Neighbor Connectivity"
	nn = getNeighborConnectivity(sparseGraph, degrees)

	print "Assortativity"
	r = getAssortativity(sparseGraph, degrees)
	print r

	#6. KNN
	#7. centrality 
	#7a. degree centrality - node wise, graph wise
	#7b. betweenness centrality - node wise, graph wise
	print "Betweenness: " 
	print sparseGraph.betweenness()	

	#7c. closeness centrality - node wise, graph wise
	#7d. eigen vector centrality - node wise, graph wise

	#8. Triange sequence
	print "Triangle Sequence: "
	print sparseGraph.triangleSequence() 



	#other interesting features of sparse graph
	print sparseGraph.fitPowerLaw()
		
	print "Degree Distribution: "
	print sparseGraph.degreeDistribution()

	print "Density: "
	print sparseGraph.density()


