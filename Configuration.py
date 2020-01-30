class Configuration:

    def __init__(self, configuration):
        self.configuration = configuration

    def __hash__(self):
        return True
        ### TODO implement hashing function