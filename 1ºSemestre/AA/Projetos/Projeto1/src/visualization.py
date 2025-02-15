import matplotlib.pyplot as plt
import os
import math
import numpy as np

greedy_directory = "./time_greedy_information"
exhaustive_directory = "./time_exhaustive_information"


def get_execution_time(directory):

    times = []
    nodes = []

    for filename in os.listdir(directory):

        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                for line in file:
                    if "Elapsed Time" in line:
                        time_str = line.split(":")[1].strip().replace("s", "")
                        print(time_str)
                        elapsed_time = float(time_str)
                        elapsed_time = math.log2(elapsed_time)
                        times.append(elapsed_time)

                    if "Nodes" in line:
                        node_str = line.replace(" ", "").split("_")[0].strip()
                        node_number = int(node_str)
                        nodes.append(node_number)

    times.sort()
    nodes.sort()

    times = np.array(times)
    nodes = np.array(nodes)

    return nodes, times

nodes, execution_time_greedy = get_execution_time(greedy_directory)
another_nodes, execution_time_exhaustive = get_execution_time(exhaustive_directory)

print(execution_time_exhaustive)
print(execution_time_greedy)

# Plot each line
plt.plot(nodes, execution_time_greedy, label="Greedy Algorithm", color="blue")  # Line 1
plt.plot(nodes, execution_time_exhaustive, label="Exhaustive Algorithm", color="orange")  # Line 2

# Add labels to the axes
plt.xlabel("Number of nodes")
plt.ylabel("Log2 for the execution time in seconds")

# Add a title
plt.title("Number of operations")

# Display legend
plt.legend()

plt.grid()

plt.savefig('output_plot.png')  # Saves to 'output_plot.png' in your current directory
plt.close()

n = 40
ns = [i for i in range(1, n + 1)]
exec_t_g = []
exec_t_e = []

def exec_time_exhaustive(nodes):
    return (nodes * (2 ** nodes) / 20 * (2 ** 20)) * 145

def exec_time_greedy(nodes):
    print(nodes)
    return (nodes * (math.log10(nodes)) / 20 * (math.log10(20))) * 0.2

for nod in ns:
    t1 = exec_time_exhaustive(nodes=nod)
    t2 = exec_time_greedy(nodes=nod)

    exec_t_g.append(t2)
    exec_t_e.append(t1)

plt.plot(ns, exec_t_g, label="Greedy Algorithm", color="blue")  # Line 1
plt.plot(ns, exec_t_e, label="Exhaustive Algorithm", color="orange")  # Line 2

# Add labels to the axes
plt.xlabel("Number of nodes")
plt.ylabel("Log2 for the execution time in seconds")

# Add a title
plt.title("Execution time")

# Display legend
plt.legend()

plt.grid()

plt.savefig('output_plot2.png')  # Saves to 'output_plot.png' in your current directory