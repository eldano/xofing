'''
Created on 05/04/2009

@author: Mauricio
'''

import random
from framework.base.base import *
 
class ResetComponent(Component):
	family = ComponentFamily.reset
	'''
	classdocs: TODO: documentar
	'''
	def __init__(self, parent):
		'''
		Constructor: TODO documentar
		'''
		Component.__init__(self, parent)
		self.resetDict = {} #dict --> key(family name, attribute name), value(list of initial values)

		
	def addAttrInit(self, familyName, attrName, values):
		'''
		familyName: string id of the component family
		attrName: string with the component attribute
		values: list with the initial values. If len(values)==1 then no random value could be chosen   
		'''
		self.resetDict[(familyName, attrName)] = values
		
	def delAttrInit(self, familyName, attrName):
		self.resetDict.pop((familyName, attrName), None) #TODO: check the return value?

	def reset(self):
		for familyName, attrName in self.resetDict.keys():
			co = self.parent.getComponent(familyName)
			#random choice
			setattr(co, attrName, random.choice(self.resetDict[(familyName, attrName)]))
