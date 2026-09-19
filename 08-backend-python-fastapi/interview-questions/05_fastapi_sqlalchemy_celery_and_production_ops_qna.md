# Python & FastAPI Master Interview Bank: Part 5 (Q81 - Q100)

## SQLAlchemy 2.0 Async, Celery, WebSockets & Production Scaling

---

### Q81: How do you configure SQLAlchemy 2.0 with Async Engine and Session Management in FastAPI?

**Answer:**

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:secret@localhost:5432/app_db"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Base number of persistent connections
    max_overflow=10,       # Extra connections during spikes
    pool_recycle=1800,     # Recycle connections every 30m to avoid dead sockets
    pool_pre_ping=True,    # Test connection health with SELECT 1 before checkout
    echo=False
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # Prevents lazy-load errors after commit in async
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

### Q82: What does `expire_on_commit=False` do in SQLAlchemy async sessions?

**Answer:**

- By default in synchronous SQLAlchemy, committing a session expires all entity attributes so the next access re-fetches fresh data from the database.
- In **asynchronous SQLAlchemy**, accessing an expired attribute triggers a synchronous lazy-load on the event loop, which fails immediately with `MissingGreenlet: greenlet_spawn has not been called`.
- Setting **`expire_on_commit=False`** keeps attribute data in memory after commit, preventing lazy-load crashes.

---

### Q83: How do you prevent the N+1 Query Problem in SQLAlchemy 2.0?

**Answer:**
Use eager loading options in `select()` queries:

- **`selectinload(User.orders)`:** Executes exactly 2 queries: one to fetch users, and a second query `SELECT ... WHERE user_id IN (...)` to fetch orders. (Optimal for 1-to-many relationships).
- **`joinedload(User.profile)`:** Uses a single SQL `LEFT OUTER JOIN` to fetch parent and child records together. (Optimal for 1-to-1 or many-to-1 relationships).

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

stmt = select(User).options(selectinload(User.orders)).where(User.is_active == True)
result = await session.scalars(stmt)
users = result.all()
```

---

### Q84: What is the difference between FastAPI `BackgroundTasks` and Celery?

**Answer:**

| Feature | FastAPI `BackgroundTasks` | Distributed Task Queue (Celery / ARQ) |
| :--- | :--- | :--- |
| **Execution** | Runs in-process inside the same ASGI web container. | Runs out-of-process on dedicated background worker servers. |
| **Persistence** | In-memory only. If server restarts, tasks are permanently lost. | Durable message broker (RabbitMQ/Redis) with persistent retry queues. |
| **Throughput** | Heavy CPU tasks freeze the web API. | Independently scalable; can scale to thousands of worker pods. |
| **Use Case** | Lightweight post-response tasks (fire-and-forget email, audit log). | Heavy tasks (>1s): video transcoding, PDF generation, batch analytics, ML inference. |

---

### Q85: How do you implement a Real-Time WebSocket Connection Manager in FastAPI?

**Answer:**

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
        await manager.broadcast(f"Client #{client_id} left")
```

---

### Q86: How do you stream Server-Sent Events (SSE) in FastAPI?

**Answer:**
Use `StreamingResponse` with `media_type="text/event-stream"`:

```python
from fastapi.responses import StreamingResponse
import asyncio

async def event_generator():
    for count in range(1, 11):
        await asyncio.sleep(1)
        yield f"data: Progress: {count * 10}%\n\n"

@app.get("/events")
async def stream_events():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

---

### Q87: How do you implement OAuth2 Password Flow with JWT in FastAPI?

**Answer:**

1. Use `OAuth2PasswordBearer(tokenUrl="/token")`.
2. Extract token from `Authorization: Bearer <token>` header.
3. Decode and verify JWT signature and expiration (`exp`) using `pyjwt` or `python-jose`:

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

---

### Q88: How do you deploy FastAPI for Maximum Throughput in Production?

**Answer:**

- **The Golden Production Architecture:** **Gunicorn as Process Manager + Uvicorn as ASGI Worker**.
- FastAPI runs inside single-threaded Python processes. To utilize all available CPU cores on a multi-core VM, run Gunicorn managing multiple Uvicorn worker instances:

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

- In **Kubernetes**, prefer **1 or 2 workers per pod** and scale horizontally via Horizontal Pod Autoscaler (HPA).

---

### Q89: How do you implement Distributed Rate Limiting in FastAPI using SlowAPI?

**Answer:**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request

limiter = Limiter(key_func=get_remote_address, storage_uri="redis://localhost:6379")
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/sensitive")
@limiter.limit("5/minute")
async def sensitive_endpoint(request: Request):
    return {"message": "Success"}
```

---

### Q90: How does Alembic manage Database Migrations with SQLAlchemy in FastAPI?

**Answer:**

1. Initialize Alembic: `alembic init alembic`.
2. Configure `alembic/env.py` to import SQLAlchemy `Base.metadata`.
3. Auto-generate migration script:
   `alembic revision --autogenerate -m "create users table"`
   (Alembic inspects SQL database schema and compares it against Python models).
4. Apply migrations: `alembic upgrade head`.

---

### Q91: What is the difference between `HTTPException` from FastAPI vs Starlette?

**Answer:**

- **`fastapi.HTTPException`**: Inherits from Starlette's exception, but allows passing any JSON-serializable Python data structure (dict, list, string) to the `detail` parameter.
- **`starlette.exceptions.HTTPException`**: Only accepts a string for `detail`.
- *Rule:* Always import `from fastapi import HTTPException`.

---

### Q92: How do you handle Database Transactions with Unit of Work pattern in FastAPI?

**Answer:**
Implement a Unit of Work class managing transaction commits and rollbacks across multiple repositories:

```python
class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
        self.orders = OrderRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
```

---

### Q93: How do you instrument FastAPI with OpenTelemetry and Prometheus?

**Answer:**
Use `opentelemetry-instrumentation-fastapi`:

```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Auto-instruments route spans with traceparent headers:
FastAPIInstrumentor.instrument_app(app)

# Exposes /metrics for Prometheus scraping:
Instrumentator().instrument(app).expose(app)
```

---

### Q94: What is ARQ and why is it preferred over Celery in Asyncio applications?

**Answer:**

- **Celery:** Synchronous by design (requires eventlet or gevent hacks to run async coroutines).
- **ARQ:** Built natively from the ground up on top of Python `asyncio` and Redis.
- Jobs are native `async def` coroutines, resulting in lower memory footprint and zero thread synchronization overhead.

---

### Q95: How do you prevent Connection Leaks in FastAPI with `httpx.AsyncClient`?

**Answer:**

- **Anti-Pattern:** Instantiating `httpx.AsyncClient()` inside individual route handlers creates a brand-new TCP/TLS socket on every HTTP request.
- **Best Practice:** Maintain a single shared client instance using the `lifespan` handler:

  ```python
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      app.state.http_client = httpx.AsyncClient(timeout=10.0)
      yield
      await app.state.http_client.aclose()
  ```

---

### Q96: What is the difference between `model.model_dump()` and `model.model_dump_json()`?

**Answer:**

- `model.model_dump()`: Returns a native Python dictionary (`dict`).
- `model.model_dump_json()`: Serializes directly into a raw UTF-8 JSON string via Rust `pydantic-core`, skipping intermediate dictionary allocations and running up to 10x faster.

---

### Q97: How do you mock database sessions in FastAPI unit tests?

**Answer:**
Use `app.dependency_overrides`:

```python
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

async def mock_get_db():
    mock_session = AsyncMock()
    yield mock_session

app.dependency_overrides[get_db] = mock_get_db
client = TestClient(app)

def test_endpoint():
    response = client.get("/users")
    assert response.status_code == 200
```

---

### Q98: How do you handle Graceful Shutdown in FastAPI / Uvicorn?

**Answer:**

- Uvicorn listens for `SIGINT` and `SIGTERM`.
- When signaled, Uvicorn stops accepting new connections and gives active requests time to complete up to `--timeout-graceful-shutdown` seconds before executing the `lifespan` shutdown block.

---

### Q99: What is the difference between Pydantic `BaseModel` and `RootModel` in V2?

**Answer:**

- `BaseModel`: Defines an object model with named fields (`{"name": "Alice", "age": 30}`).
- `RootModel[List[str]]`: Defines a model for root data types that are not JSON objects (e.g. validating a top-level JSON array `["item1", "item2"]` or top-level primitive).

---

### Q100: How do you structure a Production Multi-Tenant FastAPI Application?

**Answer:**

1. **Tenant Identification:** Extract tenant ID from subdomain (`tenant.myapp.com`) or header (`X-Tenant-ID`) via FastAPI dependency.
2. **Schema Separation:** Use PostgreSQL schemas per tenant (`search_path = tenant_id`).
3. **Connection Pooling:** Dynamic connection pool routing or schema switching per request inside a `yield` dependency.
4. **Tenant Isolation:** Enforce tenant filters on all queries to prevent cross-tenant data leakage.
