
import matplotlib.pyplot as plt
import random
import networkx as nx

class GraphV2:

    def __init__(self, nodes, edges, list_edges = []) -> None:
        self.nodes_number = nodes
        self.edges_number = edges

        self.nodes_list = [int(i) for i in range(self.nodes_number)]
        self.edge_weight = {}

        self.nodes_merged = {str(i): str(i) for i in range(self.nodes_number)}

        if list_edges == []:
            self.list_edges, self.adjency_list = self.build_edges

        else:
            final_list = []

            for i in list_edges:
                node1, node2 = i.split(" ")
                final_list.append(tuple(sorted((node1, node2))))

            self.list_edges = final_list
            self.adjency_list = self.build_adjency_matrix(self.list_edges)
        
        for i in self.list_edges:
            self.edge_weight[i] = random.randint(1, 15)

        self.nx_graph = nx.Graph()
    
    def build_edges(self, n_edges) -> dict:
        """Build a list of edges to create a connex graph"""
        is_connex = False

        while(not is_connex):
            edges = []
            i = 0

            while i < n_edges:
                node1 = random.randint(0, self.nodes_number - 1)
                node2 = random.randint(0, self.nodes_number - 1)
                
                # Prevent duplicated nodes
                while node1 == node2:
                    node2 = random.randint(0, self.nodes_number - 1)
                
                edge_sorted = tuple(sorted(node1, node2))

                if edge_sorted not in edges:
                    edges.append(edge_sorted)
                    i += 1
            
            is_connex, adjency_list = self.connex_graph(self.nodes_number, edges)
        
        return edges, adjency_list

    
    def connex_graph(self, nodes, connections) -> bool:
        """Check if a graph is connex"""

        adjacency_list = self.build_adjency_matrix(connections) # {0: [1, 2], 1: [1, 2, 3]}

        if len(adjacency_list) != nodes:
            return (False, None)
        
        pos_bool = [False for i in range(nodes)]
        stack = []

        stack.append("0")

        while stack:
            node = stack.pop()
            pos_bool[int(node)] = True
            neighbours = adjacency_list[node]

            [stack.append(i) for i in neighbours if not pos_bool[int(i)]]

        if pos_bool == [True for i in range(nodes)]:
            return (True, adjacency_list)
        
        else:
            return (False, None)

    
    def build_adjency_matrix(self, list_edges) -> dict:
        """Build the adjency matrix associated to a graph in a dict"""

        tmp = {}
        for edge_tuple in list_edges:
            node1, node2 = edge_tuple
            node1 = str(node1)
            node2 = str(node2)

            if node1 not in tmp:
                tmp[node1] = [node2]
            else:
                tmp[node1].append(node2)

            if node2 not in tmp:
                tmp[node2] = [node1]
            else:
                tmp[node2].append(node1)

        return tmp
    
    def draw_graph(self, filename) -> None:

        for node1, node2 in self.list_edges:
            self.nx_graph.add_edge(node1, node2, weight=self.edge_weight[(node1, node2)])

        edge_labels = nx.get_edge_attributes(self.nx_graph, "weight")

        nx.draw(
            self.nx_graph,
            with_labels=True
        )

        plt.savefig(filename)
        plt.clf()

    def merge_nodes(self, edge):
        """Merge the nodes of a edge"""

        # Remove edge from edge list
        self.list_edges.remove(edge)
        initial_node, final_node = edge

        node1 = self.nodes_merged[str(initial_node)]
        node2 = self.nodes_merged[str(final_node)]

        if node1 == node2:
            return
        
        # Get connections from each node
        starting_node = self.adjency_list[node1]
        ending_node = self.adjency_list[node2]

        # Remove the nodes that are going to be connected from the adjacency list
        for i in starting_node:
            if i == node2:
                starting_node.remove(i)

        for i in ending_node:
            if i == node1:
                ending_node.remove(i)

        all_nodes = starting_node + ending_node

        # Create a new key
        new_key = f"{str(node1)}:{str(node2)}"
        each_node = new_key.split(":")

        for i in each_node:
            if i in all_nodes:
                all_nodes.remove(i)

        # Update dict
        self.adjency_list[new_key] = all_nodes
        
        if node1 != node2:
            del self.adjency_list[node1]
        del self.adjency_list[node2]

        # Save the node and the new one that he represents
        self.update_merged_nodes(new_key)

        self.nodes_number -= 1

    def update_merged_nodes(self, new_key):
        """Update the nodes merged dictionary"""

        all_nodes = new_key.split(":")
        for i in all_nodes:
            self.nodes_merged[i] = new_key