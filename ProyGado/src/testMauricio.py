'''
Created on 01/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.components.GraphicComponents import LabelComponent
from framework.components.ValueComponents import StrValueComponent
from framework.components.GUIComponent import *
from framework.components.ResetComponent import ResetComponent
from framework.components.MoveComponent import *
from framework.conditions.Conditions import *
from framework.actions.Actions import *

class MyLevel(GameLevel):
	def __init__(self, loop, surface):
		GameLevel.__init__(self, loop, surface)
	
	def populate(self):
		go2 = GameObject()
		go = GameObject()
		window = Window(go2, 10, 10, 200, 200, "gui demo", "arial", 12)
		textfield = TextField(None, 10, 10, 200, "arial",12)
		move = LeftRightMoveComponent(go2, 0.5, 0.001)
		window.addChild(textfield)
		
		myLabel = LabelComponent(go, 100,100, ComponentFamily.strValue, 'valor', "arial",20)
		val = StrValueComponent(go)
		#val.addAttr('valor', 123456)
		resetComponent = ResetComponent(go)
		resetComponent.addAttrInit(ComponentFamily.strValue, 'valor', range(2,11))
		resetComponent.reset() #invoke directly the "reset" feature of this component
		self.gameLoop.drawable.append(go2)
		self.gameLoop.drawable.append(go)
		
		k1 = SpecificKeyCondition(275)
		k2 = SpecificKeyCondition(276)
		k3 = SpecificKeyCondition(32)
		write = KeyboardCondition()
		
		k1.addProxy(Action(go2, 1, ComponentFamily.move))
		k2.addProxy(Action(go2, 2, ComponentFamily.move))
		k3.addProxy(Action(go2, 0, ComponentFamily.move))
		write.addProxy(KeyboardAction(go2, ComponentFamily.graphic))
		self.gameLoop.conditions.append(k1)
		self.gameLoop.conditions.append(k2)
		self.gameLoop.conditions.append(k3)
		self.gameLoop.conditions.append(write)
		self.gameLoop.tickers.append(move)
	
	def run(self):
		self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
