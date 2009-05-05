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

	def run(self):
		code = self.gameLoop.gameLoop()
		self.gameLoop.clear()
		if code == 1:
			level = Level1(self.gameLoop, None)
			return level
	
	def populate(self):
		self.gameLoop.fillColor = (0,0,0)
		
		#Menu
		go = GameObject()
		menu = MenuComponent(go, ['Jugar', 'Salir'], 100, 100, 'Arial', 30, (255,255,255), (100,100,100))		
		self.gameLoop.drawable.append(go)

		enter = SpecificKeyCondition(13)
		up = SpecificKeyCondition(273)
		down = KeyReleaseCondition(274)
		up.addProxy(Action(go, 2, ComponentFamily.graphic))
		down.addProxy(Action(go, 1, ComponentFamily.graphic))
		
		equal = EqualCondition(go, ComponentFamily.graphic, 'selected', 0)
		
		play = AndCondition(enter, equal)
		play.addProxy(ReturnCodeAction(self.gameLoop, 1))
		
		exit = AndCondition(enter, NotCondition(equal))
		exit.addProxy(ReturnCodeAction(self.gameLoop, 0))
		
		# Condiciones menu
		
		self.gameLoop.conditions.append(up)
		self.gameLoop.conditions.append(down)
		self.gameLoop.conditions.append(play)
		self.gameLoop.conditions.append(exit)


class Level1(GameLevel):
	def __init__(self, loop, surface):
		GameLevel.__init__(self, loop, surface)
	
	def populate(self):		
		#Personaje
		self.gameLoop.fillColor = (255,255,255)
		characterGO = GameObject()
		Image(characterGO, '../data/bola2.PNG', 300, 230)
		gm = GravityMovement(characterGO, 0.7, -1.5, 0.01, 0.01)
		gm.gravity = True
		self.gameLoop.drawable.append(characterGO)
		self.gameLoop.tickers.append(characterGO)
		AABBComponent(characterGO, 300, 250, 20, 20)
		
		# Marcador
		marcador = GameObject()
		result = LabelComponent(marcador, 40,30, ComponentFamily.strValue, 'valor', "arial",20)
		result.color = (0,0,0)
		val = StrValueComponent(marcador)
		val.addAttr('valor', 'Puntae')
		self.gameLoop.drawable.append(marcador)

		marcador = GameObject()
		result = LabelComponent(marcador, 100,30, ComponentFamily.strValue, 'valor', "arial",20)
		result.color = (0,0,0)
		val = StrValueComponent(marcador)
		val.addAttr('valor', '0')
		self.gameLoop.drawable.append(marcador)


		timeCondition = TimerCondition(250)
		timeCondition.addProxy(AddAction(marcador, ComponentFamily.strValue, 'valor', -1))
		self.gameLoop.conditions.append(timeCondition) 
		
		#Frutas
		fruta = GameObject()
		Image(fruta, '../data/fruta.jpeg', 300, 50)
		AABBComponent(fruta, 300, 50, 50, 50)
		self.gameLoop.drawable.append(fruta)
		removeCondition = CollisionCondition(fruta, characterGO)
		removeCondition.addProxy(RemoveObjectAction(self.gameLoop, fruta, removeCondition))
		removeCondition.addProxy(AddAction(marcador, ComponentFamily.strValue, 'valor', 550))
		self.gameLoop.conditions.append(removeCondition) 

		fruta = GameObject()
		Image(fruta, '../data/fruta.jpeg', 450, 50)
		AABBComponent(fruta, 450, 50, 50, 50)
		self.gameLoop.drawable.append(fruta)
		removeCondition = CollisionCondition(fruta, characterGO)
		removeCondition.addProxy(RemoveObjectAction(self.gameLoop, fruta, removeCondition))
		removeCondition.addProxy(AddAction(marcador, ComponentFamily.strValue, 'valor', 550))
		self.gameLoop.conditions.append(removeCondition) 
		
		fruta = GameObject()
		Image(fruta, '../data/fruta.jpeg', 200, 150)
		AABBComponent(fruta, 200, 150, 50, 50)
		self.gameLoop.drawable.append(fruta)
		removeCondition = CollisionCondition(fruta, characterGO)
		removeCondition.addProxy(RemoveObjectAction(self.gameLoop, fruta, removeCondition))
		removeCondition.addProxy(AddAction(marcador, ComponentFamily.strValue, 'valor', 550))
		self.gameLoop.conditions.append(removeCondition) 

		fruta = GameObject()
		Image(fruta, '../data/fruta.jpeg', 50, 110)
		AABBComponent(fruta, 50, 110, 50, 50)
		self.gameLoop.drawable.append(fruta)
		removeCondition = CollisionCondition(fruta, characterGO)
		removeCondition.addProxy(RemoveObjectAction(self.gameLoop, fruta, removeCondition))
		removeCondition.addProxy(AddAction(marcador, ComponentFamily.strValue, 'valor', 550))
		self.gameLoop.conditions.append(removeCondition) 
		
		#Linea
		lineGO = GameObject()
		Line(lineGO, 0, 410, 1000, 410, (0,0,0))
		self.gameLoop.drawable.append(lineGO)
		
		# Piso
		floorGO = GameObject('floor')
		floorBVComponent = HorizontalCollider(floorGO, 0,400, 1000, (0,-1))
		floorCollisionCondition = CollisionCondition(floorGO, characterGO)
		floorCollisionCondition.addProxy(Action(characterGO, 4, ComponentFamily.move))
		floorCollisionCondition.addProxy(GenericSetValueAction(characterGO, 'y', 380, ComponentFamily.graphic))
		floorCollisionCondition.addProxy(GenericSetValueAction(characterGO, 'y', 380, ComponentFamily.bounding))

		# Limite anterior
		verticalGO = GameObject('v1')
		verticalBar = VerticalCollider(verticalGO, 0,0, 600, (1,0))
		verticalBarCondition = CollisionCondition(verticalGO, characterGO)
		verticalBarCondition.addProxy(GenericSetValueAction(characterGO, 'x', 1, ComponentFamily.graphic))
		verticalBarCondition.addProxy(GenericSetValueAction(characterGO, 'x', 1, ComponentFamily.bounding))
		self.gameLoop.conditions.append(verticalBarCondition)

		# Fin de pantalla
		verticalGO = GameObject('v1')
		Image(verticalGO, '../data/puerta.png', 625, 13)
		verticalBar = VerticalCollider(verticalGO, 640,0, 600, (1,0))
		verticalBarCondition = CollisionCondition(verticalGO, characterGO)
		verticalBarCondition.addProxy(ReturnCodeAction(self.gameLoop, 0))
		self.gameLoop.drawable.append(verticalGO)
		self.gameLoop.conditions.append(verticalBarCondition)
		
		# Barra
		
		barGO = GameObject('bar1')
		barBVComponent = HorizontalCollider(barGO, 320,200, 100, (0,-1))
		Image(barGO, '../data/pad.png', 320, 200)
		barCollisionCondition = CollisionCondition(barGO, characterGO)
		barCollisionCondition.addProxy(Action(characterGO, 4, ComponentFamily.move))
		barCollisionCondition.addProxy(GenericSetValueAction(characterGO, 'y', 170, ComponentFamily.graphic))
		barCollisionCondition.addProxy(GenericSetValueAction(characterGO, 'y', 170, ComponentFamily.bounding))
		self.gameLoop.conditions.append(barCollisionCondition)
		self.gameLoop.drawable.append(barGO)
		verticalGO = GameObject('v1')
		verticalBar = VerticalCollider(verticalGO, 305,140, 60, (1,0))
		verticalBarCondition = CollisionCondition(verticalGO, characterGO)
		verticalBarCondition.addProxy(GenericSetValueAction(characterGO, 'gravity', True, ComponentFamily.move))
		self.gameLoop.conditions.append(verticalBarCondition)
		verticalGO = GameObject('v2')
		verticalBar = VerticalCollider(verticalGO, 435,140, 60, (1,0))
		verticalBarCondition = CollisionCondition(verticalGO, characterGO)
		verticalBarCondition.addProxy(GenericSetValueAction(characterGO, 'gravity', True, ComponentFamily.move))
		self.gameLoop.conditions.append(verticalBarCondition)

		# Barra
		
		barGO = GameObject('bar1')
		barBVComponent = HorizontalCollider(barGO, 150,300, 100, (0,-1))
		Image(barGO, '../data/pad.png', 150, 300)
		barCollisionCondition = CollisionCondition(barGO, characterGO)
		barCollisionCondition.addProxy(Action(characterGO, 4, ComponentFamily.move))
		barCollisionCondition.addProxy(GenericSetValueAction(characterGO, 'y', 270, ComponentFamily.graphic))
		barCollisionCondition.addProxy(GenericSetValueAction(characterGO, 'y', 270, ComponentFamily.bounding))
		self.gameLoop.conditions.append(barCollisionCondition)
		self.gameLoop.drawable.append(barGO)
		verticalGO = GameObject('v1')
		verticalBar = VerticalCollider(verticalGO, 135,200, 100, (1,0))
		verticalBarCondition = CollisionCondition(verticalGO, characterGO)
		verticalBarCondition.addProxy(GenericSetValueAction(characterGO, 'gravity', True, ComponentFamily.move))
		self.gameLoop.conditions.append(verticalBarCondition)
		verticalGO = GameObject('v2')
		verticalBar = VerticalCollider(verticalGO, 272,200, 100, (1,0))
		verticalBarCondition = CollisionCondition(verticalGO, characterGO)
		verticalBarCondition.addProxy(GenericSetValueAction(characterGO, 'gravity', True, ComponentFamily.move))
		self.gameLoop.conditions.append(verticalBarCondition)
		
		# Condiciones
		
		# Condiciones movimiento
		
		self.gameLoop.conditions.append(floorCollisionCondition)
		
		left = SpecificKeyCondition(275)
		right = SpecificKeyCondition(276)
		up = SpecificKeyCondition(273)
		leftR = KeyReleaseCondition(276)
		rightR = KeyReleaseCondition(275)
		left.addProxy(Action(characterGO, 1, ComponentFamily.move))
		right.addProxy(Action(characterGO, 2, ComponentFamily.move))
		up.addProxy(Action(characterGO, 3, ComponentFamily.move))
		leftR.addProxy(Action(characterGO, 0, ComponentFamily.move))
		rightR.addProxy(Action(characterGO, 0, ComponentFamily.move))
		self.gameLoop.conditions.append(leftR)
		self.gameLoop.conditions.append(rightR)
		self.gameLoop.conditions.append(left)
		self.gameLoop.conditions.append(right)
		self.gameLoop.conditions.append(up)
	
	def run(self):
		code = self.gameLoop.gameLoop()
		self.gameLoop.clear()
		if code == 0:
			level = MyLevel(self.gameLoop, None)
			return level

manager = GameManager()
manager.run(MyLevel(None, None))
