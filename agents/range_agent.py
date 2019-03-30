from agent import Agent, AgentType

class RangeAgent(Agent):
	def __init__(self, x, y, r, theta, vx, vy, fov, w, h, num_lives):
		super().__init__(x, y, r, theta, vx, vy, fov, w, h, num_lives)
		self.agent_type = AgentType.Range

	def attack(self):
		super().attack()
		bullet = Bullet(self.x, self.y, self.y, self.vx, self.vy, *self.world_dims, self) 
		return bullet
