import pickle
import cv2 as cv
from agents import RangeAgent, MeleeAgent
from main import World, MainGame

class BattleWorld(World):
    def __init__(self, brains):
        super().__init__(brains)
        self.world_h = 500
        self.world_w = 500
        
        v = 20
        r = 10
        fov = 20
        num_lives = 3
        self._agents = [RangeAgent(50, 250, r, 0, v, fov, self.world_h, self.world_wi, num_lives), RangeAgent(300, 250, r, 180, v, fov, self.world_h, self.world_w, num_lives]

if __name__ == '__main__':
    brains = pickle.load(open('brains.pkl', 'rb'))

    cv.namedWindow('canvas')
