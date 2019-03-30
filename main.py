import agents.agent as ag
from agents.range_agent import RangeAgent
import nn
import genetic as gen
import numpy as np
import time
import render as rend
import pickle

num_sensors = 8
num_actioncells = 3
num_memcells = 0

def orthonormal_vector(theta):
    tant = np.tan(theta)
    c = - np.sqrt(1 / ( tant ** 2 + 1))
    u = -c * tant
    v = c
    return -u, -v

def agent_fitness(agents):
    hit_weight = 100
    dist_weight = 10
    lives_weight = 10
    acc_weight = 1000
    
    fitness = []
    for agent in agents:
        acc = agent.num_hits / agent.num_attacks
        
        ind_fit = acc_weight * acc
        ind_fit += hit_weight * agent.num_hits
        ind_fit += dist_weight * agent.distance_moved
        ind_fit += lives_weight * agent.num_lives
        
        fitness.append(ind_fit)
        
    return fitness
        

class World(object):
    
    def __init__(self, brains):
        
        self.world_h = 100
        self.world_w = 100
        self._agents = [RangeAgent(self.world_h * x, self.world_w * y, 3, 10, 10, 40, self.world_h, self.world_w, 3)
                        for x, y in np.random.rand(brains[0].shape[0], 2)]
        self._brains = brains
        self._memories = np.zeros((self._brains[0].shape[0], num_memcells))
        self._bullets = []

        
    def calc_rays(self):
        """Calculates distance to a wall in local reference frame.

        N, S, E, W"""
        rays = []
        for agent in self._agents:
            ns_vec = np.array([np.cos(agent.theta), np.sin(agent.theta)])
            ew_vec = np.array(orthonormal_vector(agent.theta))
            ns_b = np.abs((self.world_h - agent.circ.y) / np.maximum(1e-7, ns_vec[0]))
            ns_t = np.abs(-agent.circ.y / np.maximum(1e-7, ns_vec[0]))
            ns_l = np.abs((self.world_w - agent.circ.x) / np.maximum(1e-7, ns_vec[1]))
            ns_r = np.abs(-agent.circ.x / np.maximum(1e-7, ns_vec[1]))
            
            ew_b = np.abs((self.world_h - agent.circ.y) / np.maximum(1e-7, ew_vec[0]))
            ew_t = np.abs(-agent.circ.y / np.maximum(1e-7, ew_vec[0]))
            ew_l = np.abs((self.world_w - agent.circ.x) / np.maximum(1e-7, ew_vec[1]))
            ew_r = np.abs(-agent.circ.x / np.maximum(1e-7, ew_vec[1]))

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
        enemy_present = [False] * len(self._agents)
        for i, agent in enumerate(self._agents):
            for enemy in self._agents:
                if agent == enemy:
                    continue

                enemy_in_view = self.is_in_view(agent, enemy)
                enemy_present[i] = enemy_in_view
                if enemy_in_view:
                    break
        # Bullet present
        e_present = np.array(enemy_present).astype(np.uint8)[:,np.newaxis]

        bullet_present = [False] * len(self._agents)
        for i, agent in enumerate(self._agents):
            for bullet in self._bullets:
                bullet_in_view = self.is_in_view(agent, bullet)
                bullet_present[i] = bullet_in_view
                if bullet_in_view:
                    break

        b_present = np.array(bullet_present).astype(np.uint8)[:,np.newaxis]

        return np.hstack((headings, fovs, rays, e_present, b_present)) #, self._memories))

    def process_ai(self):
        inputs = self.collect_inputs()
        behav_vectors = nn.forward_prop(inputs, self._brains)
        phys_info = []
        for i, agent in enumerate(self._agents):
            lr, dfov, bullets = agent.choose_action(behav_vectors[i])
            phys_info.append((lr, dfov))
            self._bullets.extend(bullets)
            self._memories[i] = behav_vectors[i][num_actioncells:]
                
        return phys_info
        
    def update_physics(self, phys_info, dt):
        bullets_to_remove = []

        for i, bullet in enumerate(self._bullets):
            bullet.update(dt, self._agents)
            if not bullet.in_world:
                bullets_to_remove.append(i)

                
        for bullet in reversed(bullets_to_remove):
            self._bullets.pop(bullet)

                
        for i, agent in enumerate(self._agents):
            if not agent.dead:
                agent.update(*phys_info[i], dt, self._agents)

    def is_finished(self):
        pass
        
        
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
        canvas = rend.render(self.world._agents, self.world._bullets, self.world.world_h, self.world.world_w)
        cv.imshow('canvas', canvas)
        
    def is_finished(self):
        return False
    

if __name__ == "__main__":
    render = True

    if render:
        import cv2 as cv
        cv.namedWindow('canvas')

    keep_going = True
    starting_population = gen.random_generation(50, (num_sensors + num_memcells, 10), (10, 10),(10, num_actioncells + num_memcells))
    world = World(starting_population)
    game = MainGame(world)
    
    max_time = 0.5 * 60
    
    now = time.time()
    start_time = now
    
    fitness_history = []
    
    gen_number = 0
    while keep_going:
        print(f"Generation Number: {gen_number}")

        while (now - start_time) < max_time and not game.is_finished():
            game.handle_input()
            actions = game.process_ai()
            game.update_physics(actions, now - time.time())

            if render:
                game.render()
                k = cv.waitKey(1)
                if k == 27:
                    break

            now = time.time()

        pickle.dump(game.world._brains, open('brains.pkl', 'wb'))

        gen_number += 1
        fitness = agent_fitness(game.world._agents)
        print(sorted(fitness))
        fitness_history.append(fitness)
        children = gen.breed(world._brains, fitness, world._brains[0].shape[0])
        game.world = World(children)
        
        start_time = time.time()
        now = start_time

        np.mean

    if render:
        cv.destroyAllWindows()
