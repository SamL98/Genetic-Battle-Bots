from .agent import Agent, AgentType
from .bullet import Bullet

class RangeAgent(Agent):
	def __init__(self, x, y, r, theta, vx, vy, fov, w, h, num_lives):
		super().__init__(x, y, r, theta, vx, vy, fov, w, h, num_lives)
		self.agent_type = AgentType.Range

	def attack(self):
		super().attack()
		bullet = Bullet(self.circ.x, self.circ.y, self.circ.r, self.vx, self.vy, *self.world_dims, self) 
		return bullet

	def choose_action(self, behavior_vec):
		lr, dfov, shd_attack = super().choose_action(behavior_vec)
		bullets = []
		if shd_attack:
			bullets.append(self.attack())
		return lr, dfov, bullets
