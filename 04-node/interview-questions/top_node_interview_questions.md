# Top Node.js Senior Interview Questions (Runtime Internals)

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
