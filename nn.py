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
		x: The environment (input) matrix - one row per organism
		weights: A list of weight tensors - num organism x input x output length

	Returns:
		The behavior (output) matrix - one row per organism
	'''

	output = x[...,np.newaxis]
	for W in weights:
		output = W @ output
	return output.reshape(output.shape[:-1])	
