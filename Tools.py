import itertools
from Problem import Problem
# Return the list of possible 3-labellings of node with a given degre

def edge_3_labelling(degree):
    return [(a,b,degree-a-b) for a in range(0,degree+1) for b in range(0,degree+1-a)]

# Return the powerset of the given iterable oject
def powerset(that):
    return set(itertools.chain.from_iterable(itertools.combinations(that, r) for r in range(len(that)+1)))

def alpha_to_num_constraint( alpha_constraint):
    return [(x.count('A'),x.count('B'),x.count('C')) for x in alpha_constraint]

def alpha_to_problem(alpha_problem):
    white_degree = alpha_problem[2]
    black_degree = alpha_problem[3]
    return Problem(alpha_to_num_constraint(alpha_problem[0]),alpha_to_num_constraint(alpha_problem[1]),alpha_problem[2],alpha_problem[3]).get_characteristic_problem()
