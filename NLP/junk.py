'''
			commonSynset = 0
			synsets = []
			for leaf in kleafs:
				synsets.append(wn.synsets(leaf))
			if len(synsets[0]) == 0:
				disambiguatedLeafSet[key] = kleafs[1]
				break
			if len(synsets[1]) == 0:
				disambiguatedLeafSet[key] = kleafs[0]
				break
			for synset in synsets[0]:
				if synset in synsets[1]:
					commonSynset = 1
					print synsets[0] 
					print synsets[1] 
					break
			if commonSynset == 0:
				for i in range(0, synsets[0]):
					for j in range(0, synsets[1]):
						hypernyms = i.common_hypernyms(j)
						for hypernym in hypernyms:
							if hypernym in synsets[0]: 
								commonSynset = 1
							        disambiguatedLeafSet[key] = kleafs[1]	
								break
							if hypernym in synsets[1]:
								commonSynset = 1
								disambiguatedLeafSet[key] = kleafs[0]
								break
'''

