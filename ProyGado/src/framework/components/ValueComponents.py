'''
Created on 04/04/2009

@author: Pc
'''
from framework.base.base import Component
from framework.base.base import ComponentFamily

class StrValueComponent(Component):
	family = ComponentFamily.strValue
	def __init__(self, parent):
		Component.__init__(self,parent)
		
	
	def addAttr(self, attrName, attrValue):
		setattr(self, attrName, attrValue)
	
	def removeAttr(self, attrName):
		remattr(self, attrName)
		
	def getAtrValue(self, attrName):
		getattr(self, attrName)