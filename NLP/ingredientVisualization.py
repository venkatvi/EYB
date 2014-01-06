from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
import numpy as np
from optparse import OptionParser
from pymongo import Connection
import simplejson as json
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
def createEdgeList(ingredList, ingredCo):
	# get edgeList / weights for ingredients
	edgeList = {}
	ingredCoList = ingredCo.tolist()
	i = 0
	for row in ingredCoList:
		source = ingredList[i]
		j = 0
		for col in row:
			if i != j and i <= j:
				edgeWeight = col
				target = ingredList[j]
				if edgeWeight > 0 :
					key = source + "#" + target
					revKey = target + "#" + source
					if key in edgeList.keys():
						edgeList[key] += edgeWeight
					else:
						if revKey in edgeList.keys():
							edgeList[revKey] += edgeWeight
						else:
							edgeList[key] = edgeWeight
			j = j+1
		i = i+1

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
	ingredParts = ingredient.split(" ")
	text = nltk.wordpunct_tokenize(ingredient)
	pos = nltk.pos_tag(text)
	if len(pos) == 0:
		return []
	if (pos[0][1] == "JJ"):
		return [ingredParts[1]]
	if pos[1][1] == "PRP$":
		#possesive pronoun - chickpea's flour. return both ingredients
		iList = []
		if isFood(ingredParts[0],0,0):
			iList.append(ingredParts[0])
		if isFood(ingredParts[1],0,0):
			iList.append(ingredParts[1])
		return iList
	ingredSynsets = []
	for ingred in ingredParts:
		ingredSynsets.append(wn.synsets(ingred))
	maxPathSimilarity = [0,0];
	foodSynsets = wn.synsets("food")
	maxPathSimilarity[0] = findMaxPathSimilarity(ingredSynsets[0], foodSynsets)
	maxPathSimilarity[1] = findMaxPathSimilarity(ingredSynsets[1], foodSynsets)
	if maxPathSimilarity[0] > maxPathSimilarity[1]:	
		return [ingredParts[0]]
	else:
		return [ingredParts[1]]
	
#disambiguate leafs 
def disambiguateLeafs(leafs):
	leafKeys = sorted(leafs.keys())
	synsets = {}
	toRemove = []
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
		return list(recipes.distinct('ingredients'))

	
statsMap = {'Complete': 0, 'None': 1, 'First': 2, 'Last': 3, 'Both': 4}
stats = [0,0,0,0,0]
multiWordIngredMap = {}
nextIterIngredMap = {}
notFoundIngredMap = {}
globalIngredMap = {}
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
					value = value.strip()
					pkey = key.strip()
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
				nvalues = nValues.strip()
				pkey = key.strip()
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
	print leafsToSplit
	print leafsToMerge
	print leafsToRemove

	for keyLeaf, valueLeafs in leafsToSplit.iteritems():
		#remove parents of keyLeaf and push them to values in split leafs
		[parents, leafs] = splitIngredient(keyLeaf, valueLeafs, parents, leafs)

	for keyLeaf, valueLeafs in leafsToMerge.iteritems():
		#move all entries of keyLeaf to valueLeaf
		#remove entry keyLeaf in parents, leafs
		if len(valueLeafs) == 1:
			valueLeaf = valueLeafs[0]
			[parents, leafs] = replaceIngredient(keyLeaf, valueLeafs[0], parents, leafs)
		else:
			print "Trouble: " + keyLeaf
			print valueLeafs

	#check if all toRemove are already removed from leafs
	for ingred in leafsToRemove:
		if not ingred:
			print "Empty String"
		else:
			if ingred in leafs.keys():
				mergeIngred = leafsToMerge[ingred]
				if len(mergeIngred) == 1:
					[parents, leafs] = replaceIngredient(ingred, mergeIngred[0], parents, leafs)
				else:
					print "Trouble: " +  keyLeaf
					print mergeIngred
			


	#Get distinct parsed/NLPed ingredients found using NLTK
	ingredLeafs = sorted(leafs.keys())

	#create recipes vs original ingreds, recipes vs leafs (parsed out of NLP)
	recipeIngredMat = []	
	recipeLeafMat = []

	rowIndex=0
	
	#List of recipe names ? why ?
	recipes = []
	i = 0
	for recipe in dbRecipes:
		ingredVec = []
		leafVec = []
		for i in range(0, len(distinctIngredList)):
			ingredVec.append(0)
		for i in range(0, len(ingredLeafs)):
			leafVec.append(0)

		# to be deleted!
		recipes.append(recipe["_id"])


		for ingredient in recipe["ingredients"]:
			# Mark recipe[i][ingred] = 1
			ingredIndex = distinctIngredList.index(ingredient)
			if ingredIndex >= 0:
				ingredVec[ingredIndex] = 1
			else:
				print "Trouble: " + ingredient 

			#find ingredients leafs in parents
			if ingredient in parents.keys():
				ileafs = parents[ingredient]
				for leaf in ileafs:
					leafIndex = ingredLeafs.index(leaf)
					if leafIndex >= 0:
						leafVec[leafIndex] = 1
					
		recipeIngredMat.append(ingredVec)
		recipeLeafMat.append(leafVec)
		rowIndex = rowIndex+1
		
	
#	print recipeIngredMat
	rIMat = np.matrix(recipeIngredMat)
	rIMatT = rIMat.transpose()
	ingredCo = rIMatT*rIMat
	edges = createEdgeList(distinctIngredList, ingredCo);
	filename = "../coquere/ingredientNets/oldData/"+ options.cuisine + "/" + options.cuisine + "_allingred.json"
	visualizeNetwork(distinctIngredList, edges, filename)
	
	rLMat = np.matrix(recipeLeafMat)
	rLMatT = rLMat.transpose()
	leafCo = rLMatT * rLMat
	leafEdges = createEdgeList(ingredLeafs, leafCo);
	filename = "d3/" + options.cuisine + "/" + options.cuisine + "_leafs.json"
	G = visualizeNetwork(ingredLeafs, leafEdges, filename)
	
	json.dump(dict(nodes=[[n, G.node[n]] for n in G.nodes()],
		edges=[[u,v,G.edge[u][v]] for u,v in G.edges()]),
	open("hawaiian.json", 'w'), indent=2)
	
 	
