import itertools
from Problem import Problem
# Return the list of possible 3-labellings of node with a given degre

def edge_3_labelling(degree):
    return [(a,b,degree-a-b) for a in range(0,degree+1) for b in range(0,degree+1-a)]

def edge_n_labelling_generator(degree,labels):
    if len(labels) == 3:
        return {(a,b,degree-a-b) for a in range(0,degree+1) for b in range(0,degree+1-a)}
    if len(labels) == 2:
        x = [(a,degree-a) for a in range(0,degree+1)]
        labels_set = set(labels)
        if labels_set == set([0,1]):
            return {(a,b,0) for a,b in x}
        if labels_set == set([1,2]):
            return {(0,a,b) for a,b in x}
        if labels_set == set([0,2]):
            return {(a,0,b) for a,b in x}
    if len(labels) == 1:
        return set([tuple([degree if x == labels[0] else 0 for x in range(0,3)])])

# Return the powerset of the given iterable oject
def powerset(that):
    return set(itertools.chain.from_iterable(itertools.combinations(that, r) for r in range(len(that)+1)))

# Return the set of all possible n-subsets of elements from the given iterable
def subsets_of_size_n(that, n):
    return [set(elem) for elem in powerset(that) if len(elem) == n]

def alpha_to_num_constraint( alpha_constraint):
    return [(x.count('A'),x.count('B'),x.count('C')) for x in alpha_constraint]

def alpha_to_problem(alpha_problem):
    white_degree = alpha_problem[2]
    black_degree = alpha_problem[3]
    return Problem(alpha_to_num_constraint(alpha_problem[0]),alpha_to_num_constraint(alpha_problem[1]),alpha_problem[2],alpha_problem[3]).get_characteristic_problem()
