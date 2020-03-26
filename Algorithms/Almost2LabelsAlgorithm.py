import numpy as np
LABELS = [0,1,2]
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

def looping_labels(white_constraint,black_constraint):
    matrix = matrix_computation(adjancy_matrix(white_constraint),adjancy_matrix(black_constraint))
    return [i for i in LABELS if matrix[i][i]]
