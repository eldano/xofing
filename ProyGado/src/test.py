'''
Created on 01/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.components.GraphicComponents import LabelComponent
from framework.components.ValueComponents import StrValueComponent
from framework.components.GUIComponent import *
from framework.components.ResetComponent import ResetComponent

class MyLevel(GameLevel):
	def __init__(self, loop, surface):
		GameLevel.__init__(self, loop, surface)
	
	def populate(self):
		go2 = GameObject()
		go = GameObject()
		window = Window(go2, 10, 10, 300, 200, "ventana", "arial",12)
		myLabel = LabelComponent(go, 100,100, ComponentFamily.strValue, 'valor')
		val = StrValueComponent(go)
		#val.addAttr('valor', 123456)
		resetComponent = ResetComponent(go)
		resetComponent.addAttrInit(ComponentFamily.strValue, 'valor', range(2,11))
		resetComponent.reset() #invoke directly the "reset" feature of this component
		self.gameLoop.drawable.append(go2)
		self.gameLoop.drawable.append(go)
	
	def run(self):
		self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
