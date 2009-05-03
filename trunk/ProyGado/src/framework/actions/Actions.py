'''
Created on 09/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.base.vec2d import *
import copy

class Action:
	def __init__(self, go, transition, family):
		self.gameObject = go
		self.transition = transition
		self.family = family
	
	def setGameObject(self, go):
		self.gameObject = go
	
	def execute(self):
		co = self.gameObject.getComponent(self.family)
		co.stateChange(self.transition)

class KeyboardAction(Action):
	def __init__(self, go, family):
		Action.__init__(self, go, '', family)
	
	def execute(self):
		co = self.gameObject.getComponent(self.family)
		co.stateChange(InputState.downKeys)

class BounceAction(Action):
	bouncee = None
	bouncer = None
	
	def __init__(self, bouncee, bouncer):
		self.bouncee = bouncee
		self.bouncer = bouncer
		
	def sign(self, num):
		if(num > 0):
			return 1
		elif(num < 0):
			return -1
		else:
			return 0
		
	def execute(self):
		normalVector = vec2d(self.bouncer.getComponent('bounding').normal)
		incidentVector = vec2d(self.bouncee.getComponent('move').velX, self.bouncee.getComponent('move').velY)
		
		resultingVector = incidentVector - 2*(normalVector.dot(incidentVector))*normalVector
		
		signX = self.sign(normalVector[0]) * self.sign(incidentVector[0]) * (-1)
		signY = self.sign(normalVector[1]) * self.sign(incidentVector[1]) * (-1)
		if(signX == 0):
			signX = 1
		if(signY == 0):
			signY = 1
		
		self.bouncee.getComponent('move').velX = resultingVector[0] * signX
		self.bouncee.getComponent('move').velY = resultingVector[1] * signY

class ResetAction(Action):
	def  __init__(self, go):
		Action.__init__(self, go, None, None)
	
	def execute(self):
		self.gameObject.getComponent(ComponentFamily.reset).reset()

class SetValueAction(Action):
	def __init__(self, go, attr, val):
		Action.__init__(self, go, None, None)
		self.value = val
		self.attribute = attr
	
	def execute(self):
		obj = self.gameObject.getComponent(ComponentFamily.strValue)
		obj.addAttr(self.attribute, self.value)

class SetExpressionValueAction(Action):
	def __init__(self, go, attr, family, expr):
		Action.__init__(self, go, None, family)
		self.expression = expr
		self.attribute = attr
	
	def execute(self):
		component = self.gameObject.getComponent(self.family)
		exprval = self.expression.evaluate()
		setattr(component, self.attribute, exprval)

class CopyValueAction(Action):
    def __init__(self, var, displacement):
        Action.__init__(self, go, transition, family)
        
class GenericSetValueAction(Action):
    def __init__(self, go, attr, val, family):
        Action.__init__(self, go, None, None)
        self.value = val
        self.attribute = attr
        self.family = family
    
    def execute(self):
        obj = self.gameObject.getComponent(self.family)
        obj.setattr(self.attribute, self.value)

class CloneAction(Action):
	def __init__(self, go2clone, refGo, lists2add):
		self.cloned = go2clone
		self.refGo = refGo
		self.lists2add = lists2add
	def execute(self):
		clone = copy.deepcopy(self.cloned)
		clonedGC = clone.getComponent(ComponentFamily.graphic)
		refGC = self.refGo.getComponent(ComponentFamily.graphic)
		clonedGC.x = refGC.x
		clonedGC.y = refGC.y
		for list in self.lists2add:
			list.append(clone)
		