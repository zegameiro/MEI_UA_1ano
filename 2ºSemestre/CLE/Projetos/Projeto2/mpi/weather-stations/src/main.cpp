#include <chrono>
#include "processor.h"
#include "gather.h"
#include <iostream>

using namespace std::chrono;

int main(int argc, char* argv[])
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const char* filename = "";

    if (argc < 2)
    {
        if (rank == 0) std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        MPI_Finalize();
        return 1;
    }

    if (argc > 1) filename = argv[1];

    auto start = high_resolution_clock::now();

    std::map<std::string, wsData> localMap = distributeProcessFile(filename, rank, size);

    // Root merges results and prints them
    if (rank == 0) 
    {
        std::map<std::string, wsData> globalMap = gatherResults(size, rank, localMap);
        
        auto end = high_resolution_clock::now();
        
        // Print results
        for (const auto& [city, data] : globalMap) 
        {
            printf("%s: avg=%.1f min=%.1f max=%.1f\n", city.c_str(), data.sum / data.count, data.min, data.max);
        }
        
        // Display execution time
        duration<double> duration = end - start;
        std::cout << "Execution Time: " << duration.count() << " seconds" << std::endl;
    } 
    else 
    {
        gatherResults(size, rank, localMap); // All ranks call this, not just root
    }

    MPI_Finalize();
    return 0;
}