# Python & FastAPI Master Interview Bank: Part 4 (Q61 - Q80)
## FastAPI Core, ASGI, Pydantic V2 & Dependency Injection

---

### Q61: What is the architectural difference between WSGI and ASGI?
**Answer:**
```
[ WSGI (Web Server Gateway Interface - Flask / Django) ]
  ├── Synchronous Request-Response protocol.
  ├── Server allocates 1 OS thread per active HTTP connection.
  └── CANNOT handle long-lived connections (WebSockets, SSE, Streaming).

[ ASGI (Asynchronous Server Gateway Interface - FastAPI / Starlette) ]
  ├── Asynchronous, non-blocking coroutine-based protocol.
  ├── Single event loop handles thousands of concurrent connections.
  └── First-class support for HTTP/2, WebSockets, and Server-Sent Events.
```
- **ASGI Signature:** `async def app(scope, receive, send):`
  - `scope`: Dictionary containing connection metadata (headers, client IP, path).
  - `receive`: Async callable to read incoming request body chunks.
  - `send`: Async callable to stream response headers and data chunks back to client.

---

### Q62: What happens when you declare an endpoint with `def` vs `async def` in FastAPI?
**Answer:**
FastAPI treats the two declarations fundamentally differently:
- **`async def endpoint():`**
  FastAPI executes the function **directly on the main single-threaded `asyncio` event loop**.
  - *Rule:* Code inside MUST be strictly non-blocking (`await asyncio.sleep()`, `httpx`).
  - *Danger:* Calling blocking synchronous functions (`time.sleep()`, synchronous DB drivers) blocks the entire server for all users!
- **`def endpoint():` (Plain synchronous function):**
  FastAPI detects it is not a coroutine and automatically **offloads its execution to an external background ThreadPoolExecutor** (`anyio.to_thread`).
  - *Rule:* Safe for legacy synchronous libraries, synchronous ORMs, and heavy disk I/O without blocking the main event loop.

---

### Q63: How did Pydantic V2 achieve a 5x-10x performance increase?
**Answer:**
1. **Rust Core Engine (`pydantic-core`):** Validation, type coercion, and JSON parsing logic was rewritten from pure Python into compiled **Rust**.
2. **Direct JSON Parsing:** In V1, JSON was deserialized by Python into a dictionary, and then validated into models. In V2, Rust parses raw JSON strings directly into Pydantic models in a single pass without intermediate Python dictionary allocations!
3. **Rust String Serialization (`model_dump_json()`):** Serializes models directly into UTF-8 JSON bytes in compiled Rust.

---

### Q64: What is the difference between `@field_validator` and `@model_validator` in Pydantic V2?
**Answer:**
- **`@field_validator('field_name', mode='after'|'before')`:**
  Validates a single field in isolation:
  - `mode='before'`: Executes on the raw input value *before* Pydantic performs type coercion.
  - `mode='after'` (default): Executes *after* Pydantic parsed the field into its declared type.
- **`@model_validator(mode='after'|'before')`:**
  Validates cross-field dependencies and relationships across the entire object:
  - `mode='after'`: Receives the fully initialized model instance (`self`) to validate constraints (e.g. `assert self.end_date > self.start_date`).

---

### Q65: How does FastAPI's Dependency Injection (`Depends`) work under the hood?
**Answer:**
- FastAPI constructs a **Directed Acyclic Graph (DAG)** of all dependencies for an endpoint at application startup.
- When an HTTP request arrives:
  1. FastAPI traverses the DAG from leaves to root.
  2. Resolves sub-dependencies first.
  3. By default, **`use_cache=True`**: If three different services or route dependencies inject `get_db()`, FastAPI executes `get_db()` **strictly once per request** and caches the returned instance across that request's lifecycle.
  4. Injects the resolved values into the endpoint parameters.

---

### Q66: How do `yield` dependencies work in FastAPI, and how is cleanup guaranteed?
**Answer:**
- A dependency function can use `yield` instead of `return` to create a context manager:
  ```python
  async def get_db():
      session = await async_session_factory()
      try:
          yield session
          await session.commit()
      except Exception:
          await session.rollback()
          raise
      finally:
          await session.close()
  ```
- **Execution Flow:**
  1. Code *before* `yield` runs before the route handler is invoked.
  2. The yielded value is injected into the endpoint.
  3. The route handler executes and returns the HTTP response.
  4. Code *after* `yield` executes reliably in a `finally` block **after the response is sent to the client**, guaranteeing cleanup of connections or locks.

---

### Q67: What is the difference between Middleware and APIRouter Dependencies?
**Answer:**
| Dimension | Starlette Middleware | Router Dependency (`Depends`) |
| :--- | :--- | :--- |
| **Execution Layer** | Lowest ASGI layer (runs for **every single request** before path routing). | Runs **after routing** matches the endpoint. |
| **Data Access** | Raw HTTP headers and raw stream bytes only. | Typed route path parameters, query parameters, Pydantic validated body data. |
| **Response Modification**| Can modify raw response headers, compress payload (GZip). | Does not directly intercept final outgoing response. |
| **Use Case** | CORS, TLS termination, Request timing, Trace IDs. | Authentication, RBAC authorization, Database transaction boundaries. |

---

### Q68: How do you implement Global Exception Handling in FastAPI?
**Answer:**
Use `@app.exception_handler`:
```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

class DomainException(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error_code": exc.code, "detail": exc.message, "path": request.url.path}
    )
```

---

### Q69: What is `Annotated` in Python typing and how does FastAPI leverage it?
**Answer:**
- Introduced in Python 3.9 (`typing.Annotated[T, metadata]`).
- Separates type definitions from framework metadata:
  ```python
  from typing import Annotated
  from fastapi import Depends, Query

  CurrentUser = Annotated[User, Depends(get_current_active_user)]
  SearchParam = Annotated[str, Query(min_length=3, max_length=50)]

  @app.get("/items")
  def read_items(user: CurrentUser, q: SearchParam):
      return {"user": user.id, "query": q}
  ```
- **Benefit:** Cleaner function signatures, superior code reuse, and cleaner linting with static type checkers (MyPy).

---

### Q70: What is the difference between `response_model` and function return type hint?
**Answer:**
- In FastAPI:
  - If you specify `response_model=UserPublic`, FastAPI automatically filters out private fields (like `hashed_password`) from the database entity before sending JSON to the client!
  - It also generates the exact OpenAPI response schema for Swagger UI.
  - In modern FastAPI, if you use standard Python return type hints `-> UserPublic:`, FastAPI will automatically infer `response_model=UserPublic`.

---

### Q71: What is `response_model_exclude_unset=True` and why is it useful?
**Answer:**
- Prevents serializing default model fields that were not explicitly set in the data payload.
- Keeps network payloads compact and distinguishes between a field set explicitly to `None` vs a field that was simply omitted.

---

### Q72: How does FastAPI generate OpenAPI (Swagger) documentation automatically?
**Answer:**
1. At application startup, FastAPI uses reflection (`get_type_hints`, `inspect`) on all route functions and Pydantic models.
2. It constructs an internal OpenAPI 3.1.0 JSON representation served dynamically at `/openapi.json`.
3. The `/docs` endpoint serves HTML containing the Swagger UI JavaScript bundle, which renders the JSON schema into an interactive API sandbox.

---

### Q73: What is the difference between `Request` and `APIRoute` parameters?
**Answer:**
- Directly injecting `request: Request` provides raw access to the underlying Starlette Request object (client IP, cookies, raw headers, body stream).
- Usually unnecessary because FastAPI automatically extracts and validates typed parameters (`Path()`, `Query()`, `Header()`, `Body()`).

---

### Q74: What are Sub-Applications in FastAPI (`app.mount()`)?
**Answer:**
- Allows mounting completely independent WSGI or ASGI applications inside a parent FastAPI application:
  ```python
  app = FastAPI()
  admin_app = FastAPI()
  app.mount("/admin", admin_app)
  ```
- The sub-app has its own OpenAPI docs (`/admin/docs`), its own middleware, and its own exception handlers.

---

### Q75: What is the difference between Path Parameters and Query Parameters in FastAPI?
**Answer:**
- **Path Parameter (`/users/{user_id}`):** Part of the URL route path itself; strictly mandatory to match the endpoint.
- **Query Parameter (`/users?role=admin&limit=10`):** Appears after the `?` in the URL; optional by default (unless defined without a default value).

---

### Q76: How do you handle File Uploads in FastAPI (`UploadFile` vs `bytes`)?
**Answer:**
- **`File(bytes)`**: Loads the **entire file into RAM** immediately. Fails and crashes the server with OOM on large files (e.g. 500MB video).
- **`UploadFile` (Standard Best Practice):**
  - Uses a Spooled Temporary File on disk: files $< 1\text{MB}$ stay in RAM; larger files are streamed directly to a temporary file on disk.
  - Provides async methods: `await file.read()`, `await file.seek(0)`, `await file.write()`.

---

### Q77: What is CORS and how do you configure `CORSMiddleware` in FastAPI?
**Answer:**
- **CORS (Cross-Origin Resource Sharing):** Browser security mechanism that prevents web pages loaded from one origin from making API requests to a different origin unless the server explicitly sends `Access-Control-Allow-Origin` headers.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Q78: How do you organize large FastAPI applications using `APIRouter`?
**Answer:**
Divide application into domain modules using `APIRouter`:
```python
# app/routers/users.py
router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def list_users(): ...

# app/main.py
app.include_router(users.router)
app.include_router(orders.router)
```

---

### Q79: What is the `lifespan` Context Manager in FastAPI?
**Answer:**
- Replaces deprecated `@app.on_event("startup")` and `@app.on_event("shutdown")`.
- Uses an asynchronous context manager passed to `FastAPI(lifespan=lifespan)`:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Redis and DB connection pools
    redis_client = await init_redis()
    yield {"redis": redis_client}
    # Shutdown: Safely close connection pools
    await redis_client.close()

app = FastAPI(lifespan=lifespan)
```

---

### Q80: How does Pydantic V2 handle Datetime parsing and Serialization?
**Answer:**
- Parses ISO 8601 strings directly in Rust `pydantic-core` into timezone-aware `datetime.datetime` objects.
- Configurable via `model_config = ConfigDict(ser_json_timedelta='float')`.
