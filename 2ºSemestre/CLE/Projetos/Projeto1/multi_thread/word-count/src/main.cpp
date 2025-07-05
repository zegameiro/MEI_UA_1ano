#include <getopt.h>
#include <iostream>
#include <fstream>
#include <thread>
#include "word_count.h"
#include "globals.h"
#include "thread_pool.h"

using namespace std;

static option long_options[] = {
    {"lines",   no_argument, 0,  0 },
    {"words",   no_argument, 0,  0 },
    {"chars",   no_argument, 0,  0 },
    {"threads", required_argument, 0, 't' },
    {"atomic",  no_argument, 0, 'a' },
    {"help",    no_argument, 0, 'h' },
    {0,         0,           0,  0 }
};

void print_help() {
    cout << "Usage: cle-wc [options] input_file.txt" << endl;
    cout << "Options:" << endl;
    cout << "  -l, --lines          Count lines" << endl;
    cout << "  -w, --words          Count words" << endl;
    cout << "  -c, --chars          Count characters" << endl;
    cout << "  -t, --threads N      Use N threads (default: hardware concurrency)" << endl;
    cout << "  -a, --atomic         Use atomic operations for global counters" << endl;
    cout << "  -h, --help           Show this help message" << endl;
}

bool use_atomic = false;

int main(int argc, char* argv[])
{
    WordCountFlags flags;
    int numThreads = thread::hardware_concurrency();

    while(1) {
        int option_index = 0;
        int c = getopt_long(argc, argv, "lwct:ah",
          long_options, &option_index);
            if (c == -1)
            break;

        switch (c) {
            case 'l': flags.lines = true; break;
            case 'w': flags.words = true; break;
            case 'c': flags.chars = true; break;
            case 't': numThreads = atoi(optarg); break;
            case 'a': use_atomic = true; break;
            case 'h':
                print_help();
                return 0;
            case '?':
                // getopt_long already printed an error message
                print_help();
                return 1;
        }// end switch
    }// end while(1)

    if (!flags.lines && ! flags.words && !flags.chars)
        flags.lines = flags.words = flags.chars = true;

    vector<string> files;

    // check if there are any files
    if (optind < argc) {
        string fname = argv[optind];
        ifstream file(fname);
        
        if (!file.is_open())
        {
            cerr << "Error opening the file!";
            return 1;
        }

        string book_name;

        while (getline(file, book_name))
            files.push_back(book_name);

    } else {
        cout << "No files provided" << endl;
        return 1;
    }

    printf("%-20s %12s %10s %10s %10s\n", "FILE NAME", "CHAR COUNT", "LINE COUNT", "WORD COUNT", "THREADS");
    // printf("%-20s %12s %10s %10s %10s\n", "--------------------", "------------", "----------", "----------", "-------");
    
    ThreadPool pool(numThreads);
    for (size_t i = 0; i < files.size(); i++) {
        pool.enqueue([&, i]() {
            word_count(flags, files[i]);
        });
    }

    pool.wait();

    printf("%-20s %12s %10s %10s %10s\n", "======================", "===========", "==========", "==========", "=========");
    if (use_atomic) {
        printf("%-20s %12d %10d %10d %10d\n", "TOTAL", total_chars_atomic.load(), total_lines_atomic.load(), total_words_atomic.load(), numThreads);
    } else {
        printf("%-20s %12d %10d %10d %10d\n", "TOTAL", total_chars, total_lines, total_words, numThreads);
    }

    return 0;
}
