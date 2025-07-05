import pandas as pd
import matplotlib.pyplot as plt
import os

# Create charts directory if it doesn't exist
if not os.path.exists('./charts'):
    os.makedirs('./charts')

# Read the CSV file
df = pd.read_csv('./results/execution_times_all_processes_optimization3.csv')

# Get unique sample sizes
sample_sizes = sorted(df['NumSamples'].unique())

# Create a chart for each sample size
for sample_size in sample_sizes:
    # Filter data for the current sample size
    sample_data = df[df['NumSamples'] == sample_size]
    sample_data = sample_data.sort_values('NumProcesses')  # Sort by number of processes

    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Plot the line chart
    plt.plot(sample_data['NumProcesses'], sample_data['ExecutionTime'], 
             marker='o', linestyle='-', linewidth=2, color='blue', label=f'{sample_size:,} samples') 

    # Add title and labels
    plt.title(f'Execution Time vs Number of Processes ({sample_size:,} samples)', fontsize=16)
    plt.xlabel('Number of Processes', fontsize=14)
    plt.ylabel('Execution Time (seconds)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Format x-axis to show only the process counts we have
    plt.xticks(sample_data['NumProcesses'])

    # Add legend
    plt.legend(loc='best')

    # Tight layout to ensure everything fits
    plt.tight_layout()

    # Save the figure
    plt.savefig(f'./charts/optimization3/execution_time_{sample_size}_samples.png', dpi=300)

    # Close the plot to avoid overlapping
    plt.close()

# Create a combined chart with all sample sizes
plt.figure(figsize=(12, 8))

# Plot a line for each sample size
for sample_size in sample_sizes:
    sample_data = df[df['NumSamples'] == sample_size]
    sample_data = sample_data.sort_values('NumProcesses')  # Sort by number of processes
    plt.plot(sample_data['NumProcesses'], sample_data['ExecutionTime'], 
             marker='o', linestyle='-', linewidth=2, label=f'{sample_size:,} samples')

# Add title and labels
plt.title('Execution Time vs Number of Processes (All Sample Sizes)', fontsize=16)
plt.xlabel('Number of Processes', fontsize=14)
plt.ylabel('Execution Time (seconds)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis to show only the process counts we have
plt.xticks(sorted(df['NumProcesses'].unique()))

# Add legend
plt.legend(title='Sample Size', loc='best')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the combined chart
plt.savefig('./charts/optimization3/execution_time_all_samples_combined.png', dpi=300)

# Plot speedup for all sample sizes
plt.figure(figsize=(12, 8))

# Plot speedup for each sample size
for sample_size in sample_sizes:
    sample_data = df[df['NumSamples'] == sample_size]
    sample_data = sample_data.sort_values('NumProcesses')  # Sort by number of processes
    
    # Calculate speedup: Speedup = T1 / Tp
    t1 = sample_data[sample_data['NumProcesses'] == 1]['ExecutionTime'].values[0]
    sample_data['Speedup'] = t1 / sample_data['ExecutionTime']
    
    # Plot speedup
    plt.plot(sample_data['NumProcesses'], sample_data['Speedup'], 
             marker='o', linestyle='-', linewidth=2, label=f'{sample_size:,} samples')

# Add title and labels
plt.title('Speedup vs Number of Processes (All Sample Sizes)', fontsize=16)
plt.xlabel('Number of Processes', fontsize=14)
plt.ylabel('Speedup', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis to show only the process counts we have
plt.xticks(sorted(df['NumProcesses'].unique()))

# Add legend
plt.legend(title='Sample Size', loc='best')

# Tight layout to ensure everything fits
plt.tight_layout()

# Save the speedup chart
plt.savefig('./charts/optimization3/speedup_all_samples_combined.png', dpi=300)

print("Charts have been saved to the 'charts' directory.")