# Libuv Event Loop & Node.js Internal Architecture

## 1. Executive Summary
Node.js combines V8 for JavaScript execution with Libuv for asynchronous cross-platform I/O operations. Libuv manages a thread pool (default 4 threads) for blocking system tasks (file I/O, DNS lookup, crypto) and drives the 6-phase C event loop.

---

## 2. The 6 Phases of Libuv Event Loop
1. **Timers:** Executes callbacks scheduled by `setTimeout()` and `setInterval()`.
2. **Pending Callbacks:** Executes I/O callbacks deferred to the next loop iteration.
3. **Idle, Prepare:** Internal Node.js usage.
4. **Poll:** Retrieves new I/O events; executes I/O related callbacks.
5. **Check:** Executes `setImmediate()` callbacks.
6. **Close Callbacks:** Executes close events (e.g., `socket.on('close', ...)`).
