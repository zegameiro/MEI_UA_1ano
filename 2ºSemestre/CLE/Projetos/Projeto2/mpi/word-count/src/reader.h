#ifndef READER_H
#define READER_H

#include <cstddef>  // for size_t
#include <string>
#include <vector>

using namespace std;

/**
 * Function to get the size of a file
 * @param filename: name of the file
 * @return: size of the file in bytes
 */
size_t getFileSize(const char* filename);

/**
 * Function to read a file into a buffer
 * @param filename: name of the file
 * @return: pointer to the buffer containing the file content
 */
char* readFileToBuffer(const char* filename);

/**
 * Function to read a list of files from command line arguments
 * @param argc: number of command line arguments
 * @param argv: array of command line arguments
 * @param total_files: reference to store the total number of files read
 * @return: vector of strings containing the file names
 */
vector<string> readFileList(int argc, char* argv[], int& total_files);

#endif // READER_H