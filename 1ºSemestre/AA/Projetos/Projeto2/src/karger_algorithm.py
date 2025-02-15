import random
import time

class KargerAlgorithm:

    def __init__(self, graph) -> None:
        self.graph = graph

    def karger_min_cut(self, graph):
        """Find the minimum cut of a graph using the Karger Algorithm"""

        n_basic_operations = 0

        while graph.nodes_number > 2:
            n_basic_operations += 1
            
            # Choose a random edge
            try:
                random.seed(time.time())
                edge = random.choice(graph.list_edges)
            except:
                break

            # Merge the nodes of the edge
            graph.merge_nodes(edge)
        
        cost = 0

        for i in graph.list_edges:

            if type(graph.edge_weight[i]) == list:
                cost += graph.edge_weight[i][0]
                
            else:
                cost += graph.edge_weight[i]

        return graph.list_edges, cost, n_basic_operations