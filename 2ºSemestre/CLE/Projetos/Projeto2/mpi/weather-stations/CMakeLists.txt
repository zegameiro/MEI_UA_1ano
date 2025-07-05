cmake_minimum_required(VERSION 3.22.1)
project(base-mpi CXX)

# Require MPI for this project:
find_package(MPI REQUIRED)
set(CMAKE_CXX_COMPILE_FLAGS ${CMAKE_CXX_COMPILE_FLAGS} ${MPI_COMPILE_FLAGS})
set(CMAKE_CXX_LINK_FLAGS ${CMAKE_CXX_LINK_FLAGS} ${MPI_LINK_FLAGS})
include_directories(${MPI_INCLUDE_PATH})

add_executable(cle-ws-mpi
    src/processor.cpp
    src/gather.cpp
    src/types.cpp
    src/main.cpp
)
target_link_libraries(cle-ws-mpi ${MPI_LIBRARIES})
target_compile_features(cle-ws-mpi PRIVATE cxx_std_20)
target_compile_options(cle-ws-mpi PRIVATE -Wall -Wextra -O3)

add_executable(cle-samples src/create-samples.cpp)
target_link_libraries(cle-samples ${MPI_LIBRARIES})
target_compile_features(cle-samples PRIVATE cxx_std_20)
target_compile_options(cle-samples PRIVATE -Wall -Wextra -O3)
