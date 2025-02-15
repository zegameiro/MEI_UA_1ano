from getopt import GetoptError, getopt
from constants import GRAPHS
from utils import generate_random_graphs, use_teachers_graphs

import sys

def main(argv):

    folder = ""

    try:
        opts, args = getopt(argv, "hf:", ["folder="])
    except GetoptError:
        print("main.py -f <path_to_folder>")
        sys.exit(2)

    for opt, arg in opts:

        if opt == "-h":
            print("main.py -f <path_to_folder>")
            sys.exit()
        
        elif opt in ("-f", "--folder"):
            folder = arg

    if folder != "":
        use_teachers_graphs(folder)
    else:
        execution_times = generate_random_graphs(GRAPHS)
        print(execution_times)

if __name__ == '__main__':
    main(sys.argv[1:])


