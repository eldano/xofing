'''
Created on 22/02/2009

@author: Harold Selvaggi
'''

from framework.actions.actions import *
from framework.base.base import *
from framework.view.sprite import *
from framework.view.xmlparser import *
from framework.view.VComponent import *

print('Starting demo')

character1 = Component('demo')
enemy1 = Component('pepon')

character1.addRelatedAction(enemy1, PrintAction(), None)
#enemy1.raiseEvent(EventObject(enemy1, 'shot', None))

frame = Frame('../data/back.jpeg')

spriteSize = 3
allSprites = xmlparser.parseSpriteFile('../data/chapulin.xml')
zeroSprite = allSprites['chapulin']
character = miSprite(zeroSprite, spriteSize, False, 'chapulin', 6)
character.x = 150
character.y = 150
character.width = 100
character.height = 100

limiter = ObjectMover('screenLimiter', 130,200,400, 250, frame, character)

frame.addVisible(character)

base = getBase()
base.defineFrame(frame)
base.addTickListener(limiter)

character.addRelatedAction(base, KeyboardController2(), 'keyboard')
character.addRelatedAction(base, KeyboardController3(), 'keyboard')

base.runSystem()