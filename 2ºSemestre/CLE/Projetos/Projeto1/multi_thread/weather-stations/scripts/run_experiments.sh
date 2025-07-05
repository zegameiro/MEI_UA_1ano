#!/bin/bash

# Check if enough arguments are provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <filename: required> [numThreads: optional] [repetitions: optional (≤100)]"
    exit 1
fi

FILENAME=$1
NUM_THREADS=${2:-$(nproc)}  # Default to the number of available CPU threads
REPETITIONS=${3:-1}  # Default is 1 run

# Validate repetitions (must be between 1 and 100)
if [ "$REPETITIONS" -lt 1 ] || [ "$REPETITIONS" -gt 100 ]; then
    echo "Error: Repetitions must be between 1 and 100."
    exit 1
fi

OUTPUT_FILE="experiment_results.txt"
> "$OUTPUT_FILE"  # Clear previous results

echo "Running $REPETITIONS iterations with $NUM_THREADS threads on $FILENAME" | tee -a "$OUTPUT_FILE"
TOTAL_TIME=0

for ((i=1; i<=REPETITIONS; i++)); do
    echo "Executing run $i..." | tee -a "$OUTPUT_FILE"

    # Measure execution time
    START_TIME=$(date +%s.%N)
    ../build/cle-ws "$FILENAME" "$NUM_THREADS" >> "$OUTPUT_FILE" 2>&1
    END_TIME=$(date +%s.%N)

    # Calculate duration
    RUN_TIME=$(echo "$END_TIME - $START_TIME" | bc)
    TOTAL_TIME=$(echo "$TOTAL_TIME + $RUN_TIME" | bc)

    echo "Execution Time for run $i: $RUN_TIME seconds" | tee -a "$OUTPUT_FILE"
done

echo "=====================================" | tee -a "$OUTPUT_FILE"
echo "Total Execution Time: $TOTAL_TIME seconds" | tee -a "$OUTPUT_FILE"
echo "Results saved to $OUTPUT_FILE"
