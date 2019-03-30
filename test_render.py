import render
from circle import Circle
from agents.agent import Agent
from agents.melee_agent import MeleeAgent
from agents.range_agent import RangeAgent

import numpy as np
import cv2 as cv
from time import sleep

a = MeleeAgent(75, 125, 10, 0, 0, 0, 10, 200, 200, 3, 35, 3)
a.melee_r = 10
a.m_theta = 75
a.theta = 0
a.fov = 50

cv.namedWindow('canvas')

for _ in range(360):
    canv = 255*np.ones((200, 200, 3), dtype=np.uint8)
    render.render_agent(a, canv)
    cv.imshow('canvas', canv)

    a.theta = a.theta + 1
    a.fov = a.fov + 1
    if a.fov >= 90:
        a.fov = a.fov - 1

    k = cv.waitKey(20)
    if k == 27:
        break

cv.destroyAllWindows()
