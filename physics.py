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
