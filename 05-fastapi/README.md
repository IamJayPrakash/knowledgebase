# 🐍 FastAPI & Python Async Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index from **Python Async Core to High-Performance Enterprise APIs** for Senior Technical Lead & SDE-2/3 interviews.

---

## 📌 How to Use This Section
- Use this `README.md` as your master index and curriculum roadmap for FastAPI.
- Create single concept files inside `05-fastapi/` (e.g., `01_asyncio_event_loop_and_concurrency.md`) as you learn and add your notes, code snippets, and interview pointers.

---

## 🗺️ Learning Roadmap & Concept Index

### 1. Python Async Core & Concurrency
- [ ] `01_asyncio_event_loop_and_concurrency.md` — `asyncio` Event Loop, Coroutines vs Threads vs Processes, `asyncio.gather()`, `asyncio.create_task()`, Global Interpreter Lock (GIL).
- [ ] `02_async_def_vs_def_in_fastapi.md` — How FastAPI executes `async def` (on asyncio main thread) vs `def` (in Starlette ThreadPoolExecutor), Preventing blocking calls.

### 2. FastAPI Architecture & Pydantic V2
- [ ] `03_asgi_and_starlette_internals.md` — WSGI vs ASGI specification, Starlette request/response handling, Uvicorn/Gunicorn worker model.
- [ ] `04_pydantic_v2_validation_core.md` — Pydantic V2 Rust core (`pydantic-core`), Schema compilation, Field validation, `@field_validator` & `@model_validator`, Serialization performance.

### 3. Dependency Injection & API Design
- [ ] `05_dependency_injection_system.md` — FastAPI `Depends()` engine, Sub-dependencies tree resolution, Yield dependencies for DB connection lifecycle (`try...finally`).
- [ ] `06_middleware_and_exception_handling.md` — Custom ASGI Middlewares, Request context injection, Global Exception Handlers (`HTTPException` vs custom exceptions).

### 4. Database Integration & Async ORMs
- [ ] `07_async_sqlalchemy2_and_alembic.md` — Async engine, `AsyncSession`, Unit of Work pattern, Alembic async migrations, N+1 query problem prevention.
- [ ] `08_background_tasks_and_celery.md` — FastAPI `BackgroundTasks` (for lightweight tasks) vs Celery + Redis / RabbitMQ (for heavy distributed background processing).

---

## 💡 High-Yield Senior Interview Questions Pointers

1. **What happens if you run a blocking synchronous function (e.g. `time.sleep(5)`) inside an `async def` route in FastAPI?**
   * *Answer Pointer:* It blocks Python's `asyncio` event loop thread completely, freezing all incoming async requests across the entire application instance. Solution: Use `def` route (runs in threadpool) or use `await asyncio.sleep(5)` or `anyio.to_thread.run_sync()`.
2. **What is the difference between WSGI and ASGI?**
   * *Answer Pointer:* WSGI (e.g. Flask/Django) is synchronous and handles one request per worker thread. ASGI (e.g. FastAPI/Starlette) supports asynchronous I/O natively, enabling WebSockets, HTTP/2 streaming, and handling thousands of concurrent connections per worker.
3. **How does Pydantic V2 achieve 5-20x speedups over V1?**
   * *Answer Pointer:* Pydantic V2 replaced Python-based validation logic with `pydantic-core`, written in Rust. Type parsing, validation, and CPython C-API bindings occur directly in compiled C/Rust code rather than interpreted Python bytecode.
