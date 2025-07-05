/*
 * thread_pool.cpp
 *   - Implements a thread pool for parallel processing
*/

#include "thread_pool.h"
#include <iostream>

// Constructor: Initializes a fixed array of worker threads
ThreadPool::ThreadPool(int num_threads) : stop(false), activeTasks(0), numThreads(num_threads) {
    workers = make_unique<thread[]>(num_threads); // Allocate array of threads
    for (int i = 0; i < num_threads; ++i) {
        workers[i] = thread([this] {
            while (true) {
                function<void()> task;
                {
                    unique_lock<mutex> lock(queueMutex);
                    condition.wait(lock, [this] { return stop || !tasks.empty(); });
                    if (stop && tasks.empty()) return;
                    task = move(tasks.front());
                    tasks.pop();
                    ++activeTasks;
                }
                task();
                {
                    lock_guard<mutex> lock(queueMutex);
                    --activeTasks;
                    if (tasks.empty() && activeTasks == 0) finished.notify_all();
                }
            }
        });
    }
}

// Add a new task to the queue
void ThreadPool::enqueue(function<void()> task) {
    {
        unique_lock<mutex> lock(queueMutex);
        tasks.push(move(task));
    }
    condition.notify_one();
}

// Wait for all tasks to complete
void ThreadPool::wait() {
    unique_lock<mutex> lock(queueMutex);
    finished.wait(lock, [this] { return tasks.empty() && activeTasks == 0; });
}

// Destructor: Ensures all threads are joined before destruction
ThreadPool::~ThreadPool() {
    {
        unique_lock<mutex> lock(queueMutex);
        stop = true;
    }
    condition.notify_all();
    for (int i = 0; i < numThreads; ++i) {
        if (workers[i].joinable()) workers[i].join();
    }
}