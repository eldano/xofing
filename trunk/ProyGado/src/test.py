'''
Created on 01/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.components.GraphicComponents import *
from framework.components.ValueComponents import StrValueComponent
from framework.components.GUIComponent import *

class MyLevel(GameLevel):
    def __init__(self, loop, surface):
        GameLevel.__init__(self, loop, surface)
    
    def populate(self):
        go2 = GameObject()
        go = GameObject()
        window = Window(go2, 10, 10, 300, 200, "ventana", "arial",12)
        myLabel = LabelComponent(go, 100,100, ComponentFamily.strValue, 'valor')
        val = StrValueComponent(go)
        myLabel = LabelComponent(go, 100,100, ComponentFamily.strValue, 'valor')
        val.addAttr('valor', 123456)
        self.gameLoop.drawable.append(go2)
        self.gameLoop.drawable.append(go)
    
    def run(self):
        self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
