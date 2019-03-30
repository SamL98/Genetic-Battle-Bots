import agents.agent as ag
from agents.range_agent import RangeAgent
import nn
import genetic as gen
import numpy as np
import time


def orthonormal_vector(theta):
    tant = np.tan(theta)
    c = - np.sqrt(1 / ( tant ** 2 + 1))
    u = -c * tant
    v = c
    return -u, -v


class World(object):
    
    def __init__(self):
        self.world_h = 100
        self.world_w = 100
        self._agents = [RangeAgent(25, 75, 5, 10, 1, 0, 45, self.world_h, self.world_w, 3),
                        RangeAgent(75, 25, 5, 45, 0, 1, 45, self.world_h, self.world_w, 3)]
        self._brains = gen.random_generation(2, (6, 10), (10, 10))
        self._bullets = []

        
    def calc_rays(self):
        """Calculates distance to a wall in local reference frame.

        N, S, E, W"""
        rays = []
        for agent in self._agents:
            ns_vec = np.array([np.cos(agent.theta), np.sin(agent.theta)])
            ew_vec = np.array(orthonormal_vector(agent.theta))
            ns_b = np.abs((self.world_h - agent.circ.y) / ns_vec[0])
            ns_t = np.abs(-agent.circ.y / ns_vec[0])
            ns_l = np.abs((self.world_w - agent.circ.x) / ns_vec[1])
            ns_r = np.abs(-agent.circ.x / ns_vec[1])
            
            ew_b = np.abs((self.world_h - agent.circ.y) / ew_vec[0])
            ew_t = np.abs(-agent.circ.y / ew_vec[0])
            ew_l = np.abs((self.world_w - agent.circ.x) / ew_vec[1])
            ew_r = np.abs(-agent.circ.x / ew_vec[1])

            if 0 < agent.theta and agent.theta <= 90:
                rays.append((min(ns_t, ns_r), min(ns_b, ns_l), min(ew_b, ew_r), min(ew_t, ew_l)))
            elif 90 < agent.theta and agent.theta <= 180:
                rays.append((min(ns_t, ns_l), min(ns_b, ns_r), min(ew_t, ew_r), min(ew_b, ew_l)))
            elif 180 < agent.theta and agent.theta <= 270:
                rays.append((min(ns_b, ns_l), min(ns_t, ns_r), min(ew_t, ew_l), min(ew_b, ew_r)))
            else:
                rays.append((min(ns_b, ns_r), min(ns_t, ns_l), min(ew_b, ew_l), min(ew_t, ew_r)))
                
        return np.stack(rays)

    def is_in_view(self, agent, obj):
        theta = agent.theta*np.pi/180
        fov = agent.fov*np.pi/180
        x, y = agent.circ.x, agent.circ.y

        m1 = np.tan(theta-fov/2)
        b1 = y - m1*x

        m2 = np.tan(theta+fov/2)
        b2 = y - m2*x
        
        if theta > np.pi/2 and theta < 3*np.pi/2:
            m1, m2 = m2, m1
            b1, b2 = b2, b1
            
        ex, ey = obj.circ.x, obj.circ.y
        return ey >= (m1*ex+b1) and ey <= (m2*ex + b2)
            
    def collect_inputs(self):
        # Heading
        headings = np.array([agent.theta for agent in self._agents])[:, np.newaxis]
        
        # FOV angle
        fovs = np.array([agent.fov for agent in self._agents])[:, np.newaxis]
        
        # N, S, E, W
        rays = self.calc_rays()

        # Enemy present
        # Bullet present
        self.calc_rays()

        enemy_present = [False] * len(self._agents)
        for i, agent in enumerate(self._agents):
            for enemy in self._agents:
                if agent == enemy:
                    continue

                enemy_in_view = self.is_in_view(agent, enemy)
                enemy_present[i] = enemy_in_view
                if enemy_in_view:
                    break

        e_present = np.array(enemy_present).astype(np.uint8)[:,np.newaxis]

        bullet_present = [False] * len(self._agents)
        for i, agent in enumerate(self._agents):
            for bullet in self._bullets:
                bullet_in_view = self.is_in_view(agent, bullet)
                bullet_present[i] = bullet_in_view
                if bullet_in_view:
                    break

        b_present = np.array(bullet_present).astype(np.uint8)[:,np.newaxis]

        return np.hstack((headings, fovs, rays, e_present, b_present))

    def process_ai(self):
        inputs = self.collect_inputs()

        behav_vectors = nn.forward_prop(inputs, self._brains)
        phys_info = []
        for i, agent in enumerate(self._agents):
            lr, dfov, bullets = agent.choose_action(behav_vectors[i])
            phys_info.append((lr, dfov))
            self._bullets.extend(bullets)
                
        return phys_info
        
    def update_physics(self, phys_info, dt):
        for bullet in self._bullets:
            bullet.update(dt, self._agents)
                
        for i, agent in enumerate(self._agents):
            agent.update(*phys_info[i], dt, self._agents)
            print(agent.circ.y)
        
        
class MainGame(object):
    
    def __init__(self, world):
        self.world = world
    
    def handle_input(self):
        pass
    
    def process_ai(self):
        actions = self.world.process_ai()
        return actions
    
    def update_physics(self, actions, dt):
        self.world.update_physics(actions, dt)
        
    def render(self):
        pass
        
    

if __name__ == "__main__":
    
    keep_going = True
    world = World()
    game = MainGame(world)
    
    now = time.time()
    while keep_going:
        game.handle_input()
        actions = game.process_ai()
        game.update_physics(actions, now - time.time())
        game.render()
        
        now = time.time()
