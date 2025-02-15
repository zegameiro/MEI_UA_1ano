# Advanced Algorithms First Project

## Minimum Weight Cut Problem

### Description

The Minimum Weighted Cut problem is a fundamental challenge in graph theory, focusing on partitioning the vertices of an undirected graph in a way that minimises the sum of edge weights crossing the partition. Formally, given a graph G(V, E) with a set of vertices V and edges E, where each edge has an associated weight, the goal is to split the vertices into two disjoint subsets, S and T, such that every vertex in V is assigned to one of these subsets. The objective is to ensure that the total weight of edges connecting vertices in S to vertices in T is as low as possible, yielding a "cut" with minimal weight.


### Folder structure

```bash
.
├── docs
│   └── AA_First_Project_Report.pdf
├── README.md
├── requirements.txt
└── src
    ├── constants.py
    ├── exhaustive_search.py
    ├── graph.py
    ├── greedy_solution.py
    ├── main.py
    ├── time_exhaustive_information
    ├── time_greedy_information
    └── utils.py
```

### How to execute

1. Open a terminal in the the root directory of the project and create a virtual environment using this command:

```bash
python3 -m venv venv
```

2. Activate the created virtual environment:

```bash
source venv/bin/activate
```

3. Install the necessary requirements:

```bash
pip install -r requirements.txt
```

4. Navigate to the src directory

```bash
cd src/
```

5. Run the __main.py__ file with the following options:

```bash
python3 main.py -m <greedy/exhaustive> -n <max number of nodes>
```

__NOTE:__ The argument ```-n``` isn't required so if not passed the default value will be 16 now the -m is required.

### Authors

José Gameiro

### Grade: 16.5

