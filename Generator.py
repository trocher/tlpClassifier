import itertools
from Tools import edge_3_labelling,powerset
from Problem import Problem
from FileHelp import data_name, store
from timeit import default_timer as timer
import time
from tqdm import tqdm
from joblib import Parallel, delayed
import multiprocessing

WHITE_DEGREE = 2
BLACK_DEGREE = 3

DEBUG = True
#DEBUG = False

def store_RE_problem(problem):
        def mapping_function(configuration):
            return "A "*configuration[2]+"B "*configuration[1]+"C "*configuration[0]+"\n"
        w = "".join(map(mapping_function,problem.white_constraint))
        b = "".join(map(mapping_function,problem.black_constraint))
        
        def write_in_file_RE(name, active, passive):
            f= open(name,"w+")
            f.write(active + "\n" + passive + "\n")
            f.close()
        write_in_file_RE("data/problems_RE/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + str(hash(problem)) + "_w.txt",w,b)
        write_in_file_RE("data/problems_RE/" + str(WHITE_DEGREE) + "_" + str(BLACK_DEGREE) + "/" + str(hash(problem)) + "_b.txt",b,w)
        
# Return the set of all characteristics problems with the given degrees
def generate(white_degree, black_degree):
    white_configurations, black_configurations = edge_3_labelling(white_degree),edge_3_labelling(black_degree)
    white_constraints, black_constraints = powerset(white_configurations),powerset(black_configurations)
    problems_tuple = set([(frozenset(a),frozenset(b)) for a in white_constraints for b in black_constraints])
    problems = set([Problem(a,b,white_degree,black_degree) for (a,b) in problems_tuple if Problem(a,b,white_degree,black_degree).is_characteristic_problem()])
    number_of_problems = len(problems)
    problems_list = list(problems)
    if DEBUG:
        print("Number of White Configurations :",len(white_configurations))
        print("Number of Black Configurations :",len(black_configurations))
        print("Number of White Constraints :",len(white_constraints))
        print("Number of Black Constraints :",len(black_constraints))
    relaxations_dict, restrictions_dict = dict(),dict()

    #print("Storing the problems in the RE format ...")
    #for elem in tqdm(problems):
    #    store_RE_problem(elem)

    print("Computing relaxations and restrictions ...")
    num_cores = multiprocessing.cpu_count()
    #for elem in tqdm(problems):

    def processInput(elem):
        relaxations,restrictions = set(),set()
        equivalent_set = elem.equivalent_problems_instance()
        for other in problems:
            for x in equivalent_set:
                if elem != other :
                    if x.is_restriction(other) and other in problems:
                        relaxations.add(other)
                    if x.is_relaxation(other) and other in problems:
                        restrictions.add(other)
        return (relaxations,restrictions)
    

    values = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in tqdm(problems_list))
    relaxations, restrictions = map(list, zip(*values))

    relaxations_dict = dict(zip(problems_list, relaxations))
    relaxations_dict = dict(zip(problems_list, restrictions))

    for elem in tqdm(problems):
        processInput(elem)
    return (set(problems),relaxations_dict,restrictions_dict)

p = generate(WHITE_DEGREE,BLACK_DEGREE)
store(WHITE_DEGREE,BLACK_DEGREE,p,"UC")
