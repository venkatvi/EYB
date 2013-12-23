import nltk
from nltk.corpus import wordnet as wn
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import d3py

ingredParentMap = {}
def addChildren(G, parentName):
	print "Adding children for " + parentName
	childSynsets = wn.synset(parentName).hyponyms()
	for child in childSynsets:
		G.add_node(child.name, defi=child.definition, name=child.name)
		G.add_edge(G.node[parentName]['name'], child.name)
		if child.name not in ingredParentMap.keys():
			ingredParentMap[child.name] = {parentName}
		else:
			parents = ingredParentMap[child.name]
			if parentName not in parents:
				parents.add(parentName)
			ingredParentMap[child.name] = parents
		addChildren(G, child.name)
	return G

def constructGraph(rootName):
	G = nx.DiGraph()
	rootSynsets = wn.synsets(rootName)
	for root in rootSynsets:
		G.add_node(root.name, defi=root.definition, name=root.name)
		ingredParentMap[root.name] = {'None'}
		addChildren(G, root.name)
	return G
	
def isFood(word, level, isRice):
	#if "cinnamon" in word:
	#	isRice =1
	#if isRice==0:
	#	return;
	#print "Looking for " + word + "...\n Synsets are:"
	synsets = []
	if level == 0:
		synsets = wn.synsets(word)
	else:
		synset = wn.synset(word)
		synsets = { synset }
	if len(synsets) > 0:
		for synset in synsets:
	#		print "Processing synset: " + synset.name + "\n Parents: "  
			parents = synset.hypernyms()
			if len(parents) > 0:
				for parent in parents:
	#				print "Parent: " + parent.name + " level: " + str(level)
					if "food" in parent.name or "edible" in parent.name or "herb" in parent.name:
	#					print "Yay food"
						return {'isFood': 1, 'Parent':parent}
					else:
	#					print "Not a food parent.. recursing" 
						result = isFood(parent.name, level+1, isRice)
						if result['isFood'] == 1:
	#						print "yay: foood: " + parent.name + " word: " + word
							return result # you dont have to parse other parents
						else:
	#						print "continuing.. for " + word + "'s parents..."
							continue # finish parsing other parents
	#		else:
	#			print "No parents: " + synset.name + " word:" + word

		#if done traversing all parents for all synsets:
		return {'isFood': 0, 'Parent': 'None'}
	else:
	#	print "No synsets for " + word
		return {'isFood': 0, 'Parent': 	'None'}
def isCompleteTextFood(nCompleteText):
	completeSynsets = wn.synsets(nCompleteText)
	if len(completeSynsets) > 0:
		#print "Complete Synset: " + nCompleteText
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
				#stats[wordsLen][statsMap['Last']] += 1
				insertSubPhraseKey(originalText,wordKey,nLast,multiWordIngredMap)
			elif wordWiseSynsets[1]['isFood'] == 0 and wordWiseSynsets[0]['isFood'] == 1:
				#stats[statsMap['First']] += 1
				insertSubPhraseKey(originalText,wordKey,nFirst,multiWordIngredMap)
			else:		
				insertSubPhraseKey(originalText,wordKey,1,nextIterIngredMap)			
				# check pos for this combination, identify noun phrase and map it
				#stats[statsMap['Both']] += 1
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

statsMap = {'Complete': 0, 'None': 1, 'First': 2, 'Last': 3, 'Both': 4}
stats = [0,0,0,0,0]
multiWordIngredMap = {}
nextIterIngredMap = {}
notFoundIngredMap = {}
globalIngredMap = {}
i=0
if __name__ == '__main__':
	G = constructGraph("food")
	print "Graph done"
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
				i=i+1
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
				for value in nValues:
					if value in leafs.keys():
						leafs[value].append(key)
					else:
						leafs[value] = [key]
	


	#visualize as graph
	'''
	B = nx.Graph()
	B.add_nodes(leafs.keys())
	B.add_nodes(globalIngredMap.keys())
	for key in leafs.keys():
		ingredients = leafs[key]
		for ingredient in ingredients:
			B.add_edge([(key, ingredient)])

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
