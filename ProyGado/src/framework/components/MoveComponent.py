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
			self.velocity = self.velocity + self.aceleration * dt
			if(self.velocity > self.maxVelocity):
				self.velocity = self.maxVelocity
		if(self.state == 2): # Move left
			self.velocity = self.velocity - self.aceleration * dt
			if(self.velocity < - self.maxVelocity):
				self.velocity = - self.maxVelocity
		if(self.state == 0):
			if(self.velocity > 0):
				self.velocity = self.velocity - self.aceleration * dt
				if(self.velocity < 0):
				    self.velocity = 0
			if(self.velocity < 0):
				self.velocity = self.velocity + self.aceleration * dt
				if(self.velocity > 0):
				    self.velocity = 0
		if(self.state == 3):
			self.velocity = 0
		xIncrement = self.velocity * dt
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
		gr.x = gr.x + dt * self.velX
		gr.y = gr.y + dt * self.velY
		bv = self.parent.getComponent(ComponentFamily.bounding)
		if bv != None:
			bv.x = bv.off_x + gr.x
			bv.y = bv.off_y + gr.y
			
class GravityMovement(Component):
	family = ComponentFamily.move
	def __init__(self, parent, maxXVelocity, maxYVelocity, xAceleration, g):
		Component.__init__(self, parent)
		self.maxXVelocity = maxXVelocity
		self.maxYVelocity = maxYVelocity
		self.xAceleration = xAceleration
		self.g = g
		self.jump = maxYVelocity
		self.gravity = False
		self.xVelocity = 0
		self.yVelocity = 0
		self.state = 0
	
	def setattr(self, attr, value):
		if attr == 'x':
			self.x = value
		if attr == 'y':
			self.y = value
		if attr == 'gravity':
			self.gravity = value
	
	def setX(self, x, y):
		dx = self.x - x
		dy = self.y - y
		gr = self.parent.getComponent(ComponentFamily.graphic)
		if gr != None:
			gr.x = gr.x + dx
			gr.y = gr.y + dy
		bv = self.parent.getComponent(ComponentFamily.bounding)
		if bv != None:
			bv.x = bv.x + dx
			bv.y = bv.y + dy
		
	
	def update(self, dt):
		if(self.state == 1):  # Derecha
			self.xVelocity = self.xVelocity + self.xAceleration * dt
			if(self.xVelocity > self.maxXVelocity):
				self.xVelocity = self.maxXVelocity
		if(self.state == 2):  # Izquierda
			self.xVelocity = self.xVelocity - self.xAceleration * dt
			if(self.xVelocity < - self.maxXVelocity):
				self.xVelocity = - self.maxXVelocity
		
		if(self.state == 0):
			if(self.xVelocity > 0):
				self.xVelocity = self.xVelocity - dt * self.xAceleration
				if(self.xVelocity < 0):
					self.xVelocity = 0
			else:
				if(self.xVelocity < 0):
					self.xVelocity = self.xVelocity + dt * self.xAceleration
					if(self.xVelocity > 0):
						self.xVelocity = 0

		gr = self.parent.getComponent(ComponentFamily.graphic)
		if gr != None:
			gr.x = gr.x + dt * self.xVelocity
			gr.y = gr.y + dt * self.yVelocity
		bv = self.parent.getComponent(ComponentFamily.bounding)
		if bv != None:
			bv.x = bv.x + dt * self.xVelocity
			bv.y = bv.y + dt * self.yVelocity

		if self.gravity:
			self.yVelocity = self.yVelocity + self.g * dt
			
	def stateChange(self, transition):		
		if (transition == 3) and (self.yVelocity == 0):
			self.gravity = True
			self.yVelocity = self.maxYVelocity
		else:
			if(transition == 4):
				self.gravity = False
				self.yVelocity = 0
			self.state = transition

class DragAndDropComponent(Component):
	DROP = 2
	DRAG = 1
	NOSTATE = 0
	family = ComponentFamily.move
	
	def __init__(self, parent):
		Component.__init__(self, parent)
		self.state = NOSTATE
		self.pos = []
	
	def stateChange(self, transition):
		if transition == DRAG or transition == DROP:
			if self.state == DRAG:
				gr = self.parent.getComponent(ComponentFamily.graphic)
				if gr != None:
					gr.x = gr.x + self.pos[0] - InputState.mousePos[0] 
					gr.y = gr.y + self.pos[1] - InputState.mousePos[1]
				bv = self.parent.getComponent(ComponentFamily.bounding)
				if bv != None:
					bv.x = bv.x + self.pos[0] - InputState.mousePos[0]
					bv.y = bv.y + self.pos[1] - InputState.mousePos[1]
			self.pos = InputState.mousePos
		
		self.state = transition
		
		if transition == DROP:
			self.state == NOSTATE