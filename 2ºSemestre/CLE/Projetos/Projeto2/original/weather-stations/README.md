# Single Thread Weather Stations

The goal of this exercise is to load a file with weather station data and then print for each station the average temperature, minimum and maximum temperature. For the exercice you will be using C++ and CMake to build the program.

## Execution

To execute the program you will need to run the following commands:

```bash
mkdir build
cd build
cmake ..
make
./cle-wc <path to the samples file>
```

To generate samples run the following commands:

```bash
# If you haven't compiled the program yet
mkdir build
cd build
cmake ..
make
./cle-samples <number of samples>
```

The output should be similar to the following:

```
New York: avg=15.2 min=3.0 max=28.5
Los Angeles: avg=20.5 min=10.3 max=30.7
...
Execution Time: 14.3 seconds
```

A bash script was also provided to execute the single thread solution to multiple sample files. To execute this it is required to exist a directory called samples with the multiple sample files. To generate this directory follow the steps in this [README](../../multi_thread/weather-stations/README.md), at the end of the file you will find the instructions to generate the samples directory. Then to execute the bash script run the following commands:

```bash
cd scripts
chmod u+x process_samples.sh
./process_samples.sh <path to the samples directory>
```

If any errors occur during the execution, you might need to change the path to the samples directory in the argument passed and also the path to the executable in the script, depending on the error.