#include <iostream>
#include <cstring>
#include <mpi.h>

int main (int argc, char *argv[])
{
    MPI_Init(&argc, &argv); 
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int MAX_DATA = 256;
    char data[MAX_DATA];

    if (rank == 0) 
    {
        std::snprintf(data, MAX_DATA, "I am here (%d)", rank);
        printf("Process %d sending data: %s \n", rank, data);
        MPI_Send(data, MAX_DATA, MPI_CHAR, 1, 0, MPI_COMM_WORLD);
    } 

    MPI_Recv(data, MAX_DATA, MPI_CHAR, (rank - 1) % size, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    printf("Process %d received data: %s \n", rank, data);

    if (rank != 0)
    {   
        std::snprintf(data, MAX_DATA, "I am here (%d)", rank);
        MPI_Send(data, std::strlen(data) + 1, MPI_CHAR, (rank + 1) % size, 0, MPI_COMM_WORLD);
        printf("Process %d sending data: %s \n", rank, data);
    }

    MPI_Finalize();
    return EXIT_SUCCESS;
}
