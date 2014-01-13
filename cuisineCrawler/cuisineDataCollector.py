import numpy as np
from optparse import OptionParser
from pymongo import Connection
import networkx as nx
from networkx.readwrite import json_graph
def writeDict(dictData, cuisine, fileName):
	f = open(options.rootPath + "/coquere/ingredientNets/data/" + cuisine + "_" + fileName+".csv", 'wb');
	f.write("field,count\n");
	for key in sorted(dictData.keys()):
		keyStr = key.encode('utf-8')
		keyStr = keyStr.replace(",", " ")
		keyStr = keyStr.replace(" ", "_")
		f.write(keyStr + "," + str(dictData[key]) + "\n");

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

	def getRecords(self, cuisine):
		return list(self.item_collection.find())

	def getRecordsByCuisine(self, fieldType):
		records = self.item_collection.aggregate([
			{ "$group" : { "_id" : "$cuisine", "count": { "$sum" : 1 } } },
			{ "$match" : { "count" : { "$gt" : 1 } } }
			])
		return list(records["result"])
			
def addData(dbResults, globalData, fieldType):
	for result in dbResults:
		cuisine = result["_id"]
		count = result["count"]
		if cuisine not in globalData.keys():
			globalData[cuisine] = {}
			globalData[cuisine][fieldType] = count
		else:
			globalData[cuisine][fieldType] = count
	return globalData;

def getCountries(cuisine):
	if (cuisine == "asian"):
		return ["russia", "india", "mongolia", "china", "japan", "pakistan", "afghanistan", "kazakhstan", "south korea", "thailand", "indonesia"]
	elif cuisine == "australian":
		return ["australia"]
	elif cuisine == "japanese":
		return ["japan"]
	elif cuisine == "european":
		return ["europe"]
	elif cuisine == "italian":
		return ["italy"]
	elif cuisine == "pakistani":
		return ["pakistan"]
	elif cuisine == "irish":
		return ["ireland"]
	elif cuisine == "chinese":
		return ["china"]
	elif cuisine == "german":
		return ["germany"]
	elif cuisine == "portugese":
		return ["portugal"]
	elif cuisine == "hawaiian":
		return ["hawaii"]
	elif cuisine == "moroccan":
		return ["morocco"]
	elif cuisine == "mexican":
		return ["mexico"]
	elif cuisine == "jamaican":
		return ["jamaica"]
	elif cuisine == "brazilian":
		return ["brazil"]
	elif cuisine == "thai":
		return ["thailand"]
	elif cuisine == "greek":
		return ["greece"]
	elif cuisine == "caribbean":
		return ["cuba"]
	elif cuisine == "french":
		return ["france"]
	elif cuisine == "vietnamese":
		return ["viet nam"]
	elif cuisine == "spanish":
		return ["spain"]
	elif cuisine == "polish":
		return ["poland"]
	elif cuisine == "indian":
		return ["india"]
	elif cuisine == "russian":
		return ["russian federation"]
	elif cuisine == "south-american":
		return ["bolivia, plurinational state of", "guyana","colombia", "ecuador", "peru", "chile", "argentina", "uruguay", "paraguay", "venezuela, bolivarian republic of", "brazil", "suriname", "french guiana"]
	elif cuisine == "african":
		return ["algeria", "mauritania", "guinea", "gabon", "south sudan", "tanzania", "bostwana", "libya", "egypt", "sudan", "ethiopia", "somalia", "kenya", "tanzania, united republic of", "mozambique", "zambia", "zimbabwe", "botswana", "south africa", "namibia", "angola", "nigeria",  "ghana", "niger", "chad", "ghana", "morocco", "tunisia", "mali", "burkina", "congo, the democratic republic of the", "eritrea", "djibouti", "swaziland", "lesotho", "congo", "cameroon", "central african republic", "senegal", "gambia", "guinea-bissau", "guinea", "sierra leone", "liberia", "togo", "benin", "western sahara", "uganda", "rwanda", "burundi", "cote d'ivoire", "burkina faso", "malawi"]
	else: 
		print "unknown cuisine"
		return ""

	
if __name__ == '__main__':
	parser=OptionParser()
	parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="localhost")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")

        options, arguments = parser.parse_args()
        print "ipaddress: " + options.ipaddress
        print "db name: " + options.db
	
	db = EatYourBooksDB(options.db, options.ipaddress, 'cookbooks')
	cookbooksByCuisine = db.getRecordsByCuisine('cookbooks')

	db = EatYourBooksDB(options.db, options.ipaddress, 'cookbookrecipes')
	recipesByCuisine = db.getRecordsByCuisine('recipes')

	globalData = {} 

	globalData = addData(cookbooksByCuisine, globalData, "cookbooks")
	globalData = addData(recipesByCuisine, globalData, "recipes")

	for key in globalData.keys():
		globalData[key]["ingredients"] = len(db.get_distinct_ingredients_by_cuisine(key))

	lines = [line.strip() for line in open("../coquere/ingredientNets/data/world-country-names.tsv", 'r')]
	countryCodes = {}
	for line in lines:
		items = line.split("\t");
		if items[1] not in countryCodes.keys():
			countryCodes[items[1].lower()] = items[0]
	
	fw = open("../coquere/ingredientNets/data/cuisines.tsv", "w");
	fw.write("cuisine\trecipes\tingredients\tcookbooks\tid\n");
	for cuisine in globalData.keys():
		countries = getCountries(cuisine)
		codes = []
		if len(countries) > 0:
			for country in countries:
				if country in countryCodes.keys():
					codes.append(countryCodes[country])

			if len(codes) > 0:
				for code in codes:
					fw.write(cuisine + "\t" + str(globalData[cuisine]["recipes"]) + "\t" + str(globalData[cuisine]["ingredients"]) + "\t" + str(globalData[cuisine]["cookbooks"]) + "\t" + str(code) + "\n");
	fw.close();
