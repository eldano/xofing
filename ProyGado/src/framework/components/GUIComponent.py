'''
Created on 05/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import GraphicComponent
from framework.base.base import ComponentFamily
import pygame
import os

class GUIStyle:
	color = (150,150,150)
	titleColor = (150,150,230)
	textColor = (0,0,0)
	editableTextBG = (255,255,255)

class Window(GraphicComponent):
	def __init__(self, parent, x, y, width, height, title, font, size):
		GraphicComponent.__init__(self, parent, x, y)
		self.title = title
		self.width = width
		self.height = height
		self.titleBorder = 2
		
		fontFullFileName = pygame.font.match_font(font)
		self.font = pygame.font.Font(fontFullFileName, size)
		
	def draw(self, graphics, region):
		(tw, th) = self.font.size(self.title)
		graphics.fill(GUIStyle.color, (self.x, self.y, self.width, self.height))
		graphics.fill(GUIStyle.titleColor, (self.x + self.titleBorder, self.y+self.titleBorder, self.width- 2*self.titleBorder, th + 2*self.titleBorder))
		render = self.font.render(self.title, False, GUIStyle.textColor)
		graphics.blit(render, (self.x+2*self.titleBorder,self.y+2*self.titleBorder))

class TextField(GraphicComponent):
	border = 2
	def __init__(self, parent, x,y, width, font, size):
		GraphicComponent.__init__(self, parent, x, y)
		self.width = width
		self.text = ''
		self.font = pygame.font.SysFont(font, size)
		self.height = self.font.size("")[1] + TextField.border*2

	def draw(self, graphics, region):
		graphics.fill(GUIStyle.color, (self.x, self.y, self.width, self.height) )
		graphics.fill(GUIStyle.editableTextBG, (self.x + TextField.border, self.y+ TextField.border, self.width - TextField.border*2, self.height - TextField.border*2) )
