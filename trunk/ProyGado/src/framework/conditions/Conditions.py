'''
Created on 09/04/2009

@author: Harold Selvaggi
'''
from framework.base.base import *

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
        if InputState.downKeys.count(self.key) > 0:
            return True
        return False

