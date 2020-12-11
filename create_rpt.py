#!/usr/bin/python3

#import the files and if it's not available then the script will exit
try:
	import os
	import sys
	import shutil
	import re
except:
	print("please make sure that the os, sys,re and shutil are availabe in your machine")
	exit(1)


fileExtensions = set()
# The  help massage of the script
help_message = 'Script name : {0} 										\n\
Description : 	This script is used it takes a directory as and			\n\
		argument and sort the files according to its extensions 	\n\
		and put it in directory_C\n\
\n\
Usage       : 	{0} <argument_1> 							\n\
Arguments   :												\n\
		<argument_1> : the directory that we want to sort.	\n\
\n\
Examples    : 	{0} FolderA\n\
		{0} task_ws'.format(sys.argv[0].strip(" "))

# get the current path of the script 
CurrentPath = os.path.dirname(os.path.abspath(__file__))

# if the user did not give the needed arguments 
# the script will print the help massege and terminate.
RTLFiles = ["v", "vhdl"]
numberOfArguments = len(sys.argv)
if(numberOfArguments==2):
	Directory = sys.argv[1]
elif(numberOfArguments>2):
	print("This function only takes the directory as an argument")
	print(help_message)
	exit(1)
else:
	print(help_message)
	exit(1)

try:
	Directory = sys.argv[1]
except:
	print("missing input arguments")
	print(help_message)
	exit(1)

# create Directory C which contains all the output files.
try:
	directory_C = "directory_C"
	if not("directory_C" in os.listdir(CurrentPath)): 
		os.mkdir("directory_C")
except:
	print("can't create file in this path")
	print(help_message)
	exit(1)

fileAvailable = os.path.isdir(Directory)   
if(fileAvailable != True):
	print("wrong input file")
	print(help_message)
	exit(1)


#check if the / is available at the end of A directory
if(Directory[-1] == "/"):
	Directory = Directory[:-1]

numOfFilesDict = dict()
totalFiles = dict()
# this loop for recursivly find files in a directory
for root, dirs, files in os.walk(Directory, topdown=True):
	if (dirs == os.listdir(Directory)):
		#loop in the directories
		for name in dirs:
			pathName = os.path.join(Directory, name)
			print("######### input report {0}##########".format(pathName))
			filesInTheDir = os.listdir(pathName)
			#loop in the files 
			for file in filesInTheDir :
				numOfFilesDict['total'] = numOfFilesDict.get('RTL', 0) + 1
				totalFiles['total'] = totalFiles.get('total', 0) + 1
				fileExtension = file.split(".")[-1].lower()
				if (fileExtension in RTLFiles):
					numOfFilesDict['RTL'] = numOfFilesDict.get('RTL', 0) + 1
					totalFiles['RTL'] = totalFiles.get('RTL', 0) + 1
				elif(fileExtension == "sdf"):
					numOfFilesDict[fileExtension] = numOfFilesDict.get(fileExtension, 0) + 1
					totalFiles[fileExtension] = totalFiles.get(fileExtension, 0) + 1
				else:
					numOfFilesDict["other"] = numOfFilesDict.get("other", 0) + 1
					totalFiles["other"] = totalFiles.get("other", 0) + 1

			for fileType, numberOfFiles in numOfFilesDict.items():
				print("Number of Files {0} files	:{1}".format(fileType, numberOfFiles))

for root, dirs, files in os.walk(directory_C, topdown=True):
	if (dirs == os.listdir(directory_C)):
		#loop in the directories
		for name in dirs:
			pathName = os.path.join(directory_C, name)
			print("######### output report {0}##########".format(pathName))
			numberOfFiles = len(os.listdir(pathName))
			print("Number of Files 	:{0}".format(numberOfFiles))
#check if th tree command is availabe in the machine
try:
	os.system("tree {0}".format(Directory))
	os.system("tree {0}".format(directory_C))
except:
	print("please install the tree command in your machine ")

