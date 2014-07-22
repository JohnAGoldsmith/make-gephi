# -*- coding: <utf-16> -*- 

#-----------------------------------------------------------------------#
#									#
#	This program takes a word neighbor list				#	
#	and creates a gephi-readable file				#
#	John Goldsmith and Wang Xiuli 2012.	Jackson Lee 2014			#
#									#
#-----------------------------------------------------------------------#


unicode = True
import codecs
import os
import sys

 
import string
import operator
mywords=dict()
from math import sqrt
from  collections import defaultdict 
import numpy
from numpy import *
from math import sqrt
from collections import defaultdict 

sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
sys.path.append('/usr/lib64/graphviz/python/')


#---------------------------------------------------------------------------#
#	Variables to be changed by user
#---------------------------------------------------------------------------#

unicodeFlag 		= False
FileEncoding 		= ""   # "utf-16"
language 		= "english-brown"
shortname 		= "english-brown"

print "Language:", language
print "Name: ", shortname

#---------------------------------------------------------------------------#

commandlineinput = sys.argv
if len(sys.argv) < 2:

	shortfilename 		= ""
	outshortfilename 	= ""
	languagename 		= "english"

	datafolder    		= "../../data/"
	neighborfolder  	= datafolder + languagename + "/neighbors/"
	outfolder     		= datafolder + languagename + "/gexf/"
	signaturefolder		= datafolder + languagename + "/lxa/"

	neighborFileList = list()
	for f in os.listdir(neighborfolder):
		if f.endswith('nearest_neighbors.txt'):
			neighborFileList.append(neighborfolder + f)

	neighborFileListKeyboardText = [str(idx+1)+'. '+s+'\n' for (idx,s) in enumerate(neighborFileList)]
	infilenameKeyboard = raw_input('\nwhich file to read? (enter number)\n\n'
									'%s\n' % ''.join(neighborFileListKeyboardText)
									)
	infilename = neighborFileList[int(infilenameKeyboard)-1]

	signaturefilename 	=  signaturefolder + shortname + "_sigtransforms.txt"
else:
# More work needs to be done here:
	infilename = commandlineinput[1]
	outfolder = "./"
outfilenameGephi	=   outfolder + shortname  + ".gexf"  

#---------------------------------------------------------------------------#

seedwordKeyboard = raw_input("Seed word?")
if len(seedwordKeyboard) > 0:
	seedword = seedwordKeyboard
else:
	seedword = ""

#---------------------------------------------------------------------------#

numberNeighborsKeyboard = raw_input("How many neighbors? (default is 3)")
if numberNeighborsKeyboard != "":
	howManyNeighbors = int(numberNeighborsKeyboard)
else:
	howManyNeighbors 	= 3

#---------------------------------------------------------------------------#

numberGenerationsKeyboard = raw_input("How many generations? (default is 3)")
if numberGenerationsKeyboard != "":
	howManyGenerations = int(numberGenerationsKeyboard)
else:
	howManyGenerations 	= 3

#---------------------------------------------------------------------------#

ShowAllNodes = raw_input("Show only neighbor nodes on graph? (N/y)")
if ShowAllNodes == "y" or ShowAllNodes == "Y":
	ShowAllNodes = False
else:
	ShowAllNodes = True

if seedword == "":
	seedwordproxy = "All_Words"
else:
	seedwordproxy = seedword
#---------------------------------------------------------------------------#

outnametag 		= "_" + seedwordproxy + "_" + str( howManyNeighbors) + "-" + str( howManyGenerations )
outfilenameGephi	= outfolder + shortname +  outnametag + ".gexf" 
if unicodeFlag:
	outfileGephi 	= codecs.open (outfilenameGephi, "w", encoding = FileEncoding)
#infile 		= codecs.open (filename, encoding = FileEncoding)
else:
	outfileGephi 	= open (outfilenameGephi, "w")

print "gephi file printed at", outfilenameGephi
  

#import gv
# --------------------------------------------------------------------------- # 


#---------------------------------------------------------------------------#
#	Definitions before start of program.
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
class graph:
	def __init__(seed, wordlist, edgelist):
		self.nodecount = 0
		self.edgecount = 0
		self.howManychildren = 0
		self.currentgeneration = 0
		self.seed = seed
		self.generation_dict = dict()
	def generation():
		self.currentgeneration += 1
		for word in self.generation_dict:
			for (word1, word2) in edgelist:
				if word1 in self.generation_dict: 
					if word2 not in self.generation_dict:
						self.generation_dict[word2] = self.currentgeneration
				elif word2 in self.generation_dict:
					if word1 not in self.generation_dicts:
						self.generation_dict[word1] = self.currentgeneration
	

#---------------------------------------------------------------------------#
def readfile(infile, wordtoindex, indextoword, wordindex, wordlist, myedges):
#---------------------------------------------------------------------------#
	diameter = dict()
	howManyNeighborsInUnderlyingData = 0	 
	language = "" 
 	print " ******** starting to read words"  	
	for line in infile:	 
 
		words = line.split()
		if line.startswith('#') or len(words) == 0:
			continue

#		if words[0] == "#" and len(words) < 3:
#			continue
#		if words[0] == "#" and words[1] == 'language:':
#			language = words[1]
#			continue
#		if words[0] == "#" and words[1] == 'corpus:':
#			shortfilename = words[2]
#			continue
		for word in words:
			if howManyNeighborsInUnderlyingData == 0:
				howManyNeighborsInUnderlyingData = len(words) - 1
				print "how many neighbors" , howManyNeighborsInUnderlyingData
			if not word in wordtoindex:
				wordtoindex[word] = wordindex
				indextoword[wordindex] = word
				wordindex += 1
				allwordlist.append(word)				 

		word = words[0]
		wordlist.append(word)

		for i in range(1, howManyNeighborsInUnderlyingData+1):
			neighborword = words[i]
	
			if not word in myedges: #my edges is used because we often need to iterate over the second variable (across a row, so to speak)
				myedges[word] = dict()
                                
			myedges[word][neighborword]= 1
#                        if word not in diameter:
#                             diameter[word] = 0
#                        diameter[word] += 1
                       

	for (idx, word) in enumerate(wordlist):
		wordtoindex[word] = idx

	for word in wordlist: 
		wordno = wordtoindex[word]
		for word2 in myedges[word]:   
			wordno2 = wordtoindex[word2]
			edgelist.append ( (wordno, wordno2) ) #this is convenient for outputting.
			
 	print "Read words:" , len(wordlist)
	return (language, myedges, wordtoindex, wordlist, edgelist,diameter, allwordlist, howManyNeighborsInUnderlyingData )
 
#---------------------------------------------------------------------------#

def printGephinodes2(outfileGephi,NodeFamilyDict, edgelist,ShowAllNodes):
	print >>outfileGephi, "\t\t<nodes count=\"" + str(len(wordlist)) + "\"> "
	print " length of nodefamily dict" , len(NodeFamilyDict)
 	for word in NodeFamilyDict:
		i = wordtoindex[word]
		lineToPrint = "\t\t\t<node id =\""
		lineToPrint += str(i)
		lineToPrint += "\" label =\""
		if word == "&":
			continue
			word = "ampersand"
		lineToPrint += word
		lineToPrint +="\""
		lineToPrint += ">"
		print >>outfileGephi, lineToPrint
 
		#For multi-color graphs.
		if NodeFamilyDict[word] == 0 :	 
			lineToPrint =  "\t\t\t\t<viz:color r=\"255\" g=\"140\" b=\"0\" a=\"0.6\"/>"			 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint

		if NodeFamilyDict[word] == 1 :	 
			lineToPrint =  "\t\t\t\t<viz:color r=\"30\" g=\"144\" b=\"255\" a=\"0.6\"/>"		 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint
	 		 
		 
		elif NodeFamilyDict[word] == 2 :	 
			lineToPrint =  "\t\t\t\t<viz:color r=\"255\" g=\"255\" b=\"000\" a=\"0.6\"/>"		 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint
			 

		elif NodeFamilyDict[word] == 3 : 
			lineToPrint =  "\t\t\t\t<viz:color r=\"124\" g=\"144\" b=\"35\" a=\"0.6\"/>"		 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint

 		elif NodeFamilyDict[word] == 4 : 
			lineToPrint =  "\t\t\t\t<viz:color r=\"50\" g=\"60\" b=\"35\" a=\"0.6\"/>"		 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint

		elif NodeFamilyDict[word] == 5 : 
			lineToPrint =  "\t\t\t\t<viz:color r=\"124\" g=\"0\" b=\"35\" a=\"0.6\"/>"		 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint

		elif NodeFamilyDict[word] == 6 : 
			lineToPrint =  "\t\t\t\t<viz:color r=\"24\" g=\"14\" b=\"135\" a=\"0.6\"/>"		 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint

		elif NodeFamilyDict[word] == 7 : 
			lineToPrint =  "\t\t\t\t<viz:color r=\"124\" g=\"44\" b=\"235\" a=\"0.6\"/>"		 
			print >>outfileGephi, lineToPrint
			lineToPrint =  "\t\t\t\t<viz:size value=\"20\"/>"		 
			print >>outfileGephi, lineToPrint		 
		lineToPrint ="\t\t\t</node>"
		print >>outfileGephi, lineToPrint

	 
	


	print >>outfileGephi, "\t\t</nodes>"

 	 
              
        # Print Gephi edges
	print >>outfileGephi, "\t\t<edges count=\" ", edgecount, " \"> "
	for edgeno in range(len(edgelist)):
		edge = edgelist[edgeno]
		(nodeno1, nodeno2) = edge 
             	if ShowAllNodes or ( allwordlist[nodeno1] in NodeFamilyDict and allwordlist[nodeno2] in NodeFamilyDict) :   
			sourceno = nodeno1
			targetno = nodeno2
			lineToPrint = "\t\t\t<edge id =\""
			lineToPrint += str(edgeno)
			lineToPrint += "\" source = \""
			lineToPrint += str(sourceno)
			lineToPrint += "\" target = \""
			lineToPrint +=  str(targetno)
			lineToPrint += "\"/>"
			print >>outfileGephi, lineToPrint
	print >>outfileGephi, "\t\t</edges>"	 
	print >>outfileGephi, "\t</graph>"	
	print >>outfileGephi, "\t</gexf>"

 




 
# ---------------------------------------------------------------------------------------------------------------
 
 
#  Beginning of program
 
#----------------------------------------------------------------------------------------------------------------
mynodes 		= dict()
myedges 		= dict() 
mywords			= dict()
closestNeighbors 	= dict() 
wordlist 		= list()
allwordlist 		= list()
edgelist 		= list()
closestNeighbors	= dict()
edgecount 		= 0 
wordindex 		= 0
wordtoindex 		= dict()
indextoword		= dict()
 
infile 			= open(infilename) 
 

#------------------------------------------#
#	read file
#------------------------------------------#

print "read file"
 
(language,  myedges, wordtoindex, wordlist, edgelist ,diameter, allwordlist, howManyNeighborsInUnderlyingData) = readfile (infile, wordtoindex, indextoword, wordindex, wordlist, myedges)

 
if len(seedword) > 0 and seedword not in myedges:
	print "Not valid word. Goodbye."
	sys.exit()

#------------------------------------------#
#	real beginning
#------------------------------------------#
NodeFamilyDict = dict()
NewestWords = list()
NextSetOfNewestWords= list()
edgelist_subset = list()

if len(seedword) > 0:
	NodeFamilyDict[seedword] = 0
NewestWords.append(seedword)
 
 
if seedword=="":
	for word in wordlist:
		if len(word) < 1:
			print " Putting nullword in NodeFamilyDict", word		
		NodeFamilyDict[word] = 0
else:	
	for loopnumber in range(howManyGenerations):
		#print "**************************"			 
		NextSetOfNewestWords = list()
		#print "1. Generation number", loopnumber, NewestWords
		while len(NewestWords):			
			word = NewestWords.pop()
			#print "\t 2. New FROM word: (", word, ") generation number", loopnumber, NewestWords
			neighborcount = 0
			for neighbor in myedges[word]:	
				print "359", neighbor
				#print "edges", myedges[word]				 		
				neighborcount += 1
				if neighbor not in NodeFamilyDict:
					NextSetOfNewestWords.append( neighbor)
					#print "\t\tNew neighbor (", neighbor, ")", neighborcount, "\n", 
					#print "(", word,"," ,neighbor,")\n"
					NodeFamilyDict[neighbor] = loopnumber + 1
				else:
					print "Neighbor already counted", neighbor, neighborcount	
				edgelist_subset.append((wordtoindex[word], wordtoindex[neighbor]))					 
				if neighborcount >= howManyNeighbors:						 
					break

		NewestWords= NextSetOfNewestWords
	 



 
	 
print >>outfileGephi, "<gexf xmlns=\"http://www.gexf.net/1.2draft\" xmlns:viz=\"http://www.gexf.net/1.2draft/viz\">"
print >>outfileGephi, "\t<graph defaultedgetype=\"directed\" idtype=\"string\" type=\"static\">"
if ShowAllNodes:
	printGephinodes2(outfileGephi,NodeFamilyDict, edgelist, ShowAllNodes)
else:
	printGephinodes2(outfileGephi,NodeFamilyDict,edgelist_subset,ShowAllNodes)

outfileGephi.close()

if seedwordproxy == "All_Words":
    outfilenameGephi_new = outfilenameGephi.replace('3-3', str(len(wordlist)))
    os.rename(outfilenameGephi, outfilenameGephi_new)
    outfilenameGephi = outfilenameGephi_new

#------------------------------------------#
#	end
#------------------------------------------#
		 
 
print outfilenameGephi
print "Exiting successfully."







