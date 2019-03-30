from circle import Circle
from melee_arc import MeleeArc

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
