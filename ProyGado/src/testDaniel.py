from framework.base.base import *
from framework.components.GraphicComponents import Image
from framework.components.ValueComponents import StrValueComponent
from framework.components.GUIComponent import *
from framework.components.ResetComponent import ResetComponent
from framework.components.MoveComponent import *
from framework.components.Colliders import *
from framework.conditions.Conditions import *
from framework.actions.Actions import *


class TestDanielLevel(GameLevel):
    def __init__(self, loop, surface):
        GameLevel.__init__(self, loop, surface)
    
    def populate(self):
        ballGO = GameObject()
        ballGraphicComponent = Image(ballGO, '../data/bola.PNG', 300, 200)
        ballMovementComponent = XYMovement(ballGO)
        ballMovementComponent.velX = 0.05
        ballMovementComponent.velY = 0.2
        ballBVComponent = BVComponent(ballGO, 0, 0, 20, 20)
        
        pad1GO = GameObject()
        pad1GraphicComponent = Image(pad1GO, '../data/pad.PNG', 300, 450)
        pad1MovementComponent = LeftRightMoveComponent(pad1GO, 0.5, 0.001)
        
        pad2GO = GameObject()
        pad2GraphicComponent = Image(pad2GO, '../data/pad.PNG', 300, 30)
        pad2MovementComponent = LeftRightMoveComponent(pad2GO, 0.5, 0.001)
        
        floorGO = GameObject()
        floorBVComponent = HorizontalCollider(floorGO, 0, 480, 640, 1, (0,-1))
        floorCollisionCondition = CollisionCondition(floorGO, ballGO)
        floorCollisionCondition.addProxy(BounceAction(ballGO, floorGO))
        
        roofGO = GameObject()
        roofBVComponent = HorizontalCollider(roofGO, 0, 0, 640, 1, (0,1))
        roofCollisionCondition = CollisionCondition(roofGO, ballGO)
        roofCollisionCondition.addProxy(BounceAction(ballGO, roofGO))
        
        leftWallGO = GameObject()
        leftWallBVComponent = VerticalCollider(leftWallGO, 0, 0, 1, 480, (1,0))
        leftWallCollisionCondition = CollisionCondition(leftWallGO, ballGO)
        leftWallCollisionCondition.addProxy(BounceAction(ballGO, leftWallGO))
        
        rightWallGO = GameObject()
        rightWallBVComponent = VerticalCollider(rightWallGO, 640, 0, 1, 480, (-1,0))
        rightWallCollisionCondition = CollisionCondition(rightWallGO, ballGO)
        rightWallCollisionCondition.addProxy(BounceAction(ballGO, rightWallGO))
        
        leftArrowPressKeyCondition = SpecificKeyCondition(275)
        leftArrowReleaseKeyCondition = KeyReleaseCondition(275)
        
        rightArrowPressKeyCondition = SpecificKeyCondition(276)
        rightArrowReleaseKeyCondition = KeyReleaseCondition(276)
        
        leftArrowPressKeyCondition.addProxy(Action(pad1GO, 1, ComponentFamily.move))
        leftArrowReleaseKeyCondition.addProxy(Action(pad1GO, 0, ComponentFamily.move))
        
        rightArrowPressKeyCondition.addProxy(Action(pad1GO, 2, ComponentFamily.move))
        rightArrowReleaseKeyCondition.addProxy(Action(pad1GO, 0, ComponentFamily.move))
        
        self.gameLoop.drawable.append(ballGO)
        self.gameLoop.tickers.append(ballGO)
        
        self.gameLoop.drawable.append(pad1GO)
        self.gameLoop.drawable.append(pad2GO)
        self.gameLoop.tickers.append(pad1GO)
        self.gameLoop.tickers.append(pad2GO)
        
        self.gameLoop.conditions.append(floorCollisionCondition)
        self.gameLoop.conditions.append(roofCollisionCondition)
        self.gameLoop.conditions.append(leftWallCollisionCondition)
        self.gameLoop.conditions.append(rightWallCollisionCondition)
        
        self.gameLoop.conditions.append(leftArrowPressKeyCondition)
        self.gameLoop.conditions.append(leftArrowReleaseKeyCondition)
        self.gameLoop.conditions.append(rightArrowPressKeyCondition)
        self.gameLoop.conditions.append(rightArrowReleaseKeyCondition)
                
    def run(self):
        self.gameLoop.gameLoop()

manager = GameManager()
manager.run(TestDanielLevel(None, None))
