#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include "utf-8.h"
#include "word_count.h"
#include "reader.h"

using namespace std;

/**
 * Function to perform word count on a buffer
 * @param flags: flags for word count options
 * @param buffer: pointer to the buffer containing the file content
 * @param size: size of the buffer
 * @param filename: name of the file
 * @return: WordCountResult structure containing the result
 */
WordCountResult word_count(const WordCountFlags &flags, const char *buffer, size_t size, const std::string &filename)
{
    WordCountResult result;
    result.filename = filename;

    uint32_t codepoint = 0;
    UTF8DecoderState state = {0, 0, 0};

    bool is_word = false;
    char prev_byte = 0;

    // Iterate through the buffer
    for (size_t i = 0; i < size; i++)
    {
        char byte = buffer[i]; // current byte

        if (flags.chars)
            result.chars++;

        int decode_result = utf8_decode(state, static_cast<uint8_t>(byte), &codepoint);

        if (decode_result == 0 || decode_result < 0)
            continue;

        if (flags.words)
        {
            if (utf8_is_space(codepoint))
            {
                if (is_word)
                {
                    result.words++;
                    is_word = false;
                }
            }
            else
            {
                if (!is_word)
                {
                    is_word = true;
                }
            }
        }

        if (flags.lines)
        {
            if (codepoint == '\n')
            {
                result.lines++;
            }
        }

        prev_byte = static_cast<char>(codepoint);
    }

    // Count final line if not ending with newline
    if (size > 0 && prev_byte != '\n')
        result.lines++;

    return result;
}

WordCountResult word_count_file(const WordCountFlags &flags, const string &file_name)
{
    WordCountResult result;
    result.filename = file_name;
    result.chars = 0;
    result.lines = 0;
    result.words = 0;

    char byte, prev_byte = 0;
    bool is_word = false;

    uint32_t codepoint = 0;
    UTF8DecoderState state = {0, 0, 0};

    std::ifstream file(file_name);

    while (file.get(byte))
    {
        if (flags.chars)
            result.chars++;

        int decode_result = utf8_decode(state, static_cast<uint8_t>(byte), &codepoint);

        if (decode_result == 0 || decode_result < 0)
            continue;

        if (flags.words)
        {
            if (utf8_is_space(codepoint))
            {
                if (is_word)
                {
                    result.words++;
                    is_word = false;
                }
            }
            else
            {
                if (!is_word)
                {
                    is_word = true;
                }
            }
        }

        if (flags.lines)
        {
            if (codepoint == '\n')
            {
                result.lines++;
            }
        }

        prev_byte = static_cast<char>(codepoint);
    }

    if (prev_byte != '\n')
        result.lines++;

    // printf("%-20s %12d %10d %10d\n", file_name.c_str(), chars, lines, words);
    return result;
}