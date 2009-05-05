'''
Created on 01/04/2009

@author: Mauricio Eguia
'''

import copy
from framework.base.base import *
from framework.components.GraphicComponents import SpriteComponent
from framework.components.GraphicComponents import Line
from framework.components.GraphicComponents import Image
from framework.components.Colliders import VerticalCollider
from framework.components.MoveComponent import LeftRightMoveComponent, GravityMovement
from framework.conditions.Conditions import *
from framework.actions.Actions import *
import framework.base.xmlparser as xmlparser

class MyLevel(GameLevel):
	def __init__(self, loop, surface):
		GameLevel.__init__(self, loop, surface)
	
	def populate(self):
		go = GameObject("invader")
		go2 = GameObject("invaders Clone")
		spriteInfo = xmlparser.parseSpriteFile("../data/invadersprite.xml").values()[0] # por ahora asumo que hay solo un grupo de sprites
		#SpriteComponent(go, 100,100, spriteInfo)
		Image(go, "../data/pad.png", 100, 100)
		Image(go2, "../data/bola.png", 100, 100)

		pad2MovementComponent = LeftRightMoveComponent(go, 0.5, 0.001)
		gm = GravityMovement(go2, 0, 0.1, 0, 0.001)
		gm.stateChange(3)
		
		leftArrowPressKeyCondition = SpecificKeyCondition(275)
		leftArrowReleaseKeyCondition = KeyReleaseCondition(275)
		
		rightArrowPressKeyCondition = SpecificKeyCondition(276)
		rightArrowReleaseKeyCondition = KeyReleaseCondition(276)
		
		leftArrowPressKeyCondition.addProxy(Action(go, 1, ComponentFamily.move))
		leftArrowReleaseKeyCondition.addProxy(Action(go, 0, ComponentFamily.move))
		
		rightArrowPressKeyCondition.addProxy(Action(go, 2, ComponentFamily.move))
		rightArrowReleaseKeyCondition.addProxy(Action(go, 0, ComponentFamily.move))
		
		downWallGO = GameObject('downWall')
		Line(downWallGO, 0, 400, 640, 400,  (0, 255, 255), 5)
		


		downArrowPressKeyCondition = SpecificKeyCondition(274)
		downArrowPressKeyCondition.addProxy(CloneAction(go2, go, [self.gameLoop.drawable, self.gameLoop.tickers]))
		
		self.gameLoop.conditions.append(leftArrowPressKeyCondition)
		self.gameLoop.conditions.append(leftArrowReleaseKeyCondition)
		self.gameLoop.conditions.append(rightArrowPressKeyCondition)
		self.gameLoop.conditions.append(rightArrowReleaseKeyCondition)
		self.gameLoop.conditions.append(downArrowPressKeyCondition)



		#go2 = copy.deepcopy(go)
		
		self.gameLoop.drawable.append(go)
		self.gameLoop.tickers.append(go)

		#self.gameLoop.drawable.append(go2)
		#self.gameLoop.tickers.append(go2)
	
		self.gameLoop.drawable.append(downWallGO)
	def run(self):
		self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
