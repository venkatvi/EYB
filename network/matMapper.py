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
	else:
		return 'temp'

if __name__ == '__main__':
	ingredListMap = {};
	ingredListMap['french'] = getIngredList('french');
	ingredListMap['italian'] = getIngredList('italian');
	ingredListMap['indian'] = getIngredList('indian');
	ingredListMap['chinese'] = getIngredList('chinese');
	
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

