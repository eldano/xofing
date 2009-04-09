'''
Created on 30/03/2009

@author: Harold Selvaggi
'''
import pygame
import os

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

class Condition:
	def __init__(self):
		self.parameters = []
		self.proxy = []
		
	def addProxy(self, proxy):
		self.proxy.append(proxy)

	def addParameter(self, go):
		self.parameters.append(go)
		
	def removeParameter(self, go):
		self.parameters.remove(go) 

	def evaluate(self, elapsed):
		None
	
	def execute(self):
		for proxy in self.proxy:
			proxy.execute()

class TrueCondition(Condition):
	def __init__(self):
		Condition.__init__(self)
	
	def evaluate(self, elapsed):
		return True

class NotCondition(Condition):
	def __init__(self, c1):
		Condition.__init__(self)
		self.condition1 = c1
		
	def evaluate(self, elapsed):
		return not self.condition1.evaluate(elapsed)

class BinaryCondition(Condition):
	def __init__(self, c1, c2):
		Condition.__init__(self)
		self.condition1 = c1
		self.condition2 = c2
	
class AndCondition(BinaryCondition):
	def __init__(self, c1, c2):
		BinaryCondition.__init__(self, c1, c2)
	
	def evaluate(self, elapsed):
		return self.condition1.evaluate(elapsed) and self.condition2.evaluate(elapsed)

class OrCondition(BinaryCondition):
	def __init__(self, c1, c2):
		BinaryCondtiion.__init__(sefl, c1, c2)
	
	def evaluate(self, elapsed):
		return self.condition1.evaluate(elapsed) or self.condition2.evaluate(elapsed)

class ComponentFamily:
	generic = 'generic'
	graphic = 'graphic'
	bounding = 'bounding'
	move = 'move'
	gui = 'gui'
	strValue = 'strValue'
	reset = 'reset'
	
class Component:
	family = ComponentFamily.generic
	def __init__(self, gameObjectParent):
		self.parent = gameObjectParent
		if gameObjectParent != None:
			gameObjectParent.addComponent(self) #do that after setting the "family" attribute
		
	
	def update(self, elapsed):
		None
	
	def isUpdatable(self):
		return True
	
	def stateChange(self, transition):
		None

class GraphicComponent(Component):
	family = ComponentFamily.graphic
	def __init__(self, parent, x, y):
		Component.__init__(self, parent)
		self.x = x
		self.y = y

	def draw(self, graphics, region):
		None

class BVComponent(Component):
	family = ComponentFamily.bounding
	def __init__(self, parent, x, y, width, height):
		Component.__init__(self, parent)
		self.x = x  # Change to the native implementation
		self.y = y
		self.width = width
		self.height = height
	
	def inside(self, (x,y)):
		return self.x < x and self.y < y and (self.x + self.width) > x and (self.y + self.height) > y

class GameObject:
	def __init__(self):
		self.components = {}
	
	def addComponent(self, component):
		self.components[component.family] = component
	
	def getComponent(self, family):
		return self.components[family]
	
	def sendUpdate(self, elapsed):
		for up in self.components:
			up.update(elapsed)

class InputState:
	downKeys = []
	upKeys = []
	mousePos = (0,0)
	mouseButtons = (0,0,0)

class Updater:
	def __init__(self, go, family):
		self.go = go
		self.family = family
	
	def sendUpdate(self, elapsed):
		if(self.family != None):
			self.go.getComponent(self.family).update(elapsed)
		else:
			self.go.sendUpdate(elapsed)
	
class GameLoop(GameObject):
	def __init__(self, surface):
		self.drawable = []
		self.tickers = []
		self.conditions = []
		self.endState = False
		self.graphics = surface
		self.keyState = 0
		self.mouseState = 0
		self.returnCode = 0
		self.elapsed = 0
	
	def setEndGame(self):
		self.endState = True
	
	def setReturnCode(self, code):
		self.returnCode = code
	
	def __updateInputState(self, event):
		if event.type == pygame.QUIT:
			self.endState = True
			self.returnCode = -1		# The ser close by the window cross
		elif event.type == pygame.KEYDOWN:
			InputState.downKeys.append(event.key)
		elif event.type == pygame.KEYUP:
			InputState.upKeys.append(event.key)
	
	def gameLoop(self):
		clock = pygame.time.Clock()
		while not self.endState:
			self.elapsed = clock.tick() # miliseconds count
			# Update input state
			InputState.downKeys = []
			InputState.upKeys = []
			for event in pygame.event.get():
				self.__updateInputState(event)
						
			InputState.mousePos = pygame.mouse.get_pos()
			InputState.mouseButtons = pygame.mouse.get_pressed()
			
			# Evaluate all conditions
			for cond in self.conditions:
				if cond.evaluate(self.elapsed):
					cond.execute()
			
			self.graphics.fill((0,0,0))
			
			# Draw objects
			for comp in self.drawable:
				graf = comp.getComponent('graphic')
				graf.draw(self.graphics, None);
			
			pygame.display.flip()
			
			for tick in self.tickers:
				tick.sendUpdate(clock.tick())
		
		return self.returnCode
		
class GameManager:
	def __init__(self):
		# Here start pygame
		pygame.init()
		self.screen_size = (640,480)
		self.window = pygame.display.set_mode(self.screen_size)
		pygame.display.set_caption('demo')
		self.screen = pygame.display.get_surface()
		#clock = pygame.time.Clock()
	
	def run(self, level):
#		level.populate()
		level.setSurface(self.screen)
		level.run()
		
	
class GameLevel:
	def __init__(self, loop, surface):
		self.gameLoop = loop
		self.surface = surface
		if self.gameLoop == None:
			self.gameLoop = GameLoop(surface)
		self.populate()
	
	def setSurface(self, surf):
		self.surface = surf
		self.gameLoop.graphics = self.surface
	
	def populate(self):
		None	# setup the components
	
	def run(self):
		None	# State machine
