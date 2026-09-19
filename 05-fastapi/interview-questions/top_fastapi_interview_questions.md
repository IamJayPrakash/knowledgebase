# Top FastAPI Senior Interview Questions (Async Architecture & Concurrency)

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
