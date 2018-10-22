
#Anastasiya Zhukova
#INFO 3401
#Assignment 7 - Monday Problem Set

# Place any necessary imports here
import sqlite3
import parsers
import csv
import re

####################################################
# Part 0
####################################################

# Move your parsers.py file to your Problem Set 7
# directory. Once you've done so, you can use the 
# following code to have access to all of your parsing
# functions. You can access these functions using the 
# parsers.<function name> notation as in: 
# parsers.countWordsUnstructured('./state-of-the-union-corpus-1989-2017/Bush_1989.txt')




####################################################
# Part 1
####################################################

def csvParser(fileName):
	wordCounts = {}
	with open(fileName, "r+", encoding= 'utf-8') as inFile:
		data = csv.reader(inFile, delimiter = ',')
		next(data, None)
		for line in data:
			if line[0] in wordCounts.keys():
				wordCounts[line[0]][line[1]] = line[2]
			else:
				wordCounts[line[0]] = {}
				wordCounts[line[0]][line[1]] = line[2]
	return wordCounts

#Creates a dictionary of the word counts from multifile wordcounts.csv file



def getMetaData(fileName):
	pres_data = []
	with open(fileName, "r") as inFile:
		data = csv.reader(inFile, delimiter = ',')
		next(data, None) 
		for line in data:
			pres_data.append({'Start':line[2], 'End':line[3], 'Name':line[4], 'Party':line[6]})

	return pres_data

# gets us_presidents.csv data as a list of dictionaries



def populateDatabase(databaseName, wordCounts, metaData):
 	conn = sqlite3.connect(databaseName)
 	c = conn.cursor()
 	# inserting data into presidents table
 	for president in metaData:
 		query = 'INSERT INTO presidents (PresidentName, StartDate, EndDate, Party) VALUES (\"'
 		query += president['Name']
 		query += '\", \"'
 		query += president['Start']
 		query += '\", \"'
 		query += president['End']
 		query += '\", \"'
 		query += president['Party']
 		query += '\");'
 		c.execute(query)
 	conn.commit()


 	for filename in wordCounts.keys():
 		name = re.search('^([a-zA-Z]+)(?=_)', filename)[0]
 		year = re.search('(?<=_)([0-9]{4})(?=\.)', filename)[0]

 		query = 'SELECT PresidentName, rowid, StartDate, EndDate FROM presidents p WHERE p.PresidentName like \'%' + name + '%\';'
 		c.execute(query)
 		results = c.fetchall()
 		#populates the speeches table with Pres_ID, SpeechName, SpeechYear
 		if len(results) == 1:
 			query = 'INSERT INTO speeches (Pres_ID, SpeechName, SpeechYear) VALUES (' + str(results[0][1]) + ',\"' + name + '\",\"' + year + '\");'
 			c.execute(query)
 			c.execute('SELECT rowid FROM speeches WHERE speeches.Pres_ID = ' + str(results[0][1]) + ' AND speeches.SpeechYear = ' + year + ';')
 		elif len(results) > 1:
 			for result in results:
 				startYear = re.search('(?<=\D)([0-9]{2,4})$', result[2])[0]
 				endYear = re.search('(?<=\D)([0-9]{2,4})$', result[3])[0]
 				if int(year[2:]) in range(int(startYear),int(endYear)):
 					query = 'INSERT INTO speeches (Pres_ID, SpeechName, SpeechYear) VALUES (' + str(result[1]) + ',\"' + name + '\",\"' + year + '\");'
 					c.execute(query)
 					c.execute('SELECT rowid FROM speeches WHERE speeches.Pres_ID = ' + str(result[1]) + ' AND speeches.SpeechYear = ' + year + ';')
 		else:
 			print('speech president error')

 		speechID = int(c.fetchall()[-1][0])
 		for word in wordCounts[filename].keys():
 			query = 'INSERT INTO words (Speech_ID, Word, Count) VALUES (' + str(speechID) + ', \"' + word + '\", \" ' + wordCounts[filename][str(word)] + '\");'
 			c.execute(query)

 		conn.commit()




#     # Write a function that will populate your database
#     # with the contents of the word counts and us_presidents.csv
#     # to your database. 
#     # Inputs: A string containing the filepath to your database,
#     #         A word count dictionary containing wordcounts for 
#     #         each file in a directory,
#     #         A metadata file containing a dictionary of data
#     #         extracted from a supplemental file
#     # Outputs: None
#     return 0

# # Test your code here

#populateDatabase('President_Speeches_Words.db', csvParser('multifile wordcounts.csv'), getMetaData('us_presidents.csv'))



#parsers.tableTest('President Speeches Words', 'words')

# ####################################################
# # Part 2
# ####################################################

def searchDatabase(databaseName, word):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()

	c.execute('SELECT Speech_ID, Count FROM words WHERE words.Word == \"' + word + '\";')
	counts = c.fetchall()
	print(counts)
	justCounts = [x[1] for x in counts]
	highestIdx = justCounts.index(max(justCounts))
	speechID = counts[highestIdx][0]
	c.execute('SELECT Pres_ID FROM speeches WHERE rowid == ' + str(speechID) +';')
	presID = c.fetchall()[-1][0]
	c.execute('SELECT PresidentName FROM presidents WHERE rowid == ' + str(presID) +';')
	presName = c.fetchall()[-1][0]
	print('President with highest count of this word: ', presName)



#searchDatabase('President_Speeches_Words.db', 'bush')


#     # Write a function that will query the database to find the 
#     # president whose speech had the largest count of a specified word.
#     # Inputs: A database file to search and a word to search for
#     # Outputs: The name of the president whose speech contained 
#     #          the highest count of the target word
#     return 0

#get speech with highest countof word and see what pres that speech is associated with


def computeLengthByParty(databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()

	c.execute('SELECT Speech_ID, SUM(Count) FROM words GROUP BY Speech_ID')
	speeches_sum = c.fetchall()

	c.execute('SELECT presidents.Party, speeches.rowid FROM presidents JOIN speeches ON presidents.rowid == speeches.Pres_ID')
	parties = c.fetchall()

	RepSpeechID = [x[1] for x in parties if x[0] == 'Republican']
	DemSpeechID = [x[1] for x in parties if x[0] == 'Democratic']

	RepCounts = [int(x[1]) for x in speeches_sum if x[0] in RepSpeechID]
	DemCounts = [int(x[1]) for x in speeches_sum if x[0] in DemSpeechID]

	RepAvgLen = sum(RepCounts)/len(RepCounts)
	DemAvgLen = sum(DemCounts)/len(DemCounts)

	print('Republican Average Speech Length: ', RepAvgLen,'words')
	print('Democrat Average Speech Length: ', DemAvgLen,'words')



#computeLengthByParty('President_Speeches_Words.db')

#     # Write a function that will query the database to find the 
#     # average length (number of words) of a speech by presidents
#     # of the two major political parties.
#     # Inputs: A database file to search and a word to search for
#     # Outputs: The average speech length for presidents of each 
#     #          of the two major political parties.
#     return 0


#loop through speeches
#find avg number of words per speech
#get speech with highest average number of word, 
#get highest avg word count by speech = SELECT AVG(Count) AS "Highest Average Word count" FROM speeches GROUP BY Speech_ID
#speech averages = c.fetchall()
# SELECT Pres_ID FROM speeches WHERE Speech_ID == str(speech_avgs[0]) 
#join speeches & presidents on pres ID
