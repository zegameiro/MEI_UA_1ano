cmake_minimum_required(VERSION 3.22.1)
project(cle-weather-stations CXX)

add_executable(cle-ws
    src/main.cpp
    # Add your files here if needed.
)
target_compile_features(cle-ws PRIVATE cxx_std_20)
target_compile_options(cle-ws PRIVATE -Wall -Wextra -O3)

add_executable(cle-samples src/create-samples.cpp)
target_compile_features(cle-samples PRIVATE cxx_std_20)
target_compile_options(cle-samples PRIVATE -Wall -Wextra)
