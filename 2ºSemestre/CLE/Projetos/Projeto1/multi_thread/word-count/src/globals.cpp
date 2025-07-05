#include "globals.h"
#include <atomic>

std::atomic<int> total_chars_atomic = 0;
std::atomic<int> total_lines_atomic = 0;
std::atomic<int> total_words_atomic = 0;

int total_chars = 0;
int total_lines = 0;
int total_words = 0;

std::mutex global_mutex;