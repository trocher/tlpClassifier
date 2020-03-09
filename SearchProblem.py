from FileHelp import import_data_set
from Problem import Problem

def alpha_to_num_constraint( alpha_constraint):
    return [(x.count('A'),x.count('B'),x.count('C')) for x in alpha_constraint]

def search(alpha_problem):
    white_degree = alpha_problem[2]
    black_degree = alpha_problem[3]
    problems = import_data_set(white_degree, black_degree,"C")
    problem = Problem(alpha_to_num_constraint(alpha_problem[0]),alpha_to_num_constraint(alpha_problem[1]),alpha_problem[2],alpha_problem[3]).get_characteristic_problem()
    #problem.show()
    for elem in problems:
        if problem == elem:
            print(elem)

white_constraint = {'AA','BA'}
black_constraint = {'BCC','ACC','AB'}
white_degree = 2
black_degree = 3
alpha_problem = (white_constraint,black_constraint,white_degree,black_degree)
search(alpha_problem)