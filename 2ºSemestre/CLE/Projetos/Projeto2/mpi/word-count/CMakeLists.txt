cmake_minimum_required(VERSION 3.22.1)
project(base-mpi CXX)

# Require MPI for this project:
find_package(MPI REQUIRED)
set(CMAKE_CXX_COMPILE_FLAGS ${CMAKE_CXX_COMPILE_FLAGS} ${MPI_COMPILE_FLAGS})
set(CMAKE_CXX_LINK_FLAGS ${CMAKE_CXX_LINK_FLAGS} ${MPI_LINK_FLAGS})
include_directories(${MPI_INCLUDE_PATH})

add_executable(cle-mpi
    src/main.cpp
    src/utf-8.cpp
    src/word_count.cpp
    src/reader.cpp
    src/types.cpp
    src/processor.cpp
    # src/workers.cpp
    # src/masters.cpp
    # src/comm.cpp

)
target_link_libraries(cle-mpi ${MPI_LIBRARIES})
target_compile_features(cle-mpi PRIVATE cxx_std_20)
target_compile_options(cle-mpi PRIVATE -Wall -Wextra)

