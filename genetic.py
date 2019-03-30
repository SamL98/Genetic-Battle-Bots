import numpy as np

# Create a random population
def random_generation(n_organisms, *brain_structure):
    """Creates a set of random organisms with the specified brain structure.

    n_organisms: how many random organisms to create

    brain_structure: Tuples that represent the (in_dim, out_dim) of each layer of the network

    Returns: A list of the layers of each network"""
    
    generation = []
    for struct in brain_structure:
        generation.append(10 * np.random.rand(n_organisms, *struct) - 5)
        
    return generation


# Crossover
def crossover_individual(left, right):
    """Takes two organsims and computes their crossovered child."""
    
    shape = left.shape
    
    left = left.reshape(-1)
    right = right.reshape(-1)
    
    cross_point = int(np.floor(np.random.rand() * left.shape[0]))
    
    left_child = left.copy()
    left_child[cross_point:] = right[cross_point:]
    left_child = left_child.reshape(shape)
    
    right_child = right.copy()
    right_child[cross_point:] = left[cross_point:]
    right_child = right_child.reshape(shape)
    
    return left_child, right_child
    
    
def crossover_organisms(organisms, pairs):
    """Takes a population and a list of couplings to produce offspring.

    organisms: [Layerwise organism weights]
    
    pairs: [(left, right)] array of tuples of couplings

    Returns: [Layerwise organism weights] of children"""

    children = [np.zeros((len(pairs), *layer.shape[1:])) for layer in organisms]
    for i, (left, right) in enumerate(pairs):
        for layer in range(len(organisms)):
            # Always choose the "left" child
            left_org = organisms[layer][left]
            right_org = organisms[layer][right]
            children[layer][i] = crossover_individual(left_org, right_org)[0]
            
    return children


# Mutate
def mutate_organisms_normal(organisms, mutate_p=0.05, mutate_sd=0.1):
    """Mutates a population if the mutations are iid Normal centered on the current value.

    organisms: the list of weight matrices

    mutate_p: probability of mutation for a gene
    
    mutate_sd: the standard deviation of the mutations

    Returns: the mutated organisms
    """
    
    mutated = [np.zeros(layer.shape) for layer in organisms]
    
    for i, layer in enumerate(organisms):
        mutate_idx = np.random.rand(*layer.shape)
        mutate_idx = mutate_idx < mutate_p
        potential = np.random.normal(loc=layer, scale=mutate_sd)
        mutated[i] = np.where(mutate_idx, potential, organisms[i])
        
    return mutated
    
# Fitness
def random_fitness(organsism):
    """Produces a random fitness score between 0 and 1 for each organism."""
    return np.random.rand(organsism[0].shape[0])

# Breed
def breed(organisms, fit_scores, n_children, keep_best=2):
    """Breeds the organisms based on their fitness scores.

    organsisms: the list of weight matrices

    fit_scores: an array of the fitnesses in order of organism

    n_children: the size of the population of children
    """
    
    pairs = []
    
    best_orgs = np.argsort(fit_scores)[::-1]
    for i in range(keep_best):
        pairs.append((best_orgs[i], best_orgs[i]))
    
    choose_prob = np.cumsum(fit_scores)
    choose_prob = choose_prob / choose_prob[-1]
    
    for i in range(n_children - keep_best):
        left, right = np.random.rand(2)
        left = np.argmin(choose_prob < left)
        right = np.argmin(choose_prob < right)
        
        pairs.append((left, right))
        
    children = crossover_organisms(organisms, pairs)
    children = mutate_organisms_normal(organisms)
    
    return children
    
