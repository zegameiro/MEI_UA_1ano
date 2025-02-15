def calculate_cost(conj_a, conj_b, connections):
    """
        Calculate the cost of 2 subconjunctions
        - conj_a: list of nodes in the first subconjuction
        - conj_b: list of nodes in the second subconjunction
        - connections: dictionary with edges and their distances
    """

    cost = 0

    for node_1, node_2 in connections:
        # Look for edges that belong to both of the subconjunctions
        if (node_1 in conj_a and node_2 in conj_b) or (node_1 in conj_b and node_2 in conj_a):
            cost += connections[(node_1, node_2)]

    return cost

def get_all_cut_combinations(nodes) -> list[list]:
        """
            Get all possible combinations for a cut
            It is important to keep in mind that any subconjunction can be empty
        """

        all_combinations = [[]]
        for node in nodes:
            all_combinations += [lst + [node] for lst in all_combinations]

        # Remove empty subconjunctions and the ones with all the nodes
        all_combinations.remove([])
        all_combinations.remove(nodes)

        return all_combinations