#include "processor.h"
#include <iostream>
#include <fstream>
#include <cstring>
#include <sstream>

/**
 * Function to get the size of a file.
 * @param filename: The name of the file.
 * @return: The size of the file in bytes.
 */
long get_file_size(const char* filename)
{
    std::ifstream file(filename, std::ios::ate | std::ios::binary);
    if (!file.is_open())
    {
        std::cerr << "Error opening file: " << filename << std::endl;
        return -1;
    }
    return file.tellg();
}

/**
 * Function to read a file into a buffer.
 * @param filename: The name of the file.
 * @param fileSize: The size of the file.
 * @return: A pointer to the buffer containing the file data.
 */
char* readFileIntoBuffer(const char* filename, long& fileSize)
{
    fileSize = get_file_size(filename);
    if (fileSize <= 0) return nullptr;

    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) return nullptr;

    char* buffer = new char[fileSize];
    file.read(buffer, fileSize);
    file.close();

    return buffer;
}

/**
 * Function to compute the offsets and sizes of chunks for each process.
 * @param buffer: The buffer containing the file data.
 * @param fileSize: The size of the file.
 * @param size: The total number of processes.
 * @param sendcounts: Array to store the size of each chunk.
 * @param displs: Array to store the starting offset of each chunk.
 */
void computeChunksOffsets(const char* buffer, long fileSize, int size, int* sendcounts, int* displs)
{
    long chunkSize = fileSize / size;
    long start = 0;;

    for (int i = 0; i < size; ++i)
    {
        displs[i] = start;
        long end = (i == size - 1) ? fileSize : start + chunkSize;

        // Snap to next newline
        while (end < fileSize && buffer[end] != '\n') ++end;

        sendcounts[i] = end - start;
        start = end + 1;
    }
}

/**
 * Function to scatter chunks of data to each process.
 * @param buffer: The buffer containing the file data.
 * @param sendcounts: Array containing the size of each chunk.
 * @param displs: Array containing the starting offset of each chunk.
 * @param rank: The rank of the current process.
 * @param size: The total number of processes.
 * @param recvcount: Reference to store the size of the received chunk.
 * @return: A pointer to the buffer containing the received chunk.
 */
char* scatterChunks(const char* buffer, int* sendcounts, int* displs, int rank, int size, int& recvcount)
{
    MPI_Scatter(sendcounts, 1, MPI_INT, &recvcount, 1, MPI_INT, 0, MPI_COMM_WORLD);

    char* recvBuffer = new char[recvcount + 1];
    MPI_Scatterv(buffer, sendcounts, displs, MPI_CHAR, recvBuffer, recvcount, MPI_CHAR, 0, MPI_COMM_WORLD);
    recvBuffer[recvcount] = '\0'; // Null-terminate the string

    return recvBuffer;
}

/**
 * Function to process a chunk of data and update the weather station map.
 * @param chunk: The chunk of data to process.
 * @param chunkSize: The size of the chunk.
 * @param wsMap: The map to update with weather station data.
 */
void processBufferChunk(const char* chunk, int chunkSize, std::map<std::string, wsData>& wsMap)
{
    std::istringstream stream(std::string(chunk, chunkSize));
    std::string line;

    while (std::getline(stream, line))
    {
        size_t pos = line.find(';');
        if (pos == std::string::npos) continue; // Skip invalid lines

        std::string city = line.substr(0, pos);
        float temp = std::stof(line.substr(pos + 1));
        auto& data = wsMap[city];
        data.sum += temp;
        data.count++;
        data.max = std::max(data.max, temp);
        data.min = std::min(data.min, temp);
    }
}

/**
 * Function to distribute the file processing across multiple processes.
 * @param filename: The name of the file to process.
 * @param rank: The rank of the current process.
 * @param size: The total number of processes.
 * @return: A map containing the processed weather station data.
 */
std::map<std::string, wsData> distributeProcessFile(const char* filename, int rank, int size)
{
    std::map<std::string, wsData> wsMap;
    char* buffer = nullptr;
    int* sendcounts = nullptr;
    int* displs = nullptr;
    long fileSize = 0;

    if (rank == 0)
    {
        buffer = readFileIntoBuffer(filename, fileSize);
        sendcounts = new int[size];
        displs = new int[size];
        computeChunksOffsets(buffer, fileSize, size, sendcounts, displs);
    }

    int recvcount = 0;
    char* chunk = scatterChunks(buffer, sendcounts, displs, rank, size, recvcount);
    processBufferChunk(chunk, recvcount, wsMap);

    delete[] chunk;
    if (rank == 0)
    {
        delete[] buffer;
        delete[] sendcounts;
        delete[] displs;
    }
    return wsMap;
}