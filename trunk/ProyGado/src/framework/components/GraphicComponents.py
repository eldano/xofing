import pygame
pygame.font.init()
#from framework.base.base import *
from framework.base.base import GraphicComponent

class LabelComponent(GraphicComponent):
	font = pygame.font.SysFont("arial",18)

	def __init__(self, parent, x, y, componentFamily, attrName, go = None):
		GraphicComponent.__init__(self, parent, x, y)
		self.componentFamily = componentFamily
		self.attrName = attrName
		if go == None:
			self.go = parent
		else:
			self.go = go

#	def __init__(self, x, y, component_name, attr_name):
#		GraphicComponent.__init__(self, x, y)
#		self.component_name = component_name
#		self.attr_name = attr_name
#		self.type = dynamic_type
	
	def draw(self, graphics, region):
		co = self.go.getComponent(self.componentFamily)
		value = getattr(co, self.attrName, 'sin valor')
		graphics.blit(self.font.render(str(value), True, (255,255,255)), (self.x,self.y))
		#TODO: (Mauricio) : evaluar posible None value 

class Image(GraphicComponent):
	def __init__(self, parent, x, y, imagePath):
		GraphicComponent.__init__(self, parent, x, y)
		imageOsPath = os.path.join('', imagePath)
		self.image = pygame.image.load(imageOsPath)
	
	def draw(self, graphics, region):
		screen.blit(self.image, (self.x,self.y,100,200))

class Line(GraphicComponent):
	def __init__(self, parent, x, y, x2, y2, color):
		GraphicComponent.__init__(self, parent, x, y)
		self.x2 = x2
		self.y2 = y2
		self.color = color
	
	def draw(self, graphics, region):
		pygame.draw.line(graphics, self.color, (self.x,self.y), (self.x2,self.y2))