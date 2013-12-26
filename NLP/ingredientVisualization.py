import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph
import numpy as np
from optparse import OptionParser
from pymongo import Connection
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
def isCompleteTextFood(nCompleteText):
	completeSynsets = wn.synsets(nCompleteText)
	if len(completeSynsets) > 0:
		return isFood(nCompleteText, 0, 0)
	else:
		return {'isFood': 0, 'Parent': 'None'}

def analyzeWordWiseSynsets(wordWiseSynsets, words, wordsLen, text):
	if len(words)>=2 :
		for i in range(0,len(words)-1):
			wordKey = words[i] + "_" + words[i+1]
			if (isCompleteTextFood(wordKey))['isFood'] == 1:
				insertSubPhraseKey(text, wordKey, wordKey, multiWordIngredMap);
			else:
				analyzeBigramSynsets(wordWiseSynsets[i:i+2], wordKey, text, wordsLen);
def analyzeBigramSynsets(wordWiseSynsets, wordKey, originalText, originalPhraseLength):
	words = wordKey.split("_")
	nFirst=words[0]
	nLast=words[1]
	
	if len(wordWiseSynsets) == 2:
		if wordWiseSynsets[0]['isFood'] == 0 and wordWiseSynsets[1]['isFood'] == 0 :
			print "Ingredient not recognized " + text + " wordKey: " + wordKey
			stats[statsMap['None']] += 1
		else:
			if wordWiseSynsets[0]['isFood'] == 0 and wordWiseSynsets[1]['isFood'] == 1:
				insertSubPhraseKey(originalText,wordKey,nLast,multiWordIngredMap)
			elif wordWiseSynsets[1]['isFood'] == 0 and wordWiseSynsets[0]['isFood'] == 1:
				insertSubPhraseKey(originalText,wordKey,nFirst,multiWordIngredMap)
			else:		
				insertSubPhraseKey(originalText,wordKey,1,nextIterIngredMap)			
	else:
		print "Error: INVALID combination of subphrases: " + wordKey

	
def insertSubPhraseKey(parentKey, childKey, value, dataMap):
	if parentKey not in dataMap.keys():
		dataMap[parentKey] = {}
	if childKey not in dataMap[parentKey].keys():
		dataMap[parentKey][childKey] = [value] 
	else:
		if value not in dataMap[parentKey][childKey]:
			dataMap[parentKey][childKey].append(value)

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

class EatYourBooksDB:
	connection=None
	db=None
	item_collection=None
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
	db =""
	itemtype=""
	ipaddress=""
	cuisine=""
	parser=OptionParser()
	parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="localhost")
        parser.add_option("-t", "--itemtype", dest="itemtype", help="item type i.e. recipes/cookbooks to be parsed and added", default="recipes")
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="pakistani")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")

        options, arguments = parser.parse_args()
        print "ipaddress: " + options.ipaddress
        print "item type: " + options.itemtype
        print "db name: " + options.db
	print "cuisine: " + options.cuisine
	
	lines = [line.strip() for line in open('data/pakistani_ingredients.txt')]
	for line in lines:
		text = line.lstrip().rstrip()
		text = text.decode('utf-8')
		globalIngredMap[text] = "";
		words = text.split(" ")
		nCompleteText = text.replace(" ", "_")
		if (isCompleteTextFood(nCompleteText))['isFood'] == 1:
			stats[statsMap['Complete']] += 1 
			insertSubPhraseKey(text,text,text, multiWordIngredMap)
	
		else:
			wordWiseSynsets = [];
			for word in words:
				#if "chile" in word or "goat" in word or "pasta" in word or "cheese" in word or "vegetable" in word:
				#	print "Alert"
				wordWiseSynsets.append(isFood(word, 0, 0))	
			if len(wordWiseSynsets) == 1 and words[0] not in notFoundIngredMap.keys():
				notFoundIngredMap[words[0]] = 1
			else:
				analyzeWordWiseSynsets(wordWiseSynsets, words, len(words), text)
	
	nextIterIngredMap = identifyKeyword(nextIterIngredMap)


	leafs = {}
	for key in globalIngredMap.keys():
		keyFound = 0
		if key in multiWordIngredMap.keys():
			globalIngredMap[key] = multiWordIngredMap[key]
			keyFound = 1
			for nKey, nValues in multiWordIngredMap[key].iteritems():
				for value in nValues:
					if value in leafs.keys():
						leafs[value].append(key)
					else:
						leafs[value] = [key];
				
		if key in nextIterIngredMap.keys():
			if keyFound == 1:
				nMaps = nextIterIngredMap[key]
				for nKey, nValue in nMaps.iteritems():
					globalIngredMap[key][nKey] = nValue
		  	else:
				globalIngredMap[key] = nextIterIngredMap[key]		
			for nKey, nValues in nextIterIngredMap[key].iteritems():
				if nValues in leafs.keys():
					leafs[nValues].append(key)
				else:
					leafs[nValues] = [key]
	

	
		
 	nodeDegree={}	
	edgeStrength={}
	for key in leafs.keys():
		for iKey in globalIngredMap.keys():
			keyAll = key + "_" + iKey
			if keyAll in edgeStrength.keys():
				edgeStrength[keyAll] = edgeStrength[keyAll] + 1
			else:
				edgeStrength[keyAll] = 1
	#visualize as graph
	B = nx.Graph()
	B.add_nodes_from(leafs.keys(), bipartite=0)
	B.add_nodes_from(globalIngredMap.keys(), bipartite=1)
	for key in leafs.keys():
		ingredients = leafs[key]
		for ingredient in ingredients:
			B.add_edges_from([(key, ingredient)])
			B[key][ingredient]['value'] = edgeStrength[key+"_"+ingredient]
			B.node[key]['degree'] += 1
			B.node[ingredient]['degree'] += 1

	db=EatYourBooksDB(options.db, options.ipaddress, options.itemtype)
	dbRecipes=db.get_recipe_vs_ingredient(options.cuisine)
	distinctIngredList=db.get_distinct_ingredients_by_cuisine(options.cuisine)

	recipeIngredMat=[]	
	rowIndex=0
	ingredCount = len(distinctIngredList)
	recipes=[]
	for recipe in dbRecipes:
		ingredVec = []
		for i in range(0,len(distinctIngredList)):
			ingredVec.append(0)
		recipes.append(recipe["_id"])
		for ingredient in recipe["ingredients"]:
			ingredIndex = distinctIngredList.index(ingredient)
			if ingredIndex >= 0:
				ingredVec[ingredIndex]=1
			else:
				print "Trouble: " + ingredient 
		recipeIngredMat.append(ingredVec)
		rowIndex=rowIndex+1
		

	rIMat=np.matrix(recipeIngredMat)
	rIMatT=rIMat.transpose()
	ingredCo=rIMatT*rIMat

	ingredCoList = ingredCo.tolist()
	i=0
	for row in ingredCoList:
		source=distinctIngredList[i]
		j=0
		for col in row:
			if i!=j and i<=j:
				edgeWeight=col
				target=distinctIngredList[j]
				if edgeWeight > 0 :
					B.add_edge(source, target, value=edgeWeight)
					print B.node[source]
					print B.node[target]
			j=j+1
		i=i+1
			
	#write network data into json
	dumps = json_graph.dumps(B)

	with open('pakistani_bipartite.json', 'w') as file:
		file.write(dumps);


	


