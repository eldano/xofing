'''
Created on 09/04/2009

@author: Harold Selvaggi
'''
from framework.base.base import *
from framework.expressions.Expressions import *
from framework.base.base import ComponentFamily

class KeyboardCondition(Condition):
	def __init__(self):
		Condition.__init__(self)
		
	def evaluate(self, elapsed):
		if InputState.downKeys != []:
			return True
		return False

class SpecificKeyCondition(Condition):
	def __init__(self, key):
		Condition.__init__(self)
		self.key = key
		
	def evaluate(self, elapsed):
		if InputState.downKeys.__contains__(self.key):
			return True
		return False

class KeyReleaseCondition(Condition):
	def __init__(self, key):
		Condition.__init__(self)
		self.key = key
		
	def evaluate(self, elapsed):
		if InputState.upKeys.__contains__(self.key):
			return True
		return False

class InsideCondition(Condition):
	def __init__(self):
		Condition.__init__(self)
		
	def evaluate(self, elapsed):
		for p in self.parameters:
			bnd = p.getComponent(ComponentFamily.bounding)
			return bnd.inside(InputState.mousePos)

class ButtonPressedCondition(Condition):
	def __init__(self, button):
		Condition.__init__(self)
		self.button = button
		
	def evaluate(self, elapsed):
		if self.button == 3 and InputState.mouseButtons[2] == 1:
			return True
		if self.button == 2 and InputState.mouseButtons[1] == 1:
			return True
		if self.button == 1 and InputState.mouseButtons[0] == 1:
			return True
		return False
	
class ButtonReleasedCondition(Condition):
	def __init__(self, button):
		Condition.__init__(self)
		self.button = button
		
	def evaluate(self, elapsed):
		if self.button == 3 and InputState.mouseButtons[2] == 1:
			return True
		if self.button == 2 and InputState.mouseButtons[1] == 1:
			return True
		if self.button == 1 and InputState.mouseButtons[0] == 1:
			return True
		return False
	
class ClickCondition(Condition):
	def __init__(self, button):
		Condition.__init__(self)
		self.button = button
		self.pressed = False
		
	def evaluate(self, elapsed):
		if self.button == 3 and InputState.mouseButtons[2] == 1:
			self.pressed = True
		if self.button == 2 and InputState.mouseButtons[1] == 1:
			self.pressed = True
		if self.button == 1 and InputState.mouseButtons[0] == 1:
			self.pressed = True
			
		if self.button == 3 and InputState.mouseButtons[2] == 0 and self.pressed:
			self.pressed = False
			return True
		if self.button == 2 and InputState.mouseButtons[1] == 0 and self.pressed:
			self.pressed = False
			return True
		if self.button == 1 and InputState.mouseButtons[0] == 0 and self.pressed:
			self.pressed = False
			return True
		return False
	
class CollisionCondition(Condition):
	def __init__(self, go1, go2):
		Condition.__init__(self)
		self.go1 = go1
		self.go2 = go2
	
	def evaluate(self, elapsed):
		return self.go1.getComponent(ComponentFamily.bounding).checkCollision(self.go2.getComponent(ComponentFamily.bounding))

class EqualExpressionCondition(Condition):
	def __init__(self, exp, go, family, field):
		Condition.__init__(self)
		self.expression = exp
		self.family = family
		self.field = field
		self.go = go
	
	def evaluate(self, elapsed):
		val = self.expression.evaluate()
		return val == int(getattr(self.go.getComponent(self.family), self.field, 0))

class EqualCondition(Condition):
	def __init__(self, go, family, field, value):
		Condition.__init__(self)
		self.go = go
		self.family = family
		self.field = field
		self.value = value
		
	def evaluate(self, elapsed):
		val = getattr(self.go.getComponent(self.family), self.field)
		return val == self.value

class GraphicOutOfBoundsCondition(Condition):
	#TODO: terminar de implementar
	def __init__(self, go, leftWall = None, rightWall = None, upWall = None, downWall = None):
		self.__go = go
		self.__leftWall = leftWall
		self.__rightWall = rightWall
		self.__upWall = upWall
		self.__downWall = downWall

	def evaluate(self, elapsed):
		bounds = self.go.getComponent(ComponentFamily.bounding)
		if self.__leftWall is not None:
			#evaluate if the bounding component of the game object is at the left side of the leftWall
			return True
		if self.__rightWall is not None:
			#evaluate if the bounding component of the game object is at the right side of the leftWall
			return True
		if self.__upWall is not None:
			#evaluate if the bounding component of the game object is over the upWall
			return True
		if self.__downWall is not None:
			#evaluate if the bounding component of the game object is under the downWall
			return True

class MultipleCollisionCondition(Condition):
	def __init__(self, list1, list2):
		conditionResult = False
		
		rectList1 = map(lambda x: x.getcomponent(ComponentFamily.bounding).getRect(), list1)
		rectList2 = map(lambda x: x.getcomponent(ComponentFamily.bounding).getRect(), list2)
		
		self.colideList1 = []
		self.colideList2 = set()
		
		for rectIndex in xrange(len(rectList1)):
			indexList = rectList1[rectIndex].collidelistall(rectList2)
			if indexList is not []:
				conditionResult = True
				self.colideList1.append(rectIndex)
				self.colideList2.update(indexList)
		
		return conditionResult
	
	def execute(self):
		for proxy in self.proxy:
			map(lambda x: proxy.setGameObject(x) or proxy.execute(), self.colideList1) 
			map(lambda x: proxy.setGameObject(x) or proxy.execute(), self.colideList2) 


class TimerCondition(Condition):
	def __init__(self, elapsed):
		Condition.__init__(self)
		self.elapsed = elapsed
		self.time = -1
	
	def evaluate(self, elapsed):
		self.time = self.time + elapsed
		if self.time > self.elapsed:
			self.time = -1
			return True
		return False
