//
//  CBClassBuilderMacros.h
//  WaterQuiz
//
//  Created by bibi-apple on 10/1/15.
//
//

#ifndef __CBClassBuilderMacros_h
#define __CBClassBuilderMacros_h

#define CREATE_CLASS_LOADER(nodeType, baseLoader) \
class nodeType##Loader : public baseLoader \
{ \
public: \
SB_STATIC_NEW_AUTORELEASE_OBJECT_METHOD(nodeType##Loader, loader); \
private: \
SB_VIRTUAL_NEW_AUTORELEASE_CREATECCNODE_METHOD(nodeType); \
}

#define USE_NS \
USING_NS_CC; \
USING_NS_CC_EXT; \
using namespace spritebuilder;

#define CREATE_HANDLER(funcName) \
void funcName(cocos2d::Ref * sender, cocos2d::extension::Control::EventType pControlEvent)

#define CCBMEMBER_FUNCTIONS \
virtual bool onAssignCCBMemberVariable(cocos2d::Ref* pTarget, const char* pMemberVariableName, cocos2d::Node* pNode); \
virtual bool onAssignCCBCustomProperty(cocos2d::Ref* target, const char* memberVariableName, const cocos2d::Value& value){ return false; };

#define CCBSELECTOR_FUNCTIONS \
virtual cocos2d::SEL_MenuHandler onResolveCCBCCMenuItemSelector(cocos2d::Ref * pTarget, const char* pSelectorName){ return NULL; } \
virtual cocos2d::SEL_CallFuncN onResolveCCBCCCallFuncSelector(cocos2d::Ref * pTarget, const char* pSelectorName) { return NULL; } \
virtual cocos2d::extension::Control::Handler onResolveCCBCCControlSelector(cocos2d::Ref * pTarget, const char* pSelectorName);

#endif
