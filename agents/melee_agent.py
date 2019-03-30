import sys
sys.path.insert(0, '..')

from .agent import Agent, AgentType
from melee_arc import MeleeArc
import physics.collision as co

from time import time

class MeleeAgent(Agent):
	def __init__(self, x, y, r, v, theta, fov, w, h, num_lives, m_theta, m_r):
		super().__init__(x, y, r, v, theta, fov, w, h, num_lives)
		self.agent_type = AgentType.Melee
		self.m_theta = m_theta
		self.melee_r = m_r
		self.melee_active = False
		self.max_melee_time = 0.75
		self.melee_time = 0

	def update(self, lr, dfov, dt, objects):
		super().update(lr, dfov, dt, objects)

		if self.melee_active:
			self.melee_time += dt
			if self.melee_time >= self.max_melee_time:
				self.melee_time = 0
				self.melee_active = False

		if not self.melee_active:
			return

		for obj in objects:
			if not issubclass(type(obj), Agent):
				continue

			if co.detect_circle_melee_arc_collision(obj.circ, self.circ, self.melee_arc):
				obj.get_hit()
				self.num_hits += 1

	def attack(self):
		if self.melee_active:
			return

		super().attack()
		self.melee_active = True
		self.melee_time = time()
		self.melee_arc = MeleeArc(self.melee_r, self.theta - self.m_theta/2, self.m_theta)

	def choose_action(self, behavior_vec):
		lr, dfov, shd_attack = self.choose_action(behavior_vec)
		if shd_attack:
			self.attack()
		return lr, dfov, []
