import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
import d3py

if __name__ == '__main__':
	#visualize as graph
	B = nx.Graph()
	B.add_nodes_from(leafs.keys(), bipartite=0)
	B.add_nodes_from(globalIngredMap.keys(), bipartite=1)
	for key in leafs.keys():
		ingredients = leafs[key]
		for ingredient in ingredients:
			B.add_edges_from([(key, ingredient)])
			B[key][ingredient]['value'] = edgeStrength[key+"_"+ingredient]

	'''
	nx.draw(B)

	
	with d3py.NetworkXFigure(B, width=1024, height=724, host='localhost') as p:
		p+= d3py.ForceLayout()
		p.css['.node'] = {'fill': 'blue', 'stroke': 'magenta'}
		p.css['.link'] = {'stroke': 'red', 'stroke-width' :'3px'}
		p.show()
	
	#plt.savefig('pakistani.png')
	nx.write_graphml(B, 'pakistani.graphml', encoding='utf-8')	
	#nx.write_gexf(B, 'pakistani.gexf', encoding='utf-8')
	#create adjacency matrix
	'''
#
