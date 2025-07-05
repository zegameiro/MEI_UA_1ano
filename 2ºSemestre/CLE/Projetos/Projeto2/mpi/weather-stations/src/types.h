#ifndef WEATHER_STATIONS_TYPES_H
#define WEATHER_STATIONS_TYPES_H

#include <string>
#include <mpi.h>

/**
 * @struct data structure to hold weather station data.
 */
struct wsData
{
    float sum = 0.0f;
    int count = 0;
    float max = -100.0f;
    float min = 100.0f;
};

/**
 * @struct data structure to hold city data.
 */
struct CityData
{
    char city[100];
    wsData data; 
};

MPI_Datatype createWsDataType();
MPI_Datatype createCityDataType();

#endif // WEATHER_STATIONS_TYPES_H


