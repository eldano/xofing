'''
Created on 01/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.components.GraphicComponents import *
from framework.components.ValueComponents import StrValueComponent

class MyLevel(GameLevel):
    def __init__(self, loop, surface):
        GameLevel.__init__(self, loop, surface)
    
    def populate(self):
		go = GameObject()
		val = StrValueComponent(go)
		val.addAttr('valor', 123456)
		myLabel = LabelComponent(go, 100,100, ComponentFamily.strValue, 'valor')
		self.gameLoop.drawable.append(go)
    
    def run(self):
        self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
