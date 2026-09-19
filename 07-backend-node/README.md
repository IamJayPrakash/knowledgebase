# 🟢 Node.js Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index from **Core Runtime Mechanics to Distributed Backend Engineering** for Senior Technical Lead & SDE-2/3 interviews.

---

## 📌 How to Use This Section
- Use this `README.md` as your master index and curriculum roadmap for Node.js.
- Create single concept files inside `04-node/` (e.g., `01_libuv_event_loop_phases.md`) as you learn and add your notes, code snippets, and interview pointers.

---

## 🗺️ Learning Roadmap & Concept Index

### 1. Node.js Architecture & Event Loop
- [ ] `01_node_architecture_v8_libuv.md` — Node.js runtime layers (V8, Libuv, c-ares, http-parser/llhttp, C++ bindings), Thread pool default & sizing (`UV_THREADPOOL_SIZE`).
- [ ] `02_libuv_event_loop_phases.md` — 6 phases of Libuv Event Loop (Timers, Pending Callbacks, Idle/Prepare, Poll, Check, Close), Phase transitions.
- [ ] `03_process_nexttick_microtasks_setimmediate.md` — `process.nextTick` vs `Promise` microtask queue vs `setImmediate` vs `setTimeout`.

### 2. Streams, Buffers & Event Emitter
- [ ] `04_buffers_and_binary_data.md` — Buffer allocation (`Buffer.alloc` vs `Buffer.allocUnsafe`), Memory layout outside V8 heap, Encoding (`utf-8`, `hex`, `base64`).
- [ ] `05_streams_and_backpressure.md` — 4 Stream types (`Readable`, `Writable`, `Duplex`, `Transform`), `pipe()` and `pipeline()`, Backpressure management (`highWaterMark`, `drain` event).
- [ ] `06_event_emitter_pattern.md` — EventEmitter implementation, Listener limits (`setMaxListeners`), Memory leaks from orphaned listeners.

### 3. Concurrency, Multithreading & Scaling
- [ ] `07_child_processes.md` — `exec` vs `execFile` vs `spawn` vs `fork`, Inter-Process Communication (IPC) channels.
- [ ] `08_worker_threads_and_shared_memory.md` — `worker_threads` module, SharedArrayBuffer & Atomics, Worker pool architecture for CPU-bound tasks.
- [ ] `09_clustering_and_load_balancing.md` — Node `cluster` module, Master-Worker model, Zero-downtime reloads (PM2 / Kubernetes rolling updates).

### 4. Enterprise Production Patterns & Debugging
- [ ] `10_memory_leaks_and_profiling.md` — Diagnosing memory leaks, Heap snapshots, CPU profiling with `--inspect` & Chrome DevTools, Clinic.js.
- [ ] `11_error_handling_and_graceful_shutdown.md` — `uncaughtException` vs `unhandledRejection`, SIGINT/SIGTERM handlers, Draining active HTTP connections.
- [ ] `12_security_best_practices.md` — ReDoS (Regular Expression Denial of Service), Rate limiting, Helmet middleware, Input sanitization, Dependency vulnerability audits (`npm audit`).

---

## 🎯 Master Interview Questions (60 Deep Dive Questions)

For dedicated deep-dive technical interview preparation with runnable code and diagrams:
- 📖 [Node.js Master Interview Directory](./interview-questions/README.md)
- 🚀 [Part 1: Libuv Event Loop, Threadpool & Concurrency (Q1 - Q20)](./interview-questions/01_node_libuv_event_loop_and_concurrency_qna.md)
- 🌊 [Part 2: Streams, Buffers, Memory & Heap Analysis (Q21 - Q40)](./interview-questions/02_node_streams_buffers_and_memory_qna.md)
- 🛡️ [Part 3: Express/Fastify, Security & Production Scaling (Q41 - Q60)](./interview-questions/03_node_express_security_and_production_scaling_qna.md)

---

## 💡 High-Yield Senior Interview Questions Pointers


1. **How does Node.js handle I/O without blocking the main thread?**
   * *Answer Pointer:* Non-blocking OS primitives (epoll on Linux, kqueue on macOS, IOCP on Windows) are driven by Libuv's event loop. Blocking tasks (File I/O, DNS) are delegated to the Libuv C thread pool.
2. **Difference between `process.nextTick()` and `setImmediate()`?**
   * *Answer Pointer:* `process.nextTick()` fires immediately after the current operation finishes, BEFORE the event loop continues to any phase. `setImmediate()` fires during the **Check phase** of the Libuv event loop.
3. **What is Backpressure in Node Streams and why is it critical?**
   * *Answer Pointer:* Backpressure occurs when data is read faster than the writable stream can consume it. If unhandled, unconsumed chunks accumulate in RAM, leading to Out-Of-Memory crashes. Solved using `.pipe()` or monitoring `stream.write()` boolean return value.
