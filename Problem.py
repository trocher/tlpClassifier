from Complexity import Complexity
from enum import Enum
import itertools

class Configurations(Enum):
    White = 0
    Black = 1 

class Problem:

    # Creating a Problem
    # whiteConfigurations is a set of all the configurations (3-tuples) allowed for the white nodes
    # blackConfigurations is a set of all the configurations (3-tuples) allowed for the black nodes
    # whiteDegree an int, the degree of the white nodes
    # blackDegree an int, the degree of the black nodes
    def __init__(self, whiteConfigurations, blackConfigurations, whiteDegree, blackDegree):
        self.whiteConfigurations = frozenset(whiteConfigurations)
        self.blackConfigurations = frozenset(blackConfigurations)
        self.whiteDegree = whiteDegree
        self.blackDegree = blackDegree
        self.lowerbound = Complexity.Constant
        self.upperbound = Complexity.Unsolvable
        self.complexity = Complexity.Unclassified

    # The hash function for problems
    def __hash__(self):
        return hash((self.whiteConfigurations,self.blackConfigurations))

    # Equality of problem.
    def __eq__(self,other):
        return (self.whiteConfigurations == other.whiteConfigurations and self.blackConfigurations == other.blackConfigurations)

    # Test if the problem is equivalent to a given problem
    # that is the problem to be compared with
    def isEquivalent(self, that):
        return that in self.equivalentProblems()

    # Print the main characteristics of the problem in the console
    def show(self):
        print("W degree =", self.whiteDegree, "| B degree =", self.blackDegree, "| Alphabet :", self.alphabet())
        print("White Config : ", self.whiteConfigurations)
        print("Black Config : ", self.blackConfigurations)
        print(" ")

    # Write the main characteristics of the problem in a file
    # io is the stream where the problem should be written
    def writeInFile(self, io):
        io.write("W degree = "+ str(self.whiteDegree) + " | B degree = " + str(self.blackDegree) + " | Alphabet : " + str(self.alphabet()) +"\n")
        io.write("White Config : " + str(self.whiteConfigurations)+"\n")
        io.write("Black Config : " + str(self.blackConfigurations)+"\n\n")

    # Return the alphabet of the given configuration
    # configuration is either Configurations.Black or Configurations.Black
    def configurationAlphabet(self, configuration):
        alphabet = set()
        config = self.blackConfigurations if configuration == Configurations.Black else self.whiteConfigurations
        for elem in config:
            for label in [1,2,3]:
                if elem[label-1] != 0:
                    alphabet.add(label)
        return alphabet

    # Return the size of the alphabet of the given configuration
    # configuration is either Configurations.Black or Configurations.Black
    def configurationAlphabetSize(self, configuration):
        return len(self.blackConfigurations if configuration == Configurations.Black else self.whiteConfigurations)

    # Return the the alphabet of the problem
    def alphabet(self):
        return self.configurationAlphabet(Configurations.White).union(self.configurationAlphabet(Configurations.Black))

    # Return the the alphabet size of the problem
    def alphabetSize(self):
        return len(self.alphabet())

    # Check if the black configurations and the white configurations share some labels
    def hasCommonLabels(self):
        return len(self.configurationAlphabet(Configurations.White).intersection(self.configurationAlphabet(Configurations.Black))) != 0

    # Compute the set of equivalents problems of the problem
    def equivalentProblems(self):
        res = set()
        problemSet = {tuple(frozenset( (t[a],t[b],t[c]) for t in x) for x in [self.whiteConfigurations, self.blackConfigurations]) for a,b,c in itertools.permutations([0,1,2])}
        if self.blackDegree == self.whiteDegree:
            problemSet.union({(b,w) for w,b in problemSet})
        for w,b in problemSet : res.add(Problem(w,b,self.whiteDegree,self.blackDegree))
        return res


    # Check if the current problem is a restriction of the given problem
    def isRestriction(self, other):
        return self.whiteConfigurations.issubset(other.whiteConfigurations) and self.blackConfigurations.issubset(other.blackConfigurations)
   
    # Check if the current problem is a relaxation of the given problem
    def isRelaxation(self, other):
        return other.isRestriction(self)

    def setLowerBound(self,complexity):
        if self.upperbound.value < complexity.value:
            print("Error, trying to put a lowerbound (", complexity, ") bigger than the current upperbound (", self.upperbound , ")")
            self.show()
            return
        if self.lowerbound.value < complexity.value:
            self.lowerbound = complexity
            if complexity == Complexity.Unsolvable:
                self.setUpperBound(Complexity.Unsolvable)

    def setUpperBound(self,complexity):
        if self.lowerbound.value > complexity.value:
            print("Error, trying to put a upperbound (", complexity, ") lower than the current lowerbound (", self.lowerbound , ")")
            self.show()
            return
        if self.upperbound.value > complexity.value:
            self.upperbound = complexity
            if complexity == Complexity.Constant:
                self.setLowerBound(Complexity.Constant)


    # Set the complexity of the problem to the given complexity
    # complexity, a Complexity
    def setComplexity(self,complexity):
        #self.setLowerBound(complexity)
        #self.setUpperBound(complexity)
        if complexity.value < self.complexity.value:
            self.complexity = complexity

    # get the complexity of the problem
    def getComplexity(self):
        return self.complexity