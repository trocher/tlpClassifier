import itertools

def edge_3_labelling(degree):
    return [(a,b,degree-a-b) for a in range(0,degree+1) for b in range(0,degree+1-a)]


def edge_n_labelling_len(degree, n):
    if n == 1: return 1
    if n == 2: return len([(a,degree-a) for a in range(0,degree+1)])
    if n == 3: return len(edge_3_labelling(degree))
    print("error")

# Return the powerset of the given iterable oject
def powerset(that):
    return set(itertools.chain.from_iterable(itertools.combinations(that, r) for r in range(len(that)+1)))

# Return the set of all possible n-subsets of elements from the given iterable
def subsets_of_size_n(that, n):
    return [set(elem) for elem in powerset(that) if len(elem) == n]
