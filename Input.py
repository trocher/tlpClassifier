WHITEDEGREE = 2
BLACKDEGREE = 3


CONSTANTS = [

    # Round eliminator
    ({'AC', 'BC', 'AB'},
    {'BBC', 'CCC', 'AAA', 'BBB', 'ACC', 'AAB', 'ABC'},
    2,3),

    # Weak 2 coloring
    ({'AB', 'CC'},
    {'AAA', 'AAC', 'ACC', 'BBB', 'BBC', 'BCC'},
    2,3),

    #Maximal matching (depends on WHITEDEGREE and BLACKDEGREE)
    ({'AB', 'CC'},
    {'ABB', 'ABC', 'ACC', 'BBB'},
    2,3)

    ]

GLOBALS = [
    ({'AC', 'AB'},
    {'ABC'},
    2,3)
]

