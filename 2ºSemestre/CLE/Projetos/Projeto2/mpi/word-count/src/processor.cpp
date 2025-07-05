#include <vector>
#include <string>
#include <string.h>
#include <mpi.h>
#include "word_count.h"
#include "reader.h"
#include <iostream>
#include "types.h"
#include "processor.h"

using namespace std;

vector<WordCountResult> processWordCount(int argc, char *argv[], int rank, int world_size, const WordCountFlags &flags)
{
    // Read file list
    int total_files = 0;
    vector<string> files;
    
    if (rank == MASTER_RANK)
    {
        files = readFileList(argc, argv, total_files);
    }
    
    // Broadcast the total number of files
    MPI_Bcast(&total_files, 1, MPI_INT, MASTER_RANK, MPI_COMM_WORLD);
    
    // If there isn't any file, return empty results
    if (total_files == 0)
    {
        return vector<WordCountResult>();
    }
    
    // Calculate file distribution
    int chunk_size = total_files / world_size;
    
    // Allocate space for sendcounts and displacements
    int *sendcounts = nullptr;
    int *displacements = nullptr;
    
    if (rank == MASTER_RANK)
    {
        sendcounts = new int[world_size];
        displacements = new int[world_size];
        
        displacements[0] = 0;
        for (int i = 0; i < world_size; i++)
        {
            sendcounts[i] = chunk_size;
            if (i > 0)
            {
                displacements[i] = displacements[i - 1] + sendcounts[i - 1];
            }
        }
        
        // Log process distribution
        cout << "Process distribution:" << endl;
        for (int i = 0; i < world_size; i++)
        {
            cout << "Process " << i << " will handle " << sendcounts[i] << " files" << endl;
        }
    }
    
    // Distribute files
    vector<string> my_files = distributeFiles(files, total_files, rank, world_size, sendcounts, displacements);
    
    // Clean up resources
    if (rank == MASTER_RANK)
    {
        delete[] sendcounts;
        delete[] displacements;
    }
    
    // Process files
    vector<WordCountResult> local_results = processFiles(my_files, flags);
    
    return local_results;
}

// Scatter filenames from master to all processes
void scatterFilenames(char** all_filenames, char** my_filenames, int total_files, 
                     int chunk_size, int rank, int* sendcounts, int* displacements) 
{
    for (int j = 0; j < 256; j++) { 
        char *sendbuf = nullptr;
        if (rank == MASTER_RANK) {
            sendbuf = new char[total_files];
            for (int i = 0; i < total_files; i++) {
                sendbuf[i] = all_filenames[i][j];
            }
        }

        char *recvbuf = new char[chunk_size];

        MPI_Scatterv(sendbuf, sendcounts, displacements, MPI_CHAR,
                    recvbuf, chunk_size, MPI_CHAR,
                    MASTER_RANK, MPI_COMM_WORLD);

        for (int i = 0; i < chunk_size; i++) {
            my_filenames[i][j] = recvbuf[i];
        }

        delete[] recvbuf;
        if (rank == MASTER_RANK) {
            delete[] sendbuf;
        }
    }
}

// Distribute files among processes
vector<string> distributeFiles(const vector<string> &files, int total_files, int rank,
                             int world_size, int *sendcounts, int *displacements)
{
    // Calculate how many files this process will handle
    int chunk_size = total_files / world_size;

    // Prepare to receive file names
    vector<string> my_files(chunk_size);
    char **my_filenames = new char *[chunk_size];
    for (int i = 0; i < chunk_size; i++)
    {
        my_filenames[i] = new char[256];
    }

    // Master prepares the data to be scattered
    char **all_filenames = nullptr;
    if (rank == MASTER_RANK)
    {
        all_filenames = new char *[total_files];
        for (int i = 0; i < total_files; i++)
        {
            all_filenames[i] = new char[256];
            memset(all_filenames[i], 0, 256);
            strncpy(all_filenames[i], files[i].c_str(), 255);
        }
    }

    // Scatter filenames from master to all processes
    scatterFilenames(all_filenames, my_filenames, total_files, chunk_size, rank, 
                    sendcounts, displacements);

    // Convert char arrays to strings
    for (int i = 0; i < chunk_size; i++)
    {
        my_files[i] = string(my_filenames[i]);
        delete[] my_filenames[i];
    }
    delete[] my_filenames;

    // Clean up resources for master
    if (rank == MASTER_RANK && all_filenames != nullptr)
    {
        for (int i = 0; i < total_files; i++)
        {
            delete[] all_filenames[i];
        }
        delete[] all_filenames;
    }

    return my_files;
}

// Process files assigned to this rank
vector<WordCountResult> processFiles(const vector<string> &my_files, const WordCountFlags &flags)
{
    vector<WordCountResult> local_results;

    for (const auto &filename : my_files)
    {
        char *buffer = readFileToBuffer(filename.c_str());
        size_t size = getFileSize(filename.c_str());

        if (buffer)
        {
            WordCountResult result = word_count(flags, buffer, size, filename);
            local_results.push_back(result);
            delete[] buffer;
        }
        else
        {
            cerr << "Error reading file: " << filename << endl;
        }
    }

    return local_results;
}

// Gather results from all processes
vector<WordCountResult> gatherResults(const vector<WordCountResult> &local_results, int rank, int world_size)
{
    int total_results = 0;

    // First, gather the number of results from each process
    int local_num_results = local_results.size();
    vector<int> result_counts;
    vector<int> result_displs;

    if (rank == MASTER_RANK)
    {
        result_counts.resize(world_size);
        result_displs.resize(world_size);
    }

    MPI_Gather(&local_num_results, 1, MPI_INT,
               rank == MASTER_RANK ? result_counts.data() : nullptr,
               1, MPI_INT, MASTER_RANK, MPI_COMM_WORLD);

    // Calculate displacements for gathering results
    if (rank == MASTER_RANK)
    {
        result_displs[0] = 0;
        for (int i = 1; i < world_size; i++)
        {
            result_displs[i] = result_displs[i - 1] + result_counts[i - 1];
        }
        total_results = result_displs[world_size - 1] + result_counts[world_size - 1];
    }

    // Prepare data for gathering - convert to array of WordCountData
    vector<WordCountData> local_data;
    for (const auto &result : local_results)
    {
        WordCountData data;
        memset(data.filename, 0, sizeof(data.filename));
        strncpy(data.filename, result.filename.c_str(), sizeof(data.filename) - 1);
        data.chars = result.chars;
        data.lines = result.lines;
        data.words = result.words;
        local_data.push_back(data);
    }

    // Create custom MPI datatype for WordCountData
    MPI_Datatype wordCountResultType = createWordCountResultType();

    // Gather all results to master
    vector<WordCountData> all_data;
    vector<WordCountResult> results;

    if (rank == MASTER_RANK)
    {
        all_data.resize(total_results);
    }

    MPI_Gatherv(local_data.data(), local_num_results, wordCountResultType,
                rank == MASTER_RANK ? all_data.data() : nullptr,
                rank == MASTER_RANK ? result_counts.data() : nullptr,
                rank == MASTER_RANK ? result_displs.data() : nullptr,
                wordCountResultType, MASTER_RANK, MPI_COMM_WORLD);

    // Free the datatype
    MPI_Type_free(&wordCountResultType);

    // Convert gathered data back to WordCountResult
    if (rank == MASTER_RANK)
    {
        for (const auto &data : all_data)
        {
            WordCountResult result;
            result.filename = string(data.filename);
            result.chars = data.chars;
            result.lines = data.lines;
            result.words = data.words;
            results.push_back(result);
        }
    }

    return results;
}