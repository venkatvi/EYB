#!/usr/bin/python
import os
from optparse import OptionParser
def parseLines(line, category, f):
	if category==1:
		parseSplitMergeList(line, category, f);
	if category==2:
		parseSplitMergeList(line, category, f);
	if category==3:
		parseRemoveList(line, category, f);
def parseSplitMergeList(line, category, f):
	line = line.replace("{", '');
	line = line.replace("}", '');
	line = line.split("],");
	for ingred in line:
		ingred = ingred.strip();
		parts = ingred.split(":");
		origIngred = parts[0]
		splitIngred = parts[1].replace("[", ''); 
		f.write(str(category) + "," + origIngred + "," + splitIngred + "\n" );
def parseRemoveList(line, category, f):
	line = line.replace("[", '');
	line = line.replace("]", '');
	line = line.split(",");
	for ingred in line:
		f.write(str(category) + "," + ingred + "\n");
		
if __name__ == '__main__':
	home_folder = os.getenv("HOME")
	parser=OptionParser();
	parser.add_option("-f", "--file", dest="fileName", help="file that is parsed to get a csv of removed, split and merge nodes", default="indian.txt");
	options,arguments = parser.parse_args()
	print "File:" + options.fileName
	f = open(options.fileName, 'r')
	
	outFile = options.fileName.replace(".txt", ".csv");
	fw = open(outFile, "w");
	i=0;
	category=0;
	for line in f:
		if(i%2 == 0):
			category=category+1;
		else:
			parseLines(line, category, fw);
		i=i+1;

	fw.close();
	f.close();

