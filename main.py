import agents.agent as ag
from agents.range_agent import RangeAgent
import nn
import genetic as gen
import numpy as np


def orthonormal_vector(theta):
    tant = np.tan(theta)
    c = - np.sqrt(1 / ( tant ** 2 + 1))
    u = -c * tant
    v = c
    return u, v


class World(object):
    
    def __init__(self):
        self.world_h = 100
        self.world_w = 100
        self._agents = [RangeAgent(50, 50, 5, 0, 0, 0, 45, self.world_h, self.world_w, 3) for _ in range(2)]
        self._brains = gen.random_generation(2, (4, 10), (10, 10))
        self._bullets = []

        
    def calc_rays(self):
        rays = []
        for agent in self._agents:
            ns_vec = np.array([np.cos(agent.theta), np.sin(agent.theta)])
            ew_vec = np.array([orthonormal_vector(agent.theta)])
            breakpoint()

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
        
        # FOV angle
        
        # N ray
        # S ray
        # E ray
        # W ray
        
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

        bullet_present = [False] * len(self._agents)
        for i, agent in enumerate(self._agents):
            for bullet in self._bullets:
                bullet_in_view = self.is_in_view(agent, bullet)
                bullet_present[i] = bullet_in_view
                if bullet_in_view:
                    break
            
    def process_ai(self):
        inputs = self.collect_inputs()
        behav_vectors = nn.forward_prop(inputs, self._brains)
        phys_info = []
        for i, agent in enumerate(self._agents):
            lr, dfov, bullets = agent.choose_actions(behav_vectors[i])
            phys_info.append((lr, dfov))
            self._bullets.extend(bullets)
                
        return phys_info
        
    def update_physics(self, phys_info, dt):
        for bullet in self._bullets:
            bullet.update(dt, self._agents)
                
        for i, agent in enumerate(self._agents):
            agent.update(*phys_info[i], dt, self._agents)
        
        
class MainGame(object):
    
    def __init__(self, world):
        self.world = world
    
    def handle_input(self):
        pass
    
    def process_ai(self):
        actions = self.world.process_ai()
        return actions
    
    def update_physics(self, actions):
        self.world.update_physics(actions)
        
    def render(self):
        pass
        
    

if __name__ == "__main__":
    
    keep_going = True
    world = World()
    game = MainGame(world)
    
    while keep_going:
        game.handle_input()
        game.process_ai()
        game.update_physics()
        game.render()
