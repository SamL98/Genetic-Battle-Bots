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
theta = 10
fov = 20
v = 10

a = RangeAgent(x, y, r, v, theta, fov, 200, 200, 3)
start = time()

cv.namedWindow('canvas')

timestep = 0
shoot = 5
lr = SteeringDirection.Left

bullets = []

for _ in range(360):
    canv = 255*np.ones((200, 200, 3), dtype=np.uint8)
    render.render_agent(a, canv)
    for b in bullets:
        render.render_bullet(b, canv)
    cv.imshow('canvas', canv)

    if timestep % shoot== 0:
        bullet = a.attack()
        if bullet:
            bullets.append(bullet)

        if lr == SteeringDirection.Left:
            lr = SteeringDirection.Right
        else:
            lr = SteeringDirection.Left

    dfov = 0
    dt = time()-start
    start = time()
    objects = []

    a.update(lr, dfov, dt, objects)

    for b in bullets:
        b.update(dt, objects)

    timestep += 1

    k = cv.waitKey(60)
    if k == 27:
        break

cv.destroyAllWindows()
