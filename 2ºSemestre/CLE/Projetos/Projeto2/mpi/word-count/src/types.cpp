#include "types.h"
#include <iostream>

MPI_Datatype createWordCountResultType() {
    MPI_Datatype datatype;
    
    // Define the structure elements
    int blocklengths[4] = {256, 1, 1, 1};
    MPI_Datatype types[4] = {MPI_CHAR, MPI_INT, MPI_INT, MPI_INT};
    MPI_Aint displacements[4];
    
    // Calculate displacements
    WordCountData dummy;
    MPI_Aint base_address;
    MPI_Get_address(&dummy, &base_address);
    
    MPI_Get_address(&dummy.filename, &displacements[0]);
    MPI_Get_address(&dummy.chars, &displacements[1]);
    MPI_Get_address(&dummy.lines, &displacements[2]);
    MPI_Get_address(&dummy.words, &displacements[3]);
    
    // Make displacements relative to base address
    for (int i = 0; i < 4; i++) {
        displacements[i] = MPI_Aint_diff(displacements[i], base_address);
    }
    
    // Create and commit the datatype
    MPI_Type_create_struct(4, blocklengths, displacements, types, &datatype);
    MPI_Type_commit(&datatype);
    
    return datatype;
}