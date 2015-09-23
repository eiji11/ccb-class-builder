import os
import sys
from subprocess import call
import shutil
import getopt
import copy
import os

import plistlib
from pprint import pprint


def S_(spaces):
	retVal = ""
	
	for space in range(spaces):
		retVal += "\t"
	
	return retVal

class ClassBuilder:
	project = "MyGame"
	language = ""
	_ccbFileFilenamePropertyIndex = -1
	_nodeBaseClassMap = {}
	_baseClassMap = {}
	_baseClassCache = {}
	
	def __init__(self, pProject):
		self.language = "unknown"
		self.project = pProject
		
	def readFile(self, filepath, destination):		
		plist = plistlib.readPlist(filepath)
		
		topNode = plist["nodeGraph"]
		
		topNodeInfo = {}
		topNodeInfo["base_class"] = self._nodeBaseClassMap[topNode["baseClass"]]
		topNodeClass = topNode["customClass"]
		
		if not topNodeClass:
			print "ERROR IN FILE: " + filepath + "!\n"
			print "NO CUSTOM CLASS FOR ROOT NODE!"
			
			return
		
		topNodeInfo["custom_class"] = topNodeClass
		topNodeInfo["name_space"] = topNodeClass + "::"
		
		classInfo = dict()
		
		classInfo["project"] = self.project
		classInfo["class"] = topNodeInfo
		classInfo["children"] = []
		classInfo["selectors"] = []
		classInfo["ccb_classes"] = []
		classInfo["sequences"] = []
		
		topNodeChildren = topNode["children"]
		
		for child in topNodeChildren:
			self.readNodeGraph(child, classInfo)
			
		for sequenceInfo in plist["sequences"]:
			sequenceName = sequenceInfo["name"]
			classInfo["sequences"].append(sequenceName)
		
		self.buildHeaderFile(classInfo, destination)
		self.buildDefinitionFile(classInfo, destination)
		
		pprint(classInfo)
		
			
	def readNodeGraph(self, graph, classInfo):
		baseClass = graph["baseClass"]
		variableName = graph["memberVarAssignmentName"]
		
		childProperties = graph["properties"]
		
		if variableName:
			childInfo = {}
			childInfo["variable_name"] = variableName
			
			if baseClass != "CCBFile":
				childInfo["base_class"] = self._baseClassMap[baseClass]
				childInfo["custom_class"] = graph["customClass"]
			else:
				if self._ccbFileFilenamePropertyIndex == -1:
					for index in range(len(childProperties)):
						property = childProperties[index]
						if property["name"] == "ccbFile":
							self._ccbFileFilenamePropertyIndex = index
							break
					
					if self._ccbFileFilenamePropertyIndex == -1:
						return
				
				ccbFileProperty = childProperties[self._ccbFileFilenamePropertyIndex]
				
				ccbFileFilename = ccbFileProperty["value"]
				
				dotPos = ccbFileFilename.find(".")
				if dotPos == -1:
					return
				
				customClass = ccbFileFilename[:dotPos]
				
				childInfo["base_class"] = self._baseClassMap["CCLayer"]
				childInfo["custom_class"] = customClass
				
				if not customClass in classInfo["ccb_classes"]:
					classInfo["ccb_classes"].append(customClass)
			
			classInfo["children"].append(childInfo)
		
		for property in childProperties:
			if property["name"] == "block":
				blockValues = property["value"]
				selector = blockValues[0]
				selector = selector.replace(":", "")
				selectorOwner = blockValues[1]
				
				if (not selector == "") and selectorOwner == 1 and (not selector in classInfo["selectors"]):
					classInfo["selectors"].append(selector)
		
		for child in graph["children"]:
			self.readNodeGraph(child, classInfo)
			
			
	def buildHeaderFile(self, classInfo, destination):
		return
		
	def buildDefinitionFile(self, classInfo, destination):
		return
