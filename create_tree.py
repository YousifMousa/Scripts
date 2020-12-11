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
createFolderForFiles = set()
# The  help massage of the script
help_message = 'Script name : {0} 										\n\
Description : 	This script  report the following info					\n\
				1- For directory A and B :								\n\
					a- The number of total files in the directory.		\n\
					a- The number of rtl files in the directory.		\n\
					b- The number of sdf files in the directory.		\n\
					c- The number of scr files in the directory.		\n\
					d- The number of other files in the director		\n\
				2- For rtl, sdf, scr and other directories:				\n\
					a- The number of total files in the directory.		\n\
				3- Main directory tree  								\n\
Usage       : 	{0} <argument_1> 										\n\
Arguments   :															\n\
		<argument_1> : the directory that we want to sort.				\n\
																		\n\
Examples    : 	{0} FolderA\n\
		{0} task_ws'.format(sys.argv[0].strip(" "))

# get the current path of the script 
CurrentPath = os.path.dirname(os.path.abspath(__file__))

			
folderNames= ["rtl", "scr", "sdf", "other"]
scrFiles = ["tcl", "py","sh"]
# if the user did not give the needed arguments 
# the script will print the help massege and terminate.
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

	
# this loop for recursivly find files in a directory
for root, dirs, files in os.walk(Directory, topdown=True):
	for name in files:
		fileExtension = name.split(".")[-1]
		fileExtensionL = fileExtension.lower() 
		if not (fileExtensionL in createFolderForFiles):
			fileExtensions.add(fileExtension.lower())
			# create the path of the  new copied file directory which is 
			# directory_C/sdf or directory_C/sdf. 
			
			if(fileExtensionL  == "v"):
				os.mkdir(directory_C+"/"+"rtl")
				createFolderForFiles.add("v")
			elif(fileExtensionL in scrFiles):
				os.mkdir(directory_C+"/"+"scr")
				createFolderForFiles.add("py") 
				createFolderForFiles.add("tcl")
				createFolderForFiles.add("sh")
			elif(fileExtensionL == "sdf"):
				os.mkdir(directory_C+"/"+"sdf")
				createFolderForFiles.add("sdf")
			else:
				if not("others" in os.listdir(os.path.join(CurrentPath,directory_C ))): 
					os.mkdir(directory_C+"/"+"others")
			
			
		# create the path of the  new copied file directory which is 
		# directory_C/sdf or directory_C/sdf. 
		if(fileExtension == "v"):
			NewFile_directory =os.path.join( directory_C, "rtl")
		elif(fileExtension in scrFiles):
			NewFile_directory =os.path.join( directory_C, "scr")
		elif(fileExtension  == "sdf"):
			NewFile_directory =os.path.join( directory_C, "sdf")
		else:
			NewFile_directory =os.path.join( directory_C, "others")

		NewFile_path = os.path.join( NewFile_directory, name)
		if (name in  NewFile_directory):
			continue
		shutil.copyfile(os.path.join(root, name), NewFile_path)


#check if th tree command is availabe in the machine
try:
	os.system("tree {0}".format(directory_C))
except:
	print("please install the tree command in your machine ")

