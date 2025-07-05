
#include <getopt.h>
#include <iostream>
#include <fstream>

#include "word_count.h"

using namespace std;

static option long_options[] = {
    {"lines",   no_argument, 0,  0 },
    {"words",   no_argument, 0,  0 },
    {"chars",   no_argument, 0,  0 },
    {0,         0,           0,  0 }
};

int main(int argc, char* argv[])
{
    WordCountFlags flags;
    while(1) {
        int option_index = 0;
        int c = getopt_long(argc, argv, "lwc",
                 long_options, &option_index);
        if (c == -1)
            break;

        switch (c) {
            case 'l': flags.lines = true; break;
            case 'w': flags.words = true; break;
            case 'c': flags.chars = true; break;
            case '?':
                // getopt_long already printed an error message
                break;
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

    word_count(flags, files);

    return 0;
}
