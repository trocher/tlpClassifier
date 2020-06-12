from complexity import Complexity, complexity_name
from enum import Enum
import itertools
from algorithms import constraint_reduction
LABELS = [0,1,2]
class Constraints(Enum):
    White = 0
    Black = 1 

class Problem:

    # Create a Problem
    # whiteConstraint is a set of all the configurations (3-tuples) allowed for the white nodes
    # blackConstraint is a set of all the configurations (3-tuples) allowed for the black nodes
    # whiteDegree an int, the degree of the white nodes
    # blackDegree an int, the degree of the black nodes
    def __init__(self, white_constraint, black_constraint, white_degree, black_degree):
        self.white_constraint,self.black_constraint = map(lambda x : frozenset(x),constraint_reduction(frozenset(white_constraint),frozenset(black_constraint)))
        self.white_degree = white_degree
        self.black_degree = black_degree
        self.lower_bound = Complexity.Constant
        self.upper_bound = Complexity.Unsolvable
        self.constant_upper_bound = 1000
    # The hash function for problems
    def __hash__(self):
        return hash((self.white_constraint,self.black_constraint))

    # Equality of problem.
    def __eq__(self,other):
        return (self.white_constraint == other.white_constraint and self.black_constraint == other.black_constraint)

    # Print the main characteristics of the problem in the console
    def __repr__(self):
        def mapping_function(configuration):
            return "A"*configuration[0]+"B"*configuration[1]+"C"*configuration[2]
        w = ", ".join(map(mapping_function,self.white_constraint))
        b = ", ".join(map(mapping_function,self.black_constraint))
        res = w + "\n" + b + "\n"
        if(self.get_complexity() == Complexity.Unclassified):
            return  res + "Lower bound : "+ complexity_name[self.lower_bound] + "\n" + "Upper bound : " + complexity_name[self.upper_bound] + "\n"
        else :
            res = res + "Complexity : "+ complexity_name[self.lower_bound] + "\n"
        if(self.get_complexity() == Complexity.Constant):
            return res + str(self.constant_upper_bound) + " round(s) upper bound\n"
        return res

    # Write the main characteristics of the problem in a file
    # io is the stream where the problem should be written
    def write_in_file(self, io):
        io.write(self.__repr__()+"\n")



    def print_RE(self):
        def mapping_function(configuration):
            return "A "*configuration[0]+"B "*configuration[1]+"C "*configuration[2]+"\n"
        w = "".join(map(mapping_function,self.white_constraint))
        b = "".join(map(mapping_function,self.black_constraint))
        print(w + "\n" + b + "\n\n")

    def write_in_file_RE(self, name):
        f= open(name,"w+")
        def mapping_function(configuration):
            return "A "*configuration[0]+"B "*configuration[1]+"C "*configuration[2]+"\n"
        w = "".join(map(mapping_function,self.white_constraint))
        b = "".join(map(mapping_function,self.black_constraint))
        #print(w + "\n" + b + "\n\n")
        f.write(w + "\n" + b + "\n")
        f.close()

    # Return the alphabet of the given constraint
    # constraint is either Constraints.Black or Constraints.Black
    def constraint_alphabet(self, constraint):
        alphabet = set()
        config = self.black_constraint if constraint == Constraints.Black else self.white_constraint
        for elem in config:
            for label in LABELS:
                if elem[label] != 0:
                    alphabet.add(label)
        return alphabet 

    # Return the size of the alphabet of the given constraint
    # constraint is either Constraints.Black or Constraints.Black
    def constraint_size(self, constraint):
        return len(self.black_constraint if constraint == Constraints.Black else self.white_constraint)

    # Return the the alphabet of the problem
    def alphabet(self):
        return self.constraint_alphabet(Constraints.White).union(self.constraint_alphabet(Constraints.Black))

    # Return the the alphabet size of the problem
    def alphabet_size(self):
        return len(self.alphabet())

    # Check if the current problem is a restriction of the given problem
    def is_restriction(self, other):
        return self.white_constraint.issubset(other.white_constraint) and self.black_constraint.issubset(other.black_constraint)
   
    # Check if the current problem is a relaxation of the given problem
    def is_relaxation(self, other):
        return other.is_restriction(self)

    def is_relaxation_of_at_least_1(self, problemSet):   
        for elem in problemSet:
            if self.is_relaxation(elem):
                return True
        return False

    def is_restriction_of_at_least_1(self, problemSet):
        for elem in problemSet:
            if self.is_restriction(elem):
                return True
        return False
    
    # Set a lower bound for the complexity of the problem
    def set_lower_bound(self,complexity):
            # Inputs:
        #       - complexity : the new lower bound to the problem
        if self.upper_bound.value < complexity.value:
            print("Error, trying to put a lower bound (", complexity, ") bigger than the current upper bound (", self.upper_bound , ")")
            print(self)
            return
        if self.lower_bound.value < complexity.value:
            self.lower_bound = complexity
            if complexity == Complexity.Unsolvable:
                self.set_upper_bound(Complexity.Unsolvable)

    # Set an upper bound for the complexity of the problem
    def set_upper_bound(self,complexity):
        # Inputs:
        #       - complexity : the new upper bound for the problem
        if self.lower_bound.value > complexity.value:
            print("Error, trying to put a upper bound (", complexity, ") lower than the current lower bound (", self.lower_bound , ")")
            print(self)
        if self.upper_bound.value > complexity.value:
            self.upper_bound = complexity
            if complexity == Complexity.Constant:
                self.set_lower_bound(Complexity.Constant)


    # Set the complexity of the problem to the given complexity
    # complexity, a Complexity
    def set_complexity(self,complexity):
        if self.lower_bound == self.upper_bound and self.lower_bound != Complexity.Unclassified and self.lower_bound != complexity:
            print("error a different complexity has already been assigned")
        self.set_lower_bound(complexity)
        self.set_upper_bound(complexity)

    # Get the complexity of the problem
    def get_complexity(self):
        return self.lower_bound if (self.lower_bound == self.upper_bound) else Complexity.Unclassified

    # Return a list of equivalents problem to the given problem as constraints tuple
    def equivalent_problems(self):
        #x = constraint_reduction(self.white_constraint,self.black_constraint)
        x = (self.white_constraint,self.black_constraint)
        problemList = [[[ (t[a],t[b],t[c]) for t in x] for x in x] for a,b,c in itertools.permutations([0,1,2])]
        if self.black_degree == self.white_degree:
            problemList+=([[b,w] for w,b in problemList])
        return problemList

    # Return a list of equivalents problem to the given problem
    def equivalent_problems_instance(self):
        return [Problem(w,b,self.white_degree,self.black_degree) for w,b in self.equivalent_problems()]
    
    # Return the characteristic problem of the equiavalent class of problems of this problem
    def get_characteristic_problem(self):
        equivalent_problems_list = self.equivalent_problems()
        for white,black in equivalent_problems_list:
            white.sort()
            black.sort() 
        equivalent_problems_list.sort()
        white_c,black_c = equivalent_problems_list[0]
        return Problem(white_c,black_c,self.white_degree,self.black_degree)

    # Return true if and only if the given problem is the unique characteristic problem of all of its equivalents problems
    def is_characteristic_problem(self):
        return self.get_characteristic_problem() == self
