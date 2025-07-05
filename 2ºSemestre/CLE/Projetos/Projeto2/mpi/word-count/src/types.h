#ifndef TYPES_H
#define TYPES_H

#include <mpi.h>
#include <vector>

// MPI tags
#define TAG_FILE_DATA 1
#define TAG_FILENAME 2
#define TAG_RESULT 3
#define TAG_TERMINATE 4

/**
 * Structure for word count data
 * - filename: name of the file
 * - chars: number of characters
 * - lines: number of lines
 * - words: number of words
 */
struct WordCountData {
    char filename[256];
    int chars = 0;
    int lines = 0;
    int words = 0;
};

/**
 * Function to create MPI datatype for WordCountResult
 * @return: MPI_Datatype for WordCountResult
 */
MPI_Datatype createWordCountResultType();


#endif // TYPES_H   