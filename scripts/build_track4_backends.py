# -*- coding: utf-8 -*-
"""
Generator for Track 4: Node.js, Express, Spring Boot, FastAPI, and Backend Runtimes
Generates:
1. 04-node/02_streams_buffers_and_backpressure.md
2. 04-node/03_worker_threads_cluster_and_scaling.md
3. 04-node/04_memory_leaks_and_profiling.md
4. 04-node/interview-questions/top_node_interview_questions.md
5. 04-node/interview-questions/coding_custom_readable_writable_stream.md
6. 05-backend-and-runtimes/node-express/01_express_architecture_and_routing.md
7. 05-backend-and-runtimes/node-express/03_express_error_handling_and_logging.md
8. 05-backend-and-runtimes/java-springboot/02_springboot_security_jwt_oauth2.md
9. 05-backend-and-runtimes/java-springboot/03_springboot_microservices_and_resilience4j.md
10. 05-backend-and-runtimes/ruby-on-rails/02_rails_api_and_sidekiq_jobs.md
11. 05-fastapi/02_pydantic_v2_validation_and_serialization.md
12. 05-fastapi/03_dependency_injection_system.md
13. 05-fastapi/04_background_tasks_and_celery.md
14. 05-fastapi/05_high_performance_asgi_starlette_uvicorn.md
15. 05-fastapi/interview-questions/top_fastapi_interview_questions.md
16. 05-fastapi/interview-questions/coding_rate_limiting_middleware.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "04-node", "02_streams_buffers_and_backpressure.md"): """# Node.js Streams, Buffers, and Backpressure Management

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Socho aapko 10,000 litre paani ek tanki se dusri tanki mein daalna hai.
`fs.readFile` ek **Bohot Bada 10,000 Litre Ka Drum** ek sath uthane jaisa hai: Agar aapke paas itni muscle (RAM memory) nahi hai, toh drum girega aur aapki kamar toot jayegi (Out of Memory Error!).
Node.js Streams ek **Patli Paani Ki Pipe (Garden Hose)** ki tarah hai: Paani thoda-thoda karke 64KB ke chote chote packets (Chunks/Buffers) mein behta rehta hai. RAM mein sirf wahi 64KB rehta hai jo us second pipe mein hai.
**Backpressure**: Agar aage wali tanki ka pipe chota hai aur paani overflow hone laga, toh piche wale nal ko band kar diya jata hai (`readable.pause()`), aur jab aage jagah banti hai tab nal dobara khola jata hai (`readable.resume()`).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **The Four Stream Types**:
   - `Readable`: Source of data (`fs.createReadStream`, `req`).
   - `Writable`: Destination (`fs.createWriteStream`, `res`).
   - `Duplex`: Both readable and writable independently (`net.Socket`).
   - `Transform`: Duplex stream where output is computed from input (`zlib.createGzip`, crypto ciphers).
2. **Buffers**: Fixed-size raw binary memory allocated **outside the V8 heap** in C++ memory via `Buffer.allocUnsafe()` or `Buffer.from()`.
3. **The `highWaterMark`**: The threshold buffer size (Default: 64KB for normal streams, 16 for objectMode). If the internal buffer exceeds this, `writable.write()` returns `false`.
4. **Backpressure Handling**:
   - When `write()` returns `false`, pause the readable stream.
   - Wait for the `'drain'` event on the writable stream before calling `readable.resume()`.
5. **`pipeline()` vs `pipe()`**:
   - Never use `readable.pipe(writable)` in production! `pipe()` does not properly destroy intermediate streams on error, causing file descriptor and memory leaks.
   - Always use `stream.pipeline()` (or `stream/promises`) which automatically cleans up and destroys all streams if any stream fails.

---

## 📊 3. Visual Architecture Diagram

```
                       BACKPRESSURE REGULATION FLOW
                       
  [ Disk File: 10 GB ]
          │
          ▼
  [ Readable Stream ] ──(Pushes 64KB Chunk)──► [ Internal Buffer ]
                                                     │
                                       writable.write(chunk) == false?
                                       ├──► YES: readable.pause() (WAIT!)
                                       │         Writable flushes buffer to network...
                                       │         Writable emits 'drain' event ──► readable.resume()
                                       │
                                       └──► NO: Continue pushing next chunk!
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```javascript
import fs from "node:fs";
import zlib from "node:zlib";
import { pipeline } from "node:stream/promises";

// Production Stream Pipeline with Compression and Error Cleanup
async function compressLargeLogFile(sourcePath, destinationPath) {
  console.log(`Starting stream compression from ${sourcePath}...`);

  try {
    // Line 11: Create read stream with 64KB chunk buffer
    const sourceStream = fs.createReadStream(sourcePath, {
      highWaterMark: 64 * 1024
    });

    // Line 16: Create transform gzip stream
    const gzipTransform = zlib.createGzip({ level: 9 });

    // Line 19: Create destination write stream
    const destinationStream = fs.createWriteStream(destinationPath);

    // Line 22: stream.pipeline automatically forwards errors and destroys streams
    await pipeline(sourceStream, gzipTransform, destinationStream);

    console.log("File compression completed successfully with zero memory overhead!");
  } catch (error) {
    // Line 27: All file descriptors and sockets are automatically closed by pipeline()
    console.error("Stream pipeline failed:", error);
    throw error;
  }
}
```

---

## 🎯 5. The "Interview Pitch"
> "Node.js Streams are the primary mechanism for handling unbounded or massive data transfers with $O(1)$ constant memory overhead. By breaking data into sequential `Buffer` chunks allocated in C++ memory outside the V8 heap, streams prevent process crashes from heap exhaustion. Backpressure occurs when the producer emits data faster than the consumer can write it. When the internal `highWaterMark` buffer is breached, `write()` returns `false`, signaling the readable stream to pause until the writable stream emits the `drain` event. In production, we avoid raw `.pipe()` due to unhandled error leak vulnerabilities and exclusively deploy `stream.pipeline` or `stream/promises`."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: A financial reporting service crashed with `JavaScript heap out of memory` whenever generating end-of-month CSV exports for enterprise clients with 5,000,000 transactions. The Node process memory ballooned past 4 GB.
- **Task**: Enable generation of unlimited multi-gigabyte CSV exports within a strict 256 MB container memory limit.
- **Action**: We rewrote the export pipeline. Instead of loading all database records into a JS array with `knex.select('*')`, we utilized PostgreSQL cursor streaming (`pg-query-stream`) piped through a custom `Transform` stream converting rows to CSV format, piped directly into the HTTP response.
- **Result**: Container RAM consumption dropped from 4.2 GB to a flat 48 MB, file export time sped up by 40%, and zero OOM crashes occurred during peak month-end processing.
""",

    os.path.join(BASE_DIR, "04-node", "03_worker_threads_cluster_and_scaling.md"): """# Node.js Concurrency: Cluster Module vs Worker Threads

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Node.js default mein ek **Single Chef (Single Main Thread)** ki tarah hai. Agar chef ko ek heavy kaam mil jaye (jaise 10,000 page ka password hash calculate karna), toh restaurant ke baki 500 customers ko paani bhi nahi milega (Event Loop freeze!).
**Cluster Module** restaurant ki **4 Nayi Branches (Separate Processes)** kholne jaisa hai: Har branch ka apna alag kitchen hai, apna alag chef hai, aur koi aapas mein memory share nahi karta. Round-robin port sharing hoti hai.
**Worker Threads** ek hi kitchen ke andar **4 Assistant Chefs (Separate Threads)** hire karne jaisa hai: Sab ek hi room mein hain aur ek hi fridge se saman le sakte hain (**SharedArrayBuffer / Shared Memory**).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Single-Threaded Myth**: Node.js JavaScript executes on a single thread (V8), but Libuv uses a 4-thread C++ pool for file I/O, DNS, and crypto.
2. **Cluster Module (Multi-Process)**:
   - Spawns multiple OS processes using `child_process.fork()`.
   - Master process listens on the network port and distributes incoming connections using Round-Robin (except on Windows).
   - Memory is completely isolated; communication is via IPC JSON serialization.
3. **Worker Threads (`worker_threads`) (Multi-Thread)**:
   - Spawns multiple threads inside the **same OS process**.
   - Each worker gets its own V8 isolate and event loop, but shares OS process memory.
   - Supports zero-copy memory sharing using `SharedArrayBuffer` and `Atomics`.
4. **When to use Cluster**: For scaling network throughput across CPU cores (HTTP web servers).
5. **When to use Worker Threads**: For CPU-intensive algorithms (image resizing, video transcoding, PDF generation, cryptographic hashing).

---

## 📊 3. Visual Architecture Diagram

```
         CLUSTER MODULE (Processes)               WORKER THREADS (Threads)
         
            [ Master Process ]                       [ Main Process ]
             (Listens on :80)                         (Event Loop)
             ┌───────┴───────┐                                │
             ▼               ▼                                ▼
       [ Worker P1 ]   [ Worker P2 ]                 ┌─────────────────┐
       (PID: 1021)     (PID: 1022)                   ▼                 ▼
       Isolated RAM    Isolated RAM             [ Thread 1 ]      [ Thread 2 ]
                                                (V8 Isolate)      (V8 Isolate)
                                                     └────────┬────────┘
                                                              ▼
                                                   [ SharedArrayBuffer ]
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```javascript
// ==========================================
// Worker Threads for CPU-Intensive Hashing
// ==========================================
import { Worker, isMainThread, parentPort, workerData } from "node:worker_threads";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);

if (isMainThread) {
  // Main Thread logic
  export function runHeavyComputation(data) {
    return new Promise((resolve, reject) => {
      // Line 14: Spawn worker thread executing this same file
      const worker = new Worker(__filename, {
        workerData: data
      });

      // Line 19: Listen for computation result
      worker.on("message", resolve);
      worker.on("error", reject);
      worker.on("exit", (code) => {
        if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
      });
    });
  }
} else {
  // Line 28: Worker Thread execution environment
  // CPU-heavy calculation running without blocking the main event loop!
  const { iterations } = workerData;
  let hashResult = 0;
  for (let i = 0; i < iterations; i++) {
    hashResult = (hashResult + i) % 1000000007;
  }

  // Line 36: Post result back to main thread
  parentPort.postMessage({ status: "success", result: hashResult });
}
```

---

## 🎯 5. The "Interview Pitch"
> "While Node.js is celebrated for high-concurrency I/O via its non-blocking event loop, CPU-bound operations freeze the single execution thread. To scale across multi-core systems, Node offers two complementary architectures. The `cluster` module forks independent OS processes that share a server port via Libuv round-robin IPC, ideal for horizontal web server scaling. Conversely, `worker_threads` provisions separate V8 isolates within the same process that share memory via `SharedArrayBuffer` and `MessagePort`, ideal for compute-heavy tasks like image processing or cryptography without process creation overhead."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an identity verification backend, an endpoint generated high-resolution cryptographic PDF certificates. Under 50 concurrent requests, the main event loop blocked for 4.5 seconds per PDF, causing all incoming health check ping requests to time out and triggering Kubernetes pod restarts.
- **Task**: Offload PDF rendering to prevent event loop starvation and maintain sub-50ms HTTP API response times.
- **Action**: We introduced a generic worker thread pool (using `piscina`) configured to match available CPU cores. When a certificate request arrived, the task was delegated to the worker pool, leaving the main thread event loop free to handle network I/O.
- **Result**: API response latency dropped from 4,500ms to 22ms, Kubernetes pod restarts fell to 0, and CPU utilization across all 8 cores balanced uniformly at 85%.
""",

    os.path.join(BASE_DIR, "04-node", "04_memory_leaks_and_profiling.md"): """# Diagnosing Production Node.js Memory Leaks and CPU Spikes

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Node.js memory leak ek **Dhire-Dhire Bharte Huye Ship Compartment** jaisa hai: Bahar se dekhne par ship chal rahi hai, lekin andar paani jama ho raha hai. Agar aapne bilge pump (Garbage Collector) nahi chalaya ya leak band nahi kiya, toh ship achanak dub jayegi (`Process out of memory: Crash`).
Heap Profiling ek **Underwater Submarine Camera** hai jo batata hai ki ship ke kis hole se paani ghus raha hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **V8 Heap Structure**:
   - **New Space**: Short-lived allocations (Scavenge GC algorithm, ultra fast).
   - **Old Space**: Objects that survived multiple GC cycles (Mark-Sweep-Compact algorithm).
2. **Common Node.js Leaks**:
   - Unbounded in-memory caches (plain JS objects or Maps without TTL/eviction).
   - Leaked event listeners (`emitter.setMaxListeners()` warnings ignored).
   - Unclosed database connections and sockets.
   - Global variables and closures holding large request contexts.
3. **Core Diagnostic Tools**:
   - `node --inspect`: Exposes Chrome DevTools protocol.
   - `v8.writeHeapSnapshot()`: Generates `.heapsnapshot` files programmatically under high memory threshold.
   - `clinic doctor`, `clinic flame`: Diagnostic tool suites for diagnosing CPU bottlenecks and event loop lag.

---

## 📊 3. Visual Architecture Diagram

```
                 AUTOMATED HEAP DUMP TRIGGER FLOW
                 
   Periodic Memory Monitor (setInterval)
                 │
                 ▼
   Check: process.memoryUsage().heapUsed > 85% of Max Heap?
                 │
           ┌─────┴─────┐
           ▼           ▼
         [ NO ]     [ YES ]
           │           │
        Continue       ▼
        Normal   Trigger v8.writeHeapSnapshot()
        Traffic  Write snapshot to disk (/dumps/heap-dump.heapsnapshot)
                       │
                       ▼
                 Alert On-Call Engineer & Trigger Graceful Drain
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```javascript
import v8 from "node:v8";
import fs from "node:fs";
import path from "node:path";

// Production Self-Healing Heap Monitor with On-Demand Dumps
export function initializeMemoryMonitor(thresholdPercentage = 85) {
  const heapLimit = v8.getHeapStatistics().heap_size_limit;

  setInterval(() => {
    // Line 10: Extract memory usage
    const memory = process.memoryUsage();
    const percentUsed = (memory.heapUsed / heapLimit) * 100;

    console.log(`[Memory Monitor] Heap: ${(memory.heapUsed / 1024 / 1024).toFixed(2)} MB / ${(heapLimit / 1024 / 1024).toFixed(2)} MB (${percentUsed.toFixed(1)}%)`);

    // Line 16: Detect dangerous memory threshold breach
    if (percentUsed > thresholdPercentage) {
      console.warn("[ALERT] Memory threshold breached! Capturing emergency heap snapshot...");
      
      const dumpDir = path.resolve("./dumps");
      if (!fs.existsSync(dumpDir)) fs.mkdirSync(dumpDir);

      const dumpPath = path.join(dumpDir, `heap-${Date.now()}.heapsnapshot`);
      // Line 24: Write heap snapshot to disk for Chrome DevTools post-mortem
      const writtenPath = v8.writeHeapSnapshot(dumpPath);
      console.log(`Snapshot saved to ${writtenPath}. Inspect in chrome://inspect`);
    }
  }, 30000); // Check every 30 seconds
}
```

---

## 🎯 5. The "Interview Pitch"
> "When diagnosing Node.js memory leaks in production, I combine real-time APM telemetry with deterministic heap snapshot diffing. First, I monitor `process.memoryUsage().heapUsed` and RSS to establish whether memory growth is linear and fails to recover post-GC. Second, I configure automated snapshots via `v8.writeHeapSnapshot()` triggered when heap utilization exceeds 85%. Loading these snapshots into Chrome DevTools Memory Inspector, I sort by **Retained Size** to locate objects that anchor large trees—frequently unevicted Maps, un-removed event listeners on singleton streams, or closures capturing request scopes."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: A high-volume notification microservice experienced container OOM restarts every 36 hours. Kubernetes restarted the pods, masking the leak until weekend traffic surges caused cascading outages.
- **Task**: Identify the root cause of the slow leak and eliminate restarts.
- **Action**: We integrated programmatic heap snapshotting and analyzed the memory dumps in Chrome DevTools. Sorting by Retained Size identified 450,000 instances of `Socket` objects anchored in a global array. A custom WebSocket reconnection utility was pushing disconnected sockets into a retry array without removing them upon failed socket close events.
- **Result**: We replaced the array with a bounded `Set` and added explicit cleanup listeners on `socket.on('close')`. Pod memory stabilized at 90 MB continuously over 60 days without a single restart.
""",

    os.path.join(BASE_DIR, "04-node", "interview-questions", "top_node_interview_questions.md"): """# Top Node.js Senior Interview Questions (Runtime Internals)

---

## 1. Explain the difference between `process.nextTick()` and `setImmediate()`.
- `process.nextTick()`:
  - Executes **immediately after the current operation completes**, before the event loop continues to any other phase.
  - Sits in its own microtask queue. Calling it recursively can completely starve the event loop of I/O.
- `setImmediate()`:
  - Executes in the **Check Phase** of the Libuv event loop, right after I/O callbacks run.

---

## 2. What is the Libuv Thread Pool and what operations use it?
- Node's JavaScript runs on a single thread, but Libuv maintains a thread pool (Default size: 4 threads, configurable via `UV_THREADPOOL_SIZE`).
- **Uses Thread Pool**:
  - `fs` filesystem operations (synchronous & asynchronous).
  - `crypto` CPU-heavy operations (`pbkdf2`, `scrypt`, `randomBytes`).
  - `zlib` compression.
  - DNS lookups via `dns.lookup()`.
- **Does NOT use Thread Pool** (Handled directly by OS non-blocking kernel primitives like `epoll`/`kqueue`/`IOCP`):
  - Network sockets (`http`, `https`, `net`, `tls`).

---

## 3. What is an Unhandled Promise Rejection in Node.js?
- Occurs when a Promise rejects and has no `.catch()` handler attached.
- Since Node.js v15+, unhandled rejections terminate the process with a non-zero exit code by default.
- Best practice: Register `process.on('unhandledRejection', (reason, promise) => {})` for structured logging before graceful shutdown.

---

## 4. How does `Buffer.alloc()` differ from `Buffer.allocUnsafe()`?
- `Buffer.alloc(size)`: Allocates memory and fills it with zeroes (`0x00`). Safer, but slightly slower.
- `Buffer.allocUnsafe(size)`: Allocates uninitialized memory. Very fast, but the allocated buffer may contain sensitive old data (passwords, tokens) previously residing in memory. Must be immediately overwritten via `.fill()` or `.write()`.
""",

    os.path.join(BASE_DIR, "04-node", "interview-questions", "coding_custom_readable_writable_stream.md"): """# Machine Coding: Custom Transform Stream (CSV to JSON Parser)

---

## 🐣 1. Layman's Analogy
Transform stream ek **Pencil Sharpener** ki tarah hai: Ek taraf se aap lakdi ki raw pencil daalte ho (Input CSV chunks), sharpener andar gol ghoomta hai (Transform buffer parsing), aur dusri taraf se sharp sharpened pencil bahar aati hai (Formatted JSON objects stream).

---

## 💻 2. Line-by-Line Commented Code Solution

```javascript
import { Transform } from "node:stream";

/**
 * Custom Transform Stream that converts raw CSV text chunks into JSON lines
 */
export class CsvToJsonStream extends Transform {
  constructor(options = {}) {
    // Line 9: Initialize with objectMode output
    super({ ...options, objectMode: true });
    this.headers = null;
    this.residualBuffer = "";
  }

  // Line 15: _transform is invoked for every incoming buffer chunk
  _transform(chunk, encoding, callback) {
    // Line 17: Combine previous residual text with new chunk text
    const fullText = this.residualBuffer + chunk.toString("utf-8");
    const lines = fullText.split(/\r?\n/);

    // Line 21: The last element may be an incomplete line; store in residual buffer
    this.residualBuffer = lines.pop() || "";

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      // Line 28: First valid line becomes header keys
      if (!this.headers) {
        this.headers = line.split(",").map((h) => h.trim());
        continue;
      }

      // Line 34: Convert row values to JSON object
      const values = line.split(",").map((v) => v.trim());
      const record = {};
      this.headers.forEach((header, idx) => {
        record[header] = values[idx];
      });

      // Line 41: Push transformed JSON record downstream
      this.push(record);
    }

    // Line 45: Acknowledge chunk processing completion
    callback();
  }

  // Line 49: _flush is called when the readable stream ends
  _flush(callback) {
    // Line 51: Process any lingering line in residualBuffer
    if (this.residualBuffer.trim() && this.headers) {
      const values = this.residualBuffer.split(",").map((v) => v.trim());
      const record = {};
      this.headers.forEach((header, idx) => {
        record[header] = values[idx];
      });
      this.push(record);
    }
    callback();
  }
}
```
""",

    os.path.join(BASE_DIR, "05-backend-and-runtimes", "node-express", "01_express_architecture_and_routing.md"): """# Express.js Architecture: Middleware Pipelines and Routing Layer

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Express ek **Assembly Line Car Factory** ki tarah hai. Ek raw car chassis (HTTP Request) entry gate par aati hai.
Station 1: Guard ticket check karta hai (`AuthMiddleware`).
Station 2: Body paint hoti hai (`BodyParserMiddleware`).
Station 3: Engine fit hota hai (`RouteHandler`).
Har station apna kaam karta hai aur aage wale station ko bolta hai: `"next()"`! Agar kisi station par aag lag jaye (Error throw ho jaye), toh saari normal belt ruk jati hai aur car seedhe Emergency Red Lane (`ErrorHandlingMiddleware`) par bhej di jati hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Middleware Signature**: `(req, res, next) => {}`.
   - Calling `next()` passes control to the next registered middleware in the chain.
   - Calling `next(new Error('...'))` skips all remaining regular routes and jumps directly to error middlewares.
2. **Order of Registration Matters**: Express executes middlewares in the exact sequential order they are registered via `app.use()`.
3. **The Router Layer**: `express.Router()` creates modular, isolated mini-applications with their own isolated middleware stacks.
4. **Asynchronous Errors in Express 4 vs 5**:
   - In Express 4, unhandled rejected promises inside async routes hang the request unless caught with `.catch(next)`.
   - In Express 5, async route errors are automatically caught and forwarded to `next(err)`.

---

## 💻 3. Line-by-Line Commented Code Snippets

```javascript
import express from "express";

const app = express();

// Line 6: Global JSON body parsing middleware
app.use(express.json());

// Line 9: Custom Request Timing & Logging Middleware
app.use((req, res, next) => {
  const start = Date.now();
  // Intercept response finish event
  res.on("finish", () => {
    const duration = Date.now() - start;
    console.log(`[HTTP] ${req.method} ${req.originalUrl} - ${res.statusCode} (${duration}ms)`);
  });
  // Line 18: Proceed to next middleware
  next();
});

// Line 22: Modular Router for User Domain
const userRouter = express.Router();

userRouter.get("/:id", async (req, res, next) => {
  try {
    const { id } = req.params;
    if (id === "0") {
      throw new Error("Invalid User ID");
    }
    res.json({ id, username: "jay_dev" });
  } catch (err) {
    // Line 33: Forward async error to centralized error handler
    next(err);
  }
});

app.use("/api/v1/users", userRouter);

// Line 39: Centralized 4-Argument Error Middleware (Must have 4 params!)
app.use((err, req, res, next) => {
  console.error("Centralized Error Caught:", err.message);
  res.status(err.status || 500).json({
    error: {
      message: err.message || "Internal Server Error"
    }
  });
});
```

---

## 🎯 4. The "Interview Pitch"
> "Express.js is an unopinionated routing and middleware engine built on the Chain of Responsibility design pattern. Requests travel through a linked pipeline of handlers where each middleware can inspect headers, mutate the request context, end the response, or invoke `next()`. Error handling in Express relies on a specialized four-argument signature `(err, req, res, next)`. In enterprise setups, organizing domain endpoints into isolated `express.Router()` instances allows composing decoupled sub-applications with their own localized middleware guards."
""",

    os.path.join(BASE_DIR, "05-backend-and-runtimes", "node-express", "03_express_error_handling_and_logging.md"): """# Production Express Error Handling, Structured Logging, and Graceful Shutdown

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Jab hospital mein light chali jaye ya emergency aaye, doctor turant bhag nahi jata (**Ungraceful Crash**). Pehle ventilator backup generator pe switch hota hai, ongoing operations safely complete hote hain, naye patients ko doosre hospital divert kiya jata hai, aur fir safely equipment shut down kiya jata hai (**Graceful Shutdown with SIGTERM**).

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Graceful Shutdown**:
   - When Kubernetes stops a pod, it sends `SIGTERM`.
   - Stop accepting new HTTP requests: `server.close()`.
   - Allow existing requests 10-15 seconds to finish processing.
   - Close database pools and Redis connections.
   - Exit process cleanly with `process.exit(0)`.
2. **Structured Logging (Pino/Winston)**:
   - Always log in structured JSON format in production for Elasticsearch / Datadog ingestion.
   - Include unique Correlation IDs (`x-request-id`) across every log entry.

---

## 💻 3. Line-by-Line Commented Code Snippets

```javascript
import http from "node:http";
import express from "express";

const app = express();
const server = http.createServer(app);

// Line 8: Graceful Shutdown Orchestration
function setupGracefulShutdown(server, dbPool) {
  const shutdown = (signal) => {
    console.log(`Received ${signal}. Starting graceful shutdown...`);

    // Stop accepting new connections
    server.close(async () => {
      console.log("HTTP server closed. Flushing database connections...");
      try {
        if (dbPool) await dbPool.end();
        console.log("Database connections closed cleanly. Exiting.");
        process.exit(0);
      } catch (err) {
        console.error("Error during DB shutdown:", err);
        process.exit(1);
      }
    });

    // Force shutdown if cleanup hangs past 10 seconds
    setTimeout(() => {
      console.error("Forcefully shutting down due to timeout!");
      process.exit(1);
    }, 10000).unref();
  };

  process.on("SIGTERM", () => shutdown("SIGTERM"));
  process.on("SIGINT", () => shutdown("SIGINT"));
}
```
""",

    os.path.join(BASE_DIR, "05-backend-and-runtimes", "java-springboot", "02_springboot_security_jwt_oauth2.md"): """# Spring Boot 3 Security Architecture: JWT, Filter Chains, and OAuth2 Resource Server

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Spring Security ek **Multi-Tier Airport Border Security** ki tarah hai:
1. **SecurityFilterChain**: Har passenger ko alag-alag security counters se guzarna padta hai (Passport check, baggage scanner, metal detector).
2. **OncePerRequestFilter (JWT Check)**: Guard passenger ka wristband (JWT Token) scan karta hai, dekhta hai ki signature valid hai ya nahi, aur passenger ka verified identity badge (`SecurityContextHolder`) pehnata hai.
3. **Method Security (`@PreAuthorize`)**: VIP Lounge ke gate par ek aur guard khada hai jo sirf un logo ko andar jane deta hai jinke badge pe `ROLE_ADMIN` likha ho!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`SecurityFilterChain` Bean**: In Spring Boot 3 (Spring Security 6), `WebSecurityConfigurerAdapter` is deprecated. Security is configured declaratively via `@Bean SecurityFilterChain`.
2. **Session Creation Policy**: Set to `SessionCreationPolicy.STATELESS` for REST APIs to prevent server-side HTTP session storage.
3. **`OncePerRequestFilter`**: Guarantees execution exactly once per request dispatch, ideal for parsing `Authorization: Bearer <jwt>`.
4. **`SecurityContextHolder`**: Uses `ThreadLocal` storage by default to store the authenticated `Authentication` token for the duration of the thread.

---

## 💻 3. Line-by-Line Commented Code Snippets

```java
package com.knowledgebase.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableMethodSecurity // Enables @PreAuthorize("hasRole('ADMIN')")
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;

    public SecurityConfig(JwtAuthenticationFilter jwtAuthFilter) {
        this.jwtAuthFilter = jwtAuthFilter;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // Line 25: Disable CSRF since REST APIs use stateless JWT tokens
            .csrf(csrf -> csrf.disable())
            // Line 27: Enforce stateless session management
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // Line 29: Configure URL authorization rules
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**", "/actuator/health").permitAll()
                .anyRequest().authenticated()
            )
            // Line 34: Inject custom JWT filter BEFORE standard username/password filter
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```
""",

    os.path.join(BASE_DIR, "05-backend-and-runtimes", "java-springboot", "03_springboot_microservices_and_resilience4j.md"): """# Spring Boot Microservices: Resilience4j Circuit Breakers & Distributed Tracing

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Circuit Breaker ghar ke **Electric MCB (Fuse Switch)** ki tarah hai:
Agar ghar mein kisi appliance mein short circuit (Microservice B crashing) ho jaye, toh pura power house blast hone ke bajaye MCB turant trip (`OPEN`) ho jata hai! Isse baaki ghar ki lights safe rehti hain (**Cascading Failure Prevention**). Jab fault theek ho jata hai, MCB dheere se test mode (`HALF-OPEN`) mein check karta hai, aur sab theek hone par normal (`CLOSED`) ho jata hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Three Circuit Breaker States**:
   - **CLOSED**: Normal operation. Requests flow to downstream service.
   - **OPEN**: Failure rate exceeded threshold. Requests immediately short-circuited to fallback method without network latency.
   - **HALF-OPEN**: Trial state after wait duration. Allows a limited number of requests to test if downstream service recovered.
2. **Distributed Tracing with Micrometer Tracing & OpenTelemetry**:
   - Injects `traceId` (unique per distributed request) and `spanId` (unique per service hop) into logs for end-to-end tracing.

---

## 💻 3. Line-by-Line Commented Code Snippets

```java
package com.knowledgebase.service;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class PaymentGatewayClient {

    private final RestTemplate restTemplate;

    public PaymentGatewayClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // Line 17: Apply CircuitBreaker and Retry annotations
    @CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
    @Retry(name = "paymentService")
    public String processPayment(String orderId, double amount) {
        // Line 21: Remote call to external payment processor
        return restTemplate.postForObject("https://payment-api.stripe.com/charge", null, String.class);
    }

    // Line 25: Fallback method executed when circuit is OPEN or exception thrown
    public String paymentFallback(String orderId, double amount, Throwable exception) {
        System.err.println("Payment service failed or circuit open: " + exception.getMessage());
        return "FALLBACK_QUEUED_FOR_OFFLINE_PROCESSING";
    }
}
```
""",

    os.path.join(BASE_DIR, "05-backend-and-runtimes", "ruby-on-rails", "02_rails_api_and_sidekiq_jobs.md"): """# Ruby on Rails API Mode, ActiveJob, and Sidekiq Concurrency

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Rails API mode ek restaurant ke **Express Drive-Thru Window** jaisa hai: Dining room aur plates (HTML Views, Sprockets) ko hata diya gaya hai, sirf fast JSON deliver hota hai.
**Sidekiq** ek **Dedicated Delivery Boy** ki tarah hai: Customer ne pizza order kiya, counter executive ne receipt print karke kitchen hook (Redis Queue) par latka di aur customer ko 2 second mein receipt pakda di. Delivery boy (Sidekiq worker) background mein pizza pack karke delivery karta rehta hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Rails API Only Mode (`--api`)**: Strips out session management, cookies, asset pipelines, and view rendering for ultra-lean JSON APIs.
2. **Sidekiq Architecture**: Multi-threaded background job processor powered by Redis for reliable job persistence.
3. **Idempotency**: Background jobs must be idempotent because Sidekiq guarantees **at-least-once** job execution.

---

## 💻 3. Line-by-Line Commented Code Snippets

```ruby
# app/jobs/process_monthly_invoice_job.rb
class ProcessMonthlyInvoiceJob < ApplicationJob
  # Line 3: Route this job to the high-priority Sidekiq queue in Redis
  queue_as :critical

  # Line 6: Automatically retry up to 5 times with exponential backoff
  sidekiq_options retry: 5

  def perform(account_id, billing_cycle)
    # Line 10: Find account safely
    account = Account.find(account_id)
    
    # Line 13: Idempotency check to prevent double charging
    return if account.invoices.where(billing_cycle: billing_cycle).exists?

    # Line 16: Generate invoice and charge card
    invoice = account.generate_invoice!(billing_cycle)
    PaymentService.charge!(invoice)
  end
end
```
""",

    os.path.join(BASE_DIR, "05-fastapi", "02_pydantic_v2_validation_and_serialization.md"): """# FastAPI with Pydantic V2: Rust-Powered Validation & Type Serialization

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Pydantic V1 ek manual airport luggage inspector jaisa tha jo Python mein line-by-line check karta tha.
Pydantic V2 ek **High-Speed Industrial Scanner** hai jiska core engine pure **Rust (`pydantic-core`)** mein likha gaya hai. Ye 5x se 20x fast validation karta hai aur invalid data ko API router ke andar ghusne hi nahi deta.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Rust Core Architecture**: Pydantic V2 rewrote the entire validation and serialization engine in Rust (`pydantic-core`).
2. **`model_validator` & `field_validator`**: Replaces V1's `@validator` and `@root_validator`.
3. **Serialization Mode**: `model.model_dump()` replaces `.dict()`, and `model.model_dump_json()` replaces `.json()`.
4. **Strict vs Lax Mode**: By default, Pydantic coerces compatible types (e.g. string `"42"` to int `42`). Setting `strict=True` forbids coercion.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
from typing import Optional
from datetime import datetime

# Line 6: User registration model with Pydantic V2 syntax
class UserRegistrationSchema(BaseModel):
    # Line 8: Strict type constraints with Field
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Line 15: Field validator for username
    @field_validator("username")
    @classmethod
    def validate_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        return v.lower()

    # Line 23: Model validator checking cross-field rules (passwords match)
    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegistrationSchema":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match!")
        return self
```
""",

    os.path.join(BASE_DIR, "05-fastapi", "03_dependency_injection_system.md"): """# FastAPI Dependency Injection System (`Depends`)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
FastAPI ka `Depends()` ek **Automated Butler (Chaudhary)** ki tarah hai. Jab bhi aap kisi function (API Route) mein aate ho, butler pehle se aapke liye:
- Database connection khol ke table par rakh deta hai.
- User ka JWT token verify karke user object haath mein pakda deta hai.
Aur jab aapka function khatam ho jata hai, butler chupke se database connection safely close kar deta hai (`yield` teardown)!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Declarative Composition**: Dependencies can themselves depend on other dependencies, forming a clean **Directed Acyclic Graph (DAG)**.
2. **Resource Teardown via `yield`**: Using `yield` allows executing cleanup logic (closing DB sessions, releasing locks) after the response is sent.
3. **Dependency Caching (`use_cache=True`)**: By default, FastAPI resolves a shared dependency once per request, caching its return value across multiple parameter usages in that single request.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
from fastapi import FastAPI, Depends, HTTPException, status, Header
from typing import Annotated, Generator

app = FastAPI()

# Line 7: Database session dependency with clean teardown using yield
def get_db_session() -> Generator[str, None, None]:
    session = "PostgresSession[Open]"
    print(f"Acquired: {session}")
    try:
        # Line 12: Passes active session to route
        yield session
    finally:
        # Line 15: Executes cleanup AFTER response is sent to client
        print("Closed: PostgresSession[Released]")

# Line 18: Authentication dependency
def get_current_user(authorization: Annotated[str | None, Header()] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication token"
        )
    token = authorization.split(" ")[1]
    return {"user_id": "usr_99", "role": "admin", "token": token}

# Line 28: Route composing both dependencies
@app.get("/api/v1/profile")
def get_profile(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[str, Depends(get_db_session)]
):
    return {"user": current_user, "db_status": db}
```
""",

    os.path.join(BASE_DIR, "05-fastapi", "04_background_tasks_and_celery.md"): """# FastAPI Background Tasks vs Distributed Celery Workers

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
**FastAPI BackgroundTasks** ek **Waiter ka Note** hai: Waiter customer ko bill dekar bolta hai "Aap ja sakte hain", aur jaate-jaate restaurant ke register mein transaction note kar deta hai. Ye chote kamo (email bhejna, log likhna) ke liye perfect hai.
**Celery with Redis** ek **Alag Dedicated Factory** hai: Agar kaam 15 minute ka video transcoding ya heavy ML model execution hai, toh restaurant ka waiter wo kaam factory bhej deta hai. Server restart hone par bhi Celery ka kaam gayab nahi hota.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **`BackgroundTasks` (In-Process)**:
   - Runs in the same process after sending the HTTP response.
   - Ideal for lightweight, non-critical tasks (< 1-2 seconds, e.g. sending emails).
   - If the container crashes or restarts, inflight tasks are **lost forever**.
2. **Celery (Distributed Task Queue)**:
   - Runs in separate independent worker processes via Redis/RabbitMQ brokers.
   - Supports retries, rate limiting, scheduling, and task persistence.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
from fastapi import FastAPI, BackgroundTasks
import asyncio

app = FastAPI()

# Line 6: Lightweight async task function
async def send_welcome_email(email: str, username: str):
    await asyncio.sleep(1) # Simulate SMTP network latency
    print(f"[Email Sent] Successfully sent welcome email to {email} ({username})")

# Line 11: Route returning instant HTTP 202 while task runs in background
@app.post("/api/v1/register")
def register_user(email: str, username: str, background_tasks: BackgroundTasks):
    # Line 14: Enqueue task to execute post-response
    background_tasks.add_task(send_welcome_email, email, username)
    return {"message": "User registered successfully. Email queued."}
```
""",

    os.path.join(BASE_DIR, "05-fastapi", "05_high_performance_asgi_starlette_uvicorn.md"): """# High-Performance ASGI: Starlette, Uvicorn, and Concurrency Optimization

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Purane Python web frameworks (Flask/Django WSGI) ek **Single Line Toll Booth** ki tarah the: Jab tak ek gaadi toll nahi deti, piche wali gaadiyan aage nahi badh sakti thi.
FastAPI + Uvicorn (ASGI) ek **Express Fastag Toll Plaza** ki tarah hai jahan 100 gaadiyan ek sath enter karti hain. Agar kisi gaadi ka fastag scan hone mein 1 second lag raha hai (I/O wait), toh toll camera turant dusri gaadi ka photo khinch leta hai (**Asyncio Non-blocking Event Loop**)!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **WSGI vs ASGI**:
   - WSGI is synchronous: one thread per request model.
   - ASGI (Asynchronous Server Gateway Interface) supports `async`/`await`, WebSockets, and HTTP/2 long-polling natively.
2. **Uvicorn Architecture**:
   - Powered by `uvloop` (an ultra-fast C implementation of the asyncio event loop using Libuv) and `httptools`.
3. **The `def` vs `async def` Route Trap in FastAPI**:
   - `async def`: Runs directly on the main event loop thread. If you run blocking code (`time.sleep()` or synchronous database drivers) inside `async def`, you freeze the entire server!
   - `def`: FastAPI automatically offloads standard `def` functions to an internal **thread pool** (`anyio.to_thread.run_sync`), keeping the event loop unblocked!

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# Line 7: Correct: Non-blocking async route using await
@app.get("/async-fast")
async def async_endpoint():
    # Asynchronously yields control to event loop; does NOT block other requests!
    await asyncio.sleep(0.5)
    return {"status": "success"}

# Line 14: Correct: Synchronous blocking route defined as standard `def`
@app.get("/sync-safe")
def sync_blocking_endpoint():
    # FastAPI automatically runs this in a threadpool worker!
    time.sleep(0.5)
    return {"status": "safe in threadpool"}

# ANTI-PATTERN: Blocking code inside async def freezes entire server!
# @app.get("/dangerous")
# async def dangerous_endpoint():
#     time.sleep(5) # NEVER DO THIS! Freezes all concurrent users for 5s!
```
""",

    os.path.join(BASE_DIR, "05-fastapi", "interview-questions", "top_fastapi_interview_questions.md"): """# Top FastAPI Senior Interview Questions (Async Architecture & Concurrency)

---

## 1. What happens if you run blocking I/O inside an `async def` endpoint in FastAPI?
- In `async def`, the route executes directly on the single-threaded asyncio event loop.
- Running blocking synchronous code (such as `time.sleep()`, synchronous `requests.get()`, or legacy DB queries) blocks the entire event loop thread, causing all concurrent user requests to freeze.
- Solution: Either rewrite using asynchronous drivers (`httpx`, `asyncpg`, `aiofiles`), or declare the endpoint with plain `def` so FastAPI offloads it to a background thread pool.

---

## 2. How does FastAPI achieve automatic OpenAPI / Swagger documentation?
- FastAPI inspects Python type hints on route parameters and Pydantic models at application startup using reflection.
- It translates these Python types directly into JSON Schema definitions conforming to the OpenAPI 3.0+ specification.

---

## 3. What is the difference between `model_dump()` and `model_dump_json()` in Pydantic V2?
- `model_dump()`: Serializes the Pydantic model into a native Python dictionary (`dict`).
- `model_dump_json()`: Serializes the model directly into a raw JSON string using Rust `pydantic-core`, which is significantly faster than calling `json.dumps(model.model_dump())`.
""",

    os.path.join(BASE_DIR, "05-fastapi", "interview-questions", "coding_rate_limiting_middleware.md"): """# Machine Coding: Distributed Sliding Window Rate Limiting Middleware in FastAPI

---

## 🐣 1. Layman's Analogy
Rate limiter ek club ke bouncer ki tarah hai. Rules hain: "Ek minute mein ek aadmi 60 se zyada drinks nahi le sakta". Bouncer har customer ke aane ka exact time stamp register karta hai. Agar pichle 60 seconds ke andar 60 stamps ho chuke hain, toh bouncer bolta hai: `"HTTP 429: Too Many Requests, bhai 5 second wait kar!"`.

---

## 💻 2. Line-by-Line Commented Code Solution

```python
from fastapi import FastAPI, Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

class SlidingWindowRateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # In-memory storage: IP -> List of request timestamps
        # In distributed production, use Redis Sorted Sets (ZADD / ZREMRANGEBYSCORE)
        self.request_history = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Line 17: Extract client IP
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        window_start = current_time - self.window_seconds

        # Line 22: Clean up timestamps older than current window
        history = self.request_history[client_ip]
        self.request_history[client_ip] = [ts for ts in history if ts > window_start]

        # Line 26: Check rate limit threshold
        if len(self.request_history[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later."
            )

        # Line 33: Record current request timestamp
        self.request_history[client_ip].append(current_time)

        # Line 36: Forward request downstream
        response = await call_next(request)
        return response

app = FastAPI()
app.add_middleware(SlidingWindowRateLimiterMiddleware, max_requests=10, window_seconds=60)
```
"""
}

def main():
    print(f"Generating {len(FILES)} Track 4 Backend deep dive files...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Track 4 Backend generation complete!")

if __name__ == "__main__":
    main()
