import sys
sys.path.insert(0, '..')

import physics.collision as co
from .game_object import GameObject
from .agent import Agent

import numpy as np

class Bullet(GameObject):
    def __init__(self, x, y, r, v, theta, world_w, world_h, spawning_agent):
        super().__init__(x, y, r, v, theta, world_w, world_h)
        self.in_world = True
        self.spawning_agent = spawning_agent

    def update(self, dt, objects):
        super().update(dt)

        vx, vy = np.cos(self.theta*np.pi/180)*self.v, np.sin(self.theta*np.pi/180)*self.v
        walls_hit = co.detect_circle_wall_collisions(self.circ, vx, vy, *self.world_dims)
        if len(walls_hit) > 0:
            self.in_world = False
            return

        if self.circ.x < 0 or self.circ.x > self.world_w:
            self.in_world = False
            return

        if self.circ.y < 0 or self.circ.y > self.world_h:
            self.in_world = False
            return

        for obj in objects:
            if not issubclass(type(obj), Agent):
                continue

            if obj.dead:
                continue

            if co.detect_circle_circle_collision(self.circ, obj.circ):
                self.in_world = False
                obj.get_hit()
                self.spawning_agent.num_hits += 1
