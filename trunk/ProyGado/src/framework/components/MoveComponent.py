'''
Created on 05/04/2009

@author: Harold Selvaggi
'''

from framework.base.base import *

class LeftRightMoveComponent(Component):
	family = ComponentFamily.move
	def __init__(self, go, velocity, aceleration):
		Component.__init__(self, go)
		self.movingLeft = False
		self.movingRight = False
		self.velocity = 0
		self.maxVelocity = velocity
		self.aceleration = aceleration
		self.state = 0
	
	def update(self, dt):
		if(self.state == 1): # Move right
			self.velocity = self.velocity + self.aceleration*dt
			if(self.velocity > self.maxVelocity):
				self.velocity = self.maxVelocity
		if(self.state == 2): # Move left
			self.velocity = self.velocity - self.aceleration*dt
			if(self.velocity < -self.maxVelocity):
				self.velocity = -self.maxVelocity
		if(self.state == 0):
			if(self.velocity > 0):
				self.velocity = self.velocity - self.aceleration*dt
				if(self.velocity < 0):
				    self.velocity = 0
			if(self.velocity < 0):
				self.velocity = self.velocity + self.aceleration*dt
				if(self.velocity > 0):
				    self.velocity = 0
		if(self.state == 3):
			self.velocity = 0
		xIncrement = self.velocity*dt
		gr = self.parent.getComponent(ComponentFamily.graphic)
		gr.x = gr.x + xIncrement
		bv = self.parent.getComponent(ComponentFamily.bounding)
		if bv != None:
			bv.x = bv.off_x + gr.x
		

	def stateChange(self, transition):
		self.state = transition

class XYMovement(Component):
	family = ComponentFamily.move
	def __init__(self, parent):
		Component.__init__(self, parent)
		self.velX = 0
		self.velY = 0
	
	def update(self, dt):
		gr = self.parent.getComponent(ComponentFamily.graphic)
		gr.x = gr.x + dt*self.velX
		gr.y = gr.y + dt*self.velY
		bv = self.parent.getComponent(ComponentFamily.bounding)
		if bv != None:
			bv.x = bv.off_x + gr.x
			bv.y = bv.off_y + gr.y