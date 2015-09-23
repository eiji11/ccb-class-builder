import os
import sys
from subprocess import call
import shutil
import getopt
import copy
import os

from class_builder_base import *


CCNS = "cocos2d::"
CCEXTNS = CCNS + "extension::"
SBNS = "spritebuilder::"

NL = "\n"

class ClassBuilderCpp(ClassBuilder):

	def __init__(self, pProject):
		ClassBuilder.__init__(self, pProject)
		self.language = "cpp"
		
		self._nodeBaseClassMap["CCNode"] = CCNS + "Layer"
		
		self._baseClassMap["CCNode"] = CCNS + "Node"
		self._baseClassMap["CCLayer"] = CCNS + "Layer"
		self._baseClassMap["CCLayerColor"] = CCNS + "LayerColor"
		self._baseClassMap["CCLayerGradient"] = CCNS + "LayerGradient"
		
		self._baseClassMap["CCSprite"] = CCNS + "Sprite"
		self._baseClassMap["CCLabelBMFont"] = CCNS + "Label"
		self._baseClassMap["CCLabelTTF"] = CCNS + "Label"
		self._baseClassMap["CCSprite9Slice"] = CCEXTNS + "Scale9Sprite"
		
		self._baseClassMap["CCScrollView"] = CCEXTNS + "ScrollView"
		
		self._baseClassMap["CCMenu"] = CCNS + "Menu"
		self._baseClassMap["CCMenuItemImage"] = CCNS + "MenuItemImage"
		self._baseClassMap["CCControl"] = CCEXTNS + "Control"
		self._baseClassMap["CCControlButton"] = CCEXTNS + "ControlButton"
		
		self._baseClassMap["CCNodeGradient"] = CCNS + "LayerGradient"
		self._baseClassMap["CCNodeColor"] = CCNS + "LayerColor"
		
		self._baseClassMap["CCButton"] = CCEXTNS + "ControlButton"
		self._baseClassMap["CCPhysicsNode"] = CCNS + "PhysicsNode"
		
		self._baseClassMap["CCLayoutBox"] = CCNS + "LayoutBox"
		self._baseClassMap["CCSlider"] = CCEXTNS + "ControlSlider"
		self._baseClassMap["CCTextField"] = CCEXTNS + "EditBox"
	
	def buildHeaderFile(self, classInfo, destination):
		fileContents = ""
		
		classDeclarationInfo = classInfo["class"]
		
		fileContents += self.getHeaderDefineMacrosBegin(classInfo["project"], classDeclarationInfo["custom_class"])
		fileContents += self.getHeaderIncludes()
		fileContents += self.getHeaderForwardClasses(classInfo["ccb_classes"])
		fileContents += self.getHeaderClassDeclaration(classDeclarationInfo)
		
		fileContents += self.getHeaderClassCreationMethods(classDeclarationInfo["custom_class"]) + NL
		fileContents += NL
		fileContents += "private:" + NL
		fileContents += self.getHeaderSelectors(classInfo["selectors"]) + NL
		fileContents += NL
		fileContents += self.getHeaderClassDelegateMethods() + NL
		
		fileContents += NL
		
		fileContents += "private:" + NL
		fileContents += self.getHeaderClassNodeVariables(classInfo["children"])
		
		fileContents += NL + "};" + NL
		
		fileContents += NL
		
		fileContents += self.getHeaderClassSBLoaderDefinition(classDeclarationInfo)
		
		fileContents += NL
		
		fileContents += self.getHeaderDefineMacrosEnd(classInfo["project"], classDeclarationInfo["custom_class"])
		
		className = classDeclarationInfo["custom_class"]
		filePath = os.path.join(destination, className + ".h")
		file = open(filePath, "w")
		file.write(fileContents)
		
	def getHeaderDefineMacrosBegin(self, projectName, className):
		retVal = ""
		
		macro = "__" + projectName + "__" + className + "__"
		
		retVal += "#ifndef " + macro + NL
		retVal += "#define " + macro + NL
		
		retVal += NL
		
		return retVal
		
	def getHeaderDefineMacrosEnd(self, projectName, className):
		retVal = ""
		
		macro = "__" + projectName + "__" + className + "__"
		
		retVal += "#endif /* defined(" + macro + ") */" + NL
		
		return retVal
		
	def getHeaderIncludes(self):
		retVal = ""
		retVal += "#include \"cocos2d.h\"" + NL
		retVal += "#include \"extensions/cocos-ext.h\"" + NL
		retVal += "#include \"spritebuilder/SpriteBuilder.h\"" + NL
		retVal += NL
		retVal += "#include \"Defines.h\"" + NL
		retVal += NL
		
		return retVal
		
	def getHeaderForwardClasses(self, ccbClasses):
		retVal = ""
		
		for ccbClass in ccbClasses:
			retVal += "class " + ccbClass + ";" + NL
		
		retVal += NL
		
		return retVal
		
	def getHeaderClassDeclaration(self, classDefinition):
		retVal = ""
		
		retVal += "class "
		retVal += classDefinition["custom_class"]
		retVal += " : public "
		retVal += classDefinition["base_class"]
		retVal += NL + ", public " + SBNS + "CCBMemberVariableAssigner"
		retVal += NL + ", public " + SBNS + "CCBSelectorResolver"
		retVal += NL + ", public " + SBNS + "CCBAnimationManagerDelegate"
		retVal += NL + ", public " + SBNS + "NodeLoaderListener"
		retVal += NL + "{" + NL
		
		return retVal
		
	def getHeaderClassCreationMethods(self, className):
		S1 = S_(1)
		retVal = ""
		
		retVal += "public:" + NL
		retVal += S1 + "CREATE_FUNC(" + className + ");" + NL
		retVal += S1 + "static " + className + "* createFromCCB();" + NL
		
		retVal += NL
		
		retVal += S1 + className + "();" + NL
		retVal += S1 + "virtual ~" + className + "();" + NL
		
		retVal += NL
		
		retVal += S1 + "virtual void onEnter();" + NL
		retVal += S1 + "virtual void onExit();" + NL
		
		return retVal
		
		
	def getHeaderClassDelegateMethods(self):
		S1 = S_(1)
		retVal = ""
		
		retVal += S1 + "CCBMEMBER_FUNCTIONS " + NL
		retVal += S1 + "CCBSELECTOR_FUNCTIONS " + NL
		
		retVal += NL
		
		retVal += S1 + "virtual void onNodeLoaded(cocos2d::Node * pNode, spritebuilder::NodeLoader * pNodeLoader);" + NL
		
		retVal += NL
		
		retVal += S1 + "virtual void completedAnimationSequenceNamed(const char *name);" + NL
		
		return retVal
		
	def getHeaderSelectors(self, selectors):
		S1 = S_(1)
		
		retVal = ""
		
		for selector in selectors:
			retVal += S1 + "CREATE_HANDLER(" + selector + ");" + NL 
		
		return retVal
		
	def getHeaderClassNodeVariables(self, variables):
		S1 = S_(1)
		retVal = ""
		
		for variable in variables:
			classType = variable["base_class"]
			customClass = variable["custom_class"]
			
			if customClass:
				classType = customClass
			
			retVal += S1 + classType + " *" + variable["variable_name"] + ";" + NL
		
		return retVal
		
	def getHeaderClassSBLoaderDefinition(self, classDefinition):
		retVal = ""
		
		retVal += "CREATE_CLASS_LOADER(" + classDefinition["custom_class"]
		retVal += ", " + self.getBaseClassLoaderName(classDefinition["base_class"]) + ");" + NL
		
		retVal += NL
		
		return retVal
	
	def buildDefinitionFile(self, classInfo, destination):
		
		fileContents = ""
		
		classDeclarationInfo = classInfo["class"]
		
		fileContents += "#include \"" + classDeclarationInfo["custom_class"] + ".h\"" + NL
		fileContents += self.getDefinitionForwardClassesIncludes(classInfo["ccb_classes"])
		fileContents += NL
		fileContents += "USE_NS" + NL
		
		fileContents += NL
		
		fileContents += self.getDefinitionCreateMethods(classInfo)
		fileContents += NL
		fileContents += self.getDefinitionSelectorMethods(classInfo)
		fileContents += self.getDefinitionCCBMethods(classInfo) + NL
		
		
		fileContents += NL
		
		className = classDeclarationInfo["custom_class"]
		filePath = os.path.join(destination, className + ".cpp")
		file = open(filePath, "w")
		file.write(fileContents)
				
	def getDefinitionForwardClassesIncludes(self, ccbClasses):
		retVal = ""
		
		for className in ccbClasses:
			retVal += "#include \"" + className + ".h\"" + NL
			
		retVal += NL
		
		return retVal
		
	def getDefinitionCreateMethods(self, classInfo):
		retVal = ""
		
		classDeclaration = classInfo["class"]
		NS = classDeclaration["name_space"]
		className = classDeclaration["custom_class"]
		classLoaderName = className + "Loader"
		
		ccbClasses = classInfo["ccb_classes"]
		
		S1 = S_(1)
		
		retVal += className + " *" + NS + "createFromCCB()" + NL
		retVal += "{" + NL
		retVal += S1 + "NodeLoaderLibrary * ccNodeLoaderLibrary = NodeLoaderLibrary::getInstance();" + NL
		retVal += NL
		
		for ccbClass in ccbClasses:
			retVal += S1 + "ccNodeLoaderLibrary->registerNodeLoader(\"" + ccbClass + "\", "
			retVal += ccbClass + "Loader::loader());" + NL
		
		retVal += S1 + "ccNodeLoaderLibrary->registerNodeLoader(\"" + className + "\", "
		retVal += classLoaderName + "::loader());" + NL
		
		retVal += NL
		
		retVal += S1 + "spritebuilder::CCBReader *ccbReader = new spritebuilder::CCBReader(ccNodeLoaderLibrary);" + NL
		retVal += NL
		
		retVal += S1 + "return dynamic_cast<" + className + "*>(ccbReader->readNodeGraphFromFile(\"" + className + ".ccbi\"));" + NL
		
		retVal += "}" + NL
		
		retVal += NL
		
		retVal += NS + className + "() : "
		retVal += classDeclaration["base_class"] + "()"
		
		for childInfo in classInfo["children"]:
			retVal += NL + ", " + childInfo["variable_name"] + "(NULL)"
			
		retVal += NL + "{" + NL
		
		retVal += NL + "}" + NL
		
		retVal += NL
		
		retVal += NS + "~" + className + "()"
		retVal += NL + "{"
		
		for childInfo in classInfo["children"]:
			retVal += NL + S1 + "CC_SAFE_RELEASE(" + childInfo["variable_name"] + ");"
			
		retVal += NL
		retVal += "}" + NL
		
		retVal += NL
		
		retVal += "void " + NS + "onEnter()" + NL
		retVal += "{" + NL
		retVal += S1 + classDeclaration["base_class"] + "::onEnter();" + NL
		retVal += NL
		retVal += S1 + "CCBAnimationManager *animationManager = dynamic_cast<CCBAnimationManager*>(this->getUserObject());" + NL
		retVal += S1 + "animationManager->setDelegate(this);" + NL
		retVal += "}" + NL
		
		retVal += NL
		
		retVal += "void " + NS + "onExit()" + NL
		retVal += "{" + NL
		retVal += S1 + classDeclaration["base_class"] + "::onExit();" + NL
		retVal += NL
		retVal += S1 + "CCBAnimationManager *animationManager = dynamic_cast<CCBAnimationManager*>(this->getUserObject());" + NL
		retVal += S1 + "animationManager->setDelegate(NULL);" + NL
		retVal += NL
		retVal += "}" + NL
		
		return retVal
	
	def getDefinitionSelectorMethods(self, classInfo):
		S1 = S_(1)
		retVal = ""
		
		classDeclaration = classInfo["class"]
		NS = classDeclaration["name_space"]
		className = classDeclaration["custom_class"]
		selectors = classInfo["selectors"]
		
		for selector in selectors:
			retVal += "void " + NS + selector + "(cocos2d::Ref *sender, cocos2d::extension::Control::EventType pControlEvent)" + NL
			retVal += "{" + NL
			retVal += S1 + "if (pControlEvent == Control::EventType::TOUCH_UP_INSIDE)" + NL
			retVal += S1 + "{" + NL
			retVal += S_(2) + NL
			retVal += S1 + "}" + NL
			retVal += "}" + NL
			retVal += NL
		
		return retVal
		
	def getDefinitionCCBMethods(self, classInfo):
		S1 = S_(1)
		retVal = ""
		
		classDeclaration = classInfo["class"]
		NS = classDeclaration["name_space"]
		className = classDeclaration["custom_class"]
		
		retVal += NL
		retVal += "#pragma mark - CCBMemberVariableAssigner functions" + NL + NL
		
		retVal += "bool " + NS + "onAssignCCBMemberVariable(cocos2d::Ref *pTarget, const char *pMemberVariableName, cocos2d::Node *pNode)" + NL
		retVal += "{" + NL
		
		for childInfo in classInfo["children"]:
			classType = childInfo["base_class"]
			customClass = childInfo["custom_class"]
			
			if customClass:
				classType = customClass
				
			retVal += S1 + "SB_MEMBERVARIABLEASSIGNER_GLUE(this, \"" + childInfo["variable_name"] + "\", "
			retVal += classType + "*, " + childInfo["variable_name"] + ");" + NL
			
		retVal += NL
		
		retVal += S1 + "return false;" + NL
		
		retVal += "}" + NL
		
		retVal += NL + NL
		
		retVal += "#pragma mark - CCBSelectorResolver functions" + NL + NL
		
		retVal += "Control::Handler " + NS + "onResolveCCBCCControlSelector(cocos2d::Ref * pTarget, const char* pSelectorName)" + NL
		retVal += "{" + NL
		for selector in classInfo["selectors"]:
			retVal += S1 + "CCB_SELECTORRESOLVER_CCCONTROL_GLUE(this, \"" + selector + "\", " + NS + selector + ");" + NL
		
		retVal += NL
		retVal += S1 + "return NULL;" + NL
		retVal += "}" + NL
		
		retVal += NL + NL
		
		retVal += "#pragma mark - NodeLoaderListener functions" + NL + NL
		
		retVal += "void " + NS + "onNodeLoaded(cocos2d::Node * pNode, spritebuilder::NodeLoader * pNodeLoader)" + NL
		retVal += "{" + NL
		retVal += S1 + NL
		retVal += "}" + NL
		
		retVal += NL + NL
		
		retVal += "#pragma mark - CCBAnimationManagerDelegate functions" + NL + NL
		
		retVal += "void " + NS + "completedAnimationSequenceNamed(const char *name)" + NL
		retVal += "{" + NL
		
		strIf = ""
		
		for sequence in classInfo["sequences"]:
			retVal += S1 + strIf
			retVal += "if (strcmp(name, \"" + sequence + "\") == 0)" + NL
			retVal += S1 + "{" + NL
			retVal += S_(2) + NL
			retVal += S1 + "}" + NL
			strIf = "else "
		
		retVal += S1 + NL
		retVal += "}" + NL
		
		return retVal
	
	def getBaseClassNoNamespace(self, baseClass):
		retVal = ""
		
		if baseClass in self._baseClassCache:
			retVal = self._baseClassCache[baseClass]
		else:
			lastColonPos = max(0, baseClass.rfind(":"))
			retVal = baseClass[lastColonPos + 1 :]
			self._baseClassCache[baseClass] = retVal
		
		return retVal
		
	def getBaseClassLoaderName(self, baseClass):
		retVal = SBNS + self.getBaseClassNoNamespace(baseClass) + "Loader"
		
		return retVal