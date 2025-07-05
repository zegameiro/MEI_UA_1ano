#!/bin/bash

# Check if the user provided the directory and number of threads
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <samples_directory> <num_threads>"
    exit 1
fi

# Get arguments
samples_dir=$1
num_threads=$2

# Process each sample file
for file in "$samples_dir"/*; do
    if [ -f "$file" ]; then  # Ensure it's a file
        filename=$(basename -- "$file")  # Extract the filename
        output_file="${filename}-results.txt"  # Create output filename

        # Get timestamp
        timestamp=$(date +"%Y-%m-%d %H:%M:%S")

        echo "Processing $file with $num_threads threads..."
        echo "----------------------------------------" >> "$output_file"
        echo "Run at: $timestamp" >> "$output_file"
        echo "File: $file" >> "$output_file"
        
        # Execute cle-ws and append output
        ../build/cle-ws "$file" "$num_threads" >> "$output_file" 2>&1

        echo "----------------------------------------" >> "$output_file"

        echo "Results saved in $output_file."
    fi
done

echo "Processing complete for all files."