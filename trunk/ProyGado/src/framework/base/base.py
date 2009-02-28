'''
Created on 22/02/2009

@author: Harold Selvaggi
'''

import pygame
import os

appStateVar = None
baseSystem = None

def getBase():
    global baseSystem
    if baseSystem == None:
        baseSystem = Base()
    return baseSystem

def getAppState():
    global appStateVar
    if appStateVar == None:
        appStateVar = AppState()
    return appStateVar

# This class is used to save the application state.
class AppState:    
    def __init__(self):
        self.stateObjects = {}

# This is to pass event information
class EventObject:
    sender = ''
    eventName = ''
    parameter = ''

    def __init__(self, sender, ev, param):
        self.eventName = ev
        self.parameter = param
        self.sender = sender

# Base class for all the components in the system
class Component:
    sendEventsTo = []
    
    allEventActions = []
    eventActions = {}
    
    allRelatedActions = {}
    relatedActions = {}
    name = ''
    
    def __init__(self, name):
        self.name = name
        self.allEventActions = []
        self.eventActions = {}
        self.allRelatedActions = {}
        self.relatedActions = {}
        self.sendEventsTo = []

    # Action action, String eventName
    def addAction(self, action, eventName):
        if(eventName == None):
            self.allEventActions.append(action)
        else:
            if not self.eventActions.has_key(eventName):
                self.eventActions[eventName] = []
            self.eventActions[eventName].append(action)

    # Component source, Action action, String eventName
    def addRelatedAction(self, source, action, eventName):
        if(eventName == None):
            if not self.allRelatedActions.has_key(source):
                self.allRelatedActions[source] = []
            self.allRelatedActions[source].append(action)
        else:
            if not self.relatedActions.has_key(source):
                self.relatedActions[source] = {}
            if not self.relatedActions[source].has_key(eventName):
                self.relatedActions[source][eventName] = []
            self.relatedActions[source][eventName].append(action)
            
        # This collections should be optimized to only rise the events to the interested components
        source.sendEventsTo.append(self)

    # EventObject event
    def update(self, event):
        # Process the global events
        for act in self.allEventActions:
            act.react(event, self)
        
        for act in self.eventActions[event.eventName]:
            act.react(event, self)
        
    # Component obj, EventObject event
    def notify(self, obj, event):
        if self.allRelatedActions.has_key(obj):
            for act in self.allRelatedActions[obj]:
                act.react(event, self)
        
        if self.relatedActions.has_key(obj) and self.relatedActions[obj].has_key(event.eventName):
            for act in self.relatedActions[obj][event.eventName]:
                act.react(event, self)
    
    # Send an event to all listeners
    def __raiseEvent__(self, event):
        for receiver in self.sendEventsTo:
            receiver.notify(self, event)

# This is the only real visible object in the application 
class Frame(Component):
    x, y = 0, 0
    background = (0,0,0)
    hasBackground = True
    area = []
    painted = False
    visible = []
    
    def __init__(self, imagePath):
        Component.__init__(self, 'tontin')
        image = os.path.join('', imagePath)
        self.image = pygame.image.load(image)
        self.painted = False
        self.area = []
        self.visible = []
            
    def addVisible(self, comp):
        self.visible.append(comp)
    
    def addRestorePart(self, region):
        self.area.append(region)

    def paint(self, elapsed, screen):
        screen.blit(self.image, (self.x,self.y,100,200))
        for comp in self.visible:
            comp.nextFrame(elapsed)
            comp.paint(screen)
        
        self.painted = True
            
class Base(Component):
    # 4 bits, left, right, up, down
    keyMap = 0
    currentFrame = None
    globalReceivers = []
    
    def __init__(self):
        global baseSystem
        baseSystem = self
        self.keyMap = 0
        
        # Init the pygame system
        pygame.init()
        self.screen_size = (640,480)
        self.window = pygame.display.set_mode(self.screen_size)
        self.windowName = 'demo'
        self.gExit = False
        self.keyMap = 0
        
    def addTickListener(self, obj):
        self.globalReceivers.append(obj)
        
    def defineFrame(self, frame):
        self.currentFrame = frame
    
    def runSystem(self):
        pygame.display.set_caption(self.windowName)

        self.screen = pygame.display.get_surface()

	clock = pygame.time.Clock()

        while not self.gExit:
            currentKeys = self.keyMap
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gExit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == 275: # left$
                        self.keyMap = self.keyMap | 8
                    if event.key == 274: # down
                        self.keyMap = self.keyMap | 1
                    if event.key == 276: # right
                        self.keyMap = self.keyMap | 4
                    if event.key == 273: # top
                        self.keyMap = self.keyMap | 2
                elif event.type == pygame.KEYUP:
                    if event.key == 275:
                        self.keyMap = self.keyMap & 7
                    if event.key == 274:
                        self.keyMap = self.keyMap & 14
                    if event.key == 276:
                        self.keyMap = self.keyMap & 11
                    if event.key == 273:
                        self.keyMap = self.keyMap & 13
        
            for rec in self.globalReceivers:
                rec.update(EventObject(self, 'tick', 1))
        
            if not self.keyMap == currentKeys:
                Component.__raiseEvent__(self, EventObject(self, 'keyboardChanged', self.keyMap))
            Component.__raiseEvent__(self, EventObject(self, 'keyboard', self.keyMap))
        
            #gFrame.paint(screen)
            self.currentFrame.paint(clock.tick(), self.screen)
            pygame.display.flip()
