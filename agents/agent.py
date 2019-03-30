import sys
sys.path.insert(0, '..')

from enum import Enum
import numpy as np

from steering_direction import SteeringDirection
import physics.collision as co
import physics.motion as mo

from .game_object import GameObject

class AgentType(Enum):
    Melee = 'melee'
    Range = 'range'
    Normal = 'normal'

class Agent(GameObject):
    def __init__(self, x, y, r, theta, vx, vy, fov, world_w, world_h, num_lives):
        super().__init__(x, y, r, vx, vy, world_w, world_h)
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

        walls_hit = co.detect_circle_wall_collisions(self.circ, *self.world_dims)
        self.vx, self.vy = co.execute_wall_collision_response(self.circ, self.vx, self.vy, walls_hit)  
        self.walls_hit += len(walls_hit)

        for obj in objects:
            if not issubclass(type(obj), Agent) or obj == self:
                continue

            if obj.dead:
                continue

            if co.detect_circle_circle_collision(self.circ, obj.circ):
                return

        self.vx, self.vy, dtheta = mo.update_velocity(self.vx, self.vy, lr, self.theta_step)
        self.theta += dtheta
        xi, yi = self.circ.x, self.circ.y
        super().update(dt)

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
