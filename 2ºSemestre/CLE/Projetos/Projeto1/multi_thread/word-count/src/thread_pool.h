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

using namespace std;

class ThreadPool
{
    public:
        ThreadPool(int numThreads);             // Constructor
        ~ThreadPool();                          // Destructor
        void enqueue(function<void()> task);    // Add a new task to the queue
        void wait();                            // Wait for all tasks to complete

    private:
        unique_ptr<thread[]> workers;   // Fixed array of worker threads
        queue<function<void()>> tasks;  // Task queue
        mutex queueMutex;
        condition_variable condition;
        bool stop;
        atomic<size_t> activeTasks;
        condition_variable finished;
        int numThreads;
};

#endif  // THREADPOOL_H