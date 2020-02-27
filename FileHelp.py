

def add_degree_suffix(name, white_degree, black_degree):
    suffix = "_" + str(white_degree) + "_" + str(black_degree)
    return name + suffix

def data_name(white_degree,black_degree):
    return add_degree_suffix("data/problemSet",white_degree,black_degree)


# Store a given set of problems in a file
# name, a string, the name of the file
# that, the set of problems
def problems_to_file(name, that):
    f= open(name,"w+")
    for elem in that:
        elem.write_in_file(f)
    f.close()
