WHITEDEGREE = 2
BLACKDEGREE = 3

CONSTANTS = [

    # Weak 2 coloring
    ({'AB', 'CC'},
    {'AAA', 'AAC', 'ACC', 'BBB', 'BBC', 'BCC'},
    2,3)
]


GLOBALS = [
    ({'AC', 'AB'},
    {'ABC'},
    2,3)
]
ITERATED_LOGARITHMIC = [
    #MIS
    ({'BC', 'AA'},
    {'AAB', 'ABB', 'CCC', 'BBB'},
    2,3),
    #MIS
    ({'AA', 'BC', 'AC'},
    {'CCC','AAB'},
    2,3)
]
LOGARITHMIC2 = [

    # 3 vertex coloring on latex
    ({'AB', 'AC', 'BC'},
    {'AAA','BBB','CCC'},
    2,3),

    # 3 edge coloring on latex
    ({'AA', 'BB', 'CC'},
    {'ABC'},2,3)


    # 2 partial 2 coloring
    ({'AB','CC'},
    {'AAA','BBB','AAC','BBC'},2,3)

]
LOGARITHMIC = [
    ({'AC', 'BC', 'BB', 'AA', 'AB'},
    {'ACC', 'CCC', 'BCC', 'ABC'},
    2,3),

    # R&C
    ({'BB', 'AC', 'AA', 'AB'},
    {'ABC'},
    2,3),

    #########
    # B C 
    # A A
    #
    # A A B 
    # A C ABC


    ({'BC', 'AA'},
    {'AAB', 'ACA'},
    2,3),

    ({'BC', 'AA'},
    {'AAB', 'ACB'},
    2,3),

    ({'BC', 'AA'},
    {'AAB', 'ACC'},
    2,3),
    #####
    ({'BC', 'AA'},
    {'AAB', 'BBC'},
    2,3),

    ({'BC', 'AA', 'AB'},
    {'AAC', 'BBC'},
    2,3),

    ({'BC', 'AA', 'AB'},
    {'ABB', 'AAC'},2,3),


# SOO done on latex
    ({'AC', 'BC'},
    {'ABC', 'BCC'},2,3),

# SOO done on latex
    ({'AB','BC'},
    {'AAB','BBC'},2,3),

# EO done on latex 1
    ({'AC','BC'},
    {'ABC','CCC'},2,3),

# EO done on latex 2
    ({'AC','BC'},
    {'AAA','BCC'},2,3),

# EO done on latex 2
    ({'AC','BC'},
    {'ABB','ACC'},2,3),

# EO done on latex 2
    ({'AC','BC'},
    {'ABB','BCC'},2,3)
]