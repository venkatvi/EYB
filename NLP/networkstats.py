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
	


	#Centrality Measures:
	print "Computing Node wise metrics... "
	print "Networkx deg centrality..."
	deg = degree_centrality(G)


	print "Closeness_centrality..." 
	clo = closeness_centrality(G)

	print "betweeness centrality ... "
	bet = betweenness_centrality(G)
	#print "Edge betweeness: "
	#print edge_betweenness_centrality(G)

	print "eigen vector centrality... " 
	eig = eigenvector_centrality(G)

	print "communicability centrality..."
	comc = communicability_centrality(G)

	#print "closeness vitality: " 
	#print closeness_vitality(G)

	print "Neighbour Connectivity..." 
	andeg = average_neighbor_degree(G)
	
	print "Avg degree connectivity..." 
	anco = average_degree_connectivity(G)
	
	print "Avgf degree connectivity: k nearest neighbours" 
	knn = k_nearest_neighbors(G)

	print "Clustering coefficient..." 
	cc =  clustering(G)
	

	f = open("../coquere/ingredientNets/data/" + options.cuisine + "_nodeMetrics.csv" , "wb");
	f.write("node,degree,closeness,betweeness,eigenvector centrality,communicability,avg neighbor degree,clustering coefficient\n");
	for key in deg.keys():
		if key != "":
			f.write(key +"," +str(deg[key]) 
				+ "," + str(clo[key])
				+ "," + str(bet[key])
				+ "," + str(eig[key])
				+ "," + str(comc[key])
				+ "," + str(andeg[key])
				+ "," + str(cc[key]) + "\n" );
	f.close()

	print "Computing Graph level metrics..."
	print "transitivity..."
	trans =  transitivity(G)

	print "Average clustering coefficient..." 
	avcc =  average_clustering(G)
	
#	print "Communicability centrality: "
#	print communicability(G)

	print "Diameter..."
	dia =  diameter(G)
	
	print "Radius ..." 
	rad = radius(G)

	print "assortativity..." 
	asco = degree_assortativity_coefficient(G)

	f = open("../coquere/ingredientNets/data/graphMetrics.csv" , "a")
	f.write(options.cuisine +", " + str(dia) + "," + str(rad) + "," + str(asco) + "," + str(trans) + "\n");
	f.close();	


	print "Eccentricity: "
	ecc = eccentricity(G)

