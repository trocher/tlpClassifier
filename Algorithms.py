import numpy as np
LABELS = set([0,1,2])
WHITE_DEGREE = 2
BLACK_DEGREE = 3

# Return all the configurations of the given constraint that does not contains any of the given labels
def configurations_without(constraint, that):
    return {elem for elem in constraint if all([elem[i] == 0 for i in that])}

# Remove all the useless configurations from both white and black constraints
def constraint_reduction(white_constraint, black_constraint):
    # Return the alphabet of the given constraint (a set of 3-tuple)
    def constraint_alphabet(constraint):
        alphabet = set()
        for elem in constraint:
            for label in LABELS:
                if elem[label] != 0:
                    alphabet.add(label)
        return alphabet

    # Return the sets of labels that appear in and only in one constraint
    def labels_in_1_constraint(white_constraint,black_constraint):
        return (constraint_alphabet(white_constraint).union(constraint_alphabet(black_constraint))).difference(constraint_alphabet(white_constraint).intersection(constraint_alphabet(black_constraint)))

    tmp = set(LABELS)
    while(len(tmp) != 0 and len(white_constraint)!=0 and len(black_constraint)!=0):
        tmp = labels_in_1_constraint(white_constraint,black_constraint)
        white_constraint = configurations_without(white_constraint,tmp)
        black_constraint = configurations_without(black_constraint,tmp)
    return(white_constraint,black_constraint)

def redundancy_algorithm(white_constraint,black_constraint):
    def relabeled_configurations(constraint,i,j):
        tmp = set()
        for elem in constraint:
            if elem[j] != 0 :
                lst = list(elem).copy()
                lst[i] = elem[i]+elem[j]
                lst[j] = 0
                tmp.add(tuple(lst))
        return tmp
        
    for i in LABELS:
        used_labels = LABELS.copy()
        used_labels.remove(i)
        for j in used_labels:
            if relabeled_configurations(white_constraint,i,j).issubset(white_constraint) and\
                relabeled_configurations(black_constraint,i,j).issubset(black_constraint):
                return (configurations_without(white_constraint,set([j])),configurations_without(black_constraint,set([j])), LABELS - set([j]))
    return None

def greedy4Coloring(white_constraint,black_constraint):
    white = set([(1,1,0),(0,1,1),(1,0,1)])
    black = set([(BLACK_DEGREE,0,0),(0,BLACK_DEGREE,0),(0,0,BLACK_DEGREE)])
    if white == white_constraint and black.issubset(black_constraint) and len(black_constraint) > 3:
        return True

def looping_labels(white_constraint,black_constraint):
    def adjancy_matrix(constraint):
        matrix = np.array([[0, 0, 0],[0, 0, 0], [0, 0, 0]])
        for configuration in constraint:
            for x in range(0,3):
                if configuration[x] != 0:
                    adjancy_list = np.array(configuration)
                    adjancy_list[x]-=1
                    matrix[x] = [any(x) for x in zip(matrix[x],adjancy_list)]
        return matrix

    def matrix_computation(w, b):
        return np.array([w,b,w@b,b@w,w@b@w,b@w@b]).sum(axis=0)

    matrix = matrix_computation(adjancy_matrix(white_constraint),adjancy_matrix(black_constraint))
    return [i for i in LABELS if matrix[i][i]]
