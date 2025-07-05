#ifndef PROCESSOR_H
#define PROCESSOR_H

#include <vector>
#include <string>
#include "types.h"

#define MASTER_RANK 0

/**
 * Processes the word count for the given files.
 * 
 * @param argc The number of command line arguments.
 * @param argv The command line arguments.
 * @param rank The rank of the current process.
 * @param world_size The total number of processes.
 * @param flags The flags indicating which counts to perform (lines, words, chars).
 * @return A vector of WordCountResult containing the results for each file.
 */
std::vector<WordCountResult> processWordCount(int argc, char *argv[], int rank, int world_size, const WordCountFlags &flags);

/**
 * Reads the list of files from command line arguments.
 * 
 * @param argc The number of command line arguments.
 * @param argv The command line arguments.
 * @param total_files A reference to an integer to store the total number of files.
 * @return A vector of strings containing the file names.
 */
std::vector<std::string> readFileList(int argc, char *argv[], int &total_files);

/**
 * Distributes the file names among the processes.
 * 
 * @param all_filenames The array of all file names.
 * @param my_filenames The array to store the file names for this process.
 * @param total_files The total number of files.
 * @param chunk_size The number of files to distribute to each process.
 * @param rank The rank of the current process.
 * @param sendcounts The array containing the number of files each process will receive.
 * @param displacements The array containing the starting index for each process.
 */
void scatterFilenames(char **all_filenames, char **my_filenames, int total_files, int chunk_size, int rank, int *sendcounts, int *displacements);

/**
 * Distributes the files among the processes.
 * 
 * @param files The vector of all file names.
 * @param total_files The total number of files.
 * @param rank The rank of the current process.
 * @param world_size The total number of processes.
 * @param sendcounts The array containing the number of files each process will receive.
 * @param displacements The array containing the starting index for each process.
 * @return A vector of strings containing the file names for this process.
 */
std::vector<std::string> distributeFiles(const std::vector<std::string> &files, int total_files, int rank, int world_size, int *sendcounts, int *displacements);

/**
 * Processes the files assigned to this rank.
 * 
 * @param my_files The vector of file names for this process.
 * @param flags The flags indicating which counts to perform (lines, words, chars).
 * @return A vector of WordCountResult containing the results for each file.
 */
std::vector<WordCountResult> processFiles(const std::vector<std::string> &my_files, const WordCountFlags &flags);

/**
 * Gathers the results from all processes.
 * 
 * @param local_results The vector of local results for this process.
 * @param rank The rank of the current process.
 * @param world_size The total number of processes.
 * @return A vector of WordCountResult containing the combined results from all processes.
 */
std::vector<WordCountResult> gatherResults(const std::vector<WordCountResult> &local_results, int rank, int world_size);

#endif // PROCESSOR_H