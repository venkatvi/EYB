import nltk as nltk
from  nltk.corpus import wordnet as wn
from nltk.collocations import *
from nltk.probability import * 
import collections

lines = [line.strip() for line in open('data/pakistani_ingredients.txt')]
ingred_map = {}
gSim = {}

'''
line = "bay leaves"
synsets = wn.synsets(line)
print synsets
'''
bgm = nltk.collocations.BigramAssocMeasures()
finder = nltk.collocations.BigramCollocationFinder.from_words(nltk.corpus.brown.words())
scored = finder.score_ngrams(bgm.likelihood_ratio)
prefix_keys = collections.defaultdict(list)
for key,scores in scored:
	prefix_keys[key[0]].append((key[1], scores))

for key in prefix_keys:
	prefix_keys[key].sort(key=lambda x:-x[1])

tgm = nltk.collocations.TrigramAssocMeasures()

bigram_count = 0
bigrams_match_count = 0

trigram_count = 0
trigram_match_count = 0

ngram_count = 0
f=open('pakistani_pos_analysis.txt', 'w');
for line in lines:
	text = line.lstrip().rstrip()
	tok_text = nltk.word_tokenize(line)
	pos_text = nltk.pos_tag(tok_text)
	words = text.split(" ")
	if len(words) == 1:
		i1=1
	elif len(words) == 2:
		bigram_count = bigram_count + 1
		isBigram = 0
		tree = nltk.ne_chunk(pos_text)	
		prefixes = prefix_keys[words[0]]
	
		inPrefixes=0
		for prefix in prefixes:
			inPrefixes = inPrefixes + 1
			pstr = prefix[0]
			if pstr == words[1]:
				print "Case1: " + text + ": " + words[0] + ": " + prefix[0] + "-" + str(prefix[1]) + ": index:" +str(inPrefixes) + " : totalcount: " + str(len(prefixes)) 
				isBigram = 1

		prefixes = prefix_keys[words[1]]
		inPrefixes = 0	
		for prefix in prefixes:
			inPrefixes = inPrefixes + 1
			pstr = prefix[1]
			if pstr == words[0]: 
				print "Case 2: " + text + ": " + words[1] + ": " + prefix[0] + "-" + str(prefix[1]) + ": index:" +str(inPrefixes) + " : totalcount: " + str(len(prefixes)) 
				isBigram = 1
				print prefix
		if isBigram == 1:
			bigrams_match_count = bigrams_match_count + 1
		else:
			print pos_text
			print tree	
	elif len(words) == 3:
		trigram_count += 1
		'''
		tree = nltk.ne_chunk(pos_text)
		finder = TrigramCollocationFinder.from_words(tok_text)
		scored = finder.score_ngrams(tgm.raw_freq)
		print scored
		print pos_text
		'''
	elif len(words) == 4:	
		ngram_count +=1
		print line
	else:
		print line

f.close()

print "Total bigrams: " + str(bigram_count)
print "Total matches: " + str(bigrams_match_count)
print "Total trigrams: " + str(trigram_count)
'''		
print ingred_map
'''
