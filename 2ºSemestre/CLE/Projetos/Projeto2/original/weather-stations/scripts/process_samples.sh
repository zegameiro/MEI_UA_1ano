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
csv_file="$results_dir/execution_results_optimization3.csv"
echo "NumSamples,ExecutionTime" > "$csv_file"

# Process each sample file
for file in "$samples_dir"/*; do
    if [ -f "$file" ]; then  # Ensure it's a file
        filename=$(basename -- "$file")  # Extract the filename
        
        # Try to extract the number of samples from the filename (assuming pattern like "samples_10000.txt")
        num_samples=$(echo "$filename" | grep -o '[0-9]\+' | head -1)
        
        echo "Processing $file..."
        
        # Measure execution time using the `time` command
        start_time=$(date +%s.%N)
        ../build/cle-ws "$file" > /dev/null 2>&1
        end_time=$(date +%s.%N)
        
        # Calculate elapsed time
        execution_time=$(echo "$end_time - $start_time" | bc)
        
        # Append results to the CSV file
        echo "$num_samples,$execution_time" >> "$csv_file"
        
        echo "Results for $filename: NumSamples=$num_samples, ExecutionTime=${execution_time}s"
    fi
done

echo "Processing complete. Results saved in $csv_file."