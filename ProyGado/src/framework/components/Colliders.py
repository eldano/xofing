class VerticalCollider(BVComponent):
    
    x = None
    y = None
    height = None
    normal = None
    
    def __init__(self, parent, x, y, width, height, normal):
        BVComponent.__init__(self, parent, x, y, width, height)
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

class HorizontalCollider(BVComponent):
    
    x = None
    y = None
    width = None
    normal = None
    
    def __init__(self, parent, x, y, width, height, normal):
        BVComponent.__init__(self, parent, x, y, width, height)
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
            if(cy <= self.y and cy + ch > y):
                return True
        return False