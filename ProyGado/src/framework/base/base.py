'''
Created on 30/03/2009

@author: Harold Selvaggi
'''
import pygame
import os

class Action:
    def __init__(self, go, transition):
        self.gameObject = go
        self.transition = transition
    
    def setGameObject(self, go):
        self.gameObject = go
    
    def execute(self):
        None

class Condition:
    def __init__(self):
        self.parameters = []
        self.proxy = None
        
    def setProxy(self, proxy):
        self.proxy = proxy

    def addParameter(self, go):
        self.parameters.append(go)
        
    def removeParameter(self, go):
        self.parameters.remove(go) 

    def evaluate(self, keyState, mouseState, elapsed):
        None
    
    def execute(self):
        proxy.execute()

class NotCondition(Condition):
    def __init__(self, c1):
        Condition.__init__(self)
        self.condition1 = c1
        
    def evaluate(self, keyState, mouseState, elapsed):
        return not self.condition1.evaluate(keyState, mouseState, elapsed)

class BinaryCondition(Condition):
    def __init__(self, c1, c2):
        Condition.__init__(self)
        self.condition1 = c1
        self.condition2 = c2
    
class AndCondition(BinaryCondition):
    def __init__(self, c1, c2):
        BinaryCondtiion.__init__(sefl, c1, c2)
    
    def evaluate(self, keyState, mouseState, elapsed):
        return self.condition1.evaluate(keyState, mouseState, elapsed) and self.condition2.evaluate(keyState, mouseState, elapsed)

class OrCondition(BinaryCondition):
    def __init__(self, c1, c2):
        BinaryCondtiion.__init__(sefl, c1, c2)
    
    def evaluate(self, keyState, mouseState, elapsed):
        return self.condition1.evaluate(keyState, mouseState, elapsed) or self.condition2.evaluate(keyState, mouseState, elapsed)
    
class Component:
    generic = 'generico'
    graphic = 'graphic'
    bounding = 'bounding'
    
    def __init__(self):
        self.family = Component.generic
    
    def stateChange(self, transition):
        None

class GraphicComponent(Component):
    def __init__(self, x, y):
        Component.__init__(self)
        self.family = Component.graphic
        self.x = x
        self.y = y
    
    def draw(self, graphics, region):
        None

class BVComponent(Component):
    def __init__(self, x, y, width, height):
        Component.__init__(self)
        self.family = Component.bounding
        self.x = x  # Chane to the native implementation
        self.y = y
        self.width = width
        self.height = height

class GameObject:
    def __init__(self):
        self.components = {}
    
    def addComponent(self, component):
        self.components[component.family] = component
    
    def getComponent(self, family):
        return self.components[family]

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
    
    def gameLoop(self):
        
        while not self.endState:
            # Update input state
            # . . .
            
            # Evaluate all conditions
            for cond in self.conditions:
                if cond.evaluate(self.keyState, self.mouseState, self.elapsed):
                    cond.execute()
            
            # Draw objects
            for comp in drawable:
                graf = comp.getComponent('graphic')
                graf.draw(self.graphics, None);
            
            pygame.display.flip()
        
        return self.returnCode
        
class GameManager:
    def __init__(self):
        # Here start pygame
        None
    
class GameLevel:
    def __init__(self, loop, surface):
        self.gameLoop = loop
        self.surface = surface
        if self.gameLoop == None:
            self.gameLoop = GameLoop(surface)
        self.populate()
    
    def populate(self):
        None    # setup the components
    
    def run(self):
        None    # State machine