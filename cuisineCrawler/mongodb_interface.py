import numpy as np
import os
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
		return list(self.item_collection.find({'cuisine': cuisine}))
			

if __name__ == '__main__':
	home_folder = os.getenv("HOME")
	parser=OptionParser()
	parser.add_option("-i", "--ipaddress", dest="ipaddress", help="ipaddress of remote mongodbserver", default="localhost")
        parser.add_option("-t", "--itemtype", dest="itemtype", help="item type i.e. recipes/cookbooks to be parsed and added", default="recipes")
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="pakistani")
        parser.add_option("-d", "--database", dest="db", help="database name to store parsed data. Database should contain collections of the name given in --itemtype option", default="EatYourBooksDB")
        parser.add_option("-p", "--path", dest="rootPath", help="root location to store results", default=home_folder + "/EYB")

        options, arguments = parser.parse_args()
        print "ipaddress: " + options.ipaddress
        print "item type: " + options.itemtype
        print "db name: " + options.db
	print "cuisine: " + options.cuisine
	
	db=EatYourBooksDB(options.db, options.ipaddress, 'cookbooks')
	cookbooks = db.getRecords(options.cuisine);


	db=EatYourBooksDB(options.db, options.ipaddress, 'cookbookrecipes')
	recipes=db.getRecords(options.cuisine)

	authors = {}
	cookbooks = {}

	authorCount={}
	cookBookCount = {}
	categoryCount={}
	
	categoryCookBook={}
	categoryAuthor={}
	cookBookAuthor={}

	for recipe in recipes:
		author = recipe["author_str"];
		authorUrl = recipe["author_url"];
		if author not in authors.keys():
			authors[author] = authorUrl;

		cookbook = recipe["source_str"];
		cookbookUrl = recipe["source_url"];
		if cookbook not in cookbooks.keys():
			cookbooks[cookbook] = cookbookUrl;

		categories = recipe["categories"];
		for category in categories:
			if category in categoryCount.keys():
				categoryCount[category] += 1;
				if cookbook not in categoryCookBook[category]:
					categoryCookBook[category].append(cookbook)
				if author not in categoryAuthor[category]:
					categoryAuthor[category].append(author)
			else:
				categoryCount[category] = 1;
				categoryCookBook[category] = [cookbook]
				categoryAuthor[category] = [author]
			
		if author in authorCount.keys():
			authorCount[author] += 1;
		else:
			authorCount[author] = 1;
				

		if cookbook in cookBookCount.keys():
			cookBookCount[cookbook] += 1;
		else:
			cookBookCount[cookbook] = 1;
			cookBookAuthor[cookbook] = author


	
	print "Cookbook2Recipes"
	print cookBookCount
	print "Authors2Recipes"
	print authorCount
	print "Categories2Recipes"
	print categoryCount

 	writeDict(cookBookCount, options.cuisine, 'cookbooks');
	writeDict(authorCount, options.cuisine, 'authors');
	writeDict(categoryCount, options.cuisine, 'categories');	

	B = nx.Graph()
	B.add_nodes_from(authors.keys(), group=1)
	B.add_nodes_from(cookbooks.keys(), group=2)
	B.add_nodes_from(categoryCount.keys(), group=3)

	for category, authors in categoryAuthor.iteritems():
		if not 'degree' in B.node[category]:
			B.node[category]['degree'] = 1		
		else:
			B.node[category]['degree'] += 1
		for author in authors:
			if not 'degree' in B.node[author]:
				B.node[author]['degree'] = 1
			else:
				B.node[author]['degree'] += 1
			B.add_edges_from([(category, author)])

	for category, cookbooks in categoryCookBook.iteritems():
		if not 'degree' in B.node[category]:
			B.node[category]['degree'] = 1		
		else:
			B.node[category]['degree'] += 1
		for cookbook in cookbooks:
			if not 'degree' in B.node[cookbook]:
				B.node[cookbook]['degree'] = 1
			else:
				B.node[cookbook]['degree'] += 1
			B.add_edges_from([(category, cookbook)])

	for cookbook, author in cookBookAuthor.iteritems():
		if not 'degree' in B.node[cookbook]:
			B.node[cookbook]['degree'] = 1		
		else:
			B.node[cookbook]['degree'] += 1
		if not 'degree' in B.node[author]:
			B.node[author]['degree'] = 1
		else:
			B.node[author]['degree'] += 1
		B.add_edges_from([(cookbook, author)])


	json_file = options.rootPath + "/coquere/ingredientNets/data/"+options.cuisine+"_dataStats.json"	
	dumps = json_graph.dumps(B)
	with open(json_file, 'w') as file:
		file.write(dumps)		
