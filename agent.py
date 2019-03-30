from enum import Enum

import physics as ph

class AgentType(Enum):
	Melee = 'melee'
	Range = 'range'

class GameObject(object):
	def __init__(self, x, y, r, vx, vy, world_w, world_h):
		self.circ = ph.Circle(x, y, r)
		self.vx = vx
		self.vy = vy
		self.fov = fov
		self.world_dims = (world_w, world_h)

	def update(self, dt):
		x, y = ph.update_position(x, y, self.vx, self.vy, dt)
		self.circ = ph.Circle(x, y, self.circ.r)

class Bullet(object):
	def __init__(self, x, y, r, vx, vy, fov, world_w, world_h, spawning_agent):
		super().__init__(x, y, r, vx, vy, world_w, world_h)
		self.in_world = True
		self.spawning_agent = self.spawning_agent

	def update(self, dt, objects):
		super().update(dt)
		walls_hits = ph.detect_circle_wall_collisions(self.circ, *self.world_dims)
		if len(walls_hit) > 0:
			self.in_world = False

		for obj in objects:
			if not type(obj) == Agent:
				continue

			if ph.detect_circle_circle_collision(self.circ, obj.circ):
				obj.times_hist += 1
				self.spawning_agent.num_hits += 1

class Agent(GameObject):
	def __init__(self, x, y, r, vx, vy, fov, world_w, world_h):
		super().__init__(x, y, r, vx, vy, world_w, world_h)
		self.distance_moved = 0
		self.num_hits = 0
		self.num_attacks = 0
		self.times_hit = 0
		self.walls_hit = 0

	def update(self, lr, dt, objects):
		walls_hits = ph.detect_circle_wall_collisions(self.circ, *self.world_dims)
		self.vx, self.vy = ph.execute_wall_collision_response(self.circ, self.vx, self.vy, walls_hist)	
		self.walls_hit += len(walls_hist)

		for obj in objects:
			if not type(obj) == Agent or obj == self:
				continue

			if ph.detect_circle_circle_collision(self.circ, obj.circ):
				return

		self.vx, self.vy = ph.update_velocity(self.vx, self.vy, lr)
		super().update(dt)

class MeleeAgent(object):
	def __init__(self, x, y, r, vx, vy, fov, w, h, m_theta):
		super().__init__(x, y, r, vx, vy, fov, w, h)
		self.agent_type = AgentType.Melee
		self.m_theta = m_theta
		self.melee_active = False

class RangeAgent(object):
	def __init__(self, x, y, r, vx, vy, fov, w, h):
		super().__init__(x, y, r, vx, vy, fov, w, h)
		self.agent_type = AgentType.Range
