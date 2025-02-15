import matplotlib.pyplot as plt
import random
import networkx as nx


class GraphV1:

    def __init__(self, nodes, edges) -> None:
        self.nodes_number = nodes
        self.edges_number = edges

        self.nodes_merged = {str(i): str(i) for i in range(self.nodes_number)}

        self.node_positions = self.build_nodes(nodes)
        self.edge_weight = self.build_edges(edges)

        self.adjency_list = self.build_adjency_list(self.edge_weight.keys())
        self.list_edges = list(self.edge_weight.keys())

        self.nx_graph = nx.Graph()


    def build_nodes(self, n_nodes):
        """Generate random positions for each node, using ASCII codes for letters 'a' to 'z'"""

        node_positions = {}

        for i in range(n_nodes):
            node_positions[str(i)] = (random.randint(1, 20), random.randint(1, 20))

        return node_positions
    
    def build_edges(self, n_edges) -> dict:
        isConnex = False
        nodes = [str(i) for i in range(self.nodes_number)]

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
                distance = self.calculate_distance(node_1=node_1, node_2=node_2)

                if edge not in connections:
                    connections[edge] = [distance]

            # Check if the graph is connected
            isConnex = self.connex_graph(nodes, connections)

        return connections
    
    def calculate_distance(self, node_1, node_2) -> float:
        """Calculate the distance between 2 nodes"""

        x1, y1 = self.node_positions[node_1]
        x2, y2 = self.node_positions[node_2]

        return round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5, 2)
    
    def connex_graph(self, nodes, connections) -> bool:
        """Check if a graph is connex"""

        connection = [i for i in connections.keys()]
        out = set([item for t in connection for item in t])

        if (set(nodes).difference(set(out))):
            return False
        
        return True
    
    def build_adjency_list(self, list_edges) -> dict:
        """Build the adjency list associated to a graph in a dict"""

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
    
    def draw_graph(self, filename) -> None:

        for node1, node2 in self.edge_weight.keys():
            self.nx_graph.add_edge(node1, node2, weight=self.edge_weight[(node1, node2)][0])

        for node in self.node_positions.keys():
            self.nx_graph.add_node(node, pos=self.node_positions[node])

        edge_labels = nx.get_edge_attributes(self.nx_graph, "weight")
        pos = nx.get_node_attributes(self.nx_graph, "pos")
        
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels)

        nx.draw(
            self.nx_graph,
            pos,
            with_labels=True
        )

        plt.savefig(filename, format="PNG")
        plt.close()