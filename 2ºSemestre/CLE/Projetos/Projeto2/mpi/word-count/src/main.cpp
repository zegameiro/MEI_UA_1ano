#include <getopt.h>
#include <iostream>
#include <vector>
#include <string>
#include <mpi.h>
#include <chrono>
#include "word_count.h"
#include "reader.h"
#include "processor.h"
#include "types.h"

using namespace std;
using namespace std::chrono;

#define MASTER_RANK 0

static option long_options[] = {
    {"lines", no_argument, 0, 0},
    {"words", no_argument, 0, 0},
    {"chars", no_argument, 0, 0},
    {0, 0, 0, 0}};

void printResults(const vector<WordCountResult> &results);

int main(int argc, char *argv[])
{
    // Initialize MPI
    MPI_Init(&argc, &argv);

    int rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Start timing
    auto start = high_resolution_clock::now();

    WordCountFlags flags;

    while (1)
    {
        int option_index = 0;
        int c = getopt_long(argc, argv, "lwc", long_options, &option_index);
        if (c == -1)
            break;

        switch (c)
        {
        case 'l':
            flags.lines = true;
            break;
        case 'w':
            flags.words = true;
            break;
        case 'c':
            flags.chars = true;
            break;
        case '?':
            // getopt_long already printed an error message
            break;
        } // end switch
    } // end while(1)

    if (!flags.lines && !flags.words && !flags.chars)
        flags.lines = flags.words = flags.chars = true;

    // Broadcast flags to all processes
    MPI_Bcast(&flags, sizeof(WordCountFlags), MPI_BYTE, MASTER_RANK, MPI_COMM_WORLD);

    // Process files and get local results
    vector<WordCountResult> local_results = processWordCount(argc, argv, rank, world_size, flags);

    // Master process gathers and displays results
    if (rank == MASTER_RANK)
    {
        vector<WordCountResult> global_results = gatherResults(local_results, rank, world_size);

        auto end = high_resolution_clock::now();

        // Print results
        printResults(global_results);

        // Display execution time
        duration<double> duration = end - start;
        cout << "Execution Time: " << duration.count() << " seconds" << endl;
    }
    else
    {
        // Non-master processes just participate in the gather
        gatherResults(local_results, rank, world_size);
    }

    // Finalize MPI
    MPI_Finalize();
    return 0;
}

// Print the results
void printResults(const vector<WordCountResult> &results)
{
    int total_chars = 0;
    int total_lines = 0;
    int total_words = 0;

    printf("%-20s %12s %10s %10s\n", "FILENAME", "CHARS", "LINES", "WORDS");
    printf("%-20s %12s %10s %10s\n", "======================", "===========", "==========", "==========");

    for (const auto &result : results)
    {
        printf("%-20s %12d %10d %10d\n", result.filename.c_str(), result.chars, result.lines, result.words);
        total_chars += result.chars;
        total_lines += result.lines;
        total_words += result.words;
    }

    if (results.size() > 1)
    {
        printf("%-20s %12s %10s %10s\n", "======================", "===========", "==========", "==========");
        printf("%-20s %12d %10d %10d\n", "TOTAL", total_chars, total_lines, total_words);
    }
}
