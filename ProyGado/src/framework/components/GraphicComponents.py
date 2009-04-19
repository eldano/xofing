import pygame
import os
pygame.font.init()
#from framework.base.base import *
from framework.base.base import GraphicComponent

class LabelComponent(GraphicComponent):
	def __init__(self, parent, x, y, componentFamily, attrName, font, size, go = None):
		GraphicComponent.__init__(self, parent, x, y)
		self.componentFamily = componentFamily
		self.attrName = attrName
		self.font = font
		self.size = size
		self.sysFont = pygame.font.SysFont(self.font, self.size) 
		if go == None:
			self.go = parent
		else:
			self.go = go

	def draw(self, graphics, region):
		co = self.go.getComponent(self.componentFamily)
		value = getattr(co, self.attrName, 'sin valor')
		graphics.blit(self.sysFont.render(str(value), True, (255,255,255)), (self.x,self.y))
		#TODO: (Mauricio) : value may be None 

class Image(GraphicComponent):
	def __init__(self, parent, imagePath, x, y, w = None, h = None):
		'''
		The rectangle that define the area to draw out of the file may not be the same size of the image file.
		If the parameter w(or h) are None, then the value of w(or h) is the same that the image file 
		'''
		GraphicComponent.__init__(self, parent, x, y)
		imageOsPath = os.path.join('', imagePath)
		self.image = pygame.image.load(imageOsPath)
		if w is None:
			self.w = self.image.get_rect().w
		else:
			self.w = w
		if h is None:
			self.h = self.image.get_rect().h
		else:
			self.h = h
	
	def draw(self, graphics, region):
		pygame.display.get_surface().blit(self.image, (self.x,self.y,self.w,self.h))

	def update(self, dt):
		pass

class Line(GraphicComponent):
	def __init__(self, parent, x, y, x2, y2, color, width = None):
		GraphicComponent.__init__(self, parent, x, y)
		self.x2 = x2
		self.y2 = y2
		self.color = color
		self.width = width
	
	def draw(self, graphics, region):
		pygame.draw.line(graphics, self.color, (self.x,self.y), (self.x2,self.y2), self.width)
		
class SpriteComponent(GraphicComponent):
	def __init__(self, parent, x, y, spriteInfo):
		GraphicComponent.__init__(self, parent, x, y)
		self.__size = 1#size
		self.__debug = False#debug
		(img,self.__animGroups) = spriteInfo
		(img,self.__animGroups) = spriteInfo
		self.loadImage(img)
		self.__start = (0,0)
		self.__vector = (0,0)
		self.__actualGroup = self.__animGroups.keys()[0]	#TODO: fix me
		self.__animFrames = self.__animGroups[self.__actualGroup][1]	#TODO: fix me
		self.__actualFrame = 0
		self.__lastRect = (0,0,0,0)
		self.__acumulated_animation_time = 0

	def update(self, time):
		""" actualiza la animacion (con respecto a la secuencia de frames)"""
		self.__acumulated_animation_time += time
		while self.__animFrames[self.__actualFrame][1] < self.__acumulated_animation_time:
			self.__acumulated_animation_time -= self.__animFrames[self.__actualFrame][1]
			self.__actualFrame = (self.__actualFrame + 1) % len(self.__animFrames)

	def setAnim(self, animName):
		""" Cambia a la animacion de nombre animName"""
		if(self._actualGroup != animName):
			self._actualGroup = animName
			self._animFrames = self._animGroups[self._actualGroup][1]

	def draw(self,screen, region):
		(spriteId, delay) = self.__animFrames[self.__actualFrame]
#		spriteId = self._actualFrame [0]
#		delay = self._actualFrame[1]

		subsprite = self.__subSprites[spriteId]
		subsurf = self.__subSprites[spriteId][0]	#TODO: cambiar valor por constante a nivel de clase
		rectangle = self.__subSprites[spriteId][1]	#TODO: cambiar valor por constante a nivel de clase
		(hsx,hsy) = self.__subSprites[spriteId][2]	#TODO: cambiar valor por constante a nivel de clase

		hotSpotPos = self.x-hsx*self.__size,self.y-hsy*self.__size
		r = screen.blit(subsurf, hotSpotPos)
		#TODO: se puede optimizar pintando solo el rectangulo anterior y el rectangulo actual

	def loadImage(self, img):
		filename,diccSprites,colorkey = img
		self.__image = pygame.image.load("../data/"+filename)#tTODO: change this :)
		self.__subSprites = {}
		for key in diccSprites.keys():
			#rectangle,hsx,hsy = diccSprites[key]
			rectangle, (hsx,hsy) = diccSprites[key]
			
			subsurf = self.__image.subsurface(rectangle)
			if self.__debug:
				pygame.draw.line(subsurf,(255,0,0), (hsx-2, hsy), (hsx+2, hsy))
				pygame.draw.line(subsurf,(255,0,0), (hsx, hsy-2), (hsx, hsy+2))
			for i in range(self.__size-1):
				subsurf = pygame.transform.scale2x(subsurf)
				#TODO: verificar el posible "update" de variable "rectangle"
			self.__subSprites[key] = (subsurf,rectangle,(hsx,hsy))
