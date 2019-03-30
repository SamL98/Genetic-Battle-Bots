import sys
sys.path.insert(0, '..')

from agent import Agent, AgentType
from melee_arc import MeleeArc
import physics.collision as co

class MeleeAgent(Agent):
	def __init__(self, x, y, r, theta, vx, vy, fov, w, h, num_lives, m_theta):
		super().__init__(x, y, r, theta, vx, vy, fov, w, h, num_lives)
		self.agent_type = AgentType.Melee
		self.m_theta = m_theta
		self.melee_active = False

	def update(self, lr, dfov, dt, objects):
		super().update(lr, dfov, dt, objects)
		if not self.melee_active:
			return

		for obj in objects:
			if not type(obj) == Agent:
				continue

			if co.detect_circle_melee_arc_collision(obj.circ, self.circ, self.melee_arc):
				obj.get_hit()
				self.num_hits += 1

	def attack(self):
		super.attack()
		self.melee_active = True
		self.melee_arc = MeleeArc(self.melee_r, self.theta - self.m_theta/2, self.m_theta)
