
from framework.actions.actions import *
from framework.base.base import *
from framework.view.sprite import *
from framework.view.xmlparser import *
from framework.view.VComponent import *
from framework.gui.GComponent import *
from framework.base.colisionador import *

base = getBase()

print('Starting demo')

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
ball.velX = 5
ball.velY = -5

padSprite = (xmlparser.parseSpriteFile('../data/pad.xml'))['pad']
pad = miSprite(padSprite, spriteSize, False, 'pad', 6)
pad.x = 300
pad.y = 473
pad.width = 100
pad.height = 15

topWall = ColisionadorHz((0,200), (600,200), (0,1))
bottomWall = ColisionadorHz((0,480), (600,480), (0,-1))
leftWall = ColisionadorVt((0,200), (0,480), (1,0))
rightWall = ColisionadorVt((600,200), (600,480), (-1,0))

limiter = ObjectMover('screenLimiter', 130, 200, 400, 250, frame, ball)

frame.addVisible(ball)
frame.addVisible(pad)
base.defineFrame(frame)
#base.addTickListener(limiter)

ball.addRelatedAction(base, BounceAction(topWall), 'collision')
ball.addRelatedAction(base, BounceAction(bottomWall), 'collision')
ball.addRelatedAction(base, BounceAction(leftWall), 'collision')
ball.addRelatedAction(base, BounceAction(rightWall), 'collision')
pad.addRelatedAction(base, KeyboardController2(), 'keyboard')

base.runSystem()
