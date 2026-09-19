# Top 20+ Senior FastAPI & Async Python Interview Questions & Answers

---

## 🏗️ Core Architecture & Async Event Loop Internals

### Q1: What happens if you run blocking synchronous I/O inside an `async def` endpoint in FastAPI?

**Answer:**

- In an `async def` route, FastAPI runs the coroutine directly on the single OS thread executing the `asyncio` event loop.
- If you call blocking synchronous functions (e.g., `time.sleep()`, synchronous `requests.get()`, or legacy synchronous database drivers like `psycopg2`), the **entire event loop thread halts**.
- **Impact:** All concurrent requests from other clients waiting on the event loop are completely frozen until the blocking call finishes.
- **Solution:**
  1. Use non-blocking async libraries: `asyncio.sleep()`, `httpx.AsyncClient()`, `asyncpg`, `aiofiles`.
  2. If a blocking third-party library must be used, declare the route with standard `def` (without `async`). FastAPI detects `def` endpoints and automatically offloads their execution to an internal `anyio` threadpool (`concurrent.futures.ThreadPoolExecutor`), keeping the main event loop unblocked.
  3. Explicitly offload via `await anyio.to_thread.run_sync(blocking_fn, arg1)`.

```python
from fastapi import FastAPI
import asyncio
import time
import anyio

app = FastAPI()

# ❌ ANTI-PATTERN: Freezes entire server for 5 seconds for ALL clients
@app.get("/bad-sync-in-async")
async def bad_sync_in_async():
    time.sleep(5) 
    return {"status": "blocked"}

# ✅ CORRECT: Native async non-blocking sleep
@app.get("/good-async")
async def good_async():
    await asyncio.sleep(5)
    return {"status": "unblocked"}

# ✅ CORRECT: Declared as def; FastAPI offloads to threadpool
@app.get("/good-sync-threadpool")
def good_sync_threadpool():
    time.sleep(5)
    return {"status": "run in threadpool"}
```

---

### Q2: How does FastAPI achieve automatic OpenAPI / Swagger generation?

**Answer:**

- FastAPI is built on top of Starlette and Pydantic.
- At application startup, FastAPI uses Python's `inspect` module and type annotations (`typing.Annotated`, `get_type_hints`) on route functions and dependency providers.
- It translates Python type hints, Pydantic model schemas, and HTTP parameter locations (`Query`, `Path`, `Header`, `Cookie`, `Body`) into standard JSON Schema definitions conforming to the **OpenAPI 3.1.0** specification.
- These schemas are served dynamically at `/openapi.json`, which Swagger UI (`/docs`) and ReDoc (`/redoc`) consume to render interactive API exploration interfaces.

---

### Q3: What is the difference between `model_dump()` and `model_dump_json()` in Pydantic V2?

**Answer:**

- **Pydantic V1 vs V2:** Pydantic V2 completely rewrote its core validation and serialization logic in Rust (`pydantic-core`), replacing `model.dict()` and `model.json()`.
- **`model_dump()`:** Serializes a Pydantic model into a native Python dictionary (`dict`). Performs field conversions (e.g., Datetime objects, Enums, UUIDs) according to model configuration.
- **`model_dump_json()`:** Serializes the model **directly** into a UTF-8 JSON string directly in compiled Rust code. It is up to 5x-10x faster than calling `json.dumps(model.model_dump())` because it avoids intermediate Python dictionary allocations.

---

### Q4: Explain the FastAPI Dependency Injection (`Depends`) lifecycle and sub-dependencies

**Answer:**

- FastAPI's Dependency Injection system (`Depends`) resolves dependencies recursively using a directed acyclic graph (DAG).
- When a request enters an endpoint:
  1. FastAPI inspects all `Depends(...)` parameters.
  2. If a dependency itself requires sub-dependencies, those are resolved first (depth-first traversal).
  3. By default, dependencies are **cached per request** (`use_cache=True`). If three separate services or sub-dependencies inject `get_db()`, `get_db()` executes **only once** per request and all consumers receive the identical instance.
  4. Dependencies that use `yield` support clean setup and teardown logic (context managers): code before `yield` runs before the route handler, and code after `yield` executes reliably in a `finally` block even if an unhandled exception occurred in the route.

```python
from fastapi import Depends, FastAPI
from typing import Generator

app = FastAPI()

def get_db_session() -> Generator[str, None, None]:
    session = "db_connection_acquired"
    print(">>> Setup: Connection opened")
    try:
        yield session
    finally:
        print("<<< Teardown: Connection closed safely")

@app.get("/items")
def read_items(db: str = Depends(get_db_session)):
    return {"db_status": db}
```

---

### Q5: What is the difference between FastAPI `BackgroundTasks` and Celery / Redis Queues?

**Answer:**

| Dimension | FastAPI `BackgroundTasks` | Distributed Task Queue (Celery / ARQ / RQ) |
| :--- | :--- | :--- |
| **Execution Environment** | Runs in-process inside the same ASGI worker process (either event loop or threadpool). | Runs out-of-process in dedicated background worker containers. |
| **Persistence** | In-memory only. If the server crashes or restarts, pending tasks are permanently lost. | Durable message broker (RabbitMQ / Redis) with ACK/NACK and retry queues. |
| **Scalability** | Tied directly to the web container CPU/RAM. Heavy background work degrades HTTP throughput. | Independently scalable worker nodes; can autoscale to hundreds of workers. |
| **Ideal Use Case** | Trivial, non-critical post-response tasks: sending an audit log, updating an in-memory cache, fire-and-forget notification. | Long-running tasks (>1s): video transcoding, PDF generation, batch email delivery, machine learning inference. |

---

### Q6: How do you implement global Exception Handling in FastAPI without leaking stack traces?

**Answer:**
Use `@app.exception_handler` to catch custom application exceptions and standard `RequestValidationError`:

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

class EntityNotFoundException(Exception):
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

@app.exception_handler(EntityNotFoundException)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "ENTITY_NOT_FOUND",
            "message": f"{exc.entity_name} with ID '{exc.entity_id}' does not exist.",
            "path": request.url.path,
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the full traceback internally via structured logger (do NOT return exc details to client)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error_code": "INTERNAL_ERROR", "message": "An unexpected server error occurred."}
    )
```

---

### Q7: How does SQLAlchemy 2.0 async engine integrate with FastAPI connection pooling?

**Answer:**

- In async FastAPI, synchronous engines block the event loop. Use `create_async_engine` from `sqlalchemy.ext.asyncio` with an async driver like `asyncpg` (PostgreSQL) or `aiomysql` (MySQL).
- Configure `pool_size` (baseline persistent connections) and `max_overflow` (surge connections allowed above pool size).
- Always use `async_sessionmaker` and clean dependency teardown via `async with session: yield session`.

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends, FastAPI
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/app_db"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # Keep 20 persistent connections in pool
    max_overflow=10,        # Allow 10 extra temporary connections during traffic bursts
    pool_recycle=1800,      # Recycle connections every 30 mins to avoid DB socket timeouts
    pool_pre_ping=True      # Test connection health with SELECT 1 before checkout
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Crucial for async: prevents lazy-loading attributes after commit
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

---

### Q8: What is Starlette Middleware and how does it differ from a Router Dependency?

**Answer:**

- **Middleware:** Executes at the lowest ASGI protocol layer for **every single request** entering the server before routing occurs. It can inspect and modify raw headers, handle CORS, enforce TLS, compress payloads (GZip), and measure overall request latency.
- **Router Dependency (`Depends`):** Executes after Starlette routes the request to a specific endpoint. It has access to typed route path parameters, query parameters, and Pydantic validated body data.
- **Interview Rule of Thumb:** Use Middleware for universal cross-cutting network concerns (CORS, trace IDs, security headers). Use Dependencies for endpoint-specific domain logic (Authentication, RBAC authorization, DB transactions).

---

### Q9: How do you stream large data or real-time events in FastAPI?

**Answer:**
FastAPI provides `StreamingResponse` from Starlette:

1. **Large file downloads:** Stream chunks from disk or S3 without loading entire gigabytes into RAM.
2. **Server-Sent Events (SSE):** Push real-time text updates to frontend clients over long-lived HTTP connections (`media_type="text/event-stream"`).

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def event_generator():
    for step in range(1, 6):
        await asyncio.sleep(1)
        yield f"data: Progress step {step}/5 completed\n\n"

@app.get("/stream-progress")
async def stream_progress():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

---

### Q10: How do you deploy FastAPI for High Concurrency in Production?

**Answer:**

- **The Golden Production Stack:** **Gunicorn as Process Manager + Uvicorn as ASGI Worker**.
- FastAPI runs inside single-threaded Python processes. To utilize all available CPU cores on a multi-core VM or Kubernetes node, run Gunicorn managing multiple Uvicorn worker instances:

```bash
# Recommended formula: (2 * Number of CPU Cores) + 1 workers
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --keep-alive 5 \
  --access-logfile - \
  --error-logfile -
```

- In Kubernetes, prefer **1 or 2 workers per pod** and scale horizontally via Kubernetes Horizontal Pod Autoscaler (HPA) targeting CPU and memory utilization.

---

### Q11: How do you handle WebSockets in FastAPI with connection pooling?

**Answer:**
FastAPI supports native ASGI WebSockets with `WebSocketEndpoint` or `@app.websocket`:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} disconnected")
```

---

### Q12: How does Pydantic V2 Field Validation work (`@field_validator` vs `@model_validator`)?

**Answer:**

- `@field_validator`: Validates individual fields. Accepts `mode='before'` (runs on raw input prior to type coercion) or `mode='after'` (runs after Pydantic parsed the field type).
- `@model_validator`: Validates cross-field relationships across the entire object (e.g., ensuring `end_date > start_date` or `password == confirm_password`).

```python
from pydantic import BaseModel, field_validator, model_validator
from datetime import date

class BookingRequest(BaseModel):
    guest_name: str
    start_date: date
    end_date: date

    @field_validator("guest_name")
    @classmethod
    def name_must_be_capitalized(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Guest name cannot be empty")
        return v.strip().title()

    @model_validator(mode="after")
    def verify_date_range(self) -> 'BookingRequest':
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be strictly after start_date")
        return self
```

---

### Q13-Q20: Rapid-Fire Senior Architect Scenarios

 1. **How to implement API versioning in FastAPI?**  
    Use APIRouters with path prefixes: `app.include_router(v1_router, prefix="/api/v1")` and `app.include_router(v2_router, prefix="/api/v2")`.
 2. **How to protect routes with OAuth2 and JWT tokens?**  
    Use `OAuth2PasswordBearer(tokenUrl="token")` with `python-jose` or `pyjwt` to decode claims, validating expiration timestamp (`exp`) and issuer (`iss`).
 3. **What is `response_model_exclude_unset=True`?**  
    Prevents returning default model fields that were not explicitly set in the data payload, keeping responses compact.
 4. **How to handle rate limiting per IP or User ID?**  
    Integrate `slowapi` (built on `limits` with Redis backend) using decorator `@limiter.limit("60/minute")`.
 5. **How to prevent N+1 query problems in FastAPI with SQLAlchemy?**  
    Use `select(Order).options(selectinload(Order.items))` or `joinedload` to eagerly fetch relations in one or two queries.
 6. **What is Lifespan events (`lifespan` context manager)?**  
    Replaces deprecated `@app.on_event("startup")` and `@app.on_event("shutdown")`. Uses an `asynccontextmanager` passed to `FastAPI(lifespan=lifespan)` for clean startup initialization and shutdown disposal.
 7. **How to run CPU-intensive tasks without blocking the server?**  
    Offload CPU calculations to `concurrent.futures.ProcessPoolExecutor` or an external Celery/Ray cluster.
 8. **How to implement distributed tracing in FastAPI?**  
    Instrument FastAPI with OpenTelemetry (`FastAPIInstrumentor.instrument_app(app)`) to automatically export W3C TraceContext headers to Jaeger or AWS X-Ray.
