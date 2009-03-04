'''
Created on 22/02/2009

@author: Harold Selvaggi
'''

from framework.actions.actions import *
from framework.base.base import *
from framework.view.sprite import *
from framework.view.xmlparser import *
from framework.view.VComponent import *
from framework.gui.GComponent import *
from ide.gui.main import *

base = getBase()
state = getAppState()

state.stateObjects['vida'] = 100

print('Starting demo')

character1 = Component('demo')
enemy1 = Component('pepon')

#enemy1.raiseEvent(EventObject(enemy1, 'shot', None))

frame = Frame('../data/back.jpeg')

spriteSize = 3
#allSprites = xmlparser.parseSpriteFile('../data/zero.xml')
#zeroSprite = allSprites['zero']
allSprites = xmlparser.parseSpriteFile('../data/chapulin.xml')
zeroSprite = allSprites['chapulin']
character = miSprite(zeroSprite, spriteSize, False, 'megaman', 6)
character.x = 150
character.y = 450
character.width = 100
character.height = 100

enemy1 = miSprite(zeroSprite, spriteSize, False, 'tontoman', 6)
enemy1.x = 250
enemy1.y = 450
enemy1.width = 100
enemy1.height = 100

limiter = ObjectMover('screenLimiter', 130,200,400, 250, frame, character)



#gui.addRelatedAction(btn1, CodeAction('event.sender.addChild(event.sender.createWindow(\'wnd\', 150,150,300,300, \'Ventanita1\', \'arial\', 15, False))'), 'click')

gui = buildGUI()

frame.addVisible(character)
frame.addVisible(enemy1)
frame.addVisible(gui)

base.defineFrame(frame)
base.addTickListener(limiter)

character.addRelatedAction(base, KeyboardController(), 'keyboard')
character.addRelatedAction(base, KeyboardController4('walkRight', 8), 'keyboard')
character.addRelatedAction(base, KeyboardController4('walkLeft', 4), 'keyboard')

character.addRelatedAction(enemy1, MoveAction(character, 'impacto'), 'move')
character.addAction(NumericModifierAction(-1, 'vida'), 'impacto')

base.conditions.append(LessCheckerAction(0, 'vida', None, None, CodeAction('print(\'Muerto\')')))

base.runSystem()
