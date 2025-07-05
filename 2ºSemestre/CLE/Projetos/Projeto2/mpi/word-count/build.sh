#!/bin/bash
# filepath: /home/d479/Uni/MEI/1ANO/2SEMESTRE/CLE/2425-tp02-group11/mpi/word-count/build.sh

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project root directory
ROOT_DIR=$(dirname "$(readlink -f "$0")")
BUILD_DIR="${ROOT_DIR}/test_build"
OPT_DIR="${BUILD_DIR}/optimized"
UNOPT_DIR="${BUILD_DIR}/unoptimized"

# Create build directories
mkdir -p "${OPT_DIR}" "${UNOPT_DIR}"

# Helper function to build with specified optimization
build_with_optimization() {
    local build_dir="$1"
    local opt_flag="$2"
    local description="$3"
    
    echo -e "${YELLOW}Building ${description} version in ${build_dir}${NC}"
    
    # Navigate to build directory
    cd "${build_dir}"
    
    # Run CMake with the appropriate optimization flag
    # Use -DCMAKE_CXX_FLAGS_RELEASE to override default Release flags
    cmake -DCMAKE_BUILD_TYPE=Release \
          -DCMAKE_CXX_FLAGS="${opt_flag}" \
          -DCMAKE_CXX_FLAGS_RELEASE="${opt_flag}" \
          "${ROOT_DIR}"
    
    # Build using make with verbose output to verify flags
    make VERBOSE=1 -j$(nproc)
    
    # Check if build was successful
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully built ${description} version${NC}"
        return 0
    else
        echo -e "\033[0;31mFailed to build ${description} version${NC}"
        return 1
    fi
}

# Build optimized version
echo "====================================="
echo "Building optimized version (O3)..."
echo "====================================="
build_with_optimization "${OPT_DIR}" "-O3" "optimized"
opt_status=$?

# Build unoptimized version
echo "====================================="
echo "Building unoptimized version (O0)..."
echo "====================================="
build_with_optimization "${UNOPT_DIR}" "-O0" "unoptimized"
unopt_status=$?

# Summary
echo "====================================="
echo "Build Summary:"
if [ ${opt_status} -eq 0 ]; then
    echo -e "${GREEN}✓ Optimized build: ${OPT_DIR}/cle-mpi${NC}"
else
    echo -e "\033[0;31m✗ Optimized build failed${NC}"
fi

if [ ${unopt_status} -eq 0 ]; then
    echo -e "${GREEN}✓ Unoptimized build: ${UNOPT_DIR}/cle-mpi${NC}"
else
    echo -e "\033[0;31m✗ Unoptimized build failed${NC}"
fi

# Show usage examples if both builds succeeded
if [ ${opt_status} -eq 0 ] && [ ${unopt_status} -eq 0 ]; then
    echo "====================================="
    echo "Usage examples:"
    echo "Run optimized version:"
    echo "  mpiexec -n 4 ${OPT_DIR}/cle-mpi books.txt"
    echo "Run unoptimized version:"
    echo "  mpiexec -n 4 ${UNOPT_DIR}/cle-mpi books.txt"
    echo "====================================="
fi

cd "${ROOT_DIR}"