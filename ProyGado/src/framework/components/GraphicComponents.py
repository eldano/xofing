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
	def __init__(self, parent, x, y, x2, y2, color):
		GraphicComponent.__init__(self, parent, x, y)
		self.x2 = x2
		self.y2 = y2
		self.color = color
	
	def draw(self, graphics, region):
		pygame.draw.line(graphics, self.color, (self.x,self.y), (self.x2,self.y2))