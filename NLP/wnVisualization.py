import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt


def addChildren(G, parentName):
	childSynsets = wn.synset(parentName).hyponyms()
	print "addingChildren for " + parentName + " count: " + str(len(childSynsets))
	for child in childSynsets:
		G.add_node(child.name, defi=child.definition, name=child.name)
		G.add_edge(G.node[parentName]['name'], child.name)
		print " found child " + child.name + " for parent " + parentName
		addChildren(G, child.name)
	return G

def constructGraph(rootName):
	print "initGraph: " + rootName
	G = nx.DiGraph()
	rootSynsets = wn.synsets(rootName)
	for root in rootSynsets:
		G.add_node(root.name, defi=root.definition, name=root.name)
		addChildren(G, root.name)
		return G
	
	
if __name__ == '__main__':
	G = constructGraph("cashew_nuts")
	entitySynsets = wn.synsets("entity")[0].hyponyms()
	for entity in entitySynsets:
		G.add_node(entity.name, defi=entity.definition, name=entity.name)
		addChildren(G, entity.name)

	#write network data into json
	dumps = json_graph.dumps(G)

	with open(json_file, 'w') as file:
		file.write(dumps);



