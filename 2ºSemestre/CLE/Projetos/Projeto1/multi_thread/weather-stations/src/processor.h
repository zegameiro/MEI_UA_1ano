/*
 * processor.h
 *   - Header file defining weather data and a processing function
*/

#ifndef PROCESSOR_H
#define PROCESSOR_H

#include <queue>
#include <map>
#include <string>
#include <mutex>
#include <unordered_map>
#include <iostream>

struct wsData
{
    float sum = 0.0f;
    int count = 0;
    float max = -100.0f;
    float min = 100.0f;
};

extern std::map<std::string, wsData> wsMap;
extern std::mutex dataMutex;

void processBatch(std::string_view chunk, std::unordered_map<std::string, wsData>& localMap);

#endif  // PROCESSOR_H