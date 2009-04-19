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
from framework.expressions.Expressions import *
from framework.components.Colliders import *

class MyLevel(GameLevel):
	def __init__(self, loop, surface):
		GameLevel.__init__(self, loop, surface)
	
	def populate(self):
		go7 = GameObject()
		go6 = GameObject()
		go5 = GameObject()
		go4 = GameObject()
		go3 = GameObject()
		go2 = GameObject()
		go1 = GameObject()
		go = GameObject()

		result = LabelComponent(go5, 20,20, ComponentFamily.strValue, 'valor', "arial",20)
		val = StrValueComponent(go5)
		val.addAttr('valor', 'Jugando')
		
		textfield = TextField(go1, 90, 175, 40, "0", "arial",20)
		button = Button(go2, 160,130, 90, "Verificar", "arial", 20, True)
		AABBComponent(go2, 160,130,90,button.height)
		
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
		
		expression = AddExpression(NumericExpression(go, ComponentFamily.strValue, 'valor'), NumericExpression(go3, ComponentFamily.strValue, 'valor'))
		expCondition = EqualExpressionCondition(expression, go1, ComponentFamily.graphic, 'text')
		inside = InsideCondition()
		inside.addParameter(go2)
		boolean = AndCondition(inside, ClickCondition(1))

		boolCond = AndCondition(boolean, expCondition)
		boolCond.addProxy(SetValueAction(go5, 'valor', 'Ganaste, prueba de nuevo'))		
		self.gameLoop.conditions.append(boolCond)

		expCondition = NotCondition(expCondition)
		boolean = AndCondition(inside, ClickCondition(1))
		boolCond = AndCondition(boolean, expCondition)
		boolCond.addProxy(SetValueAction(go5, 'valor', 'Perdiste, prueba de nuevo'))		
		self.gameLoop.conditions.append(boolCond)

		line = Line(go4, 80, 160, 140, 160, (255,255,255))
		lineMasVt = Line(go6, 80, 120, 80, 140, (255,255,255))
		lineMashZ = Line(go7, 70, 130, 90, 130, (255,255,255))
		
		self.gameLoop.drawable.append(go7)
		self.gameLoop.drawable.append(go6)
		self.gameLoop.drawable.append(go5)
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
		
		self.gameLoop.tickers.append(Updater(go1, ComponentFamily.graphic))
	
	def run(self):
		self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
