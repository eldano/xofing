from framework.base.base import *

class Colisionador(Component):
    punto1 = (0,0)
    punto2 = (0,0)
    normalVector = (0,0)
    
    def __init__(self, punto1, punto2, normalVect):
        self.punto1 = punto1
        self.punto2 = punto2
        self.normalVector = normalVect
    
class ColisionadorHz(Colisionador):
    def checkCollision(self, component):
        cx = component.x
        cy = component.y
        cw = component.width
        ch = component.height
        
        if (cx + cw > self.punto1[0] and cx < self.punto2[0]):
            if(cy <= self.punto1[1] and cy + ch > self.punto1[1]):
                return True
        return False

class ColisionadorVt(Colisionador):
    
    def checkCollision(self, component):
        cx = component.x
        cy = component.y
        cw = component.width
        ch = component.height
        
        if(cy + ch > self.punto1[1] and cy < self.punto2[1]):
            if(cx <= self.punto1[0] and cx + cw > self.punto1[0]):
                return True
        return False