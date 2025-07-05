/*
 * thread_pool.h
 *   - Header file defining the ThreadPool class
*/

#ifndef THREADPOOL_H
#define THREADPOOL_H

#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <atomic>

class ThreadPool
{
    public:
        ThreadPool(int numThreads);             // Constructor
        ~ThreadPool();                          // Destructor
        void enqueue(std::function<void()> task);    // Add a new task to the queue
        void wait();                            // Wait for all tasks to complete

    private:
        std::unique_ptr<std::thread[]> workers;   // Fixed array of worker threads
        std::queue<std::function<void()>> tasks;  // Task queue
        std::mutex queueMutex;
        std::condition_variable condition;
        bool stop;
        std::atomic<size_t> activeTasks;
        std::condition_variable finished;
        int numThreads;
};

#endif  // THREADPOOL_H