from __future__ import division
import os
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
	d = json.load(open(json_file));
	
	f = open(options.rootPath + "/coquere/ingredientNets/data/networkdensity" + ".tsv" , "a")
	f.write(options.cuisine + "\t" + str(len(d['nodes'])) + "\t" + str(len(d['edges'])) + "\t" + stats_file + "\n");
	f.close();
if __name__ == '__main__':
	home_folder = os.getenv("HOME")
	parser=OptionParser()
	parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="23.92.17.38")
        parser.add_option("-t", "--itemtype", dest="itemtype", help="item type i.e. recipes/cookbooks to be parsed and added", default="cookbookrecipes")
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="indian")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")
        parser.add_option("-p", "--path", dest="rootPath", help="root location to store results", default=home_folder+"/EYB")

        options, arguments = parser.parse_args()
        print "ipaddress: " + options.ipaddress
        print "item type: " + options.itemtype
        print "db name: " + options.db
	print "cuisine: " + options.cuisine
	
	json_file =   options.rootPath + "/network/data/" + options.cuisine + "_cooc.json"
	calculateStats(json_file, "cooc");
	
	json_poscor_file =   options.rootPath + "/network/data/" + options.cuisine + "_ccf_pos.json"
	calculateStats(json_poscor_file, "ccf_pos");

	json_negcor_file =   options.rootPath + "/network/data/" + options.cuisine + "_ccf_neg.json"
	calculateStats(json_poscor_file, "ccf_neg");

	json_negcor_file =   options.rootPath + "/network/data/" + options.cuisine + "_pmi.json"
	calculateStats(json_negcor_file, "pmi");

	json_negcor_file =   options.rootPath + "/network/data/" + options.cuisine + "_cp.json"
	calculateStats(json_negcor_file, "cp");

