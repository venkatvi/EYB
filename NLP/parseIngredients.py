from  nltk.corpus import wordnet as wn
lines = [line.strip() for line in open('pakistani_ingredients.txt')]
ingred_map = {}
gSim = {}

'''
line = "bay leaves"
synsets = wn.synsets(line)
print synsets
'''

for line in lines:
	print line
	food_synsets = wn.synsets('food')
	words = line.split(' ')
	words.append(line.lstrip().rstrip())
	word_synset_map = {}
	for word in words:
		synsets=wn.synsets(word)
		for synset in synsets:
			sim_map = {}
			for food_synset in food_synsets:
				lcms = synset.lowest_common_hypernyms(food_synset)
				if len(lcms) > 0 and lcms[0] in food_synsets:
					word_synset_map[word] = synset
					sim_map['path'] = synset.path_similarity(food_synset)
					sim_map['lch'] = synset.lch_similarity(food_synset)
					sim_map['wup'] = synset.wup_similarity(food_synset)
				#	sim_map['res'] = synset.res_similarity(food_synset, load_ic())
				#	sim_map['jcn'] = synset.jcn_similarity(food_synset, load_ic())
				#	sim_map['lin'] = synset.lin_similarity(food_synset, load_ic())
					if synset not in gSim.keys():
						gSim[synset] = sim_map
					break;
	
	ingred_map[line] = word_synset_map

f=open('pakistani_analysis.txt', 'w');
for key,values in ingred_map.iteritems():
	f.write("===========================================\n")
	f.write(key   + "\n");
	f.write("-------------------------------------------\n")
	for value in values:
		f.write(value)
		f.write("\n")

f.write("--------------------------------------------\n");
f.close()
'''		
print ingred_map
'''
