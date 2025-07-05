#include <iostream>
#include <fstream>
#include <vector>
#include "utf-8.h"
#include "word_count.h"

using namespace std;

void word_count(const WordCountFlags& flags, const std::vector<std::string>& files)
{   
    
    int total_chars = 0;
    int total_lines = 0;
    int total_words = 0;
    
    // printf("%-20s %12s %10s %10s\n", "FILE NAME", "CHAR COUNT", "LINE COUNT", "WORD COUNT");
    // printf("%-20s %12s %10s %10s\n", "--------------------", "------------", "----------", "----------");

    for (auto& file_name : files)
    {
        int chars = 0;     
        int lines = 0;    
        int words = 0;

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

        // printf("%-20s %12d %10d %10d\n", file_name.c_str(), chars, lines, words);


        total_chars += chars;
        total_lines += lines;
        total_words += words;
    }

    if (files.size() > 1) 
    {

        printf("%-20s %12s %10s %10s\n", "======================", "===========", "==========", "==========");
        printf("%-20s %12d %10d %10d\n", "TOTAL", total_chars, total_lines, total_words);
    }
}