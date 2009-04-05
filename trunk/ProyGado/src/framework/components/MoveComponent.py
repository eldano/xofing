'''
Created on 05/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import GraphicComponent

class LeftRightMoveComponent(Component):
	family = ComponentFamily.move
	def __init__(self, go, velocity, aceleration):
		Component.__init__(self, go)
		self.movingLeft = False
		self.movingRight = False
		self.velocity = 0
		self.maxVelocity = velocity
		self.aceleration = aceleration
		
	
	def update(self):
		xIncrement = 0
		if(self.movingLeft): 
			xIncrement = -self.velocity
		if(self.movingRight): 
			xIncrement = self.velocity

	def stateChange(self, transition):
		if(transition == 1): # Move right
			self.velocity = self.velocity + self.aceleration
			if(self.velocity > self.maxVelocity):
				self.velocity = self.maxVelocity
		if(transition == 2): # Move left
			self.velocity = self.velocity - self.aceleration
			if(self.velocity < -self.maxVelocity):
				self.velocity = -self.maxVelocity