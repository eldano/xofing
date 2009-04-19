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
        ballGO = GameObject('bola')
        ballGraphicComponent = Image(ballGO, '../data/bola2.PNG', 300, 200)
        ballMovementComponent = XYMovement(ballGO)
        ballMovementComponent.velX = 0.05
        ballMovementComponent.velY = 0.2
        ballBVComponent = AABBComponent(ballGO, 0, 0, 20, 20)
        
        ballResetComponent = ResetComponent(ballGO)
        ballResetComponent.addAttrInit(ComponentFamily.graphic, 'x', [300])
        ballResetComponent.addAttrInit(ComponentFamily.graphic, 'y', [200])
        
        pad1GO = GameObject('pad1')
        pad1GraphicComponent = Image(pad1GO, '../data/pad.PNG', 300, 450)
        pad1MovementComponent = LeftRightMoveComponent(pad1GO, 0.5, 0.001)
        pad1BVComponent = HorizontalCollider(pad1GO, 0, 450, 100, (0,-1) )
        pad1GO.addComponent(pad1BVComponent)
        
        pad2GO = GameObject('pad2')
        pad2GraphicComponent = Image(pad2GO, '../data/pad.PNG', 300, 30)
        pad2MovementComponent = LeftRightMoveComponent(pad2GO, 0.5, 0.001)
        pad2BVComponent = HorizontalCollider(pad2GO, 0, 30, 100, (0,1) )
        pad2GO.addComponent(pad2BVComponent)
        
        floorGO = GameObject('floor')
        floorBVComponent = HorizontalCollider(floorGO, 0, 480, 640, (0,-1))
        floorCollisionCondition = CollisionCondition(floorGO, ballGO)
        floorCollisionCondition.addProxy(ResetAction(ballGO))
        #floorCollisionCondition.addProxy(BounceAction(ballGO, floorGO))
        floorGO.addComponent(floorBVComponent)
        
        roofGO = GameObject('roof')
        roofBVComponent = HorizontalCollider(roofGO, 0, 0, 640, (0,1))
        roofCollisionCondition = CollisionCondition(roofGO, ballGO)
        roofCollisionCondition.addProxy(ResetAction(ballGO))
        #roofCollisionCondition.addProxy(BounceAction(ballGO, roofGO))
        roofGO.addComponent(roofBVComponent)
        
        leftWallGO = GameObject('leftWall')
        leftWallBVComponent = VerticalCollider(leftWallGO, 0, 0, 480, (1,0))
        leftWallCollisionCondition = CollisionCondition(leftWallGO, ballGO)
        leftWallCollisionCondition.addProxy(BounceAction(ballGO, leftWallGO))
        leftWallGO.addComponent(leftWallBVComponent)
        
        rightWallGO = GameObject('rightWall')
        rightWallBVComponent = VerticalCollider(rightWallGO, 640, 0, 480, (-1,0))
        rightWallCollisionCondition = CollisionCondition(rightWallGO, ballGO)
        rightWallCollisionCondition.addProxy(BounceAction(ballGO, rightWallGO))
        rightWallGO.addComponent(rightWallBVComponent)
        
        pad1CollisionCondition = CollisionCondition(pad1GO, ballGO)
        pad1CollisionCondition.addProxy(BounceAction(ballGO, pad1GO))
        expr11 = FloatExpression(ballGO, ComponentFamily.move, 'velX')
        expr12 = FloatExpression(pad1GO, ComponentFamily.move, 'velocity')
        expr13 = AddFloatExpression(expr11, expr12)
        expr14 = ConstantExpression(4)
        expr15 = DivExpression(expr13, expr14)
        pad1CollisionCondition.addProxy(SetExpressionValueAction(ballGO, 'velX', ComponentFamily.move, expr15))
        
        pad2CollisionCondition = CollisionCondition(pad2GO, ballGO)
        pad2CollisionCondition.addProxy(BounceAction(ballGO, pad2GO))
        expr21 = FloatExpression(ballGO, ComponentFamily.move, 'velX')
        expr22 = FloatExpression(pad2GO, ComponentFamily.move, 'velocity')
        expr23 = AddFloatExpression(expr21, expr22)
        expr24 = ConstantExpression(4)
        expr25 = DivExpression(expr23, expr24)
        pad2CollisionCondition.addProxy(SetExpressionValueAction(ballGO, 'velX', ComponentFamily.move, expr25))
        
        leftArrowPressKeyCondition = SpecificKeyCondition(275)
        leftArrowReleaseKeyCondition = KeyReleaseCondition(275)
        
        rightArrowPressKeyCondition = SpecificKeyCondition(276)
        rightArrowReleaseKeyCondition = KeyReleaseCondition(276)
        
        leftArrowPressKeyCondition.addProxy(Action(pad1GO, 1, ComponentFamily.move))
        leftArrowReleaseKeyCondition.addProxy(Action(pad1GO, 0, ComponentFamily.move))
        
        rightArrowPressKeyCondition.addProxy(Action(pad1GO, 2, ComponentFamily.move))
        rightArrowReleaseKeyCondition.addProxy(Action(pad1GO, 0, ComponentFamily.move))
        
        ##
        
        aKeyPressCondition = SpecificKeyCondition(97)
        aKeyReleaseCondition = KeyReleaseCondition(97)
        
        dKeyPressCondition = SpecificKeyCondition(100)
        dKeyReleaseCondition = KeyReleaseCondition(100)
        
        aKeyPressCondition.addProxy(Action(pad2GO, 2, ComponentFamily.move))
        aKeyReleaseCondition.addProxy(Action(pad2GO, 0, ComponentFamily.move))
        
        dKeyPressCondition.addProxy(Action(pad2GO, 1, ComponentFamily.move))
        dKeyReleaseCondition.addProxy(Action(pad2GO, 0, ComponentFamily.move))
        
        #Agrego elementos al juego
        
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
        
        self.gameLoop.conditions.append(aKeyPressCondition)
        self.gameLoop.conditions.append(aKeyReleaseCondition)
        self.gameLoop.conditions.append(dKeyPressCondition)
        self.gameLoop.conditions.append(dKeyReleaseCondition)
        
        self.gameLoop.conditions.append(pad1CollisionCondition)
        self.gameLoop.conditions.append(pad2CollisionCondition)
                
    def run(self):
        self.gameLoop.gameLoop()

manager = GameManager()
manager.run(TestDanielLevel(None, None))
