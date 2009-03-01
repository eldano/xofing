
from framework.actions.actions import *
from framework.base.base import *
from framework.view.sprite import *
from framework.view.xmlparser import *
from framework.view.VComponent import *
from framework.gui.GComponent import *
from framework.base.colisionador import *

base = getBase()

print('Starting demo')

ball = VComponent('bola', 50, 50, 5, 5)
ball.velX = 10
ball.velY = 20

frame = Frame('../data/back.jpeg')

spriteSize = 1
#allSprites = xmlparser.parseSpriteFile('../data/zero.xml')
#zeroSprite = allSprites['zero']
ballSprite = (xmlparser.parseSpriteFile('../data/bola.xml'))['bola']
ball = miSprite(ballSprite, spriteSize, False, 'bola', 6)
ball.x = 150
ball.y = 450
ball.width = 30
ball.height = 30
ball.velX = 1
ball.velY = -2

topWall = Colisionador((0,200), (600,200), (0,1))
bottomWall = Colisionador((0,600), (600,600), (0,1))

limiter = ObjectMover('screenLimiter', 130, 200, 400, 250, frame, ball)

frame.addVisible(ball)
base.defineFrame(frame)
base.addTickListener(limiter)

ball.addRelatedAction(base, BounceAction(topWall), 'collision')
ball.addRelatedAction(base, BounceAction(bottomWall), 'collision')

base.runSystem()
