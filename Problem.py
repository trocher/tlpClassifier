from Complexity import Complexity
from enum import Enum

class Configurations(Enum):
    White = 0
    Black = 1 


class Problem:

    # Creating a Problem
    # whiteConfigurations is a set of all the configurations (tuples) allowed for the white nodes
    # blackConfigurations is a set of all the configurations (tuples) allowed for the black nodes
    def __init__(self, whiteConfigurations, blackConfigurations):
        self.whiteConfigurations = frozenset(whiteConfigurations)
        self.blackConfigurations = frozenset(blackConfigurations)
        self.whiteDegree = len(list(whiteConfigurations)[0])
        self.blackDegree = len(list(blackConfigurations)[0])
        self.lowerbound = Complexity.Constant
        self.upperbound = Complexity.Unsolvable
    # The hash function for problems
    def __hash__(self):
        return hash((self.whiteConfigurations,self.blackConfigurations))
        ### TODO implement hashing function

    # Equality of problem.
    def __eq__(self,other):
        return (self.whiteConfigurations == other.whiteConfigurations and self.blackConfigurations == other.blackConfigurations)

    def show(self):
        print("====================================================================")
        print("W degree =", self.whiteDegree, "| B degree =", self.blackDegree, "| Alphabet :", self.alphabet())
        print("White Config : ", self.whiteConfigurations)
        print("Black Config : ", self.blackConfigurations)
        
    def configurationAlphabet(self, configuration):
        alphabet = set()
        config = self.blackConfigurations if configuration == Configurations.Black else self.whiteConfigurations
        for elem in config:
            alphabet.update(elem)
        return alphabet

    def configurationSize(self, configuration):
        return len(self.blackConfigurations if configuration == Configurations.Black else self.whiteConfigurations)

    def alphabet(self):
        return self.configurationAlphabet(Configurations.White).union(self.configurationAlphabet(Configurations.Black))

    def alphabetSize(self):
        return len(self.alphabet())

    def hasCommonLabels(self):
        return len(self.configurationAlphabet(Configurations.White).intersection(self.configurationAlphabet(Configurations.Black))) != 0

    def isRestriction(self, other):
        return self.whiteConfigurations.issubset(other.whiteConfigurations) and self.blackConfigurations.issubset(other.blackConfigurations)
   
    def isRelaxation(self, other):
        return other.isRestriction(self)

    def setLowerBound(self,complexity):
        self.lowerbound = complexity

    def setUpperBound(self,complexity):
        self.upperbound = complexity

    def setComplexity(self,complexity):
        self.setLowerBound(complexity)
        self.setUpperBound(complexity)

    def getComplexity(self):
        if self.lowerbound == self.upperbound:
            return self.lowerbound