#!/usr/bin/env python
import sys
def getIngredList(cuisine):
	ingredListFile = "/home/hduser/EYB/coquere/ingredientNets/data/" + cuisine + "_ingredLeafs.txt";
	f = open(ingredListFile);
	ingredList = f.readlines()
	f.close()
	return ingredList

def getCuisineStr(cuisineId):
	if cuisineId == 1:
		return 'french'
	elif cuisineId == 2:
		return 'italian'
	elif cuisineId == 3:
		return 'indian'
	elif cuisineId == 4:
		return 'chinese'
	elif cuisineId == 5:
		return 'spanish'
	elif cuisineId == 6:
		return 'mexican'
	elif cuisineId == 7:
		return 'irish'
	elif cuisineId == 8:
		return 'german'
	elif cuisineId == 9:
		return 'russian'
	elif cuisineId == 10:
		return 'polish'
	elif cuisineId == 11:
		return 'thai'
	elif cuisineId == 12:
		return 'vietnamese'
	elif cuisineId == 13:
		return 'cambodian'
	elif cuisineId == 14:
		return 'caribbean'
	elif cuisineId == 15:
		return 'hawaiian'
	elif cuisineId == 16:
		return 'south-american'
	elif cuisineId == 17:
		return 'african'
	elif cuisineId == 18:
		return 'australian'
	elif cuisineId == 19:
		return 'brazilian'
	elif cuisineId == 20:
		return 'moroccan'
	elif cuisineId == 21:
		return 'ethiopian'
	elif cuisineId == 22:
		return 'pakistani'
	elif cuisineId == 23:
		return 'greek'
	else:
		return 'temp'

if __name__ == '__main__':
	ingredListMap = {};
	ingredListMap['french'] = getIngredList('french');
	ingredListMap['italian'] = getIngredList('italian');
	ingredListMap['indian'] = getIngredList('indian');
	ingredListMap['chinese'] = getIngredList('chinese');
	ingredListMap['spanish'] = getIngredList('spanish');
	ingredListMap['mexican'] = getIngredList('mexican');

	#ingredListMap['irish'] = getIngredList('irish');
	#ingredListMap['german'] = getIngredList('german');
	#ingredListMap['russian'] = getIngredList('russian');
	#ingredListMap['polish'] = getIngredList('polish');
	#ingredListMap['thai'] = getIngredList('thai');
	#ingredListMap['vietnamese'] = getIngredList('vietnamese');
	#ingredListMap['cambodian'] = getIngredList('cambodian');
	#ingredListMap['caribbean'] = getIngredList('caribbean');
	#ingredListMap['hawaiian'] = getIngredList('hawaiian');
	#ingredListMap['south-american'] = getIngredList('south-american');
	#ingredListMap['african'] = getIngredList('african');
	#ingredListMap['australian'] = getIngredList('australian');
	#ingredListMap['brazilian'] = getIngredList('brazilian');
	#ingredListMap['moroccan'] = getIngredList('moroccan');
	#ingredListMap['ethiopian'] = getIngredList('ethiopian');
	#ingredListMap['pakistani'] = getIngredList('pakistani');
	#ingredListMap['greek'] = getIngredList('greek');

	for line in sys.stdin:
		line = line.strip()
		row = line.split(",")	
		matType = row[-1]
		cuisineId = int(float(row[-2]));
		cuisine = getCuisineStr(cuisineId);
		if cuisine == 'temp':
			continue;
		ingredList = ingredListMap[cuisine]
		ingredId = int(float(row[-3]))
		src = ingredList[ingredId].replace("\n", "").strip()
		for col in range(0, len(row)-4):
			dest = ingredList[col].replace("\n", "").strip()
			ingreds = []
			ingreds.append(src)
			ingreds.append(dest)
			value = float(row[col])
			if value > 0:
				key = "";
				for ingred in sorted(ingreds):
					key = key + ingred + "#";
				print( "%s\t%s\t%s\t%s" % (cuisineId, matType, key, value) )

