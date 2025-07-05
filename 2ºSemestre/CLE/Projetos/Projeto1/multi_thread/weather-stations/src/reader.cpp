/*
 * reader.cpp
 *   - Implements file reading and processing
*/

#include "reader.h"
#include <sys/stat.h>    // For file size
#include <sys/mman.h>    // For mmap
#include <fcntl.h>       // open
#include <unistd.h>      // close

size_t getFileSize(const char* filename)
{
    struct stat st;
    if (stat(filename, &st) != 0)
    {
        std::cerr << "Error getting file size: " << filename << std::endl;
        return 0;
    }

    return st.st_size;
}

size_t findNextNewLine(const char* data, size_t start, size_t size)
{
    while(start < size && data[start] != '\n')
    {
        start++;
    }

    return (start < size) ? start + 1 : size;
}

void processFile(ThreadPool& pool, int numThreads, const char* filename) 
{
    size_t fileSize = getFileSize(filename);
    if (fileSize == 0) return;

    std::cout << "Processing file: " << filename << " (" << fileSize << " bytes)" << std::endl;

    int fd = open(filename, O_RDONLY);
    if (fd < 0)
    {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    char* data = (char*)mmap(nullptr, fileSize, PROT_READ, MAP_PRIVATE | MAP_POPULATE, fd, 0);
    if (data == MAP_FAILED)
    {
        std::cerr << "Error mapping file: " << filename << std::endl;
        close(fd);
        return;
    }

    size_t chunkSize = fileSize / numThreads;
    size_t chunkStarts[numThreads];

    // Calculate the start of each chunk
    for (int i = 0; i < numThreads; ++i)
    {
        chunkStarts[i] = (i == 0) ? 0 : findNextNewLine(data, i * chunkSize, fileSize);
    }

    std::unordered_map<std::string, wsData> localMaps[numThreads];

    // Assign chunks to threads
    for (int i = 0; i < numThreads; ++i)
    {
        size_t start = chunkStarts[i];
        size_t end = (i == numThreads - 1) ? fileSize : chunkStarts[i + 1];

        if (start >= end) continue; // avoid empty chunks

        pool.enqueue([data, start, end, &localMaps, i]() {
            std::string_view chunk(data + start, end - start);
            processBatch(chunk, localMaps[i]);  // Pass local map
        });
    }

    pool.wait(); // Ensure all tasks are complete

    munmap(data, fileSize);
    close(fd);

    // Merge local maps into global map (single lock)
    {
        std::lock_guard<std::mutex> lock(dataMutex);
        for (int i = 0; i < numThreads; ++i) {
            for (auto& [city, data] : localMaps[i]) {
                auto& globalData = wsMap[city];
                globalData.sum += data.sum;
                globalData.count += data.count;
                globalData.max = std::max(data.max, globalData.max);
                globalData.min = std::min(data.min, globalData.min);
            }
        }
    }
}
