#ifndef GLOBALS_H
#define GLOBALS_H

#include <atomic>
#include <mutex>

extern std::atomic<int> total_chars_atomic;
extern std::atomic<int> total_lines_atomic;
extern std::atomic<int> total_words_atomic;

extern int total_chars;
extern int total_lines;
extern int total_words;

extern std::mutex global_mutex;

#endif // GLOBALS_H
