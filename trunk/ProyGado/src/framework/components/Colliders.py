from framework.base.base import *

class AABBComponent(Component):
    family = ComponentFamily.bounding
    x = None
    y = None
    off_x = None
    off_y = None
    height = None
    width = None
    
    def __init__(self, parent, x, y, width, height):
        Component.__init__(self, parent)
        self.off_x = x
        self.off_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def inside(self, (x,y)):
        return self.x < x and self.y < y and (self.x + self.width) > x and (self.y + self.height) > y

class VerticalCollider(Component):
    family = ComponentFamily.bounding
    x = None
    y = None
    off_x = None
    off_y = None
    height = None
    normal = None
    
    def __init__(self, parent, x, y, height, normal):
        Component.__init__(self, parent)
        self.off_x = x
        self.off_y = y
        self.x = x
        self.y = y
        self.height = height
        self.normal = normal

    def checkCollision(self, boundingBox):
        cx = boundingBox.x
        cy = boundingBox.y
        cw = boundingBox.width
        ch = boundingBox.height
        
        if(cy + ch > self.y and cy < self.y + self.height):
            if(cx <= self.x and cx + cw > self.x):
                return True
        return False

class HorizontalCollider(Component):
    family = ComponentFamily.bounding
    x = None
    y = None
    off_x = None
    off_y = None
    width = None
    normal = None
    
    def __init__(self, parent, x, y, width, normal):
        Component.__init__(self, parent)
        self.off_x = x
        self.off_y = y
        self.x = x
        self.y = y
        self.width = width
        self.normal = normal

    def checkCollision(self, boundingBox):
        cx = boundingBox.x
        cy = boundingBox.y
        cw = boundingBox.width
        ch = boundingBox.height
                
        if (cx + cw > self.x and cx < self.x + self.width):
            if(cy <= self.y and cy + ch > self.y):
                return True
        return False