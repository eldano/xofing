'''
Created on 09/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.base.vec2d import *

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
        normalVector = vec2d(self.bouncer.getComponent('bounding').normalVector)
        incidentVector = vec2d(self.bouncee.getComponent('move').velX, self.bouncee.getComponent('move').velY)
        
        resultingVector = incidentVector - 2*(normalVector.dot(incidentVector))*normalVector
        
        signX = self.sign(normalVector[0]) * self.sign(incidentVector[0]) * (-1)
        signY = self.sign(normalVector[1]) * self.sign(incidentVector[1]) * (-1)
        if(signX == 0):
            signX = 1
        if(signY == 0):
            signY = 1
        
        bouncee.velX = resultingVector[0] * signX
        bouncee.velY = resultingVector[1] * signY
