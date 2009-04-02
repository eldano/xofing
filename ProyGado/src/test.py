'''
Created on 01/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.components.GraphicComponents import *

class MyLevel(GameLevel):
    def __init__(self, loop, surface):
        GameLevel.__init__(self, loop, surface)
    
    def populate(self):
        myLabel = LabelComponent(100,100, "soy un label")
	go = GameObject()
	go.addComponent( myLabel)

	self.gameLoop.drawable.append(go)
    
    def run(self):
        self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
