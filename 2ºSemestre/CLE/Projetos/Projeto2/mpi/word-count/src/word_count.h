#pragma once

#include <vector>
#include <string>

using namespace std;

/**
 * Structure to hold flags for word count options
 * - lines: count the number of new lines
 * - words: count the total number of words
 * - chars: count the total number of characters
 */
struct WordCountFlags {
    bool lines = false; // count the number of new lines
    bool words = false; // count the total number of words
    bool chars = false; // count the number of total characters
};


/**
 * Structure to hold the result of word count
 * - filename: name of the file
 * - chars: number of characters
 * - lines: number of lines
 * - words: number of words
 */
struct WordCountResult {
    std::string filename;
    int chars = 0;
    int lines = 0;
    int words = 0;
};

/**
 * Function to perform word count on a buffer
 * @param flags: flags for word count options
 * @param buffer: pointer to the buffer containing the file content
 * @param size: size of the buffer
 * @param filename: name of the file
 * @return: WordCountResult structure containing the result
 */
WordCountResult word_count(const WordCountFlags& flags, const char* buffer, size_t size, const std::string& filename);

WordCountResult word_count_file(const WordCountFlags& flags, const string& file_name);