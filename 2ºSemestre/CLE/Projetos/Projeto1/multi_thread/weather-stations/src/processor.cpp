/*
 * processor.cpp
 *   - Implements the batch processing of weather station data
*/

#include "processor.h"

void processBatch(std::string_view chunk, std::unordered_map<std::string, wsData>& localMap) {
    size_t start = 0;
    while (start < chunk.size()) {
        size_t end = chunk.find('\n', start);
        if (end == std::string_view::npos) end = chunk.size();

        std::string_view line = chunk.substr(start, end - start);
        start = end + 1;

        size_t pos = line.find(';');
        if (pos == std::string_view::npos) continue;

        std::string city = std::string(line.substr(0, pos));
        float temp = std::stof(std::string(line.substr(pos + 1)));

        auto& data = localMap[city];
        data.sum += temp;
        data.count++;
        data.max = std::max(data.max, temp);
        data.min = std::min(data.min, temp);
    }
}