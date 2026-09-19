# 🟢 Node.js Interview Questions & System Coding Index

> A categorized index of **Libuv Engine Internals, Stream Pipelines, Worker Threads, Memory Profiling, and Backend Architecture Questions** for Senior Node.js Interviews.

---

## 📌 How to Use This Directory
- Add individual markdown files for specific Node.js interview questions in this folder (e.g., `01_stream_file_upload.md`, `02_worker_threads_pool.md`).
- Use this `README.md` as your index and checklist.

---

## 📑 Interview Questions Index

### 1. Rapid-Fire / Short Questions
- [ ] `short_questions_event_loop.md` — Libuv phases, `process.nextTick` vs `setImmediate`, `UV_THREADPOOL_SIZE`.
- [ ] `short_questions_streams.md` — 4 Stream types, Backpressure, `highWaterMark` default values.

### 2. Backend Coding & Stream Processing Challenges
- [ ] `coding_stream_large_file_transform.md` — Process a 10GB CSV file line-by-line without exceeding 50MB RAM using Node Streams.
- [ ] `coding_custom_worker_pool.md` — Build a reusable `WorkerThreadPool` to process CPU-heavy tasks across worker threads.
- [ ] `coding_rate_limiter_middleware.md` — Implement a sliding-window rate limiter middleware for Express/Fastify using Redis.
- [ ] `coding_custom_event_emitter.md` — Build a memory-safe custom EventEmitter with memory leak detection.

### 3. Senior Lead & Production Outage Scenarios
- [ ] `scenario_cpu_100_percent_spike.md` — Troubleshooting and diagnosing a 100% CPU usage spike on a production Node cluster.
- [ ] `scenario_memory_leak_heapdump.md` — Analyzing heap snapshots to fix a memory leak caused by global event listeners.
