import os
import sys
from subprocess import call
import shutil
import getopt
import copy
import os
import datetime
import time

from class_builder import buildClassFile
from class_builder import strfdelta
from class_builder import printCurrentTime

def buildClassInDir(argv):
	folderpath = ""
	project = "MyGame"
	language = "cpp"
	destination = ""
	
	helpText = 'class_builder.py -f <folderpath> -p <project> -l <language> -d <destination_folder>'
	
	try:
		opts, args = getopt.getopt(argv,"hf:p:l:d:", ["folderpath=", "project=", "language=", "destination="])
	except getopt.GetoptError:
		print helpText
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print helpText
			sys.exit()
		elif opt in ("-f", "--folderpath"):
			folderpath = arg
		elif opt in ("-p", "--project"):
			project = arg
		elif opt in ("-l", "--language"):
			language = arg
		elif opt in ("-d", "--destination"):
			destination = arg
	
	if not os.path.exists(destination):
		os.makedirs(destination)
	
	for dirname, dirnames, filenames in os.walk(folderpath):
		for filename in filenames:
			if not filename.startswith('.'):
				filepath = os.path.join(folderpath, filename)
				buildClassFile(filepath, project, language, destination)

def main(argv):
	dateStart = datetime.datetime.now()
	print "STARTED TIME: " + printCurrentTime()
	
	buildClassInDir(argv)
	
	dateFinished = datetime.datetime.now()
	print "FINISHED TIME: " + printCurrentTime() + " : " + strfdelta(dateFinished - dateStart, "{hours}:{minutes}:{seconds}")
	

if __name__ == "__main__" and len(sys.argv) > 2:
	main(sys.argv[1:])