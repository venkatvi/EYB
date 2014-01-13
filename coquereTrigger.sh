#!/bin/bash
usage()
{
	echo "Usage: $0 [-c <cuisine>][-h];"
	exit 0;
}
cuisine="";
isCuisine=false
while getopts "c:h" opt; do
	case "$opt" in 
		c) isCuisine=true; cuisine=$OPTARG;;
		h) usage; exit 0;;
		\?) echo "$OPTARG is an unknown option"; exit 1;;
	esac
done
shift $((OPTIND-1))

if !$isCuisine
then
	echo "Error."
	usage
	exit 1
fi
arguments="-i 23.92.17.38 -c $cuisine -t cookbookrecipes -d EatYourBooksDB"
root="/home/vaidehi/EYB/"
networkDataPath="$root/NLP"
cmd="python $networkDataPath/ingredientVisualization.py $arguments" 
echo "--------------------"
echo $cmd
echo "--------------------"
eval $cmd

networkStatsPath="$root/network"
cmd="python $networkStatsPath/networkstats.py $arguments"
echo "--------------------"
echo $cmd
echo "--------------------"
eval $cmd

authorDataPath="$root/cuisineCrawler"
cmd="python $authorDataPath/mongodb_interface.py $arguments" 
echo "-------------------"
echo $cmd
echo "-------------------"
eval $cmd

