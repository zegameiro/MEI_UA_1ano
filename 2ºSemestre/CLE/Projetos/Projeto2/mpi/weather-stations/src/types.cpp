#include "types.h"

/**
 * Function to create a custom MPI datatype for weather station data.
 * @return: MPI_Datatype representing the weather station data structure.
 */
MPI_Datatype createWsDataType()
{
    MPI_Datatype wsDataType;
    int blockLengths[4] = { 1, 1, 1, 1 };
    MPI_Datatype types[4] = { MPI_FLOAT, MPI_INT, MPI_FLOAT, MPI_FLOAT };
    MPI_Aint offsets[4];

    offsets[0] = offsetof(wsData, sum);
    offsets[1] = offsetof(wsData, count);
    offsets[2] = offsetof(wsData, max);
    offsets[3] = offsetof(wsData, min);

    MPI_Type_create_struct(4, blockLengths, offsets, types, &wsDataType);
    MPI_Type_commit(&wsDataType);
    return wsDataType;
}

/**
 * Function to create a custom MPI datatype for city data.
 * @return: MPI_Datatype representing the city data structure.
 */
MPI_Datatype createCityDataType()
{
    MPI_Datatype cityDataType;
    MPI_Datatype wsDataType = createWsDataType();

    int cdBlockLengths[2] = { 100, 1 };
    MPI_Datatype cdTypes[2] = { MPI_CHAR, wsDataType };
    MPI_Aint cdOffsets[2];

    cdOffsets[0] = offsetof(CityData, city);
    cdOffsets[1] = offsetof(CityData, data);

    MPI_Type_create_struct(2, cdBlockLengths, cdOffsets, cdTypes, &cityDataType);
    MPI_Type_commit(&cityDataType);

    // Free the temporary wsDataType
    MPI_Type_free(&wsDataType);

    return cityDataType;
}