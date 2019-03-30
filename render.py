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

def adjust_xy(x, y, ax, theta):
	if -theta < 3*np.pi/2 and -theta > np.pi/2:
		x *= -1
	elif -theta == np.pi/2 or -theta == 3*np.pi/2:
		y = -x
		if -theta == 3*np.pi/2: y = x
		x = ax
	return x, y

def render_agent(agent, canvas):
	factor = 10
	w = agent.world_dims[1] * factor

	theta = -agent.theta*np.pi/180
	fov = agent.fov*np.pi/180

	circ = agent.circ
	x, y = circ.x, circ.y

	m1, b1 = get_fov_line_params(x, y, theta-fov/2)
	m2, b2 = get_fov_line_params(x, y, theta+fov/2)

	x1 = adjust_xy(w, 0, x, theta-fov/2)[0]
	x2 = adjust_xy(w, 0, x, theta+fov/2)[0]

	y1 = m1*x1 + b1
	if abs(m1) > np.iinfo(np.int32).max:
		y1 = np.sign(m1) * w

	y2 = m2*x2 + b2
	if abs(m2) > np.iinfo(np.int32).max:
		y2 = np.sign(m2) * w

	x1, y1 = adjust_xy(w, y1, x, theta-fov/2)
	x2, y2 = adjust_xy(w, y2, x, theta+fov/2)

	pts = np.array([
		[x, y],
		[x1, y1],
		[x2, y2]
	], dtype=np.int32)

	cv.polylines(canvas, [pts], True, (0, 0, 0), LW)

	cv.circle(canvas, (int(x), int(y)), circ.r, BLACK, -1)

	if agent.agent_type == AgentType.Melee and agent.melee_active:
		rad = agent.circ.r + agent.melee_r
		m_theta = agent.m_theta
		start = agent.theta - m_theta/2 
		cv.ellipse(canvas, (int(x), int(y)), (rad, rad), 0, 360-start, 360-(start+m_theta), BLACK, LW)

def render_bullet(bullet, canvas):
	x, y = bullet.circ.x, bullet.circ.y
	cv.circle(canvas, (int(x), int(y)), bullet.circ.r, BLACK, -1)
