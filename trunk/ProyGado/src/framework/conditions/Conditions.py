'''
Created on 09/04/2009

@author: Harold Selvaggi
'''
from framework.base.base import *
from framework.expressions.Expressions import *

class KeyboardCondition(Condition):
    def __init__(self):
        Condition.__init__(self)
        
    def evaluate(self, elapsed):
        if InputState.downKeys != []:
            return True
        return False

class SpecificKeyCondition(Condition):
    def __init__(self, key):
        Condition.__init__(self)
        self.key = key
        
    def evaluate(self, elapsed):
        if InputState.downKeys.__contains__(self.key):
            return True
        return False

class KeyReleaseCondition(Condition):
    def __init__(self, key):
        Condition.__init__(self)
        self.key = key
        
    def evaluate(self, elapsed):
        if InputState.upKeys.__contains__(self.key):
            return True
        return False

class InsideCondition(Condition):
    def __init__(self):
        Condition.__init__(self)
        
    def evaluate(self, elapsed):
        for p in self.parameters:
            bnd = p.getComponent(ComponentFamily.bounding)
            return bnd.inside(InputState.mousePos)

class ButtonPressedCondition(Condition):
    def __init__(self, button):
        Condition.__init__(self)
        self.button = button
        
    def evaluate(self, elapsed):
        if self.button == 3 and InputState.mouseButtons[2] == 1:
            return True
        if self.button == 2 and InputState.mouseButtons[1] == 1:
            return True
        if self.button == 1 and InputState.mouseButtons[0] == 1:
            return True
        return False
    
class ButtonReleasedCondition(Condition):
    def __init__(self, button):
        Condition.__init__(self)
        self.button = button
        
    def evaluate(self, elapsed):
        if self.button == 3 and InputState.mouseButtons[2] == 1:
            return True
        if self.button == 2 and InputState.mouseButtons[1] == 1:
            return True
        if self.button == 1 and InputState.mouseButtons[0] == 1:
            return True
        return False
    
class ClickCondition(Condition):
    def __init__(self, button):
        Condition.__init__(self)
        self.button = button
        self.pressed = False
        
    def evaluate(self, elapsed):
        if self.button == 3 and InputState.mouseButtons[2] == 1:
            self.pressed = True
        if self.button == 2 and InputState.mouseButtons[1] == 1:
            self.pressed = True
        if self.button == 1 and InputState.mouseButtons[0] == 1:
            self.pressed = True
            
        if self.button == 3 and InputState.mouseButtons[2] == 0 and self.pressed:
            self.pressed = False
            return True
        if self.button == 2 and InputState.mouseButtons[1] == 0 and self.pressed:
            self.pressed = False
            return True
        if self.button == 1 and InputState.mouseButtons[0] == 0 and self.pressed:
            self.pressed = False
            return True
        return False
    
class CollisionCondition(Condition):
    def __init__(self, go1, go2):
        Condition.__init__(self)
        self.go1 = go1
        self.go2 = go2
    
    def evaluate(self, elapsed):
        return self.go1.getComponent(ComponentFamily.bounding).checkCollision(self.go2.getComponent(ComponentFamily.bounding))

class EqualExpressionCondition(Condition):
    def __init__(self, exp, go, family, field):
        Condition.__init__(self)
        self.expression = exp
        self.family = family
        self.field = field
        self.go = go
    
    def evaluate(self, elapsed):
        val = self.expression.evaluate()
        return val == int(getattr(self.go.getComponent(self.family), self.field, 0))

class EqualCondition(Condition):
    def __init__(self, go, family, field, value):
        Condition.__init__(self)
        self.go = go
        self.family = family
        self.field = field
        self.value = value
        
    def evaluate(self, elapsed):
        val = getattr(self.go.getComponent(self.family), self.field)
        return val == self.value

class TimerCondition(Condition):
    def __init__(self, elapsed):
        Condition.__init__(self)
        self.elapsed = elapsed
        self.time = -1
    
    def evaluate(self, elapsed):
        self.time = self.time + elapsed
        if self.time > self.elapsed:
            self.time = -1
            return True
        return False