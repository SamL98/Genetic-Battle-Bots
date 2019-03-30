import agent as ag
import nn
import genetic as gen


class World(object):
    
    def __init__(self):
        self.world_h = 100
        self.world_w = 100
        self._agents = [ag.RangeAgent(0, 0, 5, 0, 0, 45, self.world_h, self.world_w) for range(2)]
        self._brains = gen.random_generation(2, (4, 10), (10, 10))
        self._bullets = []

        
        def collect_inputs(self):
            pass
        
        
        def process_ai(self):
            inputs = self.collect_inputs()
            behav_vectors = nn.forward_prop(inputs, self._brains)
            for i, agent in enumerate(self._agents):
                agent.choose_actions(behav_vectors[i])
        
        def update_physics(self, agent_actions, dt):
            for bullet in self._bullets:
                bullet.update(dt, self._agents)
                
            for i, agent in enumerate(self._agents):
                pass
        
        
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
