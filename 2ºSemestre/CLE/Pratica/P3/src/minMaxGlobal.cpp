#include <iostream>
#include <cstdlib>
#include <ctime>
#include <mpi.h>

int main(int argc, char *argv[])
{
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::srand(time(NULL) + rank);
    int local_number = std::rand() % 100;

    printf("Process %d generated number: %d\n", rank, local_number);
    int global_min, global_max;

    MPI_Reduce(&local_number, &global_min, 1, MPI_INT, MPI_MIN, 0, MPI_COMM_WORLD);
    MPI_Reduce(&local_number, &global_max, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);

    if (rank == 0)
    {
        printf("Global minimum: %d\nGlobal maximum: %d\n", global_min, global_max);
    }

    MPI_Finalize();
    return 0;
}
