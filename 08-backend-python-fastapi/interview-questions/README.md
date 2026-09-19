# 🐍 Python Core & FastAPI Senior & Lead Master Interview Question Bank (100 Questions)

> Comprehensive, production-grade 100-question interview bank covering everything from CPython internals, memory management, GIL, and Asyncio event loops to enterprise FastAPI, Pydantic V2, SQLAlchemy 2.0 Async, and production scaling.

---

## 📑 Curriculum & Question Bank Structure

```
08-backend-python-fastapi/interview-questions/
├── 01_python_core_mutability_memory_and_types_qna.md      ──► Questions 1 to 20
├── 02_python_functions_oop_dunder_and_mro_qna.md          ──► Questions 21 to 40
├── 03_python_gil_gc_concurrency_and_asyncio_qna.md        ──► Questions 41 to 60
├── 04_fastapi_pydantic_di_and_architecture_qna.md         ──► Questions 61 to 80
├── 05_fastapi_sqlalchemy_celery_and_production_ops_qna.md ──► Questions 81 to 100
├── coding_rate_limiting_middleware.md                     ──► Machine Coding
└── top_fastapi_interview_questions.md                     ──► Quick Refresher
```

---

## 🎯 Master Question Index (1 - 100)

### Part 1: Python Core, Mutability, Memory & Data Structures (Q1 - Q20)

* [`01_python_core_mutability_memory_and_types_qna.md`](./01_python_core_mutability_memory_and_types_qna.md)
  1. CPython execution model, bytecode compilation, and the Python Virtual Machine (PVM).
  2. Variables as reference labels ("name tags") vs memory buckets.
  3. `is` (identity/pointer) vs `==` (value equality).
  4. Small integer caching singleton range (`[-5, 256]`).
  5. String interning mechanics and `sys.intern()`.
  6. Mutable vs Immutable data types comprehensive matrix.
  7. Tuples containing mutable elements and hashability rules.
  8. Python `list` over-allocation resizing formula.
  9. Python 3.7+ Compact Dict split-table architecture (30% RAM savings).
  10. Python `set` hash table lookups and hashability requirements.
  11. `copy.copy` (shallow) vs `copy.deepcopy` (circular-safe deep copy).
  12. The mutable default argument anti-pattern (`def fn(x=[])`).
  13. List comprehensions (eager memory) vs Generator expressions (lazy $O(1)$ memory).
  14. `collections.deque` doubly linked block architecture vs `list.pop(0)`.
  15. `collections.defaultdict` and `Counter` optimizations.
  16. The Walrus Operator (`:=`) in Python 3.8+.
  17. Structural Pattern Matching (`match-case`) in Python 3.10+.
  18. `str()` (human readable) vs `repr()` (unambiguous debugging).
  19. `__slots__` attribute dictionary optimization (40% RAM savings).
  20. `frozenset` immutable hashable sets.

### Part 2: Functions, Scopes, Decorators, OOP & MRO (Q21 - Q40)

* [`02_python_functions_oop_dunder_and_mro_qna.md`](./02_python_functions_oop_dunder_and_mro_qna.md)
  21. The LEGB Scope resolution rule.
  22. `global` vs `nonlocal` keywords.
  23. Closures and the `__closure__` cell tuple.
  24. Decorator factories with arguments and `@functools.wraps`.
  25. `__new__` (instance creator) vs `__init__` (instance initializer).
  26. `@classmethod` vs `@staticmethod` vs Instance methods.
  27. Descriptor protocol (`__get__`, `__set__`) and `@property`.
  28. Method Resolution Order (MRO) and C3 Linearization.
  29. Cooperative `super()` in multiple inheritance.
  30. Metaclasses and dynamic class construction via `type`.
  31. Abstract Base Classes (`abc.ABC` and `@abstractmethod`).
  32. `__getattr__` (fallback) vs `__getattribute__` (unconditional).
  33. Context manager protocol (`__enter__` and `__exit__`).
  34. Modern `dataclasses` (`frozen=True`, `slots=True`).
  35. Monkey patching and runtime risks.
  36. Callable instances via `__call__`.
  37. `functools.lru_cache` bounded memory caching.
  38. Garbage collection interactions with `__del__`.
  39. Keyword-Only (`*`) and Positional-Only (`/`) arguments.
  40. Structural Duck Typing with `typing.Protocol`.

### Part 3: GIL, Garbage Collection, Concurrency & Asyncio Internals (Q41 - Q60)

* [`03_python_gil_gc_concurrency_and_asyncio_qna.md`](./03_python_gil_gc_concurrency_and_asyncio_qna.md)
  41. Global Interpreter Lock (GIL) purpose and reference count safety.
  42. PEP 703 Free-Threaded Python (No-GIL) in Python 3.13.
  43. When the GIL is released during I/O and C extensions.
  44. Reference Counting (`ob_refcnt`) + Generational Cyclic Garbage Collector.
  45. `multiprocessing` vs `threading` vs `asyncio` trade-off matrix.
  46. Event loop, Coroutines (`async def`), Tasks, and Futures.
  47. `asyncio.gather()` vs `asyncio.wait()` API comparison.
  48. Safely offloading blocking synchronous code via `asyncio.to_thread`.
  49. Structured Concurrency with `asyncio.TaskGroup` in Python 3.11+.
  50. Async Iterators (`__aiter__`, `__anext__`) and `async for`.
  51. Async Context Managers (`__aenter__`, `__aexit__`).
  52. `asyncio.shield()` preventing critical task cancellation.
  53. Resolving `RuntimeError: This event loop is already running`.
  54. `asyncio.Queue` non-blocking producer-consumer queues.
  55. `uvloop` C-level event loop performance.
  56. `contextvars` context-local storage in async coroutines.
  57. Timeout handling with `asyncio.timeout()`.
  58. Yielding execution to the event loop via `asyncio.sleep(0)`.
  59. `ProcessPoolExecutor` vs `ThreadPoolExecutor`.
  60. `asyncio.Semaphore` preventing connection exhaustion.

### Part 4: FastAPI Core, ASGI, Pydantic V2 & Dependency Injection (Q61 - Q80)

* [`04_fastapi_pydantic_di_and_architecture_qna.md`](./04_fastapi_pydantic_di_and_architecture_qna.md)
  61. ASGI vs WSGI architectural comparison.
  62. What happens in `def` (threadpool) vs `async def` (event loop) endpoints.
  63. Pydantic V2 Rust core (`pydantic-core`) performance optimizations.
  64. `@field_validator` vs `@model_validator` in Pydantic V2.
  65. FastAPI Dependency Injection (`Depends`) DAG and `use_cache`.
  66. `yield` dependencies and guaranteed post-response cleanup.
  67. Starlette Middleware vs APIRouter Dependencies.
  68. Global Exception Handling with `@app.exception_handler`.
  69. `typing.Annotated` for clean dependency injection.
  70. `response_model` filtering vs Python type hint inference.
  71. `response_model_exclude_unset=True` payload optimization.
  72. Automatic OpenAPI / Swagger generation via reflection.
  73. `Request` raw access vs typed parameters.
  74. Sub-Applications via `app.mount()`.
  75. Path Parameters vs Query Parameters.
  76. File Uploads: `UploadFile` (disk streaming) vs `File(bytes)` (RAM).
  77. CORS configuration with `CORSMiddleware`.
  78. Modular application structuring with `APIRouter`.
  79. The `lifespan` Context Manager in modern FastAPI.
  80. Datetime parsing and serialization in Pydantic V2.

### Part 5: SQLAlchemy 2.0 Async, Celery, WebSockets & Production Scaling (Q81 - Q100)

* [`05_fastapi_sqlalchemy_celery_and_production_ops_qna.md`](./05_fastapi_sqlalchemy_celery_and_production_ops_qna.md)
  81. SQLAlchemy 2.0 Async Engine and Session configuration.
  82. `expire_on_commit=False` preventing async lazy-load errors.
  83. Eliminating N+1 queries in SQLAlchemy (`selectinload` vs `joinedload`).
  84. FastAPI `BackgroundTasks` vs Celery / Redis Queues.
  85. Real-Time WebSocket Connection Manager and broadcast logic.
  86. Server-Sent Events (SSE) via `StreamingResponse`.
  87. OAuth2 Password Flow with JWT token validation.
  88. Production deployment: Gunicorn + UvicornWorker formula (`(2 * CPU) + 1`).
  89. Distributed Rate Limiting via SlowAPI and Redis.
  90. Database Migrations with Alembic.
  91. `fastapi.HTTPException` vs `starlette.exceptions.HTTPException`.
  92. Unit of Work pattern in async SQLAlchemy.
  93. Observability with OpenTelemetry and Prometheus.
  94. ARQ native async task queues vs Celery.
  95. Preventing connection leaks with shared `httpx.AsyncClient`.
  96. `model_dump()` vs `model_dump_json()` serialization.
  97. Mocking database sessions in FastAPI unit tests.
  98. Uvicorn graceful shutdown configurations.
  99. Pydantic `BaseModel` vs `RootModel`.
  100. Multi-tenant FastAPI application architecture.

---

## 💻 Machine Coding & Refresher

* [`coding_rate_limiting_middleware.md`](./coding_rate_limiting_middleware.md) — Distributed Sliding Window Rate Limiting Middleware.
* [`top_fastapi_interview_questions.md`](./top_fastapi_interview_questions.md) — Senior Lead Quick Refresher.
