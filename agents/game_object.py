import sys
sys.path.insert(0, '..')

import physics.motion as mo
from circle import Circle

class GameObject(object):
	def __init__(self, x, y, r, vx, vy, world_w, world_h):
		self.circ = Circle(x, y, r)
		self.vx = vx
		self.vy = vy
		self.world_dims = (world_w, world_h)

	def update(self, dt):
		x, y = mo.update_position(x, y, self.vx, self.vy, dt)
		self.circ = Circle(x, y, self.circ.r)
