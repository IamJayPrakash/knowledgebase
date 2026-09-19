# 🐍 FastAPI & Python Async Interview Questions Index

> A categorized index of **Asyncio Event Loop Questions, Pydantic V2 Challenges, ASGI Internals, and High-Performance API Design Questions** for Senior FastAPI Interviews.

---

## 📌 How to Use This Directory
- Add individual markdown files for specific FastAPI interview questions in this folder (e.g., `01_async_db_session.md`, `02_custom_pydantic_validator.md`).
- Use this `README.md` as your index and checklist.

---

## 📑 Interview Questions Index

### 1. Rapid-Fire / Short Questions
- [ ] `short_questions_asyncio.md` — Coroutines vs Tasks, `asyncio.gather()` vs `asyncio.as_completed()`, GIL impact.
- [ ] `short_questions_fastapi.md` — `async def` vs `def` routes, Starlette ASGI vs WSGI, Pydantic V2 core.

### 2. Python & FastAPI Coding Challenges
- [ ] `coding_async_middleware.md` — Write a custom ASGI middleware for log context tracing and execution timing.
- [ ] `coding_pydantic_v2_custom_schema.md` — Write complex nested Pydantic models with custom field validators and transformations.
- [ ] `coding_async_rate_limiter.md` — Build an async dependency-injected Rate Limiter using Redis and `anyio`.

### 3. Senior Lead Architectural Scenarios
- [ ] `scenario_event_loop_blocking.md` — Diagnosing and fixing an incident where a synchronous library blocked the asyncio loop.
- [ ] `scenario_async_db_connection_pooling.md` — Configuring async SQLAlchemy connection pooling under 10,000 concurrent requests.
