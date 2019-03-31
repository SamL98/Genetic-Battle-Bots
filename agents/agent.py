import sys
sys.path.insert(0, '..')

from enum import Enum
import numpy as np

from steering_direction import SteeringDirection
from circle import Circle

import physics.collision as co
import physics.motion as mo

from .game_object import GameObject

class AgentType(Enum):
    Melee = 'melee'
    Range = 'range'
    Normal = 'normal'

class Agent(GameObject):
    def __init__(self, x, y, r, v, theta, fov, world_w, world_h, num_lives):
        super().__init__(x, y, r, v, theta, world_w, world_h)
        self.theta = theta
        self.theta_step = 5
        self.fov = fov

        self.num_lives = num_lives
        self.dead = False

        self.distance_moved = 0
        self.num_hits = 0
        self.num_attacks = 0
        self.times_hit = 0
        self.walls_hit = 0

        self.agent_type = AgentType.Normal

    def update(self, lr, dfov, dt, objects):
        if self.dead:
            return

        self.fov += dfov
        self.fov = max(self.fov, 0)
        self.fov = min(self.fov, 179.9)

        vx, vy = np.cos(self.theta*np.pi/180)*self.v, np.sin(self.theta*np.pi/180)*self.v
        walls_hit = co.detect_circle_wall_collisions(self.circ, vx, vy, *self.world_dims)

        if len(walls_hit) > 0:
            self.theta = co.execute_wall_collision_response(self.circ, self.theta, walls_hit)  

            x, y = self.circ.x, self.circ.y
            x = min(max(self.circ.r, x), self.world_dims[1]-self.circ.r)
            y = min(max(self.circ.r, y), self.world_dims[0]-self.circ.r)

            self.circ = Circle(x, y, self.circ.r)
            self.walls_hit += len(walls_hit)

        for obj in objects:
            if not issubclass(type(obj), Agent) or obj == self:
                continue

            if obj.dead:
                continue

            if co.detect_circle_circle_collision(self.circ, obj.circ):
                ang = np.arctan2(self.circ.y-obj.circ.y, self.circ.x-obj.circ.x)
                x = self.circ.x + np.cos(ang)*(self.circ.r+obj.circ.r)
                y = self.circ.y + np.sin(ang)*(self.circ.r+obj.circ.r)
                self.circ = Circle(x, y, self.circ.r)
                self.theta = -ang*180/np.pi
                return

        dtheta = mo.update_velocity(lr, self.theta_step)
        self.theta += dtheta

        xi, yi = self.circ.x, self.circ.y
        super().update(dt)

        x = min(max(self.circ.r, self.circ.x), self.world_dims[1]-self.circ.r)
        y = min(max(self.circ.r, self.circ.y), self.world_dims[0]-self.circ.r)
        self.circ = Circle(x, y, self.circ.r)

        self.distance_moved += np.sqrt((self.circ.x-xi)**2 + (self.circ.y-yi)**2)

    def get_hit(self):
        self.num_lives -= 1
        if self.num_lives == 0:
            self.dead = True
        self.times_hit += 1

    def attack(self):
        self.num_attacks += 1

    def choose_action(self, behavior_vec):
        behavior = behavior_vec[:3]
        
        lr = SteeringDirection.Left
        if behavior[0] >= 0:
            lr = SteeringDirection.Right

        dfov = np.tanh(behavior[1])
        shd_attack = behavior[2] >= 0

        return lr, dfov, shd_attack
