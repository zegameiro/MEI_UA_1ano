#!/bin/bash

# Check if the user provided the directory
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <samples_directory>"
    exit 1
fi

# Get arguments
samples_dir=$1

# Create results directory if it doesn't exist
results_dir="../results"
mkdir -p "$results_dir"

# Create or overwrite the CSV file with headers
csv_file="$results_dir/execution_times_all_processes_no_optimization.csv"
echo "NumProcesses,NumSamples,ExecutionTime" > "$csv_file"

# Array of process counts to test
process_counts=(2 4 6 8)

# Process each sample file with different process counts
for file in "$samples_dir"/*; do
    if [ -f "$file" ]; then  # Ensure it's a file
        filename=$(basename -- "$file")  # Extract the filename
        
        # Try to extract sample count from filename (assuming pattern like "samples_10000.txt")
        num_samples=$(echo "$filename" | grep -o '[0-9]\+' | head -1)
        
        # Run with each process count
        for num_processes in "${process_counts[@]}"; do
            echo "Processing $file with $num_processes processes..."
            
            # Use time command to measure execution time
            # The format %e gives the elapsed real time in seconds
            exec_time=$(/usr/bin/time -f "%e" mpiexec -n "$num_processes" ../build/cle-ws-mpi "$file" 2>&1 1>/dev/null | tail -n 1)
            
            # Append to CSV
            echo "$num_processes,$num_samples,$exec_time" >> "$csv_file"
            
            echo "Results for $filename with $num_processes processes added to $csv_file"
        done
    fi
done

echo "Processing complete. Results saved in $csv_file"