#ifndef GATHER_H
#define GATHER_H

#include <map>
#include <string>
#include "types.h"

void mergeMaps(std::map<std::string, wsData>& target, const std::map<std::string, wsData>& source);
void mapToBuffer(const std::map<std::string, wsData>& wsMap, CityData* buffer);
std::map<std::string, wsData> bufferToMap(CityData* buffer, int count);
std::map<std::string, wsData> gatherResults(int size, int rank, std::map<std::string, wsData>& localMap);

#endif // GATHER_H