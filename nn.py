# Inputs:
# 	Fov angle
# 	N,S,E,W distance to wall
# 	Enemy presence
# 	Bullet presence

# Outputs:
# 	L/R take tanh > 0
# 	Attack sigmoid > 0.5
# 	Change fov angle tanh > 0

import numpy as np

def forward_prop(x, weights):
	'''
	Return the behavior vector given the environment and network weights.

	Params:
		x: The environment (input) vector
		weights: A list of matrices

	Returns:
		The behavior (output) vector
	'''

	output = x
	for W in weights:
		output = W.dot(output)
	return output	
