'''
Created on 01/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *

class MyLevel(GameLevel):
    def __init__(self, loop, surface):
        GameLevel.__init__(self, loop, surface)
    
    def populate(self):
        None
    
    def run(self):
        self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))