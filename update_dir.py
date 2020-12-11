#!/usr/bin/python3

#import the files and if it's not available then the script will exit
try:
	import os
	import sys
	import shutil
except:
	print("please make sure that the os, sys, and shutil are availabe in your machine")
	exit(1)

# The  help massage of the script
help_message = """Script name : {0} 
Description : This script is used to add a certain prefix to the 
			  module names in both the RTL and the SDF files 
			  is not specified it will be named as directory_C.
Usage       : {0} <argument_1> <argument_2> [argument_3] [-h] 
Arguments   : 
             <argument_1> : Directory of folder A
             <argument_2> : Directory of folder B
             [argument_3] : Directory of folder C
   							which have the copied files
Examples    : {0} FolderA FolderB FolderC 
Examples    : {0} FolderA FolderB""" .format(sys.argv[0])


# get the current path of the script 
CurrentPath = os.path.dirname(os.path.abspath(__file__))

try:
	DirectoryA = sys.argv[1]
	DirectoryB = sys.argv[2]
except:
	print("wrong input files ")
	print(help_message)
	exit(1)


try:
	DirectoryC = sys.argv[3]
	if(DirectoryC[-1] == "/"):
		DirectoryC = DirectoryC[:-1]
		
	if not( DirectoryC in os.listdir(CurrentPath)):
		os.mkdir(DirectoryC) 

except:
	if not('directory_C'  in os.listdir(CurrentPath)):
		os.mkdir('directory_C') 

	DirectoryC ="directory_C"
try:
	filesInA = os.listdir(DirectoryA)
	filesInB = os.listdir(DirectoryB)
except:
	print("Error : either {0} or {1} is not available".format(DirectoryA, DirectoryB))
	exit(1)
#check if the / is available at the end of A directory
if(DirectoryA[-1] == "/"):
	DirectoryA = DirectoryA[:-1]

#check if the / is available at the end of B directory
if(DirectoryB[-1] == "/"):
	DirectoryB = DirectoryB[:-1]

#copy files from B to C folder if it the files is not in A
for  File in filesInB:
	if(File in filesInA):
		FileSplit = File.split(".")
		# if the file contains more than 1 . (dot) character.
		# Then we must concatenate then we must operate on the
		# last dot because it will the one we need to change.
		if (len(FileSplit) > 1):
			FileSplit[-2] = "_B.".join([FileSplit[-2],FileSplit[-1]])
			FileSplit.pop()
			# return the name to its original state  with adding _B part.
			suffix = ".".join(FileSplit)
		else:
			suffix = "_B.".join(FileSplit)
		shutil.copyfile("{0}/{1}".format(DirectoryB, File),"{0}/{1}".format(DirectoryC, suffix))
# Copy the files from A to C but ignoring the files in B 
# because it's already been copied in the last loop.
for  File in filesInA:
	if(File in filesInB):
		continue
	
	FileSplit = File.split(".")
		# if the file contains more than 1 . (dot) character.
		# Then we must concatenate then we must operate on the
		# last dot because it will the one we need to change.
	if (len(FileSplit) > 1):
		FileSplit[-2] = "_A.".join([FileSplit[-2], FileSplit[-1]])
		FileSplit.pop()
		# return the name to its original state  with adding _B part.
		suffix = ".".join(FileSplit)
	else:
		suffix = "_A.".join(FileSplit)
	shutil.copyfile("{0}/{1}".format(DirectoryA, File),"{0}/{1}".format(DirectoryC, suffix))


#check if th tree command is availabe in the machine
try:
	os.system("tree {0}".format(DirectoryC))
except:
	print("please install the tree command in your machine ")

