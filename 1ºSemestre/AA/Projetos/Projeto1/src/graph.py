from collections import defaultdict

import matplotlib.pyplot as plt
import random
import networkx as nx

class Graph:

    def __init__(self, nodes, edges) -> None:
        self.nodes_number = nodes
        self.edges_number = edges

        self.node_positions = self.build_nodes(self.nodes_number)
        self.edge_positions = self.build_edges(self.edges_number)

        self.adjency_matrix = defaultdict(list)

        self.nx_graph = nx.Graph()


    def build_nodes(self, n_nodes) -> dict:
        """Generate random positions for each node, using ASCII codes for letters 'a' to 'z'"""
        index = 97 # ASCII code for the letter a
        node_positions = {}

        for i in range(n_nodes):

            position = (random.randint(1, 20), random.randint(1, 20))

            # Check if the position is already taken by another node
            while position in node_positions.values():
                position = (random.randint(1, 20), random.randint(1, 20))

            node_positions[chr(index + i)] = position

        return node_positions
    
    def build_edges(self, n_edges) -> dict:
        isConnex = False
        nodes = [chr(i) for i in range(97, 97 + self.nodes_number)]

        while(not isConnex):
            connections = {}

            for i in range(n_edges):
                # Choose randomly 2 nodes
                node_1 = random.choice(nodes)
                node_2 = random.choice(nodes)

                # Choose another node if both of them are equal
                while (node_1 == node_2):
                    node_2 = random.choice(nodes)

                # Create a tuple with 2 nodes
                edge = (node_1, node_2)
                edge = tuple(sorted(edge))

                # Don't allow more than one edge between 2 nodes
                while(edge in connections):
                    node_1 = random.choice(nodes)
                    node_2 = random.choice(nodes)

                    # Choose another node if both of them are equal
                    while (node_1 == node_2):
                        node_2 = random.choice(nodes)

                    # Create a tuple with 2 nodes
                    edge = (node_1, node_2)
                    edge = tuple(sorted(edge))

                # Calculate the distance between nodes
                distance = self.calculate_distance(node_1, node_2)

                if edge not in connections:
                    connections[edge] = distance

            # Check if the graph is connected
            isConnex = self.connex_graph(nodes, connections)

        return connections
    
    def calculate_distance(self, node_1, node_2) -> float:
        """Calculate the distance between 2 nodes"""

        x1, y1 = self.node_positions[node_1]
        x2, y2 = self.node_positions[node_2]

        return round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 2)
    
    def connex_graph(self, nodes, connections) -> bool:
        """Check if a graph is connex"""

        connection = [i for i in connections.keys()]
        out = set([item for t in connection for item in t])

        if (set(nodes).difference(set(out))):
            return False
        
        return True
    
    def build_adjency_matrix(self):
        """Build the adjency matrix associated to a graph"""

        for node1, node2 in self.edge_positions.keys():
            self.adjency_matrix[node1].append(node2)
            self.adjency_matrix[node2].append(node1) if node2 != node1 else None

        self.adjency_matrix = sorted(self.adjency_matrix.items())

        return self.adjency_matrix
    
    def draw_graph(self, counter, removed_edges=None) -> None:

        for node1, node2 in self.edge_positions.keys():
            if (node1, node2) in removed_edges or (node2, node1) in removed_edges:
                self.nx_graph.add_edge(node1, node2, weight=self.edge_positions[(node1, node2)], color='red')
            else:
                self.nx_graph.add_edge(node1, node2, weight=self.edge_positions[(node1, node2)], color='black')

        for node in self.node_positions.keys():
            self.nx_graph.add_node(node, pos=self.node_positions[node])

        edge_labels = nx.get_edge_attributes(self.nx_graph, "weight")
        pos = nx.get_node_attributes(self.nx_graph, "pos")
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels)

        # Get edge colors from attributes
        edge_colors = [self.nx_graph[u][v]['color'] for u, v in self.nx_graph.edges()]

        nx.draw(
            self.nx_graph,
            pos,
            edge_color=edge_colors,
            with_labels=True
        )

        plt.savefig(f"Graph{counter}Vertex{self.nodes_number}Edges{self.edges_number}.png", format="PNG")
        plt.close()