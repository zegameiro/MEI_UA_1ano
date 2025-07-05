# CLE - Practical Assignment Template

The goal of this assignment is convert the weather-stations and word-count exercises, for which you have previously developed single-threaded solutions, into distributed-memory applications using MPI (Message Passing Interface).

Your solution should be implemented in C++ using MPI (e.g., MPICH), and must support execution across multiple processes.

## Grade: 14.50

## Requirements

1. **Distributed** Task Pool:
    • Implement a task distribution strategy using MPI.
    • Each MPI process should independently process a portion of the input data.
    • Ensure that all results are gathered correctly at the master process (rank 0).
2. Weather-Stations **Output Sorting**:
    • Each process processes a subset of the input stations and computes local maxima.
    • Gather all local maxima at the root process.
    • Sort the consolidated results based on maximum temperature using MPI collective or local sort on the root.
3. **Validation** and **Performance** Evaluation:
    • Ensure output correctness compared to the single-threaded version.
    • Measure and compare execution time between single-threaded and MPI versions.
    • Calculate speedup and efficiency to evaluate scalability.

## Repository Structure

The repository has the following structure:

```bash
mpi/
├── weather-stations/
├── word-count/
single_thread/
├── weather-stations/
├── word-count/
```

The `mpi` directory contains the solutions with the MPI implementation for the weather-stations and word-count exercises. The `single_thread` directory contains the single-threaded solutions for the same exercises.
Inside each exercise directory, there is a `README.md` file with instructions on how to build and execute the program. The `README.md` files that are inside the mpi solutions have a detailed explanation of the solution implemented and some experiments that were conducted.

## Exercises
| [Weather Stations](mpi/weather-stations/README.md) | [Word Count](mpi/word-count/README.md) |
| --- | --- |

## Authors

- [Daniel Madureira](https://github.com/Dan1m4D)
- [José Gameiro](https://github.com/zegameiro)