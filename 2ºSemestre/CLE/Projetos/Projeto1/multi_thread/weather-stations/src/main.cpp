/*
 * main.cpp
 *   - Entry point for the weather station processing program
 *   - Reads the input file, distributes processing accross threads, and prints the results
*/

#include <fstream>
#include <chrono>

#include <thread_pool.h>
#include <processor.h>
#include <reader.h>

using namespace std::chrono;

// Global data structure to store weather station data
std::mutex dataMutex;
std::map<std::string, wsData> wsMap;

int main(int argc, char* argv[])
{
    const char* filename = "";
    int numThreads = std::thread::hardware_concurrency(); // Default to number of hardware threads
    
    // The samples file is a required argument
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <filename: required> [numThreads: optional]" << std::endl;
        return 1;
    }

    // Parse command line arguments
    if (argc > 1) filename = argv[1];
    if (argc > 2) numThreads = std::stoi(argv[2]);

    // Initialize the thread pool
    ThreadPool pool(numThreads);

    auto start = high_resolution_clock::now();

    // Process the file using multiple threads
    processFile(pool, numThreads, filename);

    auto end = high_resolution_clock::now();

    // Print results
    for (const auto& [city, data] : wsMap) 
    {
        printf("%s: avg=%.1f min=%.1f max=%.1f\n", city.c_str(), data.sum / data.count, data.min, data.max);
    }

    // Display execution time
    duration<double> duration = end - start;
    std::cout << "Execution Time: " << duration.count() << "seconds" << std::endl;

    return 0;
}