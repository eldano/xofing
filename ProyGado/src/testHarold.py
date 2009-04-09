'''
Created on 01/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *
from framework.components.GraphicComponents import *
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
		go4 = GameObject()
		go3 = GameObject()
		go2 = GameObject()
		go1 = GameObject()
		go = GameObject()
		textfield = TextField(go1, 90, 175, 40, "0", "arial",20)
		button = Button(go2, 160,130, 90, "Verificar", "arial", 20, True)
		BVComponent(go2, 160,130,90,button.height)
		
		myLabel = LabelComponent(go, 100,100, ComponentFamily.strValue, 'valor', "arial",20)
		val = StrValueComponent(go)
		val.addAttr('valor', 123456)
		resetComponent = ResetComponent(go)
		resetComponent.addAttrInit(ComponentFamily.strValue, 'valor', range(2,11))
		resetComponent.reset() #invoke directly the "reset" feature of this component
		
		myLabel2 = LabelComponent(go3, 100,130, ComponentFamily.strValue, 'valor', "arial",20)
		val = StrValueComponent(go3)
		val.addAttr('valor', 123456)
		resetComponent = ResetComponent(go3)
		resetComponent.addAttrInit(ComponentFamily.strValue, 'valor', range(2,11))
		resetComponent.reset() #invoke directly the "reset" feature of this component
		
		
		line = Line(go4, 80, 160, 140, 160, (255,255,255))
		
		self.gameLoop.drawable.append(go4)
		self.gameLoop.drawable.append(go3)
		self.gameLoop.drawable.append(go2)
		self.gameLoop.drawable.append(go1)
		self.gameLoop.drawable.append(go)
		
		GUIStyle.editableTextBG = (0,0,0)
		GUIStyle.textColor = (255,255,255)
		GUIStyle.darkColor = (0,0,0)
		GUIStyle.lightColor = (0,0,0)
		
		write = KeyboardCondition()
		write.addProxy(KeyboardAction(go1, ComponentFamily.graphic))
		self.gameLoop.conditions.append(write)
		
		inside = InsideCondition()
		inside.addParameter(go2)
		boolean = AndCondition(inside, ClickCondition(1))
		boolean.addProxy(ResetAction(go3))
		boolean.addProxy(ResetAction(go))
		
		self.gameLoop.conditions.append(boolean)
	
	def run(self):
		self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
