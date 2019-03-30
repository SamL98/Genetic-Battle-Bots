import cv2 as cv
import numpy as np

import agents as ag
from agents.agent import AgentType
from wall import Wall

BLACK = (0, 0, 0)
LW = 5

def get_fov_line_params(x, y, theta):
	m = np.arctan(theta)
	b = y - m*x
	return m, b

def render_circ(agent, canvas):
	factor = 10
	w = agent.world_dims[1] * factor

	if agent.theta < 3*np.pi/2 and agent.theta >= np.pi/2:
		w *= -1

	circ = agent.circ
	x, y = circ.x, circ.y

	m1, b1 = get_fov_line_params(x, y, agent.theta-agent.fov/2)
	m2, b2 = get_fov_line_params(x, y, agent.theta+agent.fov/2)

	pts = np.array([
		[x, y],
		[w, m1*w + b1],
		[w, m2*w + b2]
	], dtype=np.int32)
	print(pts)
	pts = pts.reshape((-1, 1, 2))

	cv.polylines(canvas, pts, True, (0, 0, 255), LW)

	cv.circle(canvas, (x, y), circ.r, BLACK, -1)

	if agent.agent_type == AgentType.Melee and agent.melee_active:
		rad = agent.r + agent.m_r
		start = agent.theta - agent.m_theta/2 
		cv.ellipse(canvas, (x, y), (rad, rad), 0, start, agent.m_theta, BLACK, LW)
