from getopt import GetoptError, getopt

from constants import STUDENT_NUMBER, EDGES_PERCENTAGE
from greedy_solution import GreedySolution
from exhaustive_search import ExhaustiveSearch

import sys
import random
import os
import time

def main(argv):

    mode = ''
    nodes = 16

    try:
        opts, args = getopt(argv, "hm:n:", ["mode=", "nodes="])
    except GetoptError:
        print('python3 main.py -m [GREEDY/EXHAUSTIVE] -n [MAX NODES NUMBER]')
        sys.exit(2)

    for opt, arg in opts:

        print(f"{opt} - {arg}")

        if opt in ("-m", "--mode"):
            mode = arg

        elif opt in ("-n", "--nodes"):
            nodes = int(arg)

        else:
            print('python3 main.py -m [GREEDY/EXHAUSTIVE] -n [MAX NODES NUMBER]')
            sys.exit()

    return mode, nodes

def solve_problem_write_to_file(counter, number_nodes, number_edges, start_time, is_greedy):

    file = open(f"Graph_{str(counter)}__Vertex_{str(number_nodes)}__Edges_{str(number_edges)}.txt", "w")

    print(f">>> Graph({number_nodes}_Nodes, {number_edges}_Edges)", end="\r")
    file.write(f"{number_nodes}_Nodes {number_edges}_Edges\n")

    prob = GreedySolution(nodes=number_nodes, edges=number_edges, counter=counter) if is_greedy else ExhaustiveSearch(nodes=number_nodes, edges=number_edges, counter=counter)

    solution, sub_set_a, sub_set_b, basic_operations, n_solutions = prob.solve_problem()

    end_time = time.time()

    file.write(f"Cost: {solution}\n")
    file.write(f"Sub Set A: {sub_set_a}\n")
    file.write(f"Sub Set B: {sub_set_b}\n")
    file.write(f"Adjency Matrix: {prob.graph.adjency_matrix}\n")
    file.write(f"Elapsed Time: {end_time - start_time}s\n")
    file.write(f"Basic Operations: {basic_operations}\n")
    file.write(f"Number of Solutions: {n_solutions}\n")

    file.close()

def exaustive_or_greedy_search(nodes_number, is_greedy):
    
    directory = "time_greedy_information" if is_greedy else "time_exhaustive_information"

    os.makedirs(directory, exist_ok=True)
    os.chdir(directory)

    counter = 0

    for i in range(4, nodes_number):

        number_nodes = i
        max_edges = (number_nodes * (number_nodes - 1)) / 2

        for j in EDGES_PERCENTAGE:

            number_edges = round(max_edges * j)

            if number_edges >= number_nodes - 1:

                counter += 1

                solve_problem_write_to_file(
                    counter=counter,
                    number_nodes=number_nodes,
                    number_edges=number_edges,
                    start_time=start_time,
                    is_greedy=is_greedy
                )
    os.chdir("../")


if __name__ == '__main__':

    mode, nodes_number = main(sys.argv[1:])

    random.seed(STUDENT_NUMBER)
    start_time = time.time()

    if mode.lower() == 'exhaustive':
        print("-------- Exhaustive Solution --------")
        exaustive_or_greedy_search(nodes_number=nodes_number, is_greedy=False)

    elif mode.lower() == 'greedy':
        print("-------- Greedy Solution --------")
        exaustive_or_greedy_search(nodes_number=nodes_number, is_greedy=True)


