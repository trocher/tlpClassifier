import pickle
from problem_set import Problem_set, problem_set_name

def add_degree_suffix(name, white_degree, black_degree):
    suffix = "_" + str(white_degree) + "_" + str(black_degree)
    return name + suffix

def data_name(white_degree,black_degree):
    return add_degree_suffix("data/problemSet",white_degree,black_degree)

def import_data_set(white_degree, black_degree,classified):
    problems = (set(), dict(), dict())
    with open(data_name(white_degree,black_degree) + '_' + problem_set_name[classified], 'rb') as problem_file:
        problems = pickle.load(problem_file)
    return problems

# Store the given problem set in the file with the given name
def store(white_degree,black_degree,probems,classified):
    with open(data_name(white_degree,black_degree) + '_' + problem_set_name[classified], 'wb') as problem_file:
        pickle.dump(probems, problem_file)

# Store a given set of problems in a file
# name, a string, the name of the file
# that, the set of problems
def problems_to_file(name, that):
    f= open(name,"w+")
    for elem in that:
        elem.write_in_file(f)
    f.close()
