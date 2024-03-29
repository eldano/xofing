from framework.base.base import *
from pygame import Rect
import copy

class AABBComponent(Component):
	family = ComponentFamily.bounding
	
	def __init__(self, parent, x, y, width, height):
		Component.__init__(self, parent)
		self.off_x = x
		self.off_y = y
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	
	def setattr(self, attr, value):
		if attr == 'x':
			self.x = value
		if attr == 'y':
			self.y = value

	def checkCollision(self, boundingBox):
		cx = boundingBox.x
		cy = boundingBox.y
		cw = boundingBox.width
		ch = boundingBox.height
		
		if (cx > self.x and cx < self.x + self.width) or (cx + ch < self.x + self.width and cx + ch > self.x):
			if (cy > self.y and cy < self.y + self.height) or (cy + ch < self.y + self.height and cy + ch > self.y):
				return True
		return False
	
	def inside(self, (x,y)):
		return self.x < x and self.y < y and (self.x + self.width) > x and (self.y + self.height) > y

class VerticalCollider(Component):
	family = ComponentFamily.bounding
	
	def __init__(self, parent, x, y, height, normal):
		Component.__init__(self, parent)
		self.off_x = x
		self.off_y = y
		self.x = x
		self.y = y
		self.height = height
		self.normal = normal

	def checkCollision(self, boundingBox):
		cx = boundingBox.x
		cy = boundingBox.y
		cw = boundingBox.width
		ch = boundingBox.height
		
		if(cy + ch > self.y and cy < self.y + self.height):
			if(cx <= self.x and cx + cw > self.x):
				return True
		return False

class HorizontalCollider(Component):
	family = ComponentFamily.bounding
	
	def __init__(self, parent, x, y, width, normal):
		Component.__init__(self, parent)
		self.off_x = x
		self.off_y = y
		self.x = x
		self.y = y
		self.width = width
		self.normal = normal

	def checkCollision(self, boundingBox):
		cx = boundingBox.x
		cy = boundingBox.y
		cw = boundingBox.width
		ch = boundingBox.height
				
		if (cx + cw > self.x and cx < self.x + self.width):
			if(cy <= self.y and cy + ch > self.y):
				return True
		return False

class RectColider(Component):
	family = ComponentFamily.bounding
	
	def __init__(self, x, y, w, h):
		self.__rect =  Rect(x,y,w,h)

	def getRect(self):
		"""
		Devuelve una copia del pygame.Rect que define el BoundingBox
		"""
		return copy.deepcopy( self.__rect )