'''
Created on 22/02/2009

@author: Harold
'''
from framework.base.vec2d import *
from framework.base.base import *

class Action:
    def __init__(self, obj, evName):
        self.obj = obj
        self.evName = evName
        
    # EventObject event, Component sender
    def react(self, event, sender):
        print('Action received')
        
    def __raiseEvent__(self):
        if self.obj != None:
            self.obj.update(EventObject(self, self.evName, None))

# Conditional Actions

class Condition:
    def __init__(self, obj, evName, action):
        self.obj = obj
        self.evName = evName
        self.action = action
        
    def react(self, appState):
        None
    
    def __raiseEvent__(self):
        if self.obj != None:
            self.obj.notify(self, EventObject(self, self.evName))
        else:
            if self.action == None:
                base = getBase()
                base.globalEvents.append(EventObject(self, self.evName, None))
            else:
                self.action.react(self, EventObject(self, self.evName, None))

class EqualCheckerAction(Condition):
    def __init__(self, value, varname, obj, evName, action):
        Condition.__init__(self, obj, evName, action)
        self.value = value
        self.varname = varname
        
    def react(self, appState):
        if appState.stateObjects[self.varname] == self.value:
            self.__raiseEvent__()
        else:
            base = getBase()
            base.globalEvents.append(EventObject(self, self.evName, None))
            
class LessCheckerAction(Condition):
    def __init__(self, value, varname, obj, evName, action):
        Condition.__init__(self, obj, evName, action)
        self.value = value
        self.varname = varname
        
    def react(self, appState):
        if appState.stateObjects[self.varname] < self.value:
            self.__raiseEvent__()
            
class MoreCheckerAction(Condition):
    def __init__(self, value, varname, obj, evName, action):
        Condition.__init__(self, obj, evName, action)
        self.value = value
        self.varname = varname
        
    def react(self, appState):
        if appState.stateObjects[self.varname] > self.value:
            self.__raiseEvent__()
# Normal Actions

# Let you modify the value of a property
class NumericModifierAction(Action):
    def __init__(self, change, varname):
        self.change = change
        self.varname = varname
        
    # event = None
    # sender = appState
    def react(self, event, sender):
        state = getAppState()
        state.stateObjects[self.varname] = state.stateObjects[self.varname] + self.change

class PrintAction(Action):
    def react(self, event, sender):
        print('Raising event ' + event.eventName)

# Keyboard actions
        
class KeyboardController(Action):
    def __init__(self):
        None
        
    def react(self, event, sender):
        if event.parameter & 8 != 0:
            if sender.velX == -8:
                sender.velX = 0
            else:
                sender.velX = 8
        if event.parameter & 4 != 0:
            if sender.velX == 8:
                sender.velX = 0
            else:
                sender.velX = -8
        if event.parameter & 1 != 0:
            if sender.velY == -8:
                sender.velY = 0
            else:
                sender.velY = 8
        if event.parameter & 2 != 0:
            if sender.velY == 8:
                sender.velY = 0
            else:
                sender.velY = -8
        if event.parameter & 8 == 0 and event.parameter & 4 == 0:
            sender.velX = 0
        if event.parameter & 1 == 0 and event.parameter & 2 == 0:
            sender.velY = 0

class KeyboardController2(Action):
    def __init__(self):
        None

    def react(self, event, sender):
        if event.parameter & 8 != 0:
            sender.x = sender.x+8
        if event.parameter & 4 != 0:
            sender.x = sender.x-8
        if event.parameter & 1 != 0:
            sender.y = sender.y+8
        if event.parameter & 2 != 0:
            sender.y = sender.y-8

#Controla los cambios de animacion (deprecated por hardcodeos, usar KeyboardController4)
class KeyboardController3(Action):
    def __init__(self):
        None

    def react(self, event, sender):
        if event.parameter & 8 != 0:
            sender.setAnim("walkRight")
        if event.parameter & 4 != 0:
            sender.setAnim("walkLeft")
            
#Controla los cambios de animacion
class KeyboardController4(Action):
    def __init__(self, animName, keyValue):
        self.anim = animName
        self.key = keyValue
        
    def react(self, event, sender):
        if event.parameter & self.key != 0:
            sender.setAnim(self.anim)

class KeyboardController5(Action):
    def __init__(self):
        None

    def react(self, event, sender):
        if event.parameter & 8 != 0:
            sender.punto1 = (sender.punto1[0]+8,sender.punto1[1])
            sender.punto2 = (sender.punto2[0]+8,sender.punto2[1])
        if event.parameter & 4 != 0:
            sender.punto1 = (sender.punto1[0]-8,sender.punto1[1])
            sender.punto2 = (sender.punto2[0]-8,sender.punto2[1])
        if event.parameter & 1 != 0:
            sender.punto1 = (sender.punto1[0],sender.punto1[1]+8)
            sender.punto2 = (sender.punto2[0],sender.punto2[1]+8)
        if event.parameter & 2 != 0:
            sender.punto1 = (sender.punto1[0],sender.punto1[1]-8)
            sender.punto2 = (sender.punto2[0],sender.punto2[1]-8)

class MoveAction(Action):
    def __init__(self, obj, evName):
        Action.__init__(self, obj, evName)
        
    def intersect(self, x1,w1,x2,w2):
        dist = 0
        if x1 <= x2 and x1+w1 > x2:
            dist = (x1+w1 - x2)
        if x1 >= x2 and x1 + w1 < x2 + w2:
            if x2+w2 - x1-w1 > x1-x2:
                dist = (x1+w1 - x2)
            else:
                dist = (x2+w2-x1)
        if x1 >= x2 and x1+w1 > x2 + w2 and x1 < x2+w2:
            if x1 - x2 < x2+w2 - x1:
                dist = (x1+w1 - x2)
            else:
                dist = -(x2+w2-x1)
        return dist

    def react(self, event, sender):
        distX = self.intersect(sender.x, sender.width, event.sender.x, event.sender.width)
        distY = self.intersect(sender.y, sender.height, event.sender.y, event.sender.height)
        
        if distX != 0 and distY != 0:        
            if sender.velX != 0:
                event.sender.x = event.sender.x + distX
                self.__raiseEvent__()
            if sender.velY != 0:
                event.sender.y = event.sender.y + distY
                self.__raiseEvent__()

class CodeAction(Action):
    def __init__(self, code):
        self.code= code
        
    def react(self, event, sender):
        globals()['sender'] = sender
        globals()['event'] = event
        exec(self.code)

class BounceAction(Action):
    collider = None
    
    def __init__(self, collider):
        self.collider = collider
        
    def sign(self, num):
        if(num > 0):
            return 1
        elif(num < 0):
            return -1
        else:
            return 0
        
    def react(self, event, sender):
        collisionDetected = self.collider.checkCollision(sender)
        if(collisionDetected):
            normalVector = vec2d(self.collider.normalVector)
            incidentVector = vec2d(sender.velX, sender.velY)
            resultingVector = incidentVector - 2*(normalVector.dot(incidentVector))*normalVector
            
            signX = self.sign(normalVector[0]) * self.sign(incidentVector[0]) * (-1)
            signY = self.sign(normalVector[1]) * self.sign(incidentVector[1]) * (-1)
            if(signX == 0):
                signX = 1
            if(signY == 0):
                signY = 1
            
            sender.velX = resultingVector[0] * signX
            sender.velY = resultingVector[1] * signY

# Limiting actions