from Complexity import Complexity, complexity_name
from enum import Enum
import itertools
from ConstraintReductionAlgorithm import constraint_reduction

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
        self.white_constraint = frozenset(white_constraint)
        self.black_constraint = frozenset(black_constraint)
        self.white_degree = white_degree
        self.black_degree = black_degree
        self.lower_bound = Complexity.Constant
        self.upper_bound = Complexity.Unsolvable

    # The hash function for problems
    def __hash__(self):
        return hash((self.white_constraint,self.black_constraint))

    # Equality of problem.
    def __eq__(self,other):
        return (self.white_constraint == other.white_constraint and self.black_constraint == other.black_constraint)

    # Print the main characteristics of the problem in the console
    def show(self):
        print("W degree =", self.white_degree, "| B degree =", self.black_degree, "| Alphabet :", self.alphabet())
        reduced_white_constraint, reduced_black_constraint = constraint_reduction(self)
        if(self.get_complexity()==Complexity.Unclassified):
            reduced_white_constraint, reduced_black_constraint = constraint_reduction(self)
            print("White Constraint : ", self.reduced_white_constraint)
            print("Black Constraint : ", self.reduced_black_constraint)
            print("Lower bound : ", complexity_name[self.lower_bound],"Upper bound : ", complexity_name[self.upper_bound])
        else:
            print("White Constraint : ", self.white_constraint)
            print("Black Constraint : ", self.black_constraint)
        print(" ")

    # Write the main characteristics of the problem in a file
    # io is the stream where the problem should be written
    def write_in_file(self, io):
        io.write("W degree = "+ str(self.white_degree) + " | B degree = " + str(self.black_degree) + " | Alphabet : " + str(self.alphabet()) +"\n")
        if(self.get_complexity()==Complexity.Unclassified):
            reduced_white_constraint, reduced_black_constraint = constraint_reduction(self)
            io.write("White Constraint : " + str(reduced_white_constraint)+"\n")
            io.write("Black Constraint : " + str(reduced_black_constraint)+"\n")
            io.write("Lower bound : " + complexity_name[self.lower_bound] + " | Upper bound : " + complexity_name[self.upper_bound] + "\n")
        else:
            io.write("White Constraint : " + str(reduced_white_constraint)+"\n")
            io.write("Black Constraint : " + str(reduced_black_constraint)+"\n")
        io.write("\n")

    # Return the alphabet of the given constraint
    # constraint is either Constraints.Black or Constraints.Black
    def constraint_alphabet(self, constraint):
        alphabet = set()
        config = self.black_constraint if constraint == Constraints.Black else self.white_constraint
        for elem in config:
            for label in [1,2,3]:
                if elem[label-1] != 0:
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
            self.show()
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
            self.show()
        if self.upper_bound.value > complexity.value:
            self.upper_bound = complexity
            if complexity == Complexity.Constant:
                self.set_lower_bound(Complexity.Constant)


    # Set the complexity of the problem to the given complexity
    # complexity, a Complexity
    def set_complexity(self,complexity):
        # Inputs:
        #       - complexity : the new lower bound for the problem
        self.set_lower_bound(complexity)
        self.set_upper_bound(complexity)

    # Get the complexity of the problem
    def get_complexity(self):
        return self.lower_bound if (self.lower_bound == self.upper_bound) else Complexity.Unclassified