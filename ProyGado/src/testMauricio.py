'''
Created on 01/04/2009

@author: Mauricio Eguia
'''

from framework.base.base import *
from framework.components.GraphicComponents import SpriteComponent
from framework.components.MoveComponent import LeftRightMoveComponent
from framework.conditions.Conditions import *
from framework.actions.Actions import *
import framework.base.xmlparser as xmlparser

class MyLevel(GameLevel):
	def __init__(self, loop, surface):
		GameLevel.__init__(self, loop, surface)
	
	def populate(self):
		go = GameObject("invader")
		spriteInfo = xmlparser.parseSpriteFile("../data/invadersprite.xml").values()[0] # por ahora asumo que hay solo un grupo de sprites
		#zeroSprite = spriteInfo[0]
		SpriteComponent(go, 100,100, spriteInfo)

		pad2MovementComponent = LeftRightMoveComponent( go, 0.5, 0.001)

	        leftArrowPressKeyCondition = SpecificKeyCondition(275)
        	leftArrowReleaseKeyCondition = KeyReleaseCondition(275)
        
	        rightArrowPressKeyCondition = SpecificKeyCondition(276)
        	rightArrowReleaseKeyCondition = KeyReleaseCondition(276)
        
        	leftArrowPressKeyCondition.addProxy(Action(go, 1, ComponentFamily.move))
	        leftArrowReleaseKeyCondition.addProxy(Action(go, 0, ComponentFamily.move))
        
	        rightArrowPressKeyCondition.addProxy(Action(go, 2, ComponentFamily.move))
        	rightArrowReleaseKeyCondition.addProxy(Action(go, 0, ComponentFamily.move))

	        leftWallGO = GameObject('leftWall')
        	leftWallGraphicComponent = Line(leftWallGO, 0, 0, 0, 480, (0,255,255), 5)
	        leftWallBVComponent = VerticalCollider(leftWallGO, 0, 0, 480, (1,0))
        	leftWallCollisionCondition = CollisionCondition(leftWallGO, ballGO)
	        leftWallCollisionCondition.addProxy(BounceAction(ballGO, leftWallGO))
        
        	rightWallGO = GameObject('rightWall')
	        rightWallGraphicComponent = Line(rightWallGO, 640, 0, 640, 480, (0,255,255), 5)
        	rightWallBVComponent = VerticalCollider(rightWallGO, 640, 0, 480, (-1,0))
	        rightWallCollisionCondition = CollisionCondition(rightWallGO, ballGO)
        	rightWallCollisionCondition.addProxy(BounceAction(ballGO, rightWallGO))


	        self.gameLoop.conditions.append(leftArrowPressKeyCondition)
        	self.gameLoop.conditions.append(leftArrowReleaseKeyCondition)
	        self.gameLoop.conditions.append(rightArrowPressKeyCondition)
        	self.gameLoop.conditions.append(rightArrowReleaseKeyCondition)




		
		self.gameLoop.drawable.append(go)
		self.gameLoop.tickers.append(go)
	
	def run(self):
		self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
