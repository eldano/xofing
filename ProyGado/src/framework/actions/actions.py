'''
Created on 22/02/2009

@author: Harold
'''
from framework.base.vec2d import *

class Action:
    # EventObject event, Component sender
    def react(self, event, sender):
        print('Action received')

class PrintAction(Action):
    def react(self, event, sender):
        print('Raising event ' + event.eventName)

# Keyboard actions
        
class KeyboardController(Action):
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

class MoveAction(Action):
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
            if sender.velY != 0:
                event.sender.y = event.sender.y + distY

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