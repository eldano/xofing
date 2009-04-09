'''
Created on 09/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *

class KeyboardAction(Action):
    def __init__(self, go, family):
        Action.__init__(self, go, '', family)
    
    def execute(self):
        co = self.gameObject.getComponent(self.family)
        co.stateChange(InputState.downKeys)