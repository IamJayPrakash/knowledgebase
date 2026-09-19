# JavaScript Master Interview Bank: Part 4 (Q61 - Q80)
## Async Architecture, Event Loop, Promises & Concurrency

---

### Q61: Diagram and explain the JavaScript Event Loop execution priority.
**Answer:**

```
   ┌───────────────────────────────────────────────────────────┐
   │                       CALL STACK                          │
   │  Executes synchronous code until empty.                   │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │                    MICROTASK QUEUE                        │
   │  Promises (.then/catch/finally), queueMicrotask, Mutation │
   │  Observer. EMPTIED COMPLETELY before proceeding.          │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │                  UI RENDERING & PAINT                     │
   │  requestAnimationFrame, DOM recalculation & paint tick.   │
   └─────────────────────────────┬─────────────────────────────┘
                                 │
                                 ▼
   ┌───────────────────────────────────────────────────────────┐
   │                     MACROTASK QUEUE                       │
   │  setTimeout, setInterval, setImmediate, I/O events.       │
   │  EXACTLY ONE TASK EXECUTED per event loop iteration.      │
   └───────────────────────────────────────────────────────────┘
```

**Execution Order Rules:**
1. Execute all synchronous tasks on the Call Stack.
2. Flush the **Microtask Queue** completely (including microtasks queued by running microtasks).
3. Check if UI rendering/paint is required (typically at 60Hz / 16.6ms intervals).
4. Dequeue and execute **one Macrotask** from the task queue.
5. Repeat loop from Step 1.

---

### Q62: What will be the output of this code snippet? Explain step-by-step.
```javascript
console.log("1");

setTimeout(() => console.log("2"), 0);

Promise.resolve().then(() => {
  console.log("3");
  queueMicrotask(() => console.log("4"));
}).then(() => {
  console.log("5");
});

console.log("6");
```
**Output:**
```
1
6
3
4
5
2
```
**Detailed Step-by-Step Tracing:**
1. `console.log("1")` runs synchronously $\to$ Prints **`1`**.
2. `setTimeout` registers callback in Macrotask queue with 0ms delay.
3. `Promise.resolve().then(...)` registers outer microtask in Microtask queue.
4. `console.log("6")` runs synchronously $\to$ Prints **`6`**.
5. Call Stack is empty! Drain Microtask queue:
   - Run outer Promise callback: prints **`3`**, queues `queueMicrotask` (prints 4), and resolves outer Promise (enqueuing the chained `.then(...)` that prints 5).
   - Microtask queue order is now: `[queueMicrotask, chainedPromise]`.
   - Run `queueMicrotask` $\to$ Prints **`4`**.
   - Run chained `.then` $\to$ Prints **`5`**.
6. Microtask queue is now empty. Dequeue Macrotask:
   - Run `setTimeout` callback $\to$ Prints **`2`**.

---

### Q63: What happens if a microtask recursively enqueues another microtask?
**Answer:**
- **Microtask Queue Starvation:** Because the event loop **must exhaust all microtasks** before yielding to rendering or macrotasks, recursively enqueuing microtasks (via `queueMicrotask()` or chained resolved promises) traps the engine in an infinite loop.
- **Impact:** The UI freezes completely, user clicks and keystrokes are ignored, animations stop, and macrotasks (like `setTimeout`) never run.

```javascript
// FREEZES BROWSER COMPLETELY:
function starve() {
  Promise.resolve().then(starve);
}
starve();
```

---

### Q64: What are the 3 states of a Promise, and why is state transition irreversible?
**Answer:**
A Promise is a state machine with 3 mutually exclusive states:
1. **`pending`**: Initial state, neither fulfilled nor rejected.
2. **`fulfilled`**: Operation completed successfully with a resultant `value`.
3. **`rejected`**: Operation failed with a `reason` (error).

**Irreversibility:** Once a promise transitions from `pending` to either `fulfilled` or `rejected`, it is **settled** and its state becomes permanently immutable. Subsequent calls to `resolve()` or `reject()` within the executor function are silently discarded.

---

### Q65: Implement `Promise.all` polyfill from scratch with edge cases.
**Answer:**
```javascript
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    // Handle non-iterable inputs
    if (!promises || typeof promises[Symbol.iterator] !== "function") {
      return reject(new TypeError("Argument must be iterable"));
    }

    const items = Array.from(promises);
    if (items.length === 0) {
      return resolve([]);
    }

    const results = new Array(items.length);
    let completed = 0;

    items.forEach((item, index) => {
      // Wrap in Promise.resolve to handle primitive non-promise values
      Promise.resolve(item)
        .then((val) => {
          results[index] = val; // Preserve input index order
          completed++;
          if (completed === items.length) {
            resolve(results);
          }
        })
        .catch((err) => {
          reject(err); // Fail-fast: reject immediately on first failure
        });
    });
  });
}
```

---

### Q66: What are the differences between `Promise.all`, `Promise.allSettled`, `Promise.race`, and `Promise.any`?
**Answer:**
| Method | Resolves When... | Rejects When... | Ideal Use Case |
| :--- | :--- | :--- | :--- |
| **`Promise.all`** | **All** promises fulfill. | **Any single** promise rejects (Fail-Fast). | Co-dependent parallel queries where all results are strictly mandatory. |
| **`Promise.allSettled`** | **All** promises settle (either fulfill or reject). | **Never rejects**. Returns array of `{status, value/reason}`. | Bulk operations where failures should not discard successes (e.g. multi-recipient emails). |
| **`Promise.race`** | **First** promise settles (fulfill OR reject). | **First** promise settles (fulfill OR reject). | Request timeouts (racing fetch against a timer). |
| **`Promise.any`** | **First** promise fulfills. | **All** promises reject (returns `AggregateError`). | Redundant fallback mirrors (querying 3 CDNs; take first success). |

---

### Q67: How does `async/await` work under the hood?
**Answer:**
- `async/await` is syntactic sugar over **Generators (`function*`) + Promises + recursive task runner**.
- An `async` function always returns a Promise.
- Inside the engine:
  1. Encountering `await promise` suspends execution of the coroutine.
  2. The engine attaches a `.then()` callback to the awaited promise.
  3. Control returns to the caller / event loop.
  4. When the awaited promise fulfills, its `.then()` microtask resumes the generator via `.next(resolvedValue)`.

---

### Q68: What is the difference between `return await promise` and `return promise`?
**Answer:**
```javascript
// Case A:
async function caseA() {
  return promise;
}

// Case B:
async function caseB() {
  return await promise;
}
```
1. **Outside `try...catch`:**
   - Both behave virtually identically, returning a promise resolving to the final value.
   - `return await` introduces one extra microtask tick before resolving.
2. **Inside `try...catch` (CRITICAL DIFFERENCE):**
   - `return promise`: The promise is returned immediately in pending state. If it rejects later, the local `catch` block is **bypassed** and the error bubbles up.
   - `return await promise`: The function suspends and waits. If the promise rejects, the local `catch` block **catches the error**.

```javascript
async function safeCall() {
  try {
    return await apiCall(); // ✅ Catches rejection here!
  } catch (err) {
    console.log("Caught locally!");
  }
}
```

---

### Q69: How do you cancel an ongoing `fetch` request in modern JavaScript?
**Answer:**
Use the **`AbortController` API**:

```javascript
const controller = new AbortController();
const { signal } = controller;

async function fetchUserData() {
  try {
    const res = await fetch("https://api.example.com/users", { signal });
    return await res.json();
  } catch (err) {
    if (err.name === "AbortError") {
      console.log("Fetch request aborted by client!");
    } else {
      console.error("Network error:", err);
    }
  }
}

// Trigger request
fetchUserData();

// Cancel request after 2000ms:
setTimeout(() => controller.abort(), 2000);
```

---

### Q70: How does `AbortSignal.timeout()` simplify request timeouts?
**Answer:**
Introduced in recent ECMAScript/Web standards, `AbortSignal.timeout(ms)` creates an abort signal that automatically triggers after `ms` milliseconds without manually managing `setTimeout`:

```javascript
try {
  const response = await fetch("/api/data", {
    signal: AbortSignal.timeout(5000) // Auto-aborts after 5 seconds
  });
} catch (err) {
  if (err.name === "TimeoutError") {
    console.log("Request timed out after 5 seconds");
  }
}
```

---

### Q71: How do JavaScript Generator functions work (`function*` and `yield`)?
**Answer:**
- A Generator is a function that can **pause execution** (`yield`) and resume later (`.next()`).
- Calling a generator does NOT run its body; it returns a **Generator Object** implementing the Iterable and Iterator protocols.
- Calling `gen.next(val)` resumes execution until the next `yield` expression, returning `{ value: any, done: boolean }`.
- Values passed to `.next(val)` become the evaluated result of the suspended `yield` expression inside the generator.

```javascript
function* idGenerator() {
  let id = 1;
  while (true) {
    yield id++;
  }
}

const gen = idGenerator();
console.log(gen.next().value); // 1
console.log(gen.next().value); // 2
```

---

### Q72: What is an Async Generator (`for await...of`) and when is it used?
**Answer:**
- An Async Generator (`async function*`) combines async functions and generators, yielding Promises: `yield await item`.
- Consumed via **`for await (const item of asyncGen)`**.
- **Ideal Use Cases:** Streaming chunked HTTP payloads, reading massive log files line-by-line from disk, paginated API fetching.

```javascript
async function* fetchPages(url) {
  let nextPage = 1;
  while (nextPage <= 3) {
    const res = await fetch(`${url}?page=${nextPage}`);
    const data = await res.json();
    yield data.items;
    nextPage++;
  }
}

for await (const items of fetchPages("/api/records")) {
  console.log("Received chunk:", items.length);
}
```

---

### Q73: What is the difference between `requestAnimationFrame` and `setTimeout`?
**Answer:**
- **`setTimeout(fn, 16)`**: Macrotask scheduled on timer tick. Timing is inaccurate; can drift due to queue lag. Fires regardless of monitor refresh rate or tab visibility.
- **`requestAnimationFrame(fn)` (rAF)**:
  - Synchronized directly with the display refresh rate (e.g. 60Hz = ~16.6ms, 120Hz = ~8.3ms).
  - Fires immediately **before the browser performs recalculate style, layout, and paint**.
  - Automatically paused in background inactive browser tabs, conserving battery and GPU/CPU power.

---

### Q74: What is `queueMicrotask()` and when should you use it over `Promise.resolve().then()`?
**Answer:**
- `queueMicrotask(callback)` directly schedules a callback onto the microtask queue without the overhead of creating, allocating, and resolving a dummy `Promise` object.
- **Use Case:** Executing code asynchronously after current synchronous logic completes, but strictly before rendering, DOM paints, or macrotasks run.

```javascript
function logAnalytics(event) {
  // Enqueue to send at end of current tick without blocking
  queueMicrotask(() => {
    navigator.sendBeacon("/log", JSON.stringify(event));
  });
}
```

---

### Q75: How do you implement sequential execution of an array of asynchronous tasks?
**Answer:**
**Option 1: Using `for...of` loop (Cleanest)**
```javascript
async function executeSequentially(tasks) {
  const results = [];
  for (const task of tasks) {
    results.push(await task());
  }
  return results;
}
```

**Option 2: Using `Array.prototype.reduce`**
```javascript
function executeSequentiallyReduce(tasks) {
  return tasks.reduce((promiseChain, currentTask) => {
    return promiseChain.then(chainResults => 
      currentTask().then(currentResult => [...chainResults, currentResult])
    );
  }, Promise.resolve([]));
}
```

---

### Q76: What is a Promise unhandled rejection and how do you monitor it?
**Answer:**
- When a Promise rejects and no `.catch()` handler or `try...catch` block handles the rejection, it becomes an **Unhandled Rejection**.
- In modern Node.js, unhandled rejections terminate the process with a non-zero exit code.
- **Global Handlers:**
  - Browser: `window.addEventListener("unhandledrejection", (event) => console.log(event.reason));`
  - Node.js: `process.on("unhandledRejection", (reason, promise) => console.error(reason));`

---

### Q77: What is the difference between Parallelism and Concurrency in JavaScript?
**Answer:**
- **Concurrency:** Dealing with lots of things at once (Interleaved execution). JavaScript achieves concurrency on a **single thread** via non-blocking asynchronous event loop scheduling.
- **Parallelism:** Doing lots of things at once (Simultaneous execution on multiple CPU cores). In JavaScript, true parallelism is achieved only via **Web Workers** (browsers) or **Worker Threads** / child processes (Node.js).

---

### Q78: What is `Promise.resolve(val)` vs `new Promise(resolve => resolve(val))`?
**Answer:**
- If `val` is already a Promise:
  - `Promise.resolve(val)` **returns the same Promise instance directly** ($O(1)$ unwrapping, no allocation).
  - `new Promise(resolve => resolve(val))` allocates a brand new Promise wrapper, resulting in additional execution steps and microtask delays.

---

### Q79: How do you build a concurrency-limiting Promise queue (Promise Pool)?
**Answer:**
```javascript
async function promisePool(tasks, limit) {
  const results = [];
  const executing = new Set();

  for (const task of tasks) {
    const promise = Promise.resolve().then(task);
    results.push(promise);
    executing.add(promise);

    const clean = () => executing.delete(promise);
    promise.then(clean, clean);

    if (executing.size >= limit) {
      await Promise.race(executing); // Wait for ANY executing task to finish
    }
  }

  return Promise.all(results);
}
```

---

### Q80: What is the difference between Microtasks and Macrotasks in terms of Error Handling?
**Answer:**
- If an unhandled error is thrown inside a synchronous function or a microtask, it does not stop macrotasks from running in subsequent iterations of the event loop.
- Synchronous `try...catch` cannot catch errors thrown inside asynchronous macrotask callbacks (e.g. `try { setTimeout(() => { throw new Error(); }, 0); } catch(e) {}` will NOT catch the error).
