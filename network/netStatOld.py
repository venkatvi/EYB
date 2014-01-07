from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
import numpy as np
from optparse import OptionParser
from pymongo import Connection

if __name__ == '__main__':

	freqCount = rLMat.sum(axis=0)
	lfreqCount = np.array(freqCount)[0].tolist()

	freqFrac = {};
	for j in range(0, len(lfreqCount)):
		if lfreqCount[j] not in freqFrac.keys():
			if ingredLeafs[j] != "":
				freqFrac[lfreqCount[j]] = [ingredLeafs[j]]
		else:
			if ingredLeafs[j] != "":
				freqFrac[lfreqCount[j]].append(ingredLeafs[j])


	freqFracKeys = sorted(freqFrac.keys())

	#writing frequency distribution 
	f = open('../coquere/ingredientNets/data/' + options.cuisine + "_freq.csv", 'w')
	f.write("frequency,frac\n");
	for i in range(0, len(freqFracKeys)):
		freq = freqFracKeys[i] ;
		numNodesWithFreq = len(freqFrac[freq]);
		f.write(str(np.log10(freq)) + "," + str(np.log10(numNodesWithFreq)) + "\n");
	f.close()

	#computing clustering coefficient
	leafCo = [] 
	for i in range(0, len(ingredLeafs)):
		leafVec = []
		for j in range(0, len(ingredLeafs)):
			leafVec.append(0)
		leafCo.append(leafVec)
	for i in range(0, len(recipeLeafMat)):
		for j in range(0, len(ingredLeafs)):
				for k in range(0, len(ingredLeafs)):
					if recipeLeafMat[i][j] == 1 and recipeLeafMat[i][k] == 1:
						leafCo[j][k] += 1
						leafCo[k][j] += 1

	#write clustering coefficient numbers along with degree of ingredients 
	f = open('../coquere/ingredientNets/data/' + options.cuisine + "_cc.csv", 'w')
	f.write("ingredient,degree,lcc\n")
	cluscoeff = []
	gcluscoeff = 0
	degrees = []
	for i in range(0, len(ingredLeafs)):
		neighbouredges = 0;
		degree =0
		for j in range(0, len(ingredLeafs)):
			if leafCo[i][j] > 0:
				if i!=j:
					degree = degree + 1
				for k in range(0, len(ingredLeafs)):
					if leafCo[i][k] > 0 and leafCo[j][k] > 0:
						if i!=k and i !=j and j != k:
							neighbouredges = neighbouredges + 1;
		cc = float(neighbouredges) / float((degree +1) * degree);
		cluscoeff.append(cc)
		degrees.append(degree)
		gcluscoeff += cc
		f.write(ingredLeafs[i] + "," + str(degrees[i]) + "," + str(cluscoeff[i]) + "\n");
	f.close()
	gcluscoeff = gcluscoeff/len(ingredLeafs);
	
	

			
