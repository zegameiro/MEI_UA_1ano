# CLE - First Practical Assignment

The goal of this assignment is convert the weather-stations and word-count exercices, for which you have developed single-threaded solutions, into multi-threaded applications running on Linux/Unix.

Your solution should be implemented in C++ using std::thread from the C++ Standard Library to create and manage threads. Ensure proper synchronization where necessary (e.g., using mutexes or condition variables) to avoid race conditions.

## Grade: 16.75

## Requirements

1. You must create a thread pool with a fixed number of workers. The pool should allow enqueuing an arbitrary number of tasks and provide the capability to wait until all tasks have been completed. The number of workers is an input argument.

2. Groups of three members are required to implement a multi-threaded solution to sort the output of the weather-stations result based on the maximum temperature.

3. Ensure that your implementation is properly validated:
    - Verify correctness: Confirm that the multi-threaded implementation produces results identical to the single-threaded version.
    - Compare execution time: Measure and compare the runtime of both the single-threaded and multi-threaded implementations.
    - Evaluate performance improvements: Calculate speedup and efficiency to assess the benefits of parallelization.

## Repository Structure

The repository has the following structure:

```bash
multi_thread/
├── weather-stations/
├── word-count/
single_thread/
├── weather-stations/
├── word-count/
```

The `multi_thread` directory contains the multi-threaded solutions for the weather-stations and word-count exercises. The `single_thread` directory contains the single-threaded solutions for the same exercises.
Inside each exercise directory, there is a `README.md` file with instructions on how to build and execute the program. The `README.md` files that are inside the multi-threaded solutions have a detailed explanation of the solution implemented and some experiments that were conducted.

## Exercises
| [Weather Stations](multi_thread/weather-stations/README.md) | [Word Count](multi_thread/word-count/README.md) |
| --- | --- |

## Authors

- [Daniel Madureira](https://github.com/Dan1m4D)
- [José Gameiro](https://github.com/zegameiro)