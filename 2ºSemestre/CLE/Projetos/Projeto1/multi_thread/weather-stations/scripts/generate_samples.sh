#!/bin/bash

samples=10000
max_samples=1000000000
output_dir="../samples"

# Create the output directory if it doesn't exist
if [ ! -d "$output_dir" ]; then
    mkdir "$output_dir"
    echo "Created directory: $output_dir"
fi

# Loop to generate samples, doubling each time
while [ $samples -le $max_samples ]
do
    echo "Generating $samples samples..."
    ../build/cle-samples $samples > "$output_dir/samples_$samples.txt" # Redirect output to a file in the directory
    samples=$((samples * 2))
done

echo "Sample generation complete."