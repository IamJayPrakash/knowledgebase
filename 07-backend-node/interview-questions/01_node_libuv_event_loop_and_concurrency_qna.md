# Node.js Master Interview Bank: Part 1 (Q1 - Q20)
## Libuv, 6 Event Loop Phases & Concurrency Internals

---

### Q1: Diagram and explain the 6 phases of the Libuv Event Loop in Node.js.
**Answer:**

```
   ┌───────────────────────────────────────────────────────────┐
┌─►│                      1. TIMERS                            │ ──► Executes setTimeout & setInterval callbacks
│  └─────────────────────────────┬─────────────────────────────┘
│                                │
│                                ▼
│  ┌───────────────────────────────────────────────────────────┐
│  │                  2. PENDING CALLBACKS                     │ ──► Executes deferred I/O callbacks (TCP errors, etc.)
│  └─────────────────────────────┬─────────────────────────────┘
│                                │
│                                ▼
│  ┌───────────────────────────────────────────────────────────┐
│  │                  3. IDLE, PREPARE                         │ ──► Internal Libuv subsystem preparation
│  └─────────────────────────────┬─────────────────────────────┘
│                                │
│                                ▼
│  ┌───────────────────────────────────────────────────────────┐
│  │                      4. POLL                              │ ──► Retrieves new I/O events; blocks if idle
│  └─────────────────────────────┬─────────────────────────────┘
│                                │
│                                ▼
│  ┌───────────────────────────────────────────────────────────┐
│  │                      5. CHECK                             │ ──► Executes setImmediate() callbacks
│  └─────────────────────────────┬─────────────────────────────┘
│                                │
│                                ▼
│  ┌───────────────────────────────────────────────────────────┐
│  │                  6. CLOSE CALLBACKS                       │ ──► Executes socket.on('close'), handle disposal
│  └─────────────────────────────┬─────────────────────────────┘
│                                │
└────────────────────────────────┴─────────────────────────────┘
```

**Intermediate Microtask Drain:**
Between **every single phase** of the event loop (and between individual callbacks in modern Node.js), the engine drains:
1. `process.nextTick()` queue.
2. Promise microtask queue.

---

### Q2: What is the difference between `process.nextTick()` and `setImmediate()`?
**Answer:**
- **`process.nextTick(callback)`:**
  - Despite its name, it does **not belong to the Libuv event loop**.
  - It runs **immediately after the current operation finishes**, before the event loop advances to the next phase!
  - *Risk:* Recursively calling `process.nextTick()` causes **Event Loop Starvation**, locking the thread and preventing all I/O, timers, and `setImmediate()` from running!
- **`setImmediate(callback)`:**
  - Belongs directly to the Libuv event loop's **Check Phase**.
  - Runs on the **next turn of the event loop** after the Poll phase.
  - Yields to other I/O operations, ensuring fair CPU time sharing.

---

### Q3: What will be the output of this code snippet? Explain why.
```javascript
const fs = require('fs');

fs.readFile(__filename, () => {
  setTimeout(() => console.log('setTimeout'), 0);
  setImmediate(() => console.log('setImmediate'));
});
```
**Output:**
```
setImmediate
setTimeout
```
**Why:**
- When the `fs.readFile` callback runs, the event loop is inside the **Poll Phase**.
- The code schedules a timer (`setTimeout`) and an immediate callback (`setImmediate`).
- The event loop exits the Poll phase and immediately transitions to the **Check Phase**, where it executes `setImmediate`!
- The `setTimeout` callback must wait until the event loop wraps around to the **Timers Phase** on the next loop iteration.

---

### Q4: What is the Libuv Thread Pool and what operations use it?
**Answer:**
- While JavaScript execution is single-threaded, Node.js offloads blocking system operations to a **C-level Thread Pool** managed by Libuv.
- **Operations that use the Thread Pool:**
  1. **File System I/O (`fs.*`):** OS file system APIs (POSIX `read`/`write`) are fundamentally blocking in operating systems.
  2. **DNS Lookups (`dns.lookup`):** Resolves hostnames via blocking `getaddrinfo()`.
  3. **Cryptography (`crypto.pbkdf2`, `crypto.randomBytes`):** Heavy CPU hashing algorithms.
  4. **Compression (`zlib.*`):** Deflate and gzip calculations.
- *Network Sockets (`http`, `https`, `net`, `tls`):* **DO NOT USE THE THREAD POOL!** They use non-blocking asynchronous OS primitives (`epoll` on Linux, `kqueue` on macOS, `IOCP` on Windows).

---

### Q5: What is the default size of `UV_THREADPOOL_SIZE` and how do you change it?
**Answer:**
- Default size is **4 threads**.
- If 5 concurrent clients request `crypto.pbkdf2()` simultaneously, the 5th request is queued and delayed until one of the first 4 finishes!
- **Changing the Size:**
  Set the environment variable before launching the Node process (max value: 1024):
  ```bash
  UV_THREADPOOL_SIZE=64 node server.js
  ```
  *(Note: Setting `process.env.UV_THREADPOOL_SIZE = 64` inside JavaScript code is usually ignored because Libuv initializes its threadpool before user code executes).*

---

### Q6: Compare Cluster Module vs Worker Threads in Node.js.
**Answer:**
| Feature | Cluster Module (`node:cluster`) | Worker Threads (`node:worker_threads`) |
| :--- | :--- | :--- |
| **Model** | **Multi-Process** (Forks independent OS processes via `child_process.fork()`). | **Multi-Thread** (Spawns threads within the **same OS process**). |
| **Memory** | Completely isolated memory spaces. | **Shared memory space** (supports `SharedArrayBuffer`). |
| **Port Sharing**| Master process automatically shares Server TCP port (Round-Robin). | Does NOT automatically share server ports; must communicate via messages. |
| **IPC Overhead**| Slower (data serialized via JSON over IPC pipes). | **Instant** for shared array buffers; fast message passing. |
| **Best Used For**| **Horizontal HTTP server scaling** across all CPU cores. | **CPU-bound tasks** (image processing, PDF generation, cryptography). |

---

### Q7: How does Event Loop Starvation happen in Node.js and how do you prevent it?
**Answer:**
- Occurs when synchronous execution on the Call Stack or in the `nextTick` queue monopolizes the single CPU thread (e.g. running a synchronous JSON parser on a 100MB file or an infinite loop).
- **Symptoms:** Server stops responding to HTTP requests, health probes fail, socket connections drop.
- **Prevention:**
  1. Offload CPU calculations to Worker Threads or external background workers.
  2. Partition large loops into asynchronous chunks using `setImmediate()`:
     ```javascript
     function processChunk(index) {
       // Process batch...
       if (hasMore) setImmediate(() => processChunk(index + 1));
     }
     ```

---

### Q8: What is the difference between `fork()`, `spawn()`, and `exec()` in `child_process`?
**Answer:**
- **`exec(cmd, callback)`:** Spawns a shell, executes command, buffers entire output in memory (max 1MB buffer), and returns output in callback. Vulnerable to shell injection.
- **`spawn(cmd, args)`:** Spawns a new process without a shell. Streams data using **Node.js Streams** (`stdout`, `stderr`). Ideal for large outputs.
- **`fork(modulePath)`:** Specialization of `spawn()` specifically for launching **new Node.js instances**. Automatically establishes a dedicated Inter-Process Communication (**IPC**) channel (`child.send()`, `process.on('message')`).

---

### Q9: How do Unhandled Rejections and Uncaught Exceptions differ in Node.js?
**Answer:**
- **`uncaughtException`:** Synchronous JavaScript error that bubbled all the way to the top of the call stack without a `try-catch`.
  - *Rule:* The application state is corrupted! Log the error and **terminate the process immediately with a non-zero exit code**: `process.exit(1)`. Rely on process managers (PM2/Kubernetes) to restart a clean instance.
- **`unhandledRejection`:** A Promise rejected without a `.catch()` or `try-catch` block. In modern Node.js, unhandled rejections terminate the process with exit code 1 by default unless a custom listener is attached.

---

### Q10: How does Node.js resolve module paths (Module Resolution Algorithm)?
**Answer:**
When you call `require('foo')`:
1. Checks **Core Modules** (`fs`, `path`, `http`). If matched, returns immediately.
2. If starts with `./`, `/`, or `../`: Resolves relative/absolute file path (checks `.js`, `.json`, `.node`).
3. If bare specifier (`foo`):
   - Searches for `/node_modules/foo` in current directory.
   - If not found, ascends to `../node_modules/foo`, continuing up the directory tree until the filesystem root is reached.
4. Reads package `package.json` to find `exports` or `main` entry point.

---

### Q11: How do you profile Node.js CPU performance in production?
**Answer:**
Run Node with the V8 profiler flag:
```bash
node --prof app.js
```
Generate human-readable report:
```bash
node --prof-process isolate-*.log > processed.txt
```
Or connect Chrome DevTools via **`node --inspect app.js`** $\to$ open `chrome://inspect` and record an interactive CPU Profile.

---

### Q12: What is the difference between CommonJS and ESM in Node.js?
**Answer:**
- CommonJS uses `require()` and `module.exports` (synchronous, dynamic).
- ESM uses `import` and `export` (asynchronous, static, supports top-level await).
- To use ESM in Node.js: Add `"type": "module"` in `package.json` or use `.mjs` file extension.

---

### Q13: What is `EventEmitter` and how do you prevent Memory Leak warnings?
**Answer:**
- `EventEmitter` is the core publish-subscribe mechanism in Node.js (`emitter.on()`, `emitter.emit()`).
- By default, attaching $> 10$ listeners to a single event prints a warning: `MaxListenersExceededWarning: Possible EventEmitter memory leak detected`.
- **Prevention:** Always remove listeners when disposing handles: `emitter.off('event', handler)` or `emitter.removeListener()`.

---

### Q14: What is `AsyncLocalStorage` in `node:async_hooks`?
**Answer:**
- Provides asynchronous request-scoped storage across asynchronous execution chains (the Node.js equivalent of Java's `ThreadLocal`).
- **Use Case:** Propagating a unique `traceId` or authenticated user context through deeply nested asynchronous services without passing `traceId` as an argument to every function:

```javascript
const { AsyncLocalStorage } = require('node:async_hooks');
const asyncLocalStorage = new AsyncLocalStorage();

app.use((req, res, next) => {
  const traceId = req.headers['x-trace-id'] || crypto.randomUUID();
  asyncLocalStorage.run({ traceId }, () => next());
});

function logService(msg) {
  const store = asyncLocalStorage.getStore();
  console.log(`[Trace: ${store?.traceId}] ${msg}`);
}
```

---

### Q15: How does Node.js handle DNS caching and why can `dns.lookup` cause bottlenecks?
**Answer:**
- **The Bottleneck:** By default, Node's `http.request` uses `dns.lookup()`, which calls the operating system's `getaddrinfo()`.
  - It runs on the **Libuv thread pool (4 threads)** and **does NOT cache DNS responses**!
  - Under high-volume API traffic, the 4 threads are completely saturated by DNS queries.
- **Solution:** Use **`dns.resolve4()`** (uses non-blocking c-ares over async sockets) or use an HTTP agent with connection pooling and DNS caching (`agentkeepalive`).

---

### Q16: What is the difference between `fs.readFile()` and `fs.createReadStream()`?
**Answer:**
- **`fs.readFile()`:** Loads the **entire file into memory (Buffer)** before invoking the callback. Fails with OutOfMemoryError on files larger than available RAM or V8 heap limit.
- **`fs.createReadStream()`:** Reads file in small sequential chunks (default: 64 KB), streaming data through memory with $O(1)$ constant memory overhead.

---

### Q17: What is `process.memoryUsage()` and what does each metric mean?
**Answer:**
- **`rss` (Resident Set Size):** Total physical RAM occupied by the Node.js process (Heap + Stack + Native Libuv C code).
- **`heapTotal`:** Total memory allocated by V8 for the JavaScript heap.
- **`heapUsed`:** Actual memory currently occupied by live JavaScript objects.
- **`external`:** Memory bound to C++ objects managed outside the V8 heap (e.g. Node.js `Buffer` allocations).

---

### Q18: What is the V8 Heap Limit in Node.js and how do you increase it?
**Answer:**
- By default on 64-bit systems, V8 caps heap usage at **~2.0 GB** to prevent long garbage collection pauses.
- To increase the heap limit for memory-intensive data processing pipelines:
  ```bash
  node --max-old-space-size=8192 server.js # Expands limit to 8 GB RAM
  ```

---

### Q19: What is `node:test` (Native Test Runner in Node 18+)?
**Answer:**
- Built-in test runner eliminating the need for external testing dependencies (like Jest or Mocha):
  ```javascript
  const { test, describe, it } = require('node:test');
  const assert = require('node:assert');

  test('synchronous test', () => {
    assert.strictEqual(1 + 1, 2);
  });
  ```
- Run via: `node --test`. Extremely fast execution with zero overhead.

---

### Q20: What are Diagnostic Reports in Node.js (`process.report`)?
**Answer:**
- Generates a detailed JSON diagnostics report containing call stacks, native OS thread traces, loaded libraries, memory usage, and OS environment variables:
  `process.report.writeReport('crash-report.json');`
- Can be triggered automatically on fatal OutOfMemory or unhandled exception crashes (`--report-on-fatalerror`).
