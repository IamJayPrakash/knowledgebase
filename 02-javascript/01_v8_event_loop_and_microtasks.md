# JavaScript Event Loop, Call Stack & Microtask Queue

## 1. Executive Summary
JavaScript is single-threaded, non-blocking, and asynchronous. It uses a single call stack to execute synchronous code, while delegating asynchronous operations (I/O, timers, Network) to the Web API or C++ background threads. When async tasks complete, their callbacks are queued into either the **Microtask Queue** (Promises, `queueMicrotask`, `MutationObserver`) or the **Macrotask Queue** (`setTimeout`, `setInterval`, `setImmediate`, I/O). The Microtask Queue has higher priority and is completely drained after the call stack empties and before the next macrotask is processed.

---

## 2. Under the Hood Mechanics

```text
  +-----------------------------------+
  |            Call Stack             |
  +-----------------------------------+
                   |
                   v
  +-----------------------------------+
  |         Microtask Queue           |  <--- Drained COMPLETELY until empty
  |  (Promises, process.nextTick*)   |
  +-----------------------------------+
                   |
                   v
  +-----------------------------------+
  |          Render Steps             |  <--- (Browser GUI Paint if needed)
  +-----------------------------------+
                   |
                   v
  +-----------------------------------+
  |         Macrotask Queue           |  <--- Executes ONE task per loop turn
  |  (setTimeout, setInterval, I/O)   |
  +-----------------------------------+
```

* *Note in Node.js:* `process.nextTick` runs in a special queue that executes **before** Promise microtasks.

---

## 3. Code Example & Verification

```javascript
console.log('1: Synchronous Start');

setTimeout(() => {
  console.log('2: Macrotask - setTimeout');
}, 0);

Promise.resolve().then(() => {
  console.log('3: Microtask 1');
}).then(() => {
  console.log('4: Microtask 2');
});

queueMicrotask(() => {
  console.log('5: Microtask 3');
});

console.log('6: Synchronous End');

// Expected Output Order:
// 1: Synchronous Start
// 6: Synchronous End
// 3: Microtask 1
// 5: Microtask 3
// 4: Microtask 2
// 2: Macrotask - setTimeout
```

---

## 4. Pitfalls, Edge Cases & Performance Impact

1. **Microtask Queue Starvation:** Infinitely chaining Microtasks (or `process.nextTick`) blocks the Event Loop completely, starving Macrotasks, I/O, and UI painting, causing the Node process or browser tab to freeze.
2. **`async/await` Transpilation Overhead:** `await` yields execution back to the caller and wraps the remaining code in a Microtask. In high-frequency loops (e.g., millions of iterations), unnecessary `await` calls introduce microtask queue overhead.

---

## 5. Senior / Architect Interview Questions

* **Q: Why does Node.js `process.nextTick` differ from standard `queueMicrotask`?**
  * **A:** `process.nextTick` maintains its own queue (`nextTickQueue`) managed by Node.js, which is processed immediately after the current C++ operation completes and *before* the V8 microtask queue (`Promise` callbacks).
* **Q: How does the Event Loop affect throughput in a high-concurrency Node.js server?**
  * **A:** Heavy CPU-bound computation on the main thread blocks the event loop, causing requests to pile up in the queue, increasing latency, and triggering socket timeouts. Workarounds: Offloading to Worker Threads, C++ addons, or microservice delegation.
