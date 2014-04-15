import numpy as np
from optparse import OptionParser
if __name__ == '__main__':
	parser=OptionParser()
        parser.add_option("-c", "--cuisine", dest="cuisine", help="cuisine type", default="hawaiian")
        parser.add_option("-p", "--path", dest="rootPath", help="root location to store results", default="/home/vaidehi/EYB")

        options, arguments = parser.parse_args()
	print "cuisine: " + options.cuisine
	print "path: " + options.rootPath
		
	matFile = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_rlmat.txt";
 	recipeLeafMat = np.loadtxt(matFile, delimiter=",")	
	rLMat = np.matrix(recipeLeafMat)
	freqCount = rLMat.sum(axis=0)
	lfreqCount = np.array(freqCount)[0].tolist()

	ingredientList = options.rootPath + "/coquere/ingredientNets/data/" + options.cuisine + "_ingredLeafs.txt";
	f = open(ingredientList);
	ingredLeafs = f.readlines()
	f.close()

	freqFrac = {};
	for j in range(0, len(lfreqCount)):
		if lfreqCount[j] not in freqFrac.keys():
			if ingredLeafs[j] != "":
				freqFrac[lfreqCount[j]] = [ingredLeafs[j]]
		else:
			if ingredLeafs[j] != "":
				freqFrac[lfreqCount[j]].append(ingredLeafs[j])


	freqFracKeys = sorted(freqFrac.keys())

	print "--------------------------Printing frequencyDistribution ---------------------------------"
	#writing frequency distribution 
	f = open(options.rootPath + '/coquere/ingredientNets/data/' + options.cuisine + "_freq.csv", 'w')
	f.write("frequency,frac\n");
	for i in range(0, len(freqFracKeys)):
		freq = freqFracKeys[i] ;
		numNodesWithFreq = len(freqFrac[freq]);
		f.write(str(np.log10(freq)) + "," + str(np.log10(numNodesWithFreq)) + "\n");
	f.close()



