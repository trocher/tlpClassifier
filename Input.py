WHITEDEGREE = 2
BLACKDEGREE = 3

ITERATED_LOGARITHMIC = [
    #MIS
    ({'BC', 'AA'},
    {'AAB', 'ABB', 'CCC', 'BBB'},
    2,3),
    #MIS
    ({'AA', 'BC', 'AC'},
    {'CCC','AAB'},
    2,3),

    ({'AA', 'BC', 'CC'},
    {'AAC','BBB','ABB'},
    2,3)
]

LOGARITHMIC2 = [

    # 3 vertex coloring on latex
    ({'AB', 'AC', 'BC'},
    {'AAA','BBB','CCC'},
    2,3),

    # 3 edge coloring on latex
    ({'AA', 'BB', 'CC'},
    {'ABC'},2,3),


    # 2 partial 2 coloring
    ({'AB','CC'},
    {'AAA','BBB','AAC','BBC'},2,3)

]
LOGARITHMIC = [
    #########
    # A B 
    # C C
    #
    # C C B 
    # A C ABC


    ({'AB', 'CC'},
    {'CCB', 'ACC'},
    2,3),

    #####
    ({'AB', 'CC'},
    {'BCC', 'ABB'},
    2,3),


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
    {'ABB','BCC'},2,3),

# R&C
    ({'AB','CC'},
    {'ABC'},2,3),

# R&C
    ({'AB','CC'},
    {'AAB','BBC'},2,3),

# R&C
    ({'AB','CC'},
    {'AAC','BBC'},2,3),

# R&C
    ({'AB','CC'},
    {'AAB','BCC'},2,3),

# R&C
    ({'AB','CC'},
    {'BCC','AAA'},2,3),

# R&C
    ({'AB','CC'},
    {'BBC','AAA'},2,3)

]

LOGARITHMIC_LOWER_BOUND = [
# fixed point 1
    ({'AC', 'BB', 'CC', 'AA', 'BC'},
    {'AAB','ABC','ABB'},2,3),

# fixed point 1
    ({'AC', 'AB', 'CC', 'BC'},
    {'AAA','BBC','BBB','ABB'},2,3),

# fixed point 2
    ({'BB', 'CC', 'AA'},
    {'BCC','BBC','AAC','AAB'},2,3),

# fixed point 2
    ({'BB', 'CC', 'AA'},
    {'BCC','AAC','ABB'},2,3),

# fixed point 2
    ({'AB', 'CC'},
    {'ABB','AAA','BBB','BCC','ACC'},2,3),
    
# fixed point 2
    ({'AB', 'CC'},
    {'AAB','AAA','BBB','BCC','AAC'},2,3),

# fixed point 2
    ({'CC', 'BC', 'AA'},
    {'BBC','AAB','BBB','AAC','BCC'},2,3),

# fixed point 2.5
    ({'AB', 'CC'},
    {'AAC','BBC','BBB','ABB'},2,3),

# fixed point auto
    ({'AB', 'CC'},
    {'BCC','AAC','ABB'},2,3),

# fixed point auto
    ({'AB', 'CC'},
    {'BCC','AAA','ABC'},2,3),

# fixed point auto
    ({'AB', 'CC'},
    {'BBC','AAA','ABC'},2,3),


# fixed point auto
    ({'AB', 'CC'},
    {'BCC','BBC','AAA'},2,3),


# fixed point auto
    ({'AB', 'CC'},
    {'AAA','BBB','ABC'},2,3),

# fixed point auto
    ({'AB', 'CC'},
    {'BCC','BBC','AAA','ABC'},2,3)
]