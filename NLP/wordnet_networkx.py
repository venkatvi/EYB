import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph


ingredChildCountMap = {}
ingredChildrenMap = {}
def addChildren(G, parentName):
	print "Adding children for " + parentName
	childSynsets = wn.synset(parentName).hyponyms()
	ingredChildCountMap[parentName] = len(childSynsets)
	if len(childSynsets) == 0:
		addChild(parentName, " ")	
	for child in childSynsets:
		#add parent-child map;
		addChild(parentName, child.name)
		addChildren(G, child.name)
	return G

def addChild(parent, child):
	child = child.split(".")[0]
	parent = parent.split(".")[0]
	if child.strip() == "":
		child = "NA"
	if parent  in ingredChildrenMap.keys():
		children = ingredChildrenMap[parent]
		if child not in children:
			ingredChildrenMap[parent].append(child)
	else:
		ingredChildrenMap[parent]=[child];

def constructGraph(rootName):
	G = nx.Graph()
	rootSynsets = wn.synsets(rootName)
	ingredChildCountMap['None']=len(rootSynsets)
	for root in rootSynsets:
		rootName = root.name.split(".")[0]
		addChildren(G, root.name)
	G.add_nodes_from(ingredChildrenMap.keys())
	for key in ingredChildrenMap.keys():
		children=ingredChildrenMap[key]
		G.node[key]['name']=key
		if len(children) > 1:	
			childCount=0
			for child in children:
				if child == "NA":
					print "Empty leaf"
				else:
					G.add_edges_from([(key, child)])
					childCount +=1
			G.node[key]['children']=childCount;
		else:
			if children[0] == "NA":
				print "Empty Leaf"
				G.node[key]['children']=0
			else:
				G.add_edges_from([(key, children[0])])
				G.node[key]['children'] =1
			
	return G
#def analyzeEdgeWeights(G):
	
if __name__ == '__main__':
	G = constructGraph("food")
#	G = analyzeEdgeWeights(G)
	dumps = json_graph.dumps(G)
	
	with open('wordnet_network.json', 'w') as file:
		file.write(dumps);


