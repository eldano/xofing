'''
Created on 22/02/2009

@author: Harold Selvaggi
'''

from framework.base.base import *

class VComponent(Component):
    x = 0
    y = 0
    width = 0
    height = 0
    velX = 0
    velY = 0
    
    def __init__(self, name, x, y, width, height):
        Component.__init__(self, name)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velX = 0
        self.velY = 0
    
    def paint(self):
        print('Painting')
    
    def nextFrame(self, elapsed):
        Component.__raiseEvent__(self, EventObject(self, 'move', None))
        
class ObjectMover(VComponent):
    limitedObject = None
    follower = None
    
    def __init__(self, name, x, y, width, hegiht, toMove, source):
        VComponent.__init__(self, name, x, y, width, hegiht)
        self.limitedObject = source
        self.follower = toMove;
        
    def update(self, event):        
        if self.limitedObject.x + self.limitedObject.width > self.x + self.width:
            displacement = self.limitedObject.x + self.limitedObject.width - self.x - self.width
            self.follower.x = self.follower.x - displacement
            self.x = self.x + displacement
        if self.limitedObject.x < self.x:
            displacement = self.x - self.limitedObject.x
            self.follower.x = self.follower.x + displacement
            self.x = self.x - displacement
        if self.limitedObject.y + self.limitedObject.height > self.y + self.height:
            displacement = self.limitedObject.y + self.limitedObject.height - self.y - self.height
            self.follower.y = self.follower.y - displacement
            self.y = self.y + displacement
        if self.limitedObject.y < self.y:
            displacement = self.y - self.limitedObject.y
            self.follower.y = self.follower.y + displacement
            self.y = self.y - displacement