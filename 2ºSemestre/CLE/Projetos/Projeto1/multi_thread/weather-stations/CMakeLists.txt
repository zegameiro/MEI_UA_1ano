cmake_minimum_required(VERSION 3.22.1)
project(cle-weather-stations CXX)

add_executable(cle-ws
    src/main.cpp
    src/thread_pool.cpp
    src/reader.cpp
    src/processor.cpp
)
target_compile_features(cle-ws PRIVATE cxx_std_20)
target_compile_options(cle-ws PRIVATE -Wall -Wextra)
target_include_directories(cle-ws PRIVATE src)

add_executable(cle-samples src/create-samples.cpp)
target_compile_features(cle-samples PRIVATE cxx_std_20)
target_compile_options(cle-samples PRIVATE -Wall -Wextra)