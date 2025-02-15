from graph import Graph
from utils import get_all_cut_combinations, calculate_cost

class ExhaustiveSearch:

    def __init__(self, nodes, edges, counter) -> None:
        self.nodes = nodes
        self.edges = edges
        self.graph = Graph(nodes=nodes, edges=edges)
        self.counter = counter
        
        # Build the adjency matrix
        self.adjency_matrix = self.graph.build_adjency_matrix()
    
    def solve_problem(self):
        """
            Solve a problem
            - combination -> a list of nodes that are cut([1, 2, 3])
        """

        min_cost = 400
        best_sub_set_a = ""
        best_sub_set_b = ""
        counter = 0
        n_solutions = 0

        all_nodes_list = [chr(i) for i in range(97, 97 +self.graph.nodes_number)]

        self.all_combinations = get_all_cut_combinations(
            nodes=all_nodes_list
        )

        removed_edges = []

        for sub_set_a in self.all_combinations:
            counter += 1
            sub_set_b = [chr(j) for j in range(97, 97 + self.graph.nodes_number) if chr(j) not in sub_set_a]
            x = calculate_cost(conj_a=sub_set_a, conj_b=sub_set_b, connections=self.graph.edge_positions)

            if x < min_cost:
                min_cost = x
                best_sub_set_a = sub_set_a
                best_sub_set_b = sub_set_b
                removed_edges = [(u, v) for u, v in self.graph.edge_positions.keys() if (u in sub_set_a and v in sub_set_b) or (u in sub_set_b and v in sub_set_a)]
            elif x == min_cost:
                n_solutions += 1

        # Call the draw_solution_graph method to visualize the result
        self.graph.draw_graph(counter=self.counter, removed_edges=removed_edges)

        return min_cost, best_sub_set_a, best_sub_set_b, counter, n_solutions