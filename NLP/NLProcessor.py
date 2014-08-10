from __future__ import division
import os
import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
from networkx.linalg.graphmatrix import *
import numpy as np
from optparse import OptionParser
from pymongo import Connection
import simplejson as json
import csv
def getCuisineId(cuisineName):
	if cuisineName == 'french':
		return 1
	elif cuisineName == 'italian':
		return 2
	elif cuisineName == 'indian':
		return 3
	elif cuisineName == 'chinese':
		return 4
	elif cuisineName == 'spanish':
		return 5
	elif cuisineName == 'mexican':
		return 6
	elif cuisineName == 'irish':
		return 7
	elif cuisineName == 'german':
		return 8
	elif cuisineName == 'russian':
		return 9
	elif cuisineName == 'polish':
		return 10
	elif cuisineName == 'thai': 
		return 11
	elif cuisineName == 'vietnamese':
		return 12
	elif cuisineName == 'cambodian':
		return 13
	elif cuisineName == 'caribbean':
		return 14
	elif cuisineName == 'hawaiian':
		return 15
	elif cuisineName == 'south-american':
		return 16
	elif cuisineName == 'african':
		return 17
	elif cuisineName == 'australian':
		return 18
	elif cuisineName == 'brazilian':
		return 19
	elif cuisineName == 'moroccan':
		return 20
	elif cuisineName == 'ethiopian':
		return 21
	elif cuisineName == 'pakistani':
		return 22
	elif cuisineName == 'greek':
		return 23
	else:
		return -1

def appendColumns(mat, ingredIds, cuisineIds, matType):
	dim = mat.shape;
	print dim
	mat = np.append(mat, ingredIds, axis=1)
	mat = np.append(mat, cuisineIds, axis=1)
	typeCol = np.ones([dim[0], 1])*matType
	print typeCol.shape
	mat = np.append(mat, typeCol, axis=1)
	return mat

#checks if ingredient is food
def isFood(word, level, isRice):
	synsets = []
	if level == 0:
		synsets = wn.synsets(word)
	else:
		synset = wn.synset(word)
		synsets = { synset }
	if len(synsets) > 0:
		for synset in synsets:
			parents = synset.hypernyms()
			if len(parents) > 0:
				for parent in parents:
					if "food" in parent.name or "edible" in parent.name or "herb" in parent.name:
						return {'isFood': 1, 'Parent':parent}
					else:
						result = isFood(parent.name, level+1, isRice)
						if result['isFood'] == 1:
							return result # you dont have to parse other parents
						else:
							continue # finish parsing other parents

		#if done traversing all parents for all synsets:
		return {'isFood': 0, 'Parent': 'None'}
	else:
		return {'isFood': 0, 'Parent': 	'None'}

#checks if a  phrase is ingredient
def isCompleteTextFood(nCompleteText):
	completeSynsets = wn.synsets(nCompleteText)
	if len(completeSynsets) > 0:
		return isFood(nCompleteText, 0, 0)
	else:
		return {'isFood': 0, 'Parent': 'None'}

#analyzes combination for words looking for candidate ingredient subphrases
def analyzeWordWiseSynsets(wordWiseSynsets, words, wordsLen, text):
	wnl = nltk.stem.WordNetLemmatizer()
	if len(words)>=2 :
		for i in range(0,len(words)-1):
			wordKey = words[i] + "_" + words[i+1]
			if (isCompleteTextFood(wordKey))['isFood'] == 1:
				lemma = wnl.lemmatize(wordKey, 'n')
				insertSubPhraseKey(text, wordKey, lemma, multiWordIngredMap);

			else:
				analyzeBigramSynsets(wordWiseSynsets[i:i+2], wordKey, text, wordsLen);

# reads a bigram and finds if its a potential word for ingredient
def analyzeBigramSynsets(wordWiseSynsets, wordKey, originalText, originalPhraseLength):
	words = wordKey.split("_")
	nFirst=words[0]
	nLast=words[1]
	
	wnl = nltk.stem.WordNetLemmatizer()
	if len(wordWiseSynsets) == 2:
		if wordWiseSynsets[0]['isFood'] == 0 and wordWiseSynsets[1]['isFood'] == 0 :
			print "Ingredient not recognized " + text + " wordKey: " + wordKey
			stats[statsMap['None']] += 1
		else:
			if wordWiseSynsets[0]['isFood'] == 0 and wordWiseSynsets[1]['isFood'] == 1:
				lemma = wnl.lemmatize(nLast)
				insertSubPhraseKey(originalText,wordKey,lemma,multiWordIngredMap)
			elif wordWiseSynsets[1]['isFood'] == 0 and wordWiseSynsets[0]['isFood'] == 1:
				lemma = wnl.lemmatize(nFirst)
				insertSubPhraseKey(originalText,wordKey,lemma,multiWordIngredMap)
			else:		
				insertSubPhraseKey(originalText,wordKey,1,nextIterIngredMap)			
	else:
		print "Error: INVALID combination of subphrases: " + wordKey

# inserts a subphrase of  a ingredient phase as candidate keyword into dataMap dict
def insertSubPhraseKey(parentKey, childKey, value, dataMap):
	if parentKey not in dataMap.keys():
		dataMap[parentKey] = {}
	if childKey not in dataMap[parentKey].keys():
		dataMap[parentKey][childKey] = [value] 
	else:
		if value not in dataMap[parentKey][childKey]:
			dataMap[parentKey][childKey].append(value)

#identifies keywords given a dict of words and corresponding bigram pos
def identifyKeyword(dataMap):
	wnl = nltk.stem.WordNetLemmatizer()
	for key, value in dataMap.iteritems():
		for vkey, vvalue in value.iteritems():
			vtext=vkey.replace("_", " ")
			vwords = vtext.split(" ")
			phraseLemmas = {}
			lemmatizedWord = ""	
			for word in vwords:
				if word == "chile":
					word = "chiles"
				wordLemmas = {}
				tok_text = nltk.word_tokenize(word)
				pos_text = nltk.pos_tag(tok_text)
				if 'NN'  in pos_text[0][1]:
					lemma = wnl.lemmatize(word, 'n')
					wordLemmas['n'] = lemma
				elif 'VBD' in pos_text[0][1]:
					vlemma = wnl.lemmatize(word, 'v')
					wordLemmas['v'] = vlemma
					nlemma = wnl.lemmatize(word, 'n')
					wordLemmas['n'] = nlemma
				elif 'PR' in pos_text[0][1]:
					plemma = wnl.lemmatize(word, 'n')
					wordLemmas['n'] = plemma
				elif 'JJ' in pos_text[0][1]:
					jlemma = wnl.lemmatize(word, 'a')
					wordLemmas['j'] = jlemma
					nlemma = wnl.lemmatize(word, 'n')
					wordLemmas['n'] = nlemma
				
				if len(wordLemmas.keys()) >= 1:
					if 'j' in wordLemmas.keys():
						phraseLemmas[word] = wordLemmas['j']
						lemmatizedWord += " " + wordLemmas['j']
					elif 'n' in wordLemmas.keys():
						phraseLemmas[word] = wordLemmas['n']		
						lemmatizedWord += " " + wordLemmas['n']
			lemmatizedWord = lemmatizedWord.lstrip().rstrip()			
	
			tok_text = nltk.word_tokenize(lemmatizedWord)
			pos_text = nltk.pos_tag(tok_text)
	
			prunedWord = ""
			for pos in pos_text:
				if pos[1] == 'VBD':	
					continue;
				prunedWord += " " + pos[0]
			prunedWord = prunedWord.lstrip().rstrip()
			
			dataMap[key][vkey] = prunedWord
	return dataMap		

#returns the edgeList/Weights of nodes for a given ingredientList and their co-occurence matrix
def createEdgeList(ingredList, recipeIngredMat):
	# get edgeList / weights for ingredients
	edgeList = {}
	
	for row in recipeIngredMat:
		for i in range(0, len(row)-1):
			source = ingredList[i]
			if row[i] > 0:
				for j in range(0, len(row)-1):
					# if source != target, row[j] > 0 and row[i] > 0
					if i!=j  and i <=j and row[j] > 0:
						dest = ingredList[j]
						key = source + "#" + dest
						revKey = dest + "#" + source
						if key in edgeList.keys():
							edgeList[key] += 1
						else:
							if revKey in edgeList.keys():
								edgeList[revKey] += 1
							else:
								edgeList[key] = 1
	return edgeList
#disambiguate leafs 
def disambiguateParents(parents):
	disambiguatedLeafSet = {}
	for  key in parents.keys():
		if len(parents[key]) > 1:
			kleafs = parents[key]
			commonSynset = 0
			synsets = []
			if kleafs[0] == kleafs[1]:
				disambiguatedLeafSet[key] = [kleafs[0]]
				commonSynset = 1
			else:
				for kleaf in kleafs:
					if "chile" in kleaf:
						kleaf = kleaf.replace("chile", "chili")
				  	synsets.append(wn.synsets(kleaf))
				if len(synsets[0]) == 0:
					for synset in synsets[1]:
						if isFood(synset.name, 0, 0):
							disambiguatedLeafSet[key] = [kleafs[1]]
							commonSynset = 1
				elif len(synsets[1]) == 0:
					for synset in synsets[1]:
						if isFood(synset.name, 0, 0):
							disambiguatedLeafSet[key] = [kleafs[0]]
							commonSynset = 1
				else:
					for synset in synsets[0]:
						if synset in synsets[1]:
							commonSynset = 1
							if len(kleafs[0]) > len(kleaf[1]):
								disambiguatedLeafSet[key] = [kleafs[0]]
							else:
								disambiguatedLeafSet[key] = [kleafs[1]]
							break
			if commonSynset == 0:
				for i in range(0, len(synsets[0])):
					for j in range(0, len(synsets[1])):
						hypernyms = synsets[0][i].common_hypernyms(synsets[1][j])
						for hypernym in hypernyms:
							if hypernym in synsets[0]:
								commonSynset = 1
								disambiguatedLeafSet[key] = [kleafs[0]]
							elif hypernym in synsets[1]:
								commonSynset = 1
								disambiguatedLeafSet[key] = [kleafs[1]]
							elif "food" in hypernym.name:
								commonSynset =1
								disambiguatedLeafSet[key] = [kleafs[0]]
								disambiguatedLeafSet[key].append(kleafs[1])
								break
	
	return disambiguatedLeafSet
#find max path similarity
def findMaxPathSimilarity(ingredSynsets, foodSynsets):
	maxPathSimilarity = 0
	for synseta in ingredSynsets:
		for synsetb in foodSynsets:
			pathSim = wn.path_similarity(synseta, synsetb)
			if pathSim > maxPathSimilarity: 
				maxPathSimilarity = pathSim
	return maxPathSimilarity
#chooseCandidatePhrases
def chooseCandidatePhrases(ingredient):
	if "jack" in ingredient.lower() and ("cheese" in ingredient or "pepper" in ingredient):
		ingredient = "cheese";
	ingredParts = ingredient.split(" ")
	text = nltk.wordpunct_tokenize(ingredient)
	pos = nltk.pos_tag(text)
	if len(pos) == 0:
		return []
	# Both ingreds are food related words. Choose one depending upon the following conditions. 
	# pomegranate juice - score nouns related to food - pick the one which has a better score
	# stick noodle - varied meanings of stick ejects it out of context against noodle
	foodIngredParts = [];
	scores = {}
	ingredSynsets = []
	totalScore = 0;
	for ingred in ingredParts:
		synsets = wn.synsets(ingred)
		#for each synset in synsets for "pomegranate", check if there is any hypernym which has food
		totalSynsets = 0;
		foodSynsets = 0;
		for synset in synsets:
			hypernyms = synset.hypernym_paths();
			for hypernymSet in hypernyms:
				for hypernym in hypernymSet:
					if 'food' in hypernym.name	or 'edible' in hypernym.name or 'herb' in hypernym.name:
						foodSynsets = foodSynsets + 1;
						break;
				totalSynsets = totalSynsets + 1;	
		foodLikelihood = foodSynsets/totalSynsets;
		scores[ingred] = foodLikelihood
		if foodLikelihood >= 0.1:
			foodIngredParts.append(ingred);
		totalScore = totalScore + scores[ingred]

	if len(foodIngredParts) == 0:
		print "Ingredient not candidated: " 
		print pos
		print scores
	
	return foodIngredParts
	
#disambiguate leafs 
def disambiguateLeafs(leafs):
	leafKeys = sorted(leafs.keys())
	synsets = {}
	toRemove = ['stick', 'ingredient', 'sauce', 'paste']
	dupSynsets = {}
	splitSynsets = {}
	for key in leafKeys:
		synsets[key] = wn.synsets(key)
		
	for keya in leafKeys:
		combinedKey = keya.replace(" ", "_")
		if len(synsets[keya]) == 0 and len(wn.synsets(combinedKey)) == 0:
			candidates = chooseCandidatePhrases(keya) 
			
			if len(candidates) == 0:
				toRemove.append(keya)
			else:
				splitSynsets[keya] = candidates
				toRemove.append(keya)
		else:
			if len(synsets[keya]) == 0:
				synsets[keya] = wn.synsets(combinedKey)
			for keyb in leafKeys:
				if len(synsets[keyb]) > 0:
					commonSubset = 0
					if keya != keyb and keya not in dupSynsets.keys() and keyb not in dupSynsets.keys(): 
						if keya == "dry_mustard" and keyb == "mustard":
							print "Disambiguating:" + keya + ":" + keyb
						for synseta in synsets[keya]:
							for synsetb in synsets[keyb]:
								toWSD = 0
								dupKey = keya
								if synseta == synsetb:
									# only if synset contains food
									result = isFood(synseta.name.split(".")[0], 0,0)
									if result['isFood'] == 1:
										toWSD = 1
								if toWSD:
									otherKey = keyb if (keya == dupKey) else keya
									if dupKey in dupSynsets.keys():
										if otherKey not in dupSynsets[dupKey]:
											dupSynsets[dupKey].append(otherKey)
									else:
										dupSynsets[dupKey] = [otherKey]
									toRemove.append(dupKey)
									commonSubset = 1
									break
	return [splitSynsets, dupSynsets, toRemove]	

#split ingredient into multiple ingredients
def splitIngredient(keyLeaf, valueLeafs, parents, leafs):
	pparents = leafs[keyLeaf]
	for parent in pparents:
		for newLeaf in valueLeafs:
			if newLeaf not in leafs.keys():
				leafs[newLeaf] = [parent]		
			else:
				leafs[newLeaf].append(parent)
			if newLeaf not in parents[parent]:
				parents[parent].append(newLeaf)
			if keyLeaf in parents[parent]:
				parents[parent].remove(keyLeaf)
	leafs.pop(keyLeaf)				
	return [parents, leafs]

#replace ingredient by another ingredient
def replaceIngredient(keyLeaf, valueLeaf, parents, leafs):
	if keyLeaf in leafs.keys():
		pparents = leafs[keyLeaf]
		#for each parent in keyLeaf which needs to be replaced. 
		for parent in pparents:
			if keyLeaf in parents[parent]:
				parents[parent].remove(keyLeaf)
			if valueLeaf not in parents[parent]:
				parents[parent].append(valueLeaf)
	
		if valueLeaf not in leafs.keys():
			leafs[valueLeaf] = pparents
		else:
			for parent in pparents:
				if parent not in leafs[valueLeaf]:
					leafs[valueLeaf].append(parent)
		leafs.pop(keyLeaf)

	return	[parents, leafs]
#visualize a network
def visualizeNetwork(nodes, edges, json_file):
	#visualize as graph
	B = nx.Graph()
	B.add_nodes_from(nodes)
	for edge, weight in edges.iteritems():
		nodes=edge.split("#")
		error =0
		for node in nodes:
			if node in B:
				if not 'degree' in B.node[node]:
					B.node[node]['degree'] = 1
				else:
					B.node[node]['degree'] += 1
			else:
				print "No node found: " + node
				error = 1
				break;
		if error == 0:
			B.add_edges_from([(nodes[0], nodes[1])]) 
			B[nodes[0]][nodes[1]]['value'] = weight

	#write network data into json
	dumps = json_graph.dumps(B)

	with open(json_file, 'w') as file:
		file.write(dumps);

	return B
#	np.savetxt('ingredCo_pakistani.txt', ingredCo, delimiter=",")



#class to access EatYourBooksDB (mongodb)
class EatYourBooksDB:
	connection = None
	db = None
	item_collection = None
	def __init__(self, dbname, ipaddress, item_type):
		self.connection = Connection(ipaddress, 27017)
		db_name = dbname;
		collection_name = item_type
		self.db = self.connection[db_name]
		self.item_collection = self.db[collection_name]
	def get_recipe_vs_ingredient(self, cuisine):
		recipes = self.item_collection.find({'cuisine': cuisine})
		return recipes
		
	def get_distinct_ingredients_by_cuisine(self, cuisine):
		recipes = self.item_collection.find({'cuisine': cuisine})
		print "Ingred Count: " + str(len(list(recipes.distinct('ingredients'))))
		return list(recipes.distinct('ingredients'))

	
statsMap = {'Complete': 0, 'None': 1, 'First': 2, 'Last': 3, 'Both': 4}
stats = [0,0,0,0,0]
multiWordIngredMap = {}
nextIterIngredMap = {}
notFoundIngredMap = {}
globalIngredMap = {}
if __name__ == '__main__':
	home_folder = os.getenv("HOME")
	parser=OptionParser()
	parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="localhost")
        parser.add_option("-t", "--itemtype", dest="itemtype", help="item type i.e. recipes/cookbooks to be parsed and added", default="recipes")
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="hawaiian")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")
        parser.add_option("-p", "--path", dest="rootPath", help="root location to store results", default=home_folder + "/EYB")

        options, arguments = parser.parse_args()
        print "ipaddress: " + options.ipaddress
        print "item type: " + options.itemtype
        print "db name: " + options.db
	print "cuisine: " + options.cuisine
	
	#lines = [line.strip() for line in open('data/pakistani_ingredients.txt')]

	#Connect to DB to get ingredient list	
	db = EatYourBooksDB(options.db, options.ipaddress, options.itemtype)
	dbRecipes = db.get_recipe_vs_ingredient(options.cuisine)

	#Get distinct ingredients found in recipes
	distinctIngredList=sorted(db.get_distinct_ingredients_by_cuisine(options.cuisine))
		
	for line in distinctIngredList:
		text = line.lstrip().rstrip()
		#text = text.decode('utf-8')
		
		globalIngredMap[text] = "";
		words = text.split(" ")
		nCompleteText = text.replace(" ", "_")
		#if complete text is a food ingredient: e.g. black_pepper
		if (isCompleteTextFood(nCompleteText))['isFood'] == 1:
			wnl = nltk.stem.WordNetLemmatizer()
			stats[statsMap['Complete']] += 1 
			lemma = wnl.lemmatize(nCompleteText, 'n')
			insertSubPhraseKey(text,text,lemma, multiWordIngredMap)
	
		else:
			#Get wordwise synsets which are food synsets
			wordWiseSynsets = [];
			for word in words:
				wordWiseSynsets.append(isFood(word, 0, 0))	
			# add to not found list if word synset is not found
			if len(wordWiseSynsets) == 1 and words[0] not in notFoundIngredMap.keys():
				notFoundIngredMap[words[0]] = 1
			else:
				#analyze pairwise words for combinatorial context
				analyzeWordWiseSynsets(wordWiseSynsets, words, len(words), text)
	
	#combinatorial identification of keyword/ context
	nextIterIngredMap = identifyKeyword(nextIterIngredMap)

	
	leafs = {}
	parents = {}
	#for each key in globalIngredMap, check if key in multiword or nextiteringredmap
	for key in globalIngredMap.keys():
		keyFound = 0
		if key in multiWordIngredMap.keys():
			# add values to globalIngred
			globalIngredMap[key] = multiWordIngredMap[key]
			keyFound = 1
			#for each child dict in multiwordingredmap  - add parent to leaf, add leaf to parent ingredient
			for nKey, nValues in multiWordIngredMap[key].iteritems():
				for value in nValues:
					# leafs degree can be computed 
					value = value.strip().lower()
					pkey = key.strip().lower()
					if value in leafs.keys():
						leafs[value].append(pkey)
					else:
						leafs[value] = [pkey];
					if pkey in parents.keys():
						parents[pkey].append(value)
					else:	
						parents[pkey] = [value]
				
		if key in nextIterIngredMap.keys():
			# add values to globalIngredMap
			if keyFound == 1:
				nMaps = nextIterIngredMap[key]
				for nKey, nValue in nMaps.iteritems():
					globalIngredMap[key][nKey] = nValue
		  	else:
				globalIngredMap[key] = nextIterIngredMap[key]		

			#for each child dict in nextInterIngredMap - add parent to leaf, add leaf to parent ingred
			for nKey, nValues in nextIterIngredMap[key].iteritems():
				nvalues = nValues.strip().lower()
				pkey = key.strip().lower()
				if nvalues in leafs.keys():
					leafs[nvalues].append(pkey)
				else:
					leafs[nvalues] = [pkey]
				if pkey in parents.keys():
					if nvalues not in parents[pkey]:
						parents[pkey].append(nvalues)
				else:
					parents[pkey] = [nvalues]
	
	

	disambiguateParents = disambiguateParents(parents)
	
	for parent, dleafs in disambiguateParents.iteritems():
		oldLeafs = parents[parent]
		for leaf in oldLeafs:
			if leaf not in dleafs:
				if len(leafs[leaf]) == 1:
					leafs.pop(leaf)	
				else:
					leafs[leaf].remove(parent)
		for leaf in dleafs:
			if leaf in leafs.keys():
				leafs[leaf].append(parent)
			else:
				leafs[leaf] = [parent]
		parents[parent] = dleafs
	
	[leafsToSplit, leafsToMerge, leafsToRemove] = disambiguateLeafs(leafs)			
	print "-----------------Leafs to split -----------------------------------"
	print leafsToSplit
	print "-----------------Leafs to merge -----------------------------------"
	print leafsToMerge
	print "-----------------Leafs to remove -----------------------------------"
	print leafsToRemove

	splitLeafListFile = options.rootPath + "/network/data/" + options.cuisine + "_splitLeafs_dbg.csv"
	f = open(splitLeafListFile, "wb")
	for keyLeaf, valueLeafs in leafsToSplit.iteritems():
		#remove parents of keyLeaf and push them to values in split leafs
		[parents, leafs] = splitIngredient(keyLeaf, valueLeafs, parents, leafs)
		f.write(keyLeaf + ",")
		for item in valueLeafs:
			f.write("%s," % item)
		f.write("\n")
	f.close() 

	mergeLeafListFile = options.rootPath + "/network/data/" + options.cuisine + "_mergeLeafs_dbg.csv"
	f = open(mergeLeafListFile, "wb")
	for keyLeaf, valueLeafs in leafsToMerge.iteritems():
		#move all entries of keyLeaf to valueLeaf
		#remove entry keyLeaf in parents, leafs
		if len(valueLeafs) == 1:
			valueLeaf = valueLeafs[0]
			[parents, leafs] = replaceIngredient(keyLeaf, valueLeafs[0], parents, leafs)
			f.write(keyLeaf + "," + valueLeaf + "\n");
		else:
			print "Trouble: " + keyLeaf
			print valueLeafs
	f.close()

	#check if all toRemove are already removed from leafs
	removeLeafListFile = options.rootPath + "/network/data/" + options.cuisine + "_removeLeafs_dbg.csv"
	f = open(removeLeafListFile, "wb")
	for ingred in leafsToRemove:
		#if not ingred:
		#	print "Empty String"
		#else:
		f.write(ingred + "\n");
		if ingred in leafs.keys():
			if ingred in leafsToMerge.keys():
				mergeIngred = leafsToMerge[ingred]
				if len(mergeIngred) == 1:
					[parents, leafs] = replaceIngredient(ingred, mergeIngred[0], parents, leafs)
				else:
					print "Trouble: " +  keyLeaf
					print mergeIngred
			else:
				print "Error: leaf not found in merge list: " + ingred
				# handle empty string removal
				if ingred in leafs.keys():
					pparents = leafs[ingred]
					#for each parent in keyLeaf which needs to be replaced. 
					for parent in pparents:
						if keyLeaf in parents[parent]:
							parents[parent].remove(ingred)
					leafs.pop(ingred)

	f.close();

	#Get distinct parsed/NLPed ingredients found using NLTK
	ingredLeafs = sorted(leafs.keys())

	#create recipes vs original ingreds, recipes vs leafs (parsed out of NLP)
	recipeLeafMat = []

	rowIndex=0
	
	#List of recipe names ? why ?
	recipes = []
	i = 0
	for recipe in dbRecipes:
#		ingredVec = []
		leafVec = []
		for i in range(0, len(ingredLeafs)):
			leafVec.append(0)

		for ingredient in recipe["ingredients"]:
			ingredient = ingredient.strip()
			if ingredient:
				# Mark recipe[i][ingred] = 1
				ingredIndex = distinctIngredList.index(ingredient)

				#find ingredients leafs in parents
				if ingredient in parents.keys():
					ileafs = parents[ingredient]
					for leaf in ileafs:
						if leaf in ingredLeafs:
							leafIndex = ingredLeafs.index(leaf)
							if leafIndex >= 0:
								leafVec[leafIndex] = 1
					
		recipeLeafMat.append(leafVec)
		rowIndex = rowIndex+1
		

	#get cuisineId
	cuisineId = getCuisineId(options.cuisine)
	ingredFile = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_ingredLeafs_dbg.txt"
	np.savetxt(ingredFile, ingredLeafs, fmt="%s", delimiter=",")	

	#rLMat = np.asarray(recipeLeafMat)
	rLMat = np.matrix(recipeLeafMat)
	freqCount = rLMat.sum(axis=0)
	
	rLArray = np.asarray(rLMat)
	rLT = rLArray.T
	corrcoeff = np.corrcoef(rLT)
	
	

	#statsFile = options.rootPath + "/network/data/stats_dbg.txt"
	#ingredsPerRecipe = rLMat.sum(axis=1)
	#avgIngredsPerRecipe = np.average(ingredsPerRecipe)
	#stdIngredsPerRecipe = np.std(ingredsPerRecipe)
	#sf = open(statsFile, 'a');
	#sf.write(options.cuisine + "," + str(avgIngredsPerRecipe) + "," + str(stdIngredsPerRecipe) +"\n");
	#sf.close();
	#lfreqCount = np.array(freqCount)[0].tolist()
	#dim = rLMat.shape
	#recipeCount = dim[0]
	
	#recipeFile = options.rootPath + "/network/data/recipeCounts_dbg.csv";
	#rf = open(recipeFile, 'a');
	#rf.write(options.cuisine + "," + str(recipeCount) + "\n");
	#rf.close();

	print "------------------------- Network json on ingredient co-occurences-------------------------------"
	leafEdges = createEdgeList(ingredLeafs, recipeLeafMat);
	filename = options.rootPath + "/coquere/ingredientNets/data/" +  options.cuisine + "_dbg.json"
	G = visualizeNetwork(ingredLeafs, leafEdges, filename)
	
	# write co-occurrence of this network  as cuisine_cooc.json
	A = adjacency_matrix(G, ingredLeafs, weight='value')
	A = A.tolist()
	dim = rLMat.shape
	recipeCount = dim[0]
	ingredCount = dim[1]

		
	# reiterate co-occurence matrix
	Co = np.zeros([dim[1], dim[1]])
	
	ingredIds = np.zeros([dim[1], 1])
	cuisineCol = np.zeros([dim[1], 1])

	corrCoeffvsCoocFile = options.rootPath + "/network/data/" + options.cuisine + "_corrcoeff_cooc_dbg.csv"	
	cf = open(corrCoeffvsCoocFile,'wb')
	for i in range(0, dim[1]-1):
		ingredIds[i] = i;
		cuisineCol[i] = cuisineId;
		for j in range(0, dim[1]-2):
			Co[i][j] = A[i][j]/recipeCount;
			if i <=j: 
				cf.write(ingredLeafs[i] + "," + ingredLeafs[j] + "," + str(Co[i][j]) + "," + str(A[i][j]) +  "," + str(corrcoeff[i][j]) + "\n");
	cf.close();
		
'''					

	Co = appendColumns(Co, ingredIds, cuisineCol, 1);
	
	coocFile = options.rootPath + "/network/data/" + options.cuisine + "_cooc_dbg.csv"
	ingredFile = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_ingredLeafs_dbg.txt"
	
	#np.savetxt(matFile, rLMat, fmt='%u', delimiter=",")
	np.savetxt(coocFile, Co, fmt='%5.3f', delimiter=",")
	np.savetxt(ingredFile, ingredLeafs, fmt="%s", delimiter=",")

	json.dump(dict(nodes=[[n, G.node[n]] for n in G.nodes()],
	edges=[[u,v,G.edge[u][v]] for u,v in G.edges()]),
	open(options.rootPath + "/network/data/" + options.cuisine + "_dbg.json", 'w'), indent=2)

	edges=[[u,v,G.edge[u][v]['value']] for u,v in G.edges()];
	edgeDistFile = options.rootPath + "/network/data/" + options.cuisine + "_edgeDist_dbg.csv"
	with open(edgeDistFile, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(edges)

	print recipeCount
	print ingredCount	
	print "-------------------------------------Over------------------------------------------------"
'''
