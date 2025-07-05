#include <iostream>
#include <fstream>
#include <vector>
#include <mutex>
#include "utf-8.h"
#include "word_count.h"
#include "globals.h"

extern bool use_atomic;

std::mutex mtx;

using namespace std;

void word_count(const WordCountFlags& flags, const string file_name)
{      
    int chars = 0, lines = 0, words = 0;

    char byte, prev_byte = 0;
    bool is_word = false;

    uint32_t codepoint = 0;  
    UTF8DecoderState state = {0, 0, 0}; 

    std::ifstream file(file_name);
    
    while (file.get(byte)) 
    {
        if (flags.chars) chars++;  

        int result = utf8_decode(state, static_cast<uint8_t>(byte), &codepoint);

        if (result == 0 || result < 0) continue;
    
        if (flags.words) 
        {
            if (utf8_is_space(codepoint)) 
            {
                if (is_word) 
                {
                    words++;
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
                lines++; 
            }
        }
        
        prev_byte = static_cast<char>(codepoint); 
    }

    if (prev_byte != '\n') lines++;

    if (use_atomic) {
        total_chars_atomic.fetch_add(chars, std::memory_order_relaxed);
        total_lines_atomic.fetch_add(lines, std::memory_order_relaxed);
        total_words_atomic.fetch_add(words, std::memory_order_relaxed);
    } else {
        std::lock_guard<std::mutex> lock(global_mutex);
        total_chars += chars;
        total_lines += lines;
        total_words += words;
    }
}