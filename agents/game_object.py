import sys
sys.path.insert(0, '..')

import physics.motion as mo
from circle import Circle
import numpy as np

class GameObject(object):
    def __init__(self, x, y, r, v, theta, world_w, world_h):
        self.circ = Circle(x, y, r)
        self.v = v
        self.theta = theta
        self.world_dims = (world_w, world_h)

    def update(self, dt):
        vx, vy = np.cos(self.theta*np.pi/180)*self.v, np.sin(self.theta*np.pi/180)*self.v
        x, y = mo.update_position(self.circ.x, self.circ.y, vx, vy, dt)
        self.circ = Circle(x, y, self.circ.r)
