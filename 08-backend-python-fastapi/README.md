# 🐍 Python Core & FastAPI Enterprise Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index from **Complete Python Newbie Fundamentals to Advanced CPython Internals & High-Performance FastAPI Enterprise Architecture**.

---

## 🗺️ Learning Roadmap & Concept Index

### Level 1: 🐣 Python Core Foundations (Newbie ➡️ Experienced)
- [x] [`01_python_fundamentals_syntax_types_and_mutability.md`](./01_python_fundamentals_syntax_types_and_mutability.md) — CPython execution model, Dynamic typing, Variables as name bindings (luggage tags), Memory mutability vs immutability (`int`, `str` vs `list`, `dict`), `id()`, `is` vs `==`, Small Integer Caching (`[-5, 256]`), and the Mutable Default Argument trap.
- [x] [`02_python_collections_lists_tuples_dicts_sets.md`](./02_python_collections_lists_tuples_dicts_sets.md) — `list` over-allocation resizing formula, `tuple` immutability & hashability, `set` hash table operations, Python 3.7+ Compact Dict split-table architecture, and time complexities ($O(1)$ vs $O(N)$).
- [x] [`03_python_functions_scopes_args_kwargs_and_decorators.md`](./03_python_functions_scopes_args_kwargs_and_decorators.md) — First-class functions, `*args` and `**kwargs`, LEGB scope rule, `global` vs `nonlocal`, Closures (`func.__closure__`), Decorator factories with arguments, and why `@functools.wraps` is mandatory.
- [x] [`04_python_oop_classes_dunder_methods_and_mro.md`](./04_python_oop_classes_dunder_methods_and_mro.md) — `__init__` vs `__new__`, `@classmethod` vs `@staticmethod` vs `@property`, Dunder methods (`__str__`, `__repr__`, `__len__`, `__getitem__`, `__eq__`, `__hash__`), Diamond problem, C3 Linearization (MRO), and cooperative `super()`.
- [x] [`05_python_generators_iterators_and_context_managers.md`](./05_python_generators_iterators_and_context_managers.md) — Iteration protocol (`__iter__`, `__next__`, `StopIteration`), `yield` stack frame suspension, Generator expressions memory benchmarking, `with` statement, `__enter__` and `__exit__`, and `@contextlib.contextmanager`.
- [x] [`06_python_memory_gc_gil_and_concurrency.md`](./06_python_memory_gc_gil_and_concurrency.md) — CPython reference counting (`ob_refcnt`), Cyclic Garbage Collector (Generations 0, 1, 2), Global Interpreter Lock (GIL) internals, and the concurrency matrix: `multiprocessing` (CPU-bound) vs `threading` vs `asyncio` (I/O-bound).
- [x] [`07_python_exceptions_typing_and_modern_features.md`](./07_python_exceptions_typing_and_modern_features.md) — Exception hierarchy, `try-except-else-finally`, explicit exception chaining (`raise ... from`), Static typing with `typing.Protocol`, Walrus operator (`:=`), and Python 3.10+ Structural Pattern Matching (`match-case`).

### Level 2: 🚀 Advanced Asyncio & Enterprise FastAPI Framework
- [x] [`08_asyncio_event_loop_and_concurrency.md`](./08_asyncio_event_loop_and_concurrency.md) — Python `asyncio` single-threaded cooperative multitasking, Coroutines, Tasks, Futures, and Starlette worker threading.
- [x] [`09_pydantic_v2_validation_and_serialization.md`](./09_pydantic_v2_validation_and_serialization.md) — Rust-based `pydantic-core`, Field and model validators, and high-throughput serialization.
- [x] [`10_dependency_injection_system.md`](./10_dependency_injection_system.md) — FastAPI `Depends()` Directed Acyclic Graph (DAG) resolution, yield dependencies for database transaction lifecycles.
- [x] [`11_background_tasks_and_celery.md`](./11_background_tasks_and_celery.md) — In-process `BackgroundTasks` vs distributed Celery worker task queues with Redis/RabbitMQ.
- [x] [`12_high_performance_asgi_starlette_uvicorn.md`](./12_high_performance_asgi_starlette_uvicorn.md) — ASGI specification, Uvicorn uvloop event loop, Gunicorn process manager, and connection backpressure.

---

## 💡 High-Yield Senior Interview Questions Pointers

1. **Why does Python have a Global Interpreter Lock (GIL), and how do you bypass it?**
   * *Answer Pointer:* The GIL protects CPython's non-thread-safe reference counting memory management. For CPU-bound parallel workloads, bypass the GIL using `multiprocessing` (independent OS processes with dedicated Python interpreters) or native C/Rust extensions (e.g. NumPy).
2. **What happens if you run a blocking synchronous call inside an `async def` route in FastAPI?**
   * *Answer Pointer:* It blocks Python's single asyncio event loop thread, completely freezing all concurrent requests across the worker. Solution: Use normal `def` (which runs in Starlette's threadpool) or use `await anyio.to_thread.run_sync()`.
3. **Difference between `is` and `==` in Python?**
   * *Answer Pointer:* `==` checks value equality (via `__eq__`), whereas `is` checks object identity (whether both operands reference the exact same memory address via `id()`).
