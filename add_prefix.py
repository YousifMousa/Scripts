#!/usr/bin/python3

#import the files and if it's not available then the script will exit
try:
	import os
	import sys
	import shutil
	import re
except:
#if any of the libraries are not installed
	print("please make sure that the os, sys,re and shutil are availabe in your machine")
	exit(1)
	
def CreateDir(mainPath, RelativePath):
	#Create the path of the Folder.
	FolderPath = os.path.join(mainPath,RelativePath)
	#Check if the folder or not because os.mkdir craches if the folder is not available
	try: 
		os.mkdir(FolderPath)
	except OSError as error: 
		#if the file is availble in that path then print an error massege for the user 
		print("error because of creating {0} it may exists in that path file system".format(FolderPath)) 
		#check if the user want to proceed to the next part of the program.
		YesOrNo = input("Do you want to proceed Y/N:")
		if(YesOrNo.lower() == 'n'):
			exit(1)

#function to copy files from one directory to another
def CpyFile(SrcDirectory,DesDirectory,FileName):
#fget the source and destination path and names of files
	SrcFilePath = os.path.join(SrcDirectory,FileName)
	DesFilePath = os.path.join(DesDirectory,FileName)
#Copy the files from the source to the desitnation.
	shutil.copyfile(SrcFilePath, DesFilePath)

#this function is used to remove comments also to add a prefix
def ChangeModuleName(Directory,FileName, prefix, removeComments = 0):
	#get the file path  of the file 
	FilePath = os.path.join(Directory,FileName)
	#open the file  in read write mode
	with open(FilePath, "r+")as file:
		#get the file in one string
		FileAsAstring = file.read()
		#split the file name to get the file type
		FileExtension = FilePath.split(".")
		#clear the source to rewrite it back
		file.truncate(0)
		#split the lines to remove the last line 
		FileSpliteed = FileAsAstring.split("\n")
		#get the last line to save it 
		LastLine = FileAsAstring[-1]
		#check the type of the file if it is .v
		if(FileExtension[-1].lower() == 'v'):
			#get the regex of the word after module
			matchedWord = re.search(r"(?<=\bmodule\s)(\w+)(.*\W\()", FileAsAstring)
			#check if there is a matched words
			if (matchedWord):
				#remove the matched words with a substition
				result = re.sub(r"(?<=\bmodule\s)(\w+)(.*\W\()",matchedWord[1]+"_"+prefix+"\n(", FileAsAstring,1)
				#check if the user wanted to remove the comments  
				if (removeComments):
					#remove anything starts with  //
					result = re.sub(r"(//.*)","", result) 
				#write back to the file
				file.write(result)
				#write the last line
				file.write(LastLine)
		elif(FileExtension[-1].lower() == 'sdf'):
			#get the regex of between ""
			matchedWord = re.search(r"\"(\w+)\"", FileAsAstring)
			#check if the user wanted to remove the comments  
			if (matchedWord):
				#remove the matched words with a substition
				result = re.sub(r"\"(\w+)\"", '"'+matchedWord[1]+"_"+prefix+'"', FileAsAstring) 
				#check if the user wanted to remove the comments  
				if (removeComments):
					#remove anything starts with  //
					result = re.sub(r"(//.*)","", result) 
				#write back to the file
				file.write(result)
				#write the last line
				file.write(LastLine)
	#close the file
	file.close()


# The  help massage of the script
help_message = """Script name : {0} 
Description : This script is used to change the name of the 
			  module name by adding a prefix. if a comment option 
			  is provided then it removes all the comment except
			  the comment that gives which directory this file 
			  come from.

Usage       : {0} <argument_1> <argument_2> [argument_3] 
Arguments   : 
             <argument_1> : Directory of folder A
             <argument_2> : The prefix that you want to add
             [argument_3] : -remove_comment if you want to remove 
   							the comments in the files.
Examples    : {0} FolderA FolderB FolderC 
Examples    : {0} FolderA FolderB""" .format(sys.argv[0])

# get the current path of the script 
CurrentPath = os.path.dirname(os.path.abspath(__file__))

# if the user did not give the needed arguments 
# the script will print the help massege and terminate.
try:
	Directory = sys.argv[1]
	prefix = sys.argv[2]
except:
	print("wrong input arguments ")
	print(help_message)
	exit(1)

#the name of the directory of the new created files
directory_C = "directory_C/"
# create Directory C which contains all the output files.
try:
	if not(directory_C[:-1] in os.listdir(CurrentPath)): 
		os.mkdir(directory_C)
except:
	print("can't create file in this path")
	print(help_message)
	exit(1)

removeCommentsOption = 0
#Extensions of RTL files and SDF files
Extensions = ["sdf", "v", "vhdl"]
# get the length of the arguments to know if the user
# give the comments option or not.
argumentsNum = len(sys.argv)
if(argumentsNum >3):
	AddComment  = sys.argv[3]
	if (AddComment !="-remove_comment"):
		print("wrong arguments ")
		print(help_message)
		exit(1)
	else:
		removeCommentsOption = 1

#print(Directory)
#print(os.getcwd())
fileAvailable = os.path.isdir(Directory)   

if(fileAvailable != True):
	print("wrong input file")
	print(help_message)
	exit(1)

#go through the files in the Directory 
for root, dirs, files in os.walk(Directory,topdown=True):
	#get the paths of directory_C in relation to the other Directory 
	NewDirectory= root.replace(Directory,directory_C,1)
	# loop through the directories and create them in directory_C
	for name in dirs:
		#create the Directory 
		CreateDir(NewDirectory ,name)
		#get the path of the Source and the  desintation of the current
		#copied directory
		DesFolderPath = os.path.join(NewDirectory ,name)
		SrcFolderPath  = os.path.join(root ,name)
		#get the files in the original directory 
		for file in os.listdir(SrcFolderPath):
			FilePath = os.path.join(SrcFolderPath,file)
			if os.path.isfile(FilePath):
				#copy the files to the the Directory in directory_C
				CpyFile(SrcFolderPath,DesFolderPath,file)
				#make the modification in that file 
				ChangeModuleName(DesFolderPath,file,prefix,removeCommentsOption)
		