from .agent import Agent, AgentType
from .bullet import Bullet

from time import time

class RangeAgent(Agent):
	def __init__(self, x, y, r, theta, vx, vy, fov, w, h, num_lives):
		super().__init__(x, y, r, theta, vx, vy, fov, w, h, num_lives)
		self.agent_type = AgentType.Range
		self.cooldown_time = 0.75
		self.last_attack_time = 0

	def attack(self):
		if time()-self.last_attack_time < self.cooldown_time:
			return

		super().attack()
		bullet = Bullet(self.circ.x, self.circ.y, self.circ.r, self.vx, self.vy, *self.world_dims, self) 
		self.last_attack_time = time()
		return bullet

	def choose_action(self, behavior_vec):
		lr, dfov, shd_attack = super().choose_action(behavior_vec)
		bullets = []
		if shd_attack:
			bullet = self.attack()
			if bullet:
				bullets.append(bullet)
		return lr, dfov, bullets
