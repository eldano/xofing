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
	lightColor = (180, 200, 200)
	darkColor = (110, 110, 110)
	titleColor = (150,150,230)
	textColor = (0,0,0)
	editableTextBG = (255,255,255)
	font = 'arial'

class Window(GraphicComponent):
	def __init__(self, parent, x, y, width, height, title, font, size):
		GraphicComponent.__init__(self, parent, x, y)
		self.title = title
		self.width = width
		self.height = height
		self.titleBorder = 2		
		fontFullFileName = pygame.font.match_font(font)
		self.font = pygame.font.Font(fontFullFileName, size)
		self.child = []
	
	def addChild(self, child):
		self.child.append(child)
		
	def draw(self, graphics, region):
		(tw, th) = self.font.size(self.title)
		graphics.fill(GUIStyle.color, (self.x, self.y, self.width, self.height))
		graphics.fill(GUIStyle.titleColor, (self.x + self.titleBorder, self.y+self.titleBorder, self.width- 2*self.titleBorder, th + 2*self.titleBorder))
		render = self.font.render(self.title, False, GUIStyle.textColor)
		graphics.blit(render, (self.x+2*self.titleBorder,self.y+2*self.titleBorder))
		for c in self.child:
			c.x = c.x + self.x
			c.y = c.y + self.y + th + 2*self.titleBorder
			c.draw(graphics, region)
			c.x = c.x - self.x
			c.y = c.y - self.y - th - 2*self.titleBorder

	def stateChange(self, param):
		for c in self.child:
			c.stateChange(param)

class Button(GraphicComponent):
	border = 2
	def __init__(self, parent, x, y, width, text, font, size, rectangular):
		GraphicComponent.__init__(self, parent, x, y)
		self.width = width
		self.font = pygame.font.SysFont(font, size)
		self.height = self.font.size("")[1] + TextField.border*2
		self.rectangular = rectangular
		self.text = text
		self.clicked = False
		
	def stateChange(self, transition):
		self.clicked = not self.clicked
		print self.clicked
	
	def draw(self, graphics, region):		
		if(self.rectangular):
			pygame.draw.line(graphics, GUIStyle.lightColor, (self.x, self.y), (self.x + self.width- TextField.border, self.y), self.border)
			pygame.draw.line(graphics, GUIStyle.lightColor, (self.x, self.y), (self.x, self.y + self.height- TextField.border), self.border)
			pygame.draw.line(graphics, GUIStyle.darkColor, (self.x + self.width- TextField.border, self.y), (self.x + self.width- TextField.border, self.y + self.height- TextField.border), self.border)
			pygame.draw.line(graphics, GUIStyle.darkColor, (self.x, self.y + self.height- TextField.border), (self.x + self.width- TextField.border, self.y + self.height- TextField.border), self.border)
			graphics.fill(GUIStyle.color, (self.x + Button.border, self.y+ TextField.border, self.width - Button.border*2, self.height - Button.border*2) )
		else:
			pygame.draw.ellipse(graphics, GUIStyle.color, (self.x, self.y, self.x + self.width, self.y + self.height), 1)	

		render = self.font.render(self.text, False, GUIStyle.textColor)
		graphics.blit(render, (self.x+2,self.y+2))		
			
class TextField(GraphicComponent):
	border = 2
	counter = 20
	limit = 200
	def __init__(self, parent, x,y, width, text, font, size):
		GraphicComponent.__init__(self, parent, x, y)
		self.width = width
		self.text = text
		self.font = pygame.font.SysFont(font, size)
		self.height = self.font.size("")[1] + TextField.border*2
		self.cursor = True
		self.focus = True

	def stateChange(self, keys):
		for key in keys:
			if(key < 255):
				if(key == 8):
					self.text = self.text[0:len(self.text)-1]
				else:
					self.text = self.text + chr(key)
	
	def update(self, elapsed):
		if not self.focus:
			return
		self.counter = self.counter - 1
		if(self.counter == 0):
			self.cursor = not self.cursor
			self.counter = self.limit

	def draw(self, graphics, region):
		pygame.draw.line(graphics, GUIStyle.lightColor, (self.x, self.y), (self.x + self.width- TextField.border, self.y), self.border)
		pygame.draw.line(graphics, GUIStyle.lightColor, (self.x, self.y), (self.x, self.y + self.height- TextField.border), self.border)
		
		pygame.draw.line(graphics, GUIStyle.darkColor, (self.x + self.width- TextField.border, self.y), (self.x + self.width- TextField.border, self.y + self.height- TextField.border), self.border)
		pygame.draw.line(graphics, GUIStyle.darkColor, (self.x, self.y + self.height- TextField.border), (self.x + self.width- TextField.border, self.y + self.height- TextField.border), self.border)
		#graphics.fill(GUIStyle.color, (self.x, self.y, self.width, self.height) )
		graphics.fill(GUIStyle.editableTextBG, (self.x + TextField.border, self.y+ TextField.border, self.width - TextField.border*2, self.height - TextField.border*2) )
		(tw, th) = self.font.size(self.text)
		render = self.font.render(self.text, False, GUIStyle.textColor)
		graphics.blit(render, (self.x+2,self.y+2))
		
		if(self.cursor and self.focus):
			pygame.draw.line(graphics, GUIStyle.textColor, (self.x + tw+self.border, self.y + self.border), (self.x + tw+self.border, self.y + self.border + th), 2)