# 🟢 Node.js Interview Questions & System Coding Index

> A categorized index of **Libuv Engine Internals, Stream Pipelines, Worker Threads, Memory Profiling, and Backend Architecture Questions** for Senior Node.js Interviews.

---

## 📌 How to Use This Directory

- Add individual markdown files for specific Node.js interview questions in this folder (e.g., `01_stream_file_upload.md`, `02_worker_threads_pool.md`).
- Use this `README.md` as your index and checklist.

---

## 📑 Master Interview Question Banks (60 Deep Dive Questions)

| Part | File | Topics Covered | Range |
| :--- | :--- | :--- | :--- |
| **Part 1** | [Libuv Event Loop, Threadpool & Concurrency](./01_node_libuv_event_loop_and_concurrency_qna.md) | Libuv 6 phases, Microtasks, `process.nextTick`, Threadpool, Worker Threads, IPC | Q1 – Q20 |
| **Part 2** | [Streams, Buffers, Memory & Garbage Collection](./02_node_streams_buffers_and_memory_qna.md) | 4 Stream types, Backpressure, `pipeline()`, Buffers, V8 Heap, Heapdumps, Leaks | Q21 – Q40 |
| **Part 3** | [Express, Fastify, Security & Production Scaling](./03_node_express_security_and_production_scaling_qna.md) | Express vs Fastify, Middleware, ReDoS, SSRF, Cluster, Graceful Shutdown, PM2 | Q41 – Q60 |

---

## 📌 Coding & Scenario Challenges

- [x] Stream Pipelines & Backpressure (`02_node_streams_buffers_and_memory_qna.md`)
- [x] Worker Threads Pool Implementation (`01_node_libuv_event_loop_and_concurrency_qna.md`)
- [x] Memory Leak Diagnosis & Heapdump Analysis (`02_node_streams_buffers_and_memory_qna.md`)
- [x] Production Graceful Shutdown & Zero Downtime Reloads (`03_node_express_security_and_production_scaling_qna.md`)
