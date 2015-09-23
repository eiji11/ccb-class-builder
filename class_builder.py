import os
import sys
from subprocess import call
import shutil
import getopt
import copy
import os
import datetime
import time

from class_builder_base import *
from class_builder_cpp import ClassBuilderCpp


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
    
def printCurrentTime():
    return time.strftime("%X", time.gmtime())

def buildClassFile(filepath, project, language, destination):
	if language == "cpp":
		builder = ClassBuilderCpp(project)
	elif language == "objc":
		return
	else:
		return
	
	builder.readFile(filepath, destination)
	

def buildClass(argv):
	filepath = ""
	project = "MyGame"
	language = "cpp"
	destination = ""
	
	helpText = "class_builder.py -f <filepath> -p <project> -l <language> -d <destination_folder>"
	
	try:
		opts, args = getopt.getopt(argv,"hf:p:l:d:", ["filepath=", "project=", "language=", "destination="])
	except getopt.GetoptError:
		print helpText
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print helpText
			sys.exit()
		elif opt in ("-f", "--filepath"):
			filepath = arg
		elif opt in ("-p", "--project"):
			project = arg
		elif opt in ("-l", "--language"):
			language = arg
		elif opt in ("-d", "--destination"):
			destination = arg
	
	if not os.path.exists(destination):
		os.makedirs(destination)
	 
 	buildClassFile(filepath, project, language, destination)

def main(argv):
	dateStart = datetime.datetime.now()
	print "STARTED TIME: " + printCurrentTime()
	
	buildClass(argv)
	
	dateFinished = datetime.datetime.now()
	print "FINISHED TIME: " + printCurrentTime() + " : " + strfdelta(dateFinished - dateStart, "{hours}:{minutes}:{seconds}")
	

if __name__ == "__main__" and len(sys.argv) > 2:
	main(sys.argv[1:])