from framework.actions.actions import *
from framework.base.base import *
from framework.view.sprite import *
from framework.view.xmlparser import *
from framework.view.VComponent import *
from framework.gui.GComponent import *

def buildGUI():
    appState = getAppState()

    gui = getUIManager()
    tools = Panel('tools', 0, 0, 150,600)
    gui.addChild(tools)

    layout = YLayout('layout', 0, 0, 150, 600)
    tools.addChild(layout)

    # tools buttons
    spriteButton = ToggleButton('sprite', 0, 0, 'Sprite', 'arial black', 12)
    actionButton = ToggleButton('actions', 0, 0, 'Action', 'arial black', 12)

    layout.addChild(spriteButton)
    layout.addChild(actionButton)

    appState.stateObjects['spriteButton'] = spriteButton
    appState.stateObjects['actionButton'] = actionButton
    
    return gui