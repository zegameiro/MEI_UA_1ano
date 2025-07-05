import os
import subprocess
import time
import matplotlib.pyplot as plt
import argparse
import numpy as np

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def run_with_progressive_threads(executable, input_file, output_file):
    results = []
    for threads in range(1, 17):
        start_time = time.time()
        subprocess.run([executable, '--threads', str(threads), input_file])
        end_time = time.time()
        elapsed_time = end_time - start_time
        results.append((threads, elapsed_time))
        print(f"Threads: {threads}, Time: {elapsed_time:.2f} seconds")
    
    with open(output_file, 'w') as f:
        for threads, elapsed_time in results:
            f.write(f"{threads},{elapsed_time}\n")
    
    return results

def run_with_doubling_file_size(executable, input_file, output_file, max_multiplier=128):
    results = []
    original_size = os.path.getsize(input_file)
    current_multiplier = 1
    current_file = input_file

    while current_multiplier < max_multiplier:
        start_time = time.time()
        subprocess.run([executable, '--threads', '1', current_file])
        end_time = time.time()
        elapsed_time = end_time - start_time
        results.append((current_multiplier, elapsed_time))
        print(f"Size Multiplier: {current_multiplier}, Time: {elapsed_time:.2f} seconds")

        if current_multiplier < max_multiplier:
            new_file = f"{input_file}.{current_multiplier * 2}"
            with open(current_file, 'r') as src, open(new_file, 'w') as dst:
                for _ in range(2):
                    src.seek(0)
                    dst.write(src.read())
            current_file = new_file
            current_multiplier *= 2
    
    with open(output_file, 'w') as f:
        for multiplier, elapsed_time in results:
            f.write(f"{multiplier},{elapsed_time}\n")
    
    return results

def compare_multithread_to_single_thread(executable, input_file, output_file, max_multiplier=128):
    results = []
    original_size = os.path.getsize(input_file)
    current_multiplier = 1
    current_file = input_file

    while current_multiplier < max_multiplier:
        # Single-threaded run
        start_time = time.time()
        subprocess.run([executable, '--threads', '1', current_file])
        end_time = time.time()
        single_thread_time = end_time - start_time

        # Multi-threaded run
        start_time = time.time()
        subprocess.run([executable, '--threads', str(os.cpu_count()), current_file])
        end_time = time.time()
        multi_thread_time = end_time - start_time

        speedup = single_thread_time / multi_thread_time
        efficiency = speedup / os.cpu_count()
        results.append((current_multiplier, single_thread_time, multi_thread_time, speedup, efficiency))
        print(f"Size Multiplier: {current_multiplier}, Single-thread Time: {single_thread_time:.2f} seconds, Multi-thread Time: {multi_thread_time:.2f} seconds, Speedup: {speedup:.2f}, Efficiency: {efficiency:.2f}")

        if current_multiplier < max_multiplier:
            new_file = f"{input_file}.{current_multiplier * 2}"
            with open(current_file, 'r') as src, open(new_file, 'w') as dst:
                for _ in range(2):
                    src.seek(0)
                    dst.write(src.read())
            current_file = new_file
            current_multiplier *= 2
    
    with open(output_file, 'w') as f:
        for multiplier, single_thread_time, multi_thread_time, speedup, efficiency in results:
            f.write(f"{multiplier},{single_thread_time},{multi_thread_time},{speedup},{efficiency}\n")
    
    return results

def compare_atomic_to_mutex_with_varying_threads(executable, input_file, output_file, max_threads=16):
    results = []
    for threads in range(2, max_threads + 1):
        # Mutex run
        start_time = time.time()
        subprocess.run([executable, '--threads', str(threads), input_file])
        end_time = time.time()
        mutex_time = end_time - start_time

        # Atomic run
        start_time = time.time()
        subprocess.run([executable, '--threads', str(threads), '--atomic', input_file])
        end_time = time.time()
        atomic_time = end_time - start_time

        speedup = mutex_time / atomic_time
        efficiency = speedup / threads
        results.append((threads, mutex_time, atomic_time, speedup, efficiency))
        print(f"Threads: {threads}, Mutex Time: {mutex_time:.2f} seconds, Atomic Time: {atomic_time:.2f} seconds, Speedup: {speedup:.2f}, Efficiency: {efficiency:.2f}")
    
    with open(output_file, 'w') as f:
        for threads, mutex_time, atomic_time, speedup, efficiency in results:
            f.write(f"{threads},{mutex_time},{atomic_time},{speedup},{efficiency}\n")
    
    return results

def plot_results(results, labels, title, xlabel, ylabel, output_image, log_scale=False, y_index=1):
    plt.figure()
    for result, label in zip(results, labels):
        x = [r[0] for r in result]
        y = [r[y_index] for r in result]
        plt.plot(x, y, marker='o', label=label)
    if log_scale:
        plt.xscale('log')
        plt.yscale('log')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.savefig(output_image)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run performance tests on cle-wc program.")
    parser.add_argument("--output-dir", type=str, default="results", help="Output directory for results")
    parser.add_argument("--executable", type=str, default="./cle-wc", help="Path to the executable")
    parser.add_argument("--input-file", type=str, default="./input_files/books.txt", help="Path to the input file")
    args = parser.parse_args()

    executable = args.executable
    input_file = args.input_file
    output_dir = args.output_dir

    # Create results directories
    create_directory(f"{output_dir}/csv")
    create_directory(f"{output_dir}/images")

    # Run with progressively more threads
    progressive_threads_results = run_with_progressive_threads(executable, input_file, f"{output_dir}/csv/progressive_threads_results.csv")
    plot_results([progressive_threads_results], ["Progressive Threads"], "Time vs Number of Threads", "Number of Threads", "Time (seconds)", f"{output_dir}/images/progressive_threads.png")

    # Compare multithread to single thread with doubling file size
    compare_results = compare_multithread_to_single_thread(executable, input_file, f"{output_dir}/csv/compare_results.csv")
    single_thread_results = [(result[0], result[1]) for result in compare_results]
    multi_thread_results = [(result[0], result[2]) for result in compare_results]
    plot_results([single_thread_results], ["Single-thread"], "Time vs File Size Multiplier (Single-thread)", "File Size Multiplier", "Time (seconds)", f"{output_dir}/images/single_thread.png")
    plot_results([multi_thread_results], ["Multi-thread"], "Time vs File Size Multiplier (Multi-thread)", "File Size Multiplier", "Time (seconds)", f"{output_dir}/images/multi_thread.png")
    plot_results([single_thread_results, multi_thread_results], ["Single-thread", "Multi-thread"], "Single-thread vs Multi-thread", "File Size Multiplier", "Time (seconds)", f"{output_dir}/images/comparison.png")
    plot_results([single_thread_results, multi_thread_results], ["Single-thread", "Multi-thread"], "Single-thread vs Multi-thread (with Log Scale)", "File Size Multiplier", "Time (seconds)", f"{output_dir}/images/comparison_log.png", log_scale=True)
    plot_results([compare_results], ["Speedup"], "Speedup vs File Size Multiplier", "File Size Multiplier", "Speedup", f"{output_dir}/images/speedup.png", y_index=3)
    plot_results([compare_results], ["Efficiency"], "Efficiency vs File Size Multiplier", "File Size Multiplier", "Efficiency", f"{output_dir}/images/efficiency.png", y_index=4)

    # Create a 16x multiplier file for atomic vs mutex comparison
    multiplier_file = f"{input_file}.16x"
    with open(input_file, 'r') as src, open(multiplier_file, 'w') as dst:
        for _ in range(16):
            src.seek(0)
            dst.write(src.read())

    # Compare atomic to mutex with varying threads
    atomic_mutex_results = compare_atomic_to_mutex_with_varying_threads(executable, multiplier_file, f"{output_dir}/csv/atomic_mutex_results.csv")
    mutex_results = [(result[0], result[1]) for result in atomic_mutex_results]
    atomic_results = [(result[0], result[2]) for result in atomic_mutex_results]
    plot_results([mutex_results], ["Mutex"], "Time vs Number of Threads (Mutex)", "Number of Threads", "Time (seconds)", f"{output_dir}/images/mutex.png")
    plot_results([atomic_results], ["Atomic"], "Time vs Number of Threads (Atomic)", "Number of Threads", "Time (seconds)", f"{output_dir}/images/atomic.png")
    plot_results([mutex_results, atomic_results], ["Mutex", "Atomic"], "Mutex vs Atomic", "Number of Threads", "Time (seconds)", f"{output_dir}/images/mutex_vs_atomic.png")
    plot_results([mutex_results, atomic_results], ["Mutex", "Atomic"], "Mutex vs Atomic (with Log Scale)", "Number of Threads", "Time (seconds)", f"{output_dir}/images/mutex_vs_atomic_log.png", log_scale=True)
    plot_results([atomic_mutex_results], ["Efficiency"], "Efficiency vs Number of Threads", "Number of Threads", "Efficiency", f"{output_dir}/images/efficiency_atomic.png", y_index=4)

    print("Done!")
