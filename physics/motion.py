import numpy as np
from steering_direction import SteeringDirection

def update_position(x, y, vx, vy, dt):
	'''
	Update the position of an agent given their velocity

	Params:
		x: The current x component of the position
		y: The y component
		vx: The x component of the velocity
		vy: The y component
		dt: The timestep since the last update

	Returns:
		The new (x, y) position
	'''

	return x + vx*dt, y + vy*dt

def update_velocity(vx, vy, lr, theta_step=5):
	'''
	Update the velocity of an agent given their steering angle

	Params:
		vx: The x component of the velocity
		vy: The y component
		lr: A SteeringDirection (left or right) 
		theta_step: The delta theta to use

	Returns:
		The new (vx, vy) velocity
	'''

	dtheta = -theta_step
	if lr == SteeringDirection.Right:
		dtheta *= -1

	v_theta = np.atan(vy/np.max(1e-7, vx))
	v_mag = np.sqrt(vx**2 + vy**2)

	new_theta = v_theta + dtheta
	return (v_mag * np.cos(new_theta), v_mag * np.sin(new_theta))
