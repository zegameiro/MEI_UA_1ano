cmake_minimum_required(VERSION 3.22.1)
project(project-name CXX)

add_executable(cle-tp
    src/main.cpp
    # Add your files here if needed.
)
target_compile_features(cle-tp PRIVATE cxx_std_20)
target_compile_options(cle-tp PRIVATE -Wall -Wextra)
target_include_directories(cle-tp PRIVATE include src)
