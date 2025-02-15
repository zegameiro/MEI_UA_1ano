from graph import Graph
from utils import get_all_cut_combinations, calculate_cost

class GreedySolution:

    def __init__(self, nodes, edges, counter) -> None:
        self.nodes = nodes
        self.edges = edges
        self.counter = counter
        self.graph = Graph(nodes=nodes, edges=edges)

        # Build the adjency matrix
        self.adjency_matrix = self.graph.build_adjency_matrix()
        self.adjency_matrix = sorted(self.adjency_matrix, key=lambda x: len(x[1]))

        self.min_edges = len(self.adjency_matrix[0][1])
        

    def solve_problem(self):

        n_solutions = 0
        min_cost = 40000
        best_sub_set_a=""
        best_sub_set_b=""
        counter=0

        removed_edges = []

        for i in self.adjency_matrix:

            if len(i[1]) == self.min_edges:
                # i -> node with less edges
                # connected_nodes -> nodes connected to node i

                counter += 1
                connected_nodes = i[1]
                self.adjency_matrix.remove(i)
                self.combinations = get_all_cut_combinations(nodes=(list(connected_nodes) + list(i[0])))

                for sub_set_a in self.combinations:

                    sub_set_b = [chr(j) for j in range(97, 97 + self.graph.nodes_number) if chr(j) not in sub_set_a]

                    x = calculate_cost(conj_a=sub_set_a, conj_b=sub_set_b, connections=self.graph.edge_positions)

                    if x < min_cost:
                        min_cost = x
                        best_sub_set_a = sub_set_a
                        best_sub_set_b = sub_set_b
                        removed_edges = [(u, v) for u, v in self.graph.edge_positions.keys() if (u in sub_set_a and v in sub_set_b) or (u in sub_set_b and v in sub_set_a)]
                    elif x == min_cost:
                        n_solutions += 1

        self.graph.draw_graph(counter=self.counter, removed_edges=removed_edges)

        return min_cost, best_sub_set_a, best_sub_set_b, counter, n_solutions