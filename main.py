import agents.agent as ag
from agents.range_agent import RangeAgent
import nn
import genetic as gen


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
