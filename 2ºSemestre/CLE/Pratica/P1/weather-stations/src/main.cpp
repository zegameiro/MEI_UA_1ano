
#include <iostream>
#include <fstream>
#include <map>
#include <chrono>

using namespace std;
using namespace std::chrono;

struct wsData
{
    float sum = 0.0f;
    int count = 0;
    float max = -100.0f;
    float min = 100.0f;
};

int main(int argc, char* argv[])
{
    // Use default file ...
    const char* file = "measurements.txt";
    if (argc > 1)
    {
        // ... or the first argument.
        file = argv[1];
    }
    ifstream fh(file);
    if (not fh.is_open())
    {
        std::cerr << "Unable to open '" << file << "'" << std::endl;
        return 1;
    }

    // Variable to store each line from the file
    string line;

    map<string, wsData> wsMap;

    auto start = high_resolution_clock::now();

    // Read each line from the file and print it
    while (getline(fh, line))
    {
        // Split the line
        size_t pos = line.find(';');

        // Extract the city and the temperature
        string city = line.substr(0, pos);
        float temp = stof(line.substr(pos + 1));

        // Update the wsMap
        wsMap[city].sum += temp;
        wsMap[city].count++;
        wsMap[city].max = max(temp, wsMap[city].max);
        wsMap[city].min = min(temp, wsMap[city].max);
    }

    // Sort the wsMap by city name
    map<string, wsData> wsMapSorted(wsMap.begin(), wsMap.end());

    // Print the results
    for (auto& [city, data] : wsMap)
    {
        printf("%s: avg=%.1f min=%.1f max=%.1f\n", city.c_str(), data.sum / data.count, data.min, data.max);
    }

    // Always close the file when done
    fh.close();

    return 0;
}
