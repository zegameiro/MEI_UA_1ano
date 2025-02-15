from constants import STUDENT_NUMBER, EDGES_PERCENTAGE
from graph_v1 import GraphV1
from graph_v2 import GraphV2
from karger_algorithm import KargerAlgorithm

import random
import os
import time
import networkx as nx

def generate_random_graphs(graphs_number):

    random.seed(STUDENT_NUMBER)
    os.makedirs("./random_graphs", exist_ok=True)
    os.chdir("random_graphs")

    counter = 0
    all_execution_times = {}
    # key: (nodes, edges)
    # value: elapsed time in miliseconds

    for i in range(4, graphs_number + 1):

        nodes_number = i
        max_edges = (nodes_number * (nodes_number - 1)) / 2

        for j in EDGES_PERCENTAGE:
            edge_number = int(max_edges * j)

            if edge_number >= nodes_number - 1:

                f = open(f"Graph_(Nodes_{nodes_number}, Edges_{edge_number}).txt", "w")

                all_min_cut = []
                all_time = []
                all_number_operations = []

                # Execute the algorithm 10 times to have more variety
                for m in range(10):
                    random.seed(STUDENT_NUMBER)

                    # Calculate execution time
                    start = time.time()
                    counter += 1
                    print(f">> Graph {counter}(Nodes {nodes_number}, Edges {edge_number})", end="\r")

                    graph = GraphV1(nodes=nodes_number, edges=edge_number)
                    graph.draw_graph(filename=f"Graph_{i}(Nodes_{graph.nodes_number}, Edges_{graph.edges_number})_random.png")

                    karger_alg = KargerAlgorithm(graph=graph)
                    edges_cut, min_cut, number_operations = karger_alg.karger_min_cut(graph=graph)
                    all_number_operations.append(number_operations)

                    end = time.time() - start

                    all_min_cut.append(min_cut)
                    all_time.append(end)

                    f.write(
                        f">> Graph_{m}(Nodes_{nodes_number}, Edges_{edge_number}) \nCost: {min_cut}\nEdges to cut: {edges_cut}\nTime: {end}\nNumber of operations: {number_operations}\n\n"
                    )

                    # Draw the graph
                    graph.draw_graph(
                        filename=f"Graph_{m}(Nodes_{nodes_number}, Edges_{edge_number}).png"
                    )
                
                f.write(str(sum(all_time) / len(all_time)))
                f.write("\n")
                f.close()

                all_execution_times[(nodes_number, edge_number)] = str(sum(all_time) / len(all_time))

    os.chdir("..")

    return all_execution_times


def use_teachers_graphs(folder):

    os.chdir(folder) 

    # Open that files that matter to the execution
    files = [i for i in os.listdir() if i.startswith("SW") and i.endswith("G.txt") and "DG" not in i and "DAG" not in i and i not in "SWtinyG.txt" and i not in "SWlargeG.txt"]
    counter = 0

    for file in files:

        f = open(file, "r")
        
        is_direct = int(f.readline())
        exists_weight = int(f.readline())

        assert is_direct == 0
        assert exists_weight == 0

        nodes = int(f.readline())
        edges = int(f.readline())

        connections = f.readlines()
        f.close()

        temp_conn = [i.replace("\n", "") for i in connections]

        os.makedirs("solution", exist_ok=True)
        os.chdir("solution")

        f = open(f"Graph(Nodes_{nodes}, Edges_{edges}).txt", "w")

        all_min_cut = []
        all_time = []
        all_number_operations = []

        for i in range(10):
            start = time.time()
            print(f">> {counter}: {file}", end="\r")

            counter += 1
            graph = GraphV2(nodes=nodes, edges=edges, list_edges=temp_conn)

            karger_alg = KargerAlgorithm(graph=graph)
            edges_cut, min_cut, number_operations = karger_alg.karger_min_cut(graph=graph)
            all_number_operations.append(number_operations)

            end = time.time() - start

            f.write(
                f">> Graph_{i}(Nodes_{nodes}, Edges_{edges}) \nCost: {min_cut}\nEdges to cut: {edges_cut}\nTime: {end}\nNumber of operations: {number_operations}\n\n"
            )

            all_min_cut.append(min_cut)
            all_time.append(end)

        f.write(
            f"MinCut: {str(min(all_min_cut))}, time: {str(sum(all_min_cut)/len(all_time))}, number of Basic Operations: {str(sum(all_number_operations)/len(all_number_operations))}"
        )
        f.write("\n")
        f.close()
        os.chdir("..")


            