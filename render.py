import cv2 as cv
import numpy as np

import agents as ag
from agents.agent import AgentType
from wall import Wall

BLACK = (0, 0, 0)
LW = 1

def get_fov_line_params(x, y, theta):
	m = np.tan(theta)
	b = y - m*x
	return m, b

def render_circ(agent, canvas):
	factor = 10
	w = agent.world_dims[1] * factor

	theta = -agent.theta*np.pi/180
	fov = agent.fov*np.pi/180

	x1, x2 = w, w
	if theta < 3*np.pi/2 and theta > np.pi/2:
		x1 *= -1
		x2 *= -1
	elif theta == np.pi/2:
		x2 *= -1
	elif theta == 3*np.pi/2:
		x1 *= -1

	circ = agent.circ
	x, y = circ.x, circ.y

	m1, b1 = get_fov_line_params(x, y, theta-fov/2)
	m2, b2 = get_fov_line_params(x, y, theta+fov/2)

	pts = np.array([
		[x, y],
		[x1, m1*x1 + b1],
		[x2, m2*x2 + b2]
	], dtype=np.int32)

	cv.polylines(canvas, [pts], True, (0, 0, 0), LW)

	cv.circle(canvas, (x, y), circ.r, BLACK, -1)

	if agent.agent_type == AgentType.Melee and agent.melee_active:
		rad = agent.r + agent.m_r
		m_theta = agent.m_theta*np.pi/180
		start = agent.theta - m_theta/2 
		cv.ellipse(canvas, (x, y), (rad, rad), 0, start, agent.m_theta, BLACK, LW)
