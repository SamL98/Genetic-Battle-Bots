import render
from circle import Circle
from agents.agent import Agent
from agents.melee_agent import MeleeAgent
from agents.range_agent import RangeAgent
from steering_direction import SteeringDirection

import numpy as np
import cv2 as cv
from time import time

x, y = 75, 125
r = 10
theta = 0
fov = 20
vx, vy = 50, 50
melee_r = 10
m_theta = 75

a = MeleeAgent(x, y, r, theta, vx, vy, fov, 200, 200, 3, m_theta, melee_r)
start = time()

cv.namedWindow('canvas')

for _ in range(360):
    canv = 255*np.ones((200, 200, 3), dtype=np.uint8)
    render.render_agent(a, canv)
    cv.imshow('canvas', canv)

    lr = SteeringDirection.Left
    dfov = 0
    dt = time()-start
    start = time()
    objects = []

    a.update(lr, dfov, dt, objects)

    k = cv.waitKey(60)
    if k == 27:
        break

cv.destroyAllWindows()
