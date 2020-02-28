# Return the alphabet of the given constraint (a set of 3-tuple)
def constraint_alphabet(constraint):
    alphabet = set()
    for elem in constraint:
        for label in [1,2,3]:
            if elem[label-1] != 0:
                alphabet.add(label)
    return alphabet

# Return all the configurations of the given constraint that does not contains any of the given labels
def configurations_without(constraint, that):
    return {elem for elem in constraint if all([elem[i-1] == 0 for i in that])}

# Return the sets of labels that appear in and only in one constraint
def labels_in_1_constraint(white_constraint,black_constraint):
    return (constraint_alphabet(white_constraint).union(constraint_alphabet(black_constraint))).difference(constraint_alphabet(white_constraint).intersection(constraint_alphabet(black_constraint)))

# Remove all the useless configurations from both white and black constraints
def constraint_reduction(problem):
    white_constraint = problem.white_constraint
    black_constraint = problem.black_constraint
    tmp = set([1,2,3])
    while(len(tmp) != 0 and len(white_constraint)!=0 and len(black_constraint)!=0):
        tmp = labels_in_1_constraint(white_constraint,black_constraint)
        white_constraint = configurations_without(white_constraint,tmp)
        black_constraint = configurations_without(black_constraint,tmp)
    return(white_constraint,black_constraint)