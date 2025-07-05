#include <iostream>
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
        std::snprintf(data, MAX_DATA, "Process %d is alive and well", rank);
        for (int i = 1; i < size; ++i)
        {
            MPI_Send(data, MAX_DATA, MPI_CHAR, i, 0, MPI_COMM_WORLD);
        }
    }

    if (rank != 0)
    {
        MPI_Recv(data, MAX_DATA, MPI_CHAR, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Process %d received data: %s \n", rank, data);
        std::snprintf(data, MAX_DATA, "Process %d is alive and well", rank);
        MPI_Send(data, MAX_DATA, MPI_CHAR, 0, 0, MPI_COMM_WORLD);
    }

    if (rank == 0)
    {
        for (int i = 1; i < size; ++i)
        {
            MPI_Recv(data, MAX_DATA, MPI_CHAR, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            printf("Process %d received data: %s \n", i, data);
        }
    }

    MPI_Finalize();
    return 0;
}