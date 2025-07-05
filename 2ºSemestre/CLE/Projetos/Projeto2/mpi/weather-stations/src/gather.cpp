#include "gather.h"
#include <cstring>
#include <mpi.h>

/** 
 * Function to merge two maps containing weather station data.
 * @param target: The target map to merge into.
 * @param source: The source map to merge from.
 * @return: void
 */
void mergeMaps(std::map<std::string, wsData>& target, const std::map<std::string, wsData>& source)
{
    for (const auto& [city, data] : source)
    {
        auto it = target.find(city);
        if (it == target.end())
            target[city] = data;
        else
        {
            it->second.sum += data.sum;
            it->second.count += data.count;
            it->second.max = std::max(it->second.max, data.max);
            it->second.min = std::min(it->second.min, data.min);
        }
    }
}

/**
 * Function to transform a map containing weather station data into a CityData buffer.
 * @param wsMap: The map containing weather station data.
 * @param buffer: The buffer to store the transformed data.
 * @return: MPI_Datatype representing the CityData structure.
 */
void mapToBuffer(const std::map<std::string, wsData>& wsMap, CityData* buffer)
{
    int i = 0;
    for (const auto& [city, data] : wsMap)
    {
        std::strncpy(buffer[i].city, city.c_str(), sizeof(buffer[i].city) - 1);
        buffer[i].city[sizeof(buffer[i].city) - 1] = '\0'; // Ensure null-termination
        buffer[i].data = data;
        i++;
    }
}

/**
 * Function to transfom a CityData buffer into a map.
 * @param buffer: The buffer containing CityData.
 * @param count: The number of elements in the buffer.
 * @return: A map containing the transformed data.
 */
std::map<std::string, wsData> bufferToMap(CityData* buffer, int count)
{
    std::map<std::string, wsData> map;
    for (int i = 0; i < count; ++i)
    {
        map[buffer[i].city] = buffer[i].data;
    }
    return map;
}

/**
 * Function to receive data from other working processes and merge it into the local map.
 * @param size: The total number of processes.
 * @param rank: The rank of the current process.
 * @param localMap: The local map containing weather station data.
 * @return: A merged map containing data from all processes.
 */
std::map<std::string, wsData> gatherResults(int size, int rank, std::map<std::string, wsData>& localMap)
{
    MPI_Datatype cityType = createCityDataType();

    int step = 1;
    while (step < size)
    {
        if (rank % (2 * step) == 0)
        {
            int sender = rank + step;
            if (sender < size)
            {
                int recvCount;
                MPI_Recv(&recvCount, 1, MPI_INT, sender, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                CityData* recvBuffer = new CityData[recvCount];
                MPI_Recv(recvBuffer, recvCount, cityType, sender, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

                // Merge received data
                for (int i = 0; i < recvCount; ++i)
                {
                    std::string city(recvBuffer[i].city);
                    wsData& entry = localMap[city];
                    const wsData& incoming = recvBuffer[i].data;

                    entry.sum += incoming.sum;
                    entry.count += incoming.count;
                    entry.max = std::max(entry.max, incoming.max);
                    entry.min = std::min(entry.min, incoming.min);
                }
                delete[] recvBuffer;
            }
        }
        else 
        {
            int receiver = rank - step;
            int sendCount = localMap.size();
            CityData* sendBuffer = new CityData[sendCount];
            int idx = 0;
            for (const auto& [city, data] : localMap)
            {
                std::strncpy(sendBuffer[idx].city, city.c_str(), sizeof(sendBuffer[idx].city) - 1);
                sendBuffer[idx].city[sizeof(sendBuffer[idx].city) - 1] = '\0'; // Ensure null-termination
                sendBuffer[idx].data = data;
                idx++;
            }

            // Send and exit loop
            MPI_Send(&sendCount, 1, MPI_INT, receiver, 0, MPI_COMM_WORLD);
            MPI_Send(sendBuffer, sendCount, cityType, receiver, 0, MPI_COMM_WORLD);
            delete[] sendBuffer;
            break;
        }

        step *= 2;
    }

    return localMap;
}