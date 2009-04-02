import pygame
pygame.font.init()
from framework.base.base import *

class LabelComponent(GraphicComponent):
	static_type = 'StaticType'
	dynamic_type = 'DynamicType'
	font = pygame.font.SysFont("arial",12)

	def __init__(self, x, y, str):
		GraphicComponent.__init__(self, x, y)
		self.displayString = str
		self.type = self.static_type

#	def __init__(self, x, y, component_name, attr_name):
#		GraphicComponent.__init__(self, x, y)
#		self.component_name = component_name
#		self.attr_name = attr_name
#		self.type = dynamic_type
	
	def draw(self, graphics, region):
		if self.type == self.static_type:
			graphics.blit(self.font.render(self.displayString, True, (255,255,255), (0,0,0)), (self.x,self.y))
		else:
			pass
			#TODO (Mauricio) : en algun momento se va a implementar el label mas generico
