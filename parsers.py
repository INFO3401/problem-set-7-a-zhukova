## Anastasiya Zhukova - INFO 3401
## Received help from Kexin Zhai

################################################################################
# PART #1
################################################################################
import string

def countWordsUnstructured(filename):
    wordcounts = {}
    my_file = open(filename, encoding= 'utf-8')
    for word in my_file.read().lower().split():
        for mark in string.punctuation:
            word = word.replace(mark, "")
        if word not in wordcounts:
            wordcounts[word] = 1
        else:
            wordcounts[word] += 1

    return wordcounts

################################################################################
# PART 2
################################################################################
import csv

def generateSimpleCSV(targetfile, dict_data):
	with open(targetfile, 'w', newline = '') as csvfile:
		w = csv.writer(csvfile, delimiter = ',')
		w.writerow(['Word', 'Count'])
		for key, value in dict_data.items():
			w.writerow([key, value])
	csvfile.close()
	return csvfile


# Test your part 2 code below


################################################################################
# PART 3
################################################################################
import os
from os import listdir

def countWordsMany(directory):
	dirs = os.listdir(directory)
	dictOfDicts = {}
	for files in dirs:
		eachWordCount = countWordsUnstructured(directory+"\\"+files)
		dictOfDicts[files] = eachWordCount
	return dictOfDicts

# filename[words:counts]
# open directory
# pull a list of file names (from os import listdir)
#create an empty dictionary
# loop thru list of files
	#for each file:
		#Call countwordsunstructured(filename)
		# append to empty dictionary
#Return dictionary 


# This function should create a dictionary of word count dictionaries
# The dictionary should have one dictionary per file in the directory
# Each entry in the dictionary should be a word count dictionary
# Inputs: A directory containing a set of text files
# Outputs: A dictionary containing a word count dictionary for each
#          text file in the directory

# Test your part 3 code below

################################################################################
# PART 4
################################################################################
def generateDirectoryCSV(wordCounts, targetfile):
	with open(targetfile, 'w', encoding = 'utf-8', newline = '') as csvfile:
		csvWriter = csv.writer(csvfile, delimiter = ',')
		csvWriter.writerow(['Filename', 'Word', 'Count'])
		for key, value in wordCounts.items():
			for inkey, invalue in value.items():
				csvWriter.writerow([key, inkey, invalue])
	return csvfile
	# outFile = open(targetfile, 'w+', encoding= 'utf-8')
	# csvWriter = csv.DictWriter(outFile, fieldnames = ['Filename','Word', 'Count'])
	# csvWriter.writeheader()

	# for fileName in wordCounts.keys():
	# 	for fileWord in wordCounts[fileName].keys():
	# 		csvWriter.writerow({'Filename': fileName, 'Word': fileWord, 'Count': wordCounts[fileName][fileWord]})





#open file you want to write to (specify name, 'read/write method', encoding)
#write file using DictWriter, indicate fiield names
#write the headers

#interate through the keys(words) in each file in directory from wordCountsMany():
	#for each word in dictOfDicts[for that fileName], grab its key:
		#write each row (Filename: fileName, word:fileWord, count: wordCounts fro dictOfDicts, get word from the dictOfDicts for that file)



# This function should create a CSV containing the word counts generated in
# part 3 with the header:
# Filename, Word, Count
# Inputs: A word count dictionary and a name for the target file
# Outputs: A CSV file named targetfile containing the word count data

# Test your part 4 code below

################################################################################
# PART 5
################################################################################
import json

def generateJSONFile(wordCounts, targetfile):
	with open(targetfile, 'w+') as f:
		json.dump(wordCounts, f)
	return wordCounts


#https://developer.rhino3d.com/guides/rhinopython/python-xml-json/


# This function should create an containing the word counts generated in
# part 3. Architect your JSON file such that the hierarchy will allow
# the user to quickly navigate and compare word counts between files.
# Inputs: A word count dictionary and a name for the target file
# Outputs: An JSON file named targetfile containing the word count data

# Test your part 5 code below

################################################################################
# PART 6
################################################################################
def searchCSV(csvfile, word):
	count = 0
	wordCount = 0
	with open(csvfile, "r+", encoding= 'utf-8') as inFile:
		data = csv.reader(inFile, delimiter = ',')
		next(data, None)
		for column in data:
			wordCount = int(column[2])
			if column[1] == word and wordCount > count:
				count = wordCount
				fileName = column[0]
	return fileName, wordCount


#set a counter to 0
#set another counter to 0
#open csvfile, read it, and assign to the inFile variable
#	access data in inFile with reader method, assign to variable data
#	iterate through every line
#	for every column in data:
#		word count is column 2
#		if input word matches column 1 and the word count is more than 0:
#			set counter 1 to equal counter 2 (counter 1 checks if word is more than 0 and counter 2 actually holds word count)
#			get file name, set file name equal to column 0
#return file name and word count


#https://www.foxinfotech.in/2018/09/python-read-csv-columns-into-list.html (more about reading CSVs)

#https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row/3348664
# explains why Windows csv writer generates blank lines between rows

def searchJSON(JSONfile, word):
	with open(JSONfile, 'r+', encoding = 'utf-8') as inFile:
		data = json.load(inFile)
		inFile.close()

		for fileName in data.keys():
			if word in data[fileName].keys():
				data[fileName] = (data[fileName])[word]

		maxCount = max(data.values())
		for fileName in data.keys():
			if maxCount == data[fileName]:
				return fileName, maxCount






# This function should search a CSV file from part 4 and find the filename
# with the largest count of a specified word
# Inputs: A CSV file to search and a word to search for
# Outputs: The filename containing the highest count of the target word\

#open file
# indicate that thisfile is a python obj
# search through each file (top level)
# for eachh file, whats the count for that word within that file
# save count to an empty dict fileName:count
# get max count within the empty dict max(dictName.values())
# for all keys in dict.keys:
	# if val for that key is the max, add to list
#return list of fileNames w/ max word count



# This function should search a JSON file from part 5 and find the filename
# with the largest count of a specified word
# Inputs: An JSON file to search and a word to search for
# Outputs: The filename containing the highest count of the target word

# Test your part 6 code to find which file has the highest count of a given word

# +1 bonus point for figuring out how many datapoints you had to process to
# compute this value



#The following code creates a database


import sqlite3

def createDatabase(databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('''CREATE TABLE presidents(Pres_ID int primary key, PresidentName varchar, StartDate varchar, EndDate varchar, Party varchar)''');
	c.execute('''CREATE TABLE speeches(Pres_ID int, Speech_ID int primary key, SpeechName varchar, SpeechYear varchar)''');
	c.execute('''CREATE TABLE words(Speech_ID int, Word_ID int primary key, Word varchar, Count int)''');
	conn.commit()
	conn.close()


#This one allows you to see the schema of the database created above

def schemaTest(databaseName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('''SELECT name from sqlite_master where type = 'table';''')
	print(c.fetchall())
	conn.close()


#

def tableTest(databaseName, tableName):
	conn = sqlite3.connect(databaseName)
	c = conn.cursor()
	c.execute('SELECT * FROM ' + tableName + ' LIMIT 20;')
	print(c.fetchall())
	conn.close()

################################################################################
# TESTS
################################################################################


#countWordsUnstructured('.\state-of-the-union-corpus-1989-2017\Bush_1989.txt')

#generateSimpleCSV("wordcounts.csv", countWordsUnstructured('.\state-of-the-union-corpus-1989-2017\Bush_1989.txt'))

# countWordsMany('.\state-of-the-union-corpus-1989-2017')

#generateDirectoryCSV(countWordsMany('.\state-of-the-union-corpus-1989-2017'), "multifile wordcounts.csv")

#generateJSONFile(countWordsMany('.\state-of-the-union-corpus-1989-2017'), "JSONmultifileCounts.json")

#print(searchCSV('.\multifile wordcounts.csv', 'if'))

#print(searchJSON('.\JSONmultifileCounts.json', 'if'))

#createDatabase('President_Speeches_Words.db')

#schemaTest('President_Speeches_Words')

#tableTest('President_Speeches_Words', 'words')


