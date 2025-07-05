/*
 * thread_pool.cpp
 *   - Implements a thread pool for parallel processing
*/

#include "thread_pool.h"
#include <iostream>

// Constructor: Initializes a fixed array of worker threads
ThreadPool::ThreadPool(int num_threads) : stop(false), activeTasks(0), numThreads(num_threads) {
    workers = std::make_unique<std::thread[]>(num_threads); // Allocate array of threads
    for (int i = 0; i < num_threads; ++i) {
        workers[i] = std::thread([this] {
            while (true) {
                std::function<void()> task;
                {
                    std::unique_lock<std::mutex> lock(queueMutex);
                    condition.wait(lock, [this] { return stop || !tasks.empty(); });
                    if (stop && tasks.empty()) return;
                    task = move(tasks.front());
                    tasks.pop();
                    ++activeTasks;
                }
                task();
                {
                    std::lock_guard<std::mutex> lock(queueMutex);
                    --activeTasks;
                    if (tasks.empty() && activeTasks == 0) finished.notify_all();
                }
            }
        });
    }
}

// Add a new task to the queue
void ThreadPool::enqueue(std::function<void()> task) {
    {
        std::unique_lock<std::mutex> lock(queueMutex);
        tasks.push(move(task));
    }
    condition.notify_one();
}

// Wait for all tasks to complete
void ThreadPool::wait() {
    std::unique_lock<std::mutex> lock(queueMutex);
    finished.wait(lock, [this] { return tasks.empty() && activeTasks == 0; });
}

// Destructor: Ensures all threads are joined before destruction
ThreadPool::~ThreadPool() {
    {
        std::unique_lock<std::mutex> lock(queueMutex);
        stop = true;
    }
    condition.notify_all();
    for (int i = 0; i < numThreads; ++i) {
        if (workers[i].joinable()) workers[i].join();
    }
}