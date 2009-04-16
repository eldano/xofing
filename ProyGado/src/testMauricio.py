'''
Created on 01/04/2009

@author: Mauricio Eguia
'''

from framework.base.base import *
from framework.components.GraphicComponents import SpriteComponent
import framework.base.xmlparser as xmlparser

class MyLevel(GameLevel):
	def __init__(self, loop, surface):
		GameLevel.__init__(self, loop, surface)
	
	def populate(self):
		go = GameObject("zero")
		spriteInfo = xmlparser.parseSpriteFile("../data/zero.xml").values()[0] # por ahora asumo que hay solo un grupo de sprites
		#zeroSprite = spriteInfo[0]
		SpriteComponent(go, 100,100, spriteInfo)
		self.gameLoop.drawable.append(go)
		self.gameLoop.tickers.append(go)
	
	def run(self):
		self.gameLoop.gameLoop()

manager = GameManager()
manager.run(MyLevel(None, None))
