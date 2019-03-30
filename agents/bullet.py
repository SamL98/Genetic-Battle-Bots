import sys
sys.path.insert(0, '..')

import physics.collision as co
from game_object import GameObject

class Bullet(GameObject):
	def __init__(self, x, y, r, vx, vy, world_w, world_h, spawning_agent):
		super().__init__(x, y, r, vx, vy, world_w, world_h)
		self.in_world = True
		self.spawning_agent = self.spawning_agent

	def update(self, dt, objects):
		super().update(dt)
		walls_hits = co.detect_circle_wall_collisions(self.circ, *self.world_dims)
		if len(walls_hit) > 0:
			self.in_world = False
			return

		for obj in objects:
			if not type(obj) == Agent:
				continue

			if co.detect_circle_circle_collision(self.circ, obj.circ):
				obj.get_hit()
				self.spawning_agent.num_hits += 1