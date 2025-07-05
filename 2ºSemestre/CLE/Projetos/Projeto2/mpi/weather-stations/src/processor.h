#ifndef PROCESSOR_H
#define PROCESSOR_H

#include <mpi.h>
#include <map>
#include <string>
#include "types.h"


std::map<std::string, wsData> distributeProcessFile(const char* filename, int rank, int size);
char* readFileIntoBuffer(const char* filename, long& fileSize);
void computeChunksOffsets(const char* buffer, long fileSize, int size, int* sendcounts, int* displs);
char* scatterChunks(const char* buffer, int* sendcounts, int* displs, int rank, int size, int& recvcount);
void processBufferChunk(const char* chunk, int chunkSize, std::map<std::string, wsData>& wsMap);
long get_file_size(const char* filename);

#endif  // PROCESSOR_H