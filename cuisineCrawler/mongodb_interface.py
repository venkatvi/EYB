import numpy as np
from optparse import OptionParser
from pymongo import Connection
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
	
	db=EatYourBooksDB(options.db, options.ipaddress, options.itemtype)
	dbRecipes=db.get_recipe_vs_ingredient(options.cuisine)
	distinctIngredList=db.get_distinct_ingredients_by_cuisine(options.cuisine)

	recipeIngredMat=[]	
	rowIndex=0
	ingredCount = len(distinctIngredList)
	recipes=[]
	for recipe in dbRecipes:
		ingredVec =[0] * len(distinctIngredList);
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
	
	
	
