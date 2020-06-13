import numpy as np
import itertools, tempfile, re, subprocess,os
import problem
LABELS = set([0,1,2])
WHITE_DEGREE = 2
BLACK_DEGREE = 3
SERVER_DIR = os.path.dirname(os.path.realpath(__file__))+'/server'

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


#for tuple (x,x) if alphabet =3
#on the doc (x,x) (ex : 3,2)
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


# For tuple (2,3)
# on the doc (3,2)
# could be (3,x)
def greedy4Coloring(problem):
    white = set([(1,1,0),(0,1,1),(1,0,1)])
    black = set([(BLACK_DEGREE,0,0),(0,BLACK_DEGREE,0),(0,0,BLACK_DEGREE)])
    if white == problem.white_constraint and black.issubset(problem.black_constraint) and len(problem.black_constraint) > 3:
        return True

def round_eliminator_constant(problem):
    iter_label = [(20,3),(9,4),(4,5),(4,6)]
    #for i in range(len(iter_label)):
    for i in [1,2]:
        ub = round_eliminator(problem,'autoub', iter_label[i][0], iter_label[i][1])
        if ub >= 0:
            if i > 0:
                print(" done in : ",i," with a ub of : ",ub)
            return ub
    return -1

def round_eliminator(problem, function, iterations, labels):
    with tempfile.NamedTemporaryFile(mode = 'w+',suffix='.txt',newline='\n') as temp_file_w, tempfile.NamedTemporaryFile(mode = 'w+',suffix='.txt',newline='\n') as temp_file_b:
        
        temp_file_b.write(problem.re_format_black())
        temp_file_w.write(problem.re_format_white())

        temp_file_b.flush()
        temp_file_w.flush()

        result_b = subprocess.getoutput(SERVER_DIR + " " + function + ' -f ' + temp_file_b.name + ' --iter ' + str(iterations) +' --labels ' + str(labels))
        result_w = subprocess.getoutput(SERVER_DIR + " " + function + ' -f ' + temp_file_w.name + ' --iter ' + str(iterations) +' --labels ' + str(labels))
        if not result_b and not result_w:
            return -1
        else :
            if not result_b or not result_w:
                print(problem)
            def get_value(result):
                search_string = 'Upper bound of '
                index = result.find(search_string)
                return int(result[len(search_string)+index])
            w = 444
            b = 444
            if result_w:
                w = get_value(result_w)
            if result_b:
                b = get_value(result_b)
            return min(w,b)

def round_eliminator_lb(problem,iterations,labels):
    file_name = str(hash(problem))
    print(file_name)
    result_b = subprocess.run(['/Users/tanguy/Documents/tlpClassifier/server','autolb','-f','data/problems_RE/2_3/'+file_name + '_b.txt','--iter',str(iterations),'--labels',str(labels)],stdout=subprocess.PIPE, text=True)
    result_w = subprocess.run(['/Users/tanguy/Documents/tlpClassifier/server','autolb','-f','data/problems_RE/2_3/'+file_name + '_w.txt','--iter',str(iterations),'--labels',str(labels)],stdout=subprocess.PIPE, text=True)
    if not result_b.stdout and not result_w.stdout:
        return -1
    else :
        print(file_name)
        print("===========================")
        def get_lower_bound(result):
            if "Lower bound of " + str(iterations+1)+" rounds." in result:
                return True
            return False

        if get_lower_bound(result_w.stdout) or get_lower_bound(result_b.stdout):
            problem.print_RE()
            return True

def cover_map_1(white_constraint,black_constraint):
    w = set([(w0-b0,w1-b1,w2-b2) for (w0,w1,w2) in black_constraint for (b0,b1,b2) in white_constraint if w0-b0 >= 0 and w1-b1 >=0 and w2-b2>=0])
    b = set([(w0a+w0b,w1a+w1b,w2a+w2b) for (w0a,w1a,w2a) in w for (w0b,w1b,w2b) in w if (w0a+w0b,w1a+w1b,w2a+w2b) in white_constraint])
    return not b

def log_test(white_constraint,black_constraint):
    def num_to_alpha_configuration(num_configuration):
        return "A"*num_configuration[0]+"B"*num_configuration[1]+"C"*num_configuration[2]

    def alpha_to_num_configuration(alpha_configuration):
        return (alpha_configuration.count('A'),alpha_configuration.count('B'),alpha_configuration.count('C'))

    def can_be_neighbors(ordered_configuration_1,ordered_configuration_2,white_constraint):
        zipped_configurations = list(zip(ordered_configuration_1,ordered_configuration_2))
        return all([alpha_to_num_configuration(x) in white_constraint for x in zipped_configurations])

    def c_ordered_configurations(a,b):
        lst = [
            (a[0],a[1],b[2]),
            (a[0],b[1],b[2]),
            (a[0],b[1],a[2]),
            (b[0],a[1],b[2]),
            (b[0],a[1],a[2]),
            (b[0],b[1],a[2])
        ]
        return lst

    black_c_alpha = [list(num_to_alpha_configuration(x)) for x in black_constraint]
    black_c_ordered_alpha = list({x for lst in black_c_alpha for x in itertools.permutations(lst)})
    for a in black_c_alpha:
        y = [b for b in black_c_ordered_alpha if can_be_neighbors(a,b,white_constraint)]
        for b in y:
            c = c_ordered_configurations(a,b)
            if all([any([can_be_neighbors(x,y,white_constraint) for y in black_c_ordered_alpha]) for x in c]):
                return True
    return False
