from optparse import OptionParser
import numpy as np
import simplejson as json
import networkx as nx
if __name__ == '__main__':
	cuisine = ""
	netType = "";
	parser	= OptionParser()
	parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="indian")
	parser.add_option("-t", "--nettype", dest="netType", help="network type", default="cooc")
	options, arguments = parser.parse_args()
	print "cuisine:" + options.cuisine
	print "net type:" + options.netType

	recipeCount = 1;
	if (options.netType == 'cooc'):
		recipeCountFile = "/home/hduser/EYB/network/data/recipeCounts.csv";
		f = open(recipeCountFile, 'r');
		for line in f.readlines():
			val = line.strip().split(",");
			if val[0] == options.cuisine:
				recipeCount = int(val[1]);
		f.close();
	
	json_file = "data/" + options.cuisine + "_" + options.netType + ".json"
	G = nx.Graph()
	d = json.load(open(json_file))
	G.add_nodes_from(d['nodes'])
	G.add_edges_from(d['edges'])
	
	weightDistFile = 'data/' + options.cuisine + "_" + options.netType + "_wtDist.csv"
	f = open(weightDistFile, 'w')
	f.write("src,dest,wt\n");
	for edge in d['edges']:
		edgeWt = edge[2]['value']/recipeCount
		if(options.netType == 'cooc'):
			G[edge[0]][edge[1]]['weight']=edgeWt
		f.write(edge[0] + "," + edge[1] + "," + str(edgeWt) + "\n");
	f.close();
	
