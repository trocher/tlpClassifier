class Problem:

    # Creating a Problem
    # whiteConfigurations is a set of all the configurations (tuples) allowed for the white nodes
    # blackConfigurations is a set of all the configurations (tuples) allowed for the black nodes
    def __init__(self, whiteConfigurations, blackConfigurations):
        self.whiteConfigurations = whiteConfigurations
        self.blackConfigurations = blackConfigurations
        self.whiteDegree = len(whiteConfigurations)
        self.blackDegree = len(blackConfigurations)

    
    # The hash function for problems
    def __hash__(self):
        print(type(self.whiteConfigurations))
        return hash((self.whiteConfigurations,self.blackConfigurations))
        ### TODO implement hashing function

    # Equality of problem.
    def __eq__(self,other):
        return (self.whiteConfigurations == other.whiteConfigurations and self.blackConfigurations == other.blackConfigurations)

    def configurationAlphabet(self, configuration):
        alphabet = set()
        for elem in configuration:
            alphabet.update(elem)
        return alphabet

    def alphabet(self):
        return self.configurationAlphabet(self.whiteConfigurations).union(self.configurationAlphabet(self.blackConfigurations))

    def alphabetSize(self):
        return len(self.alphabet())

    def hasCommonLabels(self):
        return len(self.configurationAlphabet(self.whiteConfigurations).intersection(self.configurationAlphabet(self.blackConfigurations))) != 0