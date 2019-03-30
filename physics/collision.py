from circle import Circle
from melee_arc import MeleeArc
from wall import Wall

def detect_circle_wall_collision(c, w, h):
	'''
	Detect what walls, if any the circle is colliding with

	Params:
		c: The circle
		w: Width of the world
		h: Height of the world

	Returns:
		A list of Walls that the circle is colliding with
	'''

	walls = []
	bbox = {x: c.x - c.r, y: c.y - c.r, w: 2*c.r, h: 2*c.r}

	if bbox.x <= 0: walls.append(Wall.East)
	if bbox.y <= 0: walls.append(Wall.North)
	if bbox.x >= w: walls.append(Wall.West)
	if bbox.y >= h: walls.append(Wall.South)
	
	return walls

def execute_wall_collision_response(c, vx, vy, walls):
	'''	
	Updates the velocity of the circle depending on what walls it's colliding with

	Params:
		c: The circle
		vx, vy: The components of the velocity
		walls: The walls that are in collision with the circle

	Returns:
		The new (vx, vy) of the circle
	'''	

	new_vx, new_vy = vx, vy
	
	if Wall.East or Wall.West in walls: new_vy *= -1
	if Wall.North or Wall.South in walls: new_vx *= -1

	return (new_vx, new_vy)

def detect_circle_circle_collision(c1, c2):
	'''
	Detect whether or not two circles are colliding

	Params:
		c1: A (x, y, r) namedtuple of the first circle
		c2: A (x, y, r) namedtuple of the second circle

	Returns:
		Whether or not the two circles are colliding
	'''

	return (c1.x - c2.x)**2 + (c1.y - c2.y)**2 <= c1.r + c2.r

def detect_circle_melee_arc_collision(c1, c2, m):
	'''
	Detect whether or not a circle and a melee arc are colliding

	Params:
		c1: The first circle namedtuple
		c2: The second circle namedtuple
		m: The melee arc for the second circle

	Returns:
		Whether or not c1 and m are colliding
	'''

	if (c1.x - c2.x)**2 + (c1.y - c2.y)*2 > c1.r + c2.r + m.dr:
		return False

	theta_pad = np.atan(c1.r / np.max(1e-7, c1.r + c2.r))
	theta = m.theta - theta_pad
	phi = m.phi + 2*theta_pad

	c_theta = np.atan((c1.x - c2.x) / np.max(1e-7, c1.y - c2.y))
	return c_theta >= theta and c_theta <= theta+phi
