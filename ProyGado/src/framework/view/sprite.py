# Harold Selvaggi, Mauricio Eguia
# Distributed under GNU GPL v3.0

import pygame
from pygame.locals import *
from sys import exit
from framework.base.base import *
from framework.view.VComponent import *

import xmlparser

pause = False
mifont = None

class miSprite(pygame.sprite.Sprite, VComponent):

	updater = 1
	raisedMoved = False
	needToMove = False

	def __init__(self, spriteInfo, size, debug, name, updater):
		pygame.sprite.Sprite.__init__(self)
		VComponent.__init__(self, name, 0, 0, 0, 0)
		self.raisedMoved = False
		self.needToMove = False

		Component.framed = True
		
		self._size = size
		self._debug = debug
		(img,self._animGroups) = spriteInfo
		self.loadImage(img)
		#self._spriteName = spriteName
		self._start = (0,0)
		self._vector = (0,0)
		self._actualGroup = self._animGroups.keys()[0]
		self._animFrames = self._animGroups[self._actualGroup][1]
		self._actualFrame = 0
		self.dirX = False
		self.dirY = False

		self.updateRate = 0
		self._lastRect = (0,0,0,0)
		self.updater = updater
		self._acumulated_animation_time = 0

	def processEvent(self, e):
		Component.processEvent(self, e)

	def nextFrameOld(self):
		# el siguiente frame, sin evaluar los tiempos
		self._actualFrame = (self._actualFrame + 1) % len(self._animFrames)

	def lastFrame(self):
		# el frame anterior, sin evaluar los tiempos
		self._actualFrame = (self._actualFrame - 1) % len(self._animFrames)

	def nextFrame(self, time):
		# TODO: evaluar el tiempo para saber cual es el frame actual.
		self._acumulated_animation_time += time
		self.raisedMoved = False
		
		self.x = self.x + self.velX #TODO: evaluar optimizacion
		self.y = self.y + self.velY #TODO: evaluar optimizacion
		
		#if self.updateRate == 0:
		#	self.nextFrameOld()
		#	self.updateRate = 4
		#else:
		#	self.updateRate -= 1
		while self._animFrames[self._actualFrame][1] < self._acumulated_animation_time:
			self._acumulated_animation_time -= self._animFrames[self._actualFrame][1]
			self._actualFrame = (self._actualFrame + 1) % len(self._animFrames)
		
		self.dirX = False
		self.dirY = False

	def setAnim(self, animName):
		# Cambia a la animacion de nombre animName
		if(self._actualGroup != animName):
			self._actualGroup = animName
			self._animFrames = self._animGroups[self._actualGroup][1]
	
	def paint(self, screen):
		for i in range(self.updater):
			self.draw(screen)
			#self.nextFrame(1)
	
	def draw(self,screen):
		(spriteId, delay) = self._animFrames[self._actualFrame]
#		spriteId = self._actualFrame [0]
#		delay = self._actualFrame[1]

		subsprite =  self._subSprites[spriteId]
		subsurf = self._subSprites[spriteId][0]
		rectangle = self._subSprites[spriteId][1]
		(hsx,hsy) = self._subSprites[spriteId][2]
		frame = getBase().currentFrame

		hotSpotPos = self.x-hsx*self._size+frame.x,self.y-hsy*self._size+frame.y
		r = screen.blit(subsurf, hotSpotPos)
		#screen.blit(mifont.render("frame:"+str(spriteId),True, (255,255,255)),(100, 450))

	def loadImage(self, img):
		filename,diccSprites,colorkey = img
		self._image = pygame.image.load(filename)
		self._subSprites = {}
		if colorkey == None:
			colorkey = self._image.get_at((0,0))
			self._image.set_colorkey(colorkey)
		else:
			self._image.set_colorkey(colorkey)
		for key in diccSprites.keys():
			#x,y,w,h,hsx,hsy = diccSprites[key]
			rectangle, (hsx,hsy) = diccSprites[key]
			
			#rectangle = pygame.rect.Rect(int(x),int(y),int(w),int(h))
			subsurf = self._image.subsurface(rectangle)
			if self._debug:
				pygame.draw.line(subsurf,(255,0,0), (hsx-2, hsy), (hsx+2, hsy))
				pygame.draw.line(subsurf,(255,0,0), (hsx, hsy-2), (hsx, hsy+2))
			for i in range(self._size-1):
				subsurf = pygame.transform.scale2x(subsurf)
				#TODO: verificar el posible "update" de variable "rectangle"
			subsurf.set_colorkey(subsurf.get_at((0,0)))
			subsurf.set_colorkey(colorkey)
			self._subSprites[key] = (subsurf,rectangle,(hsx,hsy))
			
	def reaction(self):
		if not self.raisedMoved:
			self.raisedMoved = True
