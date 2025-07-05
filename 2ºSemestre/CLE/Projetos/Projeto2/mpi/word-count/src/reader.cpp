// reads file content to a buffer and then sends the file to another process via mpi
#include <iostream>
#include <sys/stat.h>
#include <string>
#include <unistd.h>
#include <sys/mman.h>
#include <fstream>
#include <mpi.h>
#include "reader.h"

using namespace std;


size_t getFileSize(const char* filename)
{
    struct stat st;
    if (stat(filename, &st) != 0) {
        std::cerr << "Error getting file size for file" << filename << std::endl;
        return 0;
    }

    return st.st_size;
}

char* readFileToBuffer(const char* filename)
{
    ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error opening file " << filename << std::endl;
        return nullptr;
    }

    int file_size = getFileSize(filename);

    if (file_size <= 0) {
        std::cerr << "Error getting file size for file " << filename << std::endl;
        return nullptr;
    }

    char* buffer = new char[file_size + 1];
    if (!buffer) {
        std::cerr << "Error allocating memory for file buffer " << filename << std::endl;
        return nullptr;
    }

    file.read(buffer, file_size);
    if (!file) {
        std::cerr << "Error reading file " << filename << std::endl;
        delete[] buffer;
        return nullptr;
    }
    buffer[file_size] = '\0'; // Null-terminate the buffer
    file.close();
    return buffer;
}

vector<string> readFileList(int argc, char* argv[], int& total_files) {
    vector<string> files;
    
    // check if there are any files
    if (optind < argc) {
        string fname = argv[optind];
        ifstream file(fname);

        if (!file.is_open()) {
            cerr << "Error opening the file!" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
            return files;
        }

        string book_name;
        while (getline(file, book_name))
            files.push_back(book_name);
        
        total_files = files.size();
    } else {
        cout << "No files provided" << endl;
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    
    return files;
}