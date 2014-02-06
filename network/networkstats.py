from __future__ import division
import math
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
from networkx.linalg.graphmatrix import *
import sys
def getCountries(cuisine):
	if (cuisine == "asian"):
		return ["russia", "india", "mongolia", "china", "japan", "pakistan", "afghanistan", "kazakhstan", "south korea", "thailand", "indonesia"]
	elif cuisine == "australian":
		return ["australia"]
	elif cuisine == "japanese":
		return ["japan"]
	elif cuisine == "european":
		return ["europe"]
	elif cuisine == "italian":
		return ["italy"]
	elif cuisine == "pakistani":
		return ["pakistan"]
	elif cuisine == "irish":
		return ["ireland"]
	elif cuisine == "chinese":
		return ["china"]
	elif cuisine == "german":
		return ["germany"]
	elif cuisine == "portugese":
		return ["portugal"]
	elif cuisine == "hawaiian":
		return ["hawaii"]
	elif cuisine == "moroccan":
		return ["morocco"]
	elif cuisine == "mexican":
		return ["mexico"]
	elif cuisine == "jamaican":
		return ["jamaica"]
	elif cuisine == "brazilian":
		return ["brazil"]
	elif cuisine == "thai":
		return ["thailand"]
	elif cuisine == "greek":
		return ["greece"]
	elif cuisine == "caribbean":
		return ["cuba"]
	elif cuisine == "french":
		return ["france"]
	elif cuisine == "vietnamese":
		return ["viet nam"]
	elif cuisine == "spanish":
		return ["spain"]
	elif cuisine == "polish":
		return ["poland"]
	elif cuisine == "indian":
		return ["india"]
	elif cuisine == "russian":
		return ["russian federation"]
	elif cuisine == "south-american":
		return ["bolivia, plurinational state of", "guyana","colombia", "ecuador", "peru", "chile", "argentina", "uruguay", "paraguay", "venezuela, bolivarian republic of", "brazil", "suriname", "french guiana"]
	elif cuisine == "african":
		return ["algeria", "mauritania", "guinea", "gabon", "south sudan", "tanzania", "bostwana", "libya", "egypt", "sudan", "ethiopia", "somalia", "kenya", "tanzania, united republic of", "mozambique", "zambia", "zimbabwe", "botswana", "south africa", "namibia", "angola", "nigeria",  "ghana", "niger", "chad", "ghana", "morocco", "tunisia", "mali", "burkina", "congo, the democratic republic of the", "eritrea", "djibouti", "swaziland", "lesotho", "congo", "cameroon", "central african republic", "senegal", "gambia", "guinea-bissau", "guinea", "sierra leone", "liberia", "togo", "benin", "western sahara", "uganda", "rwanda", "burundi", "cote d'ivoire", "burkina faso", "malawi"]
	else: 
		print "unknown cuisine"
		return ""


def computeDGraphCentrality(nodeCentralities):
	maxC = max(nodeCentralities)
	sumAll = 0
	n = len(nodeCentralities)
	for node in nodeCentralities:
		sumAll += maxC - node;
	return float(sumAll / float((n-1)*(n-2)))
def computeBGraphCentrality(nodeCentralities):
	maxC = max(nodeCentralities)
	sumAll = 0
	n = len(nodeCentralities)
	for node in nodeCentralities:
		sumAll += maxC - node;
	return float(sumAll / float(n-1))
def computeCGraphCentrality(nodeCentralities):
	maxC = max(nodeCentralities)
	sumAll = 0
	n = len(nodeCentralities)
	for node in nodeCentralities:
		sumAll += maxC - node;
	return float((sumAll*(2*n -3)) / float((n-1)*(n-2)))

def calculateStats(json_file, stats_file):
	G = nx.Graph()
	d = json.load(open(json_file));
	G.add_nodes_from(d['nodes'])
	G.add_edges_from(d['edges'])
	
	#Centrality Measures:
	print "Computing Node wise metrics... "
	print "Degree..."
	deg = G.degree()

	print "Networkx deg centrality..."
	degC = degree_centrality(G)


	print "Closeness_centrality..." 
	clo = closeness_centrality(G)

	print "betweeness centrality ... "
	bet = betweenness_centrality(G)
	#print "Edge betweeness: "
	#print edge_betweenness_centrality(G)

	try:
		print "eigen vector centrality... " 
		eig = eigenvector_centrality(G)
	except:
		print "Unable to converge.. "
		z = sys.exc_info()[0]
		print z
		eig = {};
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
	

	dCentralities = []
	bCentralities = []
	cCentralities = []
	eCentralities = []
	f = open(options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_" + stats_file + "_nodeMetrics.csv" , "wb");
	f.write("node,degree,degreeCentrality,closeness,betCentrality,eigenvectorCentrality,communicability,avgNeigDegree,clusCoeff\n");
	for key in deg.keys():
		if key != "":
			b=0 
			e=0
			if bet[key] > 0:
				b = np.log10(bet[key])
			if key in eig.keys() and eig[key] > 0:
				e = np.log10(eig[key])
				eCentralities.append(eig[key])
			else:
				e = 0;
				eCentralities.append(0)

			f.write(key + "," + str(deg[key])
				+ "," + str(degC[key]) 
				+ "," + str(clo[key])
				+ "," + str(b)
				+ "," + str(e)
				+ "," + str(comc[key])
				+ "," + str(andeg[key])
				+ "," + str(cc[key]) + "\n" );
			dCentralities.append(degC[key])
			bCentralities.append(bet[key])
			cCentralities.append(clo[key])
	f.close()

	print "Computing Graph level metrics..."
	print "transitivity..."
	trans =  transitivity(G)

	print "Average clustering coefficient..." 
	avcc =  average_clustering(G)
	
#	print "Communicability centrality: "
#	print communicability(G)

#	print "Diameter..."
#	dia =  diameter(G)
	
#	print "Radius ..." 
#	rad = radius(G)

	dgraph = computeDGraphCentrality(dCentralities)
	bgraph = computeBGraphCentrality(bCentralities)
	cgraph = computeCGraphCentrality(cCentralities)
	print "assortativity..." 
	asco = degree_assortativity_coefficient(G)
	
	lines = [line.strip() for line in open(options.rootPath + "/coquere/ingredientNets/data/world-country-names.tsv", 'r')]
	countryCodes = {}
	for line in lines:
		items = line.split("\t");
		if items[1] not in countryCodes.keys():
			countryCodes[items[1].lower()] = items[0]
	
	f = open(options.rootPath + "/coquere/ingredientNets/data/graphMetrics" + "_" + stats_file + ".tsv" , "a")
	countries = getCountries(options.cuisine)
	codes = []
	if len(countries) > 0:
		for country in countries:
			if country in countryCodes.keys():
				codes.append(countryCodes[country])
		if len(codes) > 0:
			for code in codes:
				f.write(options.cuisine + "\t" + str(asco) + "\t" + str(trans) + "\t" + str(avcc) + "\t" + str(dgraph) + "\t" + str(bgraph) + "\t" + str(cgraph) + "\t" + str(code) +  "\n");
	f.close();
if __name__ == '__main__':
	parser=OptionParser()
	parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="localhost")
        parser.add_option("-t", "--itemtype", dest="itemtype", help="item type i.e. recipes/cookbooks to be parsed and added", default="recipes")
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="hawaiian")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")
        parser.add_option("-p", "--path", dest="rootPath", help="root location to store results", default="/home/vaidehi/EYB")

        options, arguments = parser.parse_args()
        print "ipaddress: " + options.ipaddress
        print "item type: " + options.itemtype
        print "db name: " + options.db
	print "cuisine: " + options.cuisine
	
	json_file =   options.rootPath + "/network/data/" + options.cuisine + ".json"
	print json_file

	calculateStats(json_file, "cooc");
	
	json_poscor_file =   options.rootPath + "/network/data/" + options.cuisine + "_posNet.json"
	print json_poscor_file

	calculateStats(json_poscor_file, "posCorr");

	json_negcor_file =   options.rootPath + "/network/data/" + options.cuisine + "_negNet.json"
	print json_negcor_file


	calculateStats(json_negcor_file, "negCorr");
