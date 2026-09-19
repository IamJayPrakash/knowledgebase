# Python & FastAPI Master Interview Bank: Part 3 (Q41 - Q60)
## GIL, Garbage Collection, Concurrency & Asyncio Internals

---

### Q41: What is the Global Interpreter Lock (GIL) in CPython and why was it implemented?
**Answer:**
- **The GIL:** A mutual exclusion lock used by CPython to prevent multiple OS threads from executing Python bytecode simultaneously.
- Even on an 8-core CPU with 8 threads running CPU-intensive code, **CPython executes on only 1 core at any instant**.
- **Why Implemented:**
  1. CPython's memory management is NOT thread-safe. Reference counting (`ob_refcnt`) would suffer race conditions and corrupted memory if two threads altered reference counts concurrently without locks.
  2. Acquiring a single global interpreter lock was much faster and simpler than managing thousands of fine-grained locks on every single object in memory.
  3. Easy C extension integration (C libraries could run without complex lock management).

---

### Q42: What is PEP 703 (Free-Threaded Python / No-GIL) in Python 3.13?
**Answer:**
- **PEP 703 (Making the Global Interpreter Lock Optional):**
  - Accepted for Python 3.13+ as an experimental build (`python3.13t`).
  - Replaces the GIL with:
    1. **Biased Reference Counting:** Single-threaded objects use fast thread-local reference counts; multi-threaded shared objects use atomic instructions.
    2. **Mimalloc Memory Allocator:** Thread-safe, high-performance mimalloc engine.
    3. **Stop-The-World GC Pauses:** For cyclic garbage collection when needed.
- **Impact:** Enables true multi-core parallel CPU execution across standard Python threads!

---

### Q43: When does the GIL release control to other threads in standard Python?
**Answer:**
The GIL is automatically released:
1. **During I/O Operations:** Network socket reads/writes (`requests`, `urllib`), file disk I/O, database queries, and `time.sleep()`.
2. **During Compute in C Extensions:** NumPy matrix operations, OpenCV image processing, and Cryptography algorithms release the GIL during pure C/Fortran math.
3. **Check Interval (Preemptive Switch):** Every 5 milliseconds (or 100 bytecode instructions), CPython pauses the running thread and releases the GIL, allowing waiting threads to contend for execution.

---

### Q44: How does Python's Garbage Collection work? Reference Counting + Cyclic GC.
**Answer:**
Python uses a **two-tier memory management architecture**:
1. **Primary: Reference Counting (Instant Collection)**
   - Every object has a header struct `PyObject` containing `ob_refcnt`.
   - Incremented when referenced; decremented when dereferenced (`del`, exiting scope).
   - When `ob_refcnt == 0`, memory is **freed immediately**.
2. **Secondary: Generational Cyclic GC (`gc` module)**
   - Reference counting fails on **Circular References** (Object A points to B, and B points to A; `refcnt` is 1 even if unreachable from GC roots).
   - The cyclic GC tracks container objects (`list`, `dict`, `set`, class instances) across 3 generations (Gen 0, Gen 1, Gen 2).
   - Detects cycles by finding unreachable subgraphs and reclaims them.

---

### Q45: Compare `multiprocessing` vs `threading` vs `asyncio` in Python.
**Answer:**
| Dimension | `multiprocessing` | `threading` | `asyncio` |
| :--- | :--- | :--- | :--- |
| **Model** | Multiple independent OS processes. | Multiple OS threads in single process. | **Single thread**, single process cooperative multitasking. |
| **Memory** | Completely isolated memory (requires IPC/Pickle). | Shared memory space (requires locks). | Shared memory space (zero thread race conditions). |
| **GIL Impact**| **Bypasses GIL** (1 process per CPU core). | Constrained by GIL for CPU tasks. | Runs on single thread (GIL irrelevant). |
| **Overhead** | High (process spawn, memory duplication). | Medium (thread stack memory ~8MB). | **Ultra-low** (millions of coroutines in single heap). |
| **Ideal Workload**| Heavy CPU tasks (ML, video encoding, math). | Blocking legacy I/O libraries. | High-concurrency I/O (WebSockets, REST APIs). |

---

### Q46: How does `asyncio` work under the hood? Coroutines, Tasks, and Event Loop.
**Answer:**
- **Event Loop:** A single-threaded infinite loop that manages and distributes the execution of different asynchronous events (backed by `epoll` on Linux, `kqueue` on macOS, `IOCP` on Windows).
- **Coroutine (`async def`):** A special function that returns a coroutine object. Execution pauses at `await` and yields control back to the event loop.
- **Task (`asyncio.create_task`):** A wrapper that schedules a coroutine onto the event loop to run concurrently in the background as an independent cooperative unit.
- **Future:** A low-level object representing an eventual result of an asynchronous operation.

---

### Q47: What is the difference between `asyncio.gather()` and `asyncio.wait()`?
**Answer:**
- **`asyncio.gather(*coros_or_tasks, return_exceptions=False)`:**
  - High-level API for running tasks in parallel.
  - Returns a **list of results in the exact order of the passed coroutines**.
  - If `return_exceptions=True`, errors are returned as values in the result list rather than aborting the gather.
- **`asyncio.wait(fs, return_when=ALL_COMPLETED)`:**
  - Lower-level control.
  - Returns two sets: `(done_tasks, pending_tasks)`.
  - Supports `return_when=FIRST_COMPLETED` or `FIRST_EXCEPTION`, enabling early termination patterns.

---

### Q48: How do you safely run blocking synchronous code inside an `asyncio` application?
**Answer:**
Never call blocking functions directly in the event loop! Use **`loop.run_in_executor`** or **`asyncio.to_thread`** (Python 3.9+):

```python
import asyncio
import time

def blocking_io(name):
    time.sleep(2) # Synchronous blocking call
    return f"Done: {name}"

async def main():
    # Offloads execution to ThreadPoolExecutor without freezing the event loop:
    result = await asyncio.to_thread(blocking_io, "Image Processing")
    print(result)
```

---

### Q49: What is `asyncio.TaskGroup` in Python 3.11+?
**Answer:**
- Modern **Structured Concurrency** API replacing `asyncio.gather()`.
- Implemented as an asynchronous context manager (`async with asyncio.TaskGroup() as tg:`).
- **Safety Guarantee:** If any child task inside the group fails, the TaskGroup **automatically cancels all other sibling tasks**, waiting for their cancellation to complete before raising an `ExceptionGroup` containing all errors!

```python
import asyncio

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(1))
        task2 = tg.create_task(fetch_orders(1))
    # Both guaranteed complete here; zero orphaned task leaks!
    print(task1.result(), task2.result())
```

---

### Q50: How do Async Iterators (`__aiter__`, `__anext__`) work?
**Answer:**
- An object implementing `__aiter__()` returning an object implementing `__anext__()` returning an awaitable value.
- Consumed via **`async for item in async_iterable:`**.
- Throws `StopAsyncIteration` to terminate iteration.

```python
class AsyncCounter:
    def __init__(self, limit):
        self.limit = limit
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count < self.limit:
            await asyncio.sleep(0.1) # Asynchronous pause
            self.count += 1
            return self.count
        raise StopAsyncIteration
```

---

### Q51: How do Async Context Managers (`__aenter__`, `__aexit__`) work?
**Answer:**
- Used with `async with`:
  - `async def __aenter__(self)`: Awaits setup (e.g. acquiring async DB connection or HTTP session).
  - `async def __aexit__(self, exc_type, exc, tb)`: Awaits teardown (e.g. closing socket).

---

### Q52: What is `asyncio.shield()` and when should you use it?
**Answer:**
- `asyncio.shield(task)` prevents a task from being cancelled if the outer enclosing coroutine is cancelled.
- **Use Case:** Critical write operations (e.g., logging payment audit record) that must complete even if the client disconnects and cancels the HTTP request.

---

### Q53: What causes `RuntimeError: This event loop is already running`?
**Answer:**
- Occurs when calling `asyncio.run(coro())` from inside a thread that already has an active, running event loop (e.g., inside Jupyter Notebooks, Tornado, or FastAPI).
- **Fix:** In existing event loops, use `await coro()` or `asyncio.create_task(coro())`, or use the `nest_asyncio` library.

---

### Q54: How does `asyncio.Queue` enable Producer-Consumer pipelines?
**Answer:**
- Single-threaded, non-blocking asynchronous queue.
- `await queue.put(item)`: Suspends if queue reaches `maxsize`.
- `await queue.get()`: Suspends if queue is empty.
- Enables high-throughput async processing without thread locks.

---

### Q55: What is `uvloop` and why is it faster than standard `asyncio`?
**Answer:**
- `uvloop` is a drop-in replacement for the standard Python `asyncio` event loop.
- Written in Cython and built on top of **`libuv`** (the high-performance C library powering Node.js).
- **Performance:** 2x to 4x faster than standard Python `asyncio`, achieving speeds comparable to Node.js and Go. (Used by default in Uvicorn).

---

### Q56: What are `contextvars` in Python and why are they vital for Asyncio?
**Answer:**
- In multithreaded code, `threading.local` stores thread-isolated data.
- In `asyncio`, thousands of coroutines run on the **same single thread**, so `threading.local` leaks data across concurrent user requests!
- **`contextvars` (PEP 567):** Provides context-local storage that follows the asynchronous execution flow of coroutines and tasks without cross-contamination. (Used for request IDs and auth context in FastAPI).

---

### Q57: How do you handle Timeouts in `asyncio`?
**Answer:**
- Python 3.11+: Use **`asyncio.timeout(delay)`** context manager:
  ```python
  try:
      async with asyncio.timeout(2.5):
          await fetch_data()
  except TimeoutError:
      print("Timed out!")
  ```
- Python 3.10 and earlier: `await asyncio.wait_for(coro(), timeout=2.5)`.

---

### Q58: What is `asyncio.sleep(0)` and why is it used?
**Answer:**
- `await asyncio.sleep(0)` forces the current coroutine to **yield execution back to the event loop**.
- Gives other ready tasks in the event loop queue an opportunity to execute, preventing a long-running CPU loop from starving other coroutines.

---

### Q59: What is ProcessPoolExecutor vs ThreadPoolExecutor in `concurrent.futures`?
**Answer:**
- **`ThreadPoolExecutor`**: Pools OS threads within the same process. Bound by GIL; best for legacy blocking I/O calls.
- **`ProcessPoolExecutor`**: Spawns a pool of independent Python processes. Completely bypasses the GIL; best for CPU-bound computations. Arguments and return values must be serializable via `pickle`.

---

### Q60: How does `asyncio.Semaphore` prevent connection pool exhaustion?
**Answer:**
- Caps the number of concurrent asynchronous operations accessing a scarce external resource:
  ```python
  sem = asyncio.Semaphore(10) # Max 10 concurrent requests

  async def safe_fetch(url):
      async with sem:
          return await http_client.get(url)
  ```
