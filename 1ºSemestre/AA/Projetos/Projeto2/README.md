# Advanced Algorithms Second Project

## Randomized algorihtms for Minimum Weight Cut Problem

The minimum weight cut problem in graph theory involves finding the smallest total weight of edges that need to be removed to divide a graph into two disjoint subsets, effectively disconnecting it. Given a graph where each edge has an associated weight, the goal is to identify a partition of the vertices such that the sum of the weights of edges crossing between the two subsets is minimized. The main goal of this project is to solve this problem using randomized algorithms.

### Folder Structure

```bash
.
├── data
│   ├── README.txt
│   ├── SW10000EWD.txt
│   ├── SW1000EWD.txt
│   ├── SWlargeG.txt
│   ├── SWmediumDG.txt
│   ├── SWmediumEWD.txt
│   ├── SWmediumG.txt
│   ├── SWtinyDAG.txt
│   ├── SWtinyDG.txt
│   ├── SWtinyEWD.txt
│   └── SWtinyG.txt
├── docs
│   ├── AA_2425_Trab_2.pdf
│   ├── AA_Second_Proj_Report.pdf
│   ├── Assignments_TP1.pdf
│   ├── Assignments_TP2.pdf
│   └── Links_to_Graph_Repositories.pdf
├── LICENSE
├── README.md
├── requirements.txt
└── src
    ├── constants.py
    ├── graph_v1.py
    ├── graph_v2.py
    ├── karger_algorithm.py
    ├── main.py
    └── utils.py

4 directories, 25 files
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
python3 main.py -f <path to folder with teacher algorihtms>
```

### Authors

José Gameiro

### Grade: 16.5

