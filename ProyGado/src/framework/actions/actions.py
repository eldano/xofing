'''
Created on 22/02/2009

@author: Harold
'''



class Action():
    # EventObject event, Component sender
    def react(self, event, sender):
        print('Action received')

class PrintAction(Action):
    def react(self, event, sender):
        print('Raising event ' + event.eventName)

# Keyboard actions
        
class KeyboardController(Action):
    def react(self, event, sender):
        if event.parameter & 8 != 0:
            if sender.velX == -8:
                sender.velX = 0
            else:
                sender.velX = 8
        if event.parameter & 4 != 0:
            if sender.velX == 8:
                sender.velX = 0
            else:
                sender.velX = -8
        if event.parameter & 1 != 0:
            if sender.velY == -8:
                sender.velY = 0
            else:
                sender.velY = 8
        if event.parameter & 2 != 0:
            if sender.velY == 8:
                sender.velY = 0
            else:
                sender.velY = -8

class KeyboardController2(Action):
    def react(self, event, sender):
        if event.parameter & 8 != 0:
            sender.x = sender.x+8
        if event.parameter & 4 != 0:
            sender.x = sender.x-8
        if event.parameter & 1 != 0:
            sender.y = sender.y+8
        if event.parameter & 2 != 0:
            sender.y = sender.y-8

#Controla los cambios de animacion
class KeyboardController3(Action):
    def react(self, event, sender):
        if event.parameter & 8 != 0:
            sender.setAnim("walkRight")
        if event.parameter & 4 != 0:
            sender.setAnim("walkLeft")
# Limiting actions
