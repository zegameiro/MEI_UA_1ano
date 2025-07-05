/*
 * reader.h
 *   - Header file defining reading and processing function for a file
*/

#ifndef READER_H
#define READER_H

#include <queue>
#include <string>
#include <fstream>
#include <iostream>

#include <thread_pool.h>
#include <processor.h>

size_t getFileSize(const char* filename);
size_t findNextNewLine(const char* data, size_t start, size_t size);
void processFile(ThreadPool& pool, int numThreads, const char* filename);

#endif  // READER_H