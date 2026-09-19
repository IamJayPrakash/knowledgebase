# scripts/elevate_backend_pillars.py
import os

BASE_DIR = r"D:\Projects\knowledgebase"

PY_DIR = os.path.join(BASE_DIR, "08-backend-python-fastapi")
JAVA_DIR = os.path.join(BASE_DIR, "09-backend-java-springboot")

PYDANTIC_EXTRA = """
---

## 4. 📊 Visual Architecture Diagram

```text
Pydantic V2 Rust Engine Validation Pipeline:

   Incoming JSON Payload (HTTP Request)
                │
                v
   ┌─────────────────────────────────────────┐
   │            pydantic-core (Rust)         │
   │  ┌───────────────────────────────────┐  │
   │  │ Compiled Schema Validator in C/Rust│  │ <── Validates types & constraints at C speed!
   │  └───────────────────────────────────┘  │
   └─────────────────────────────────────────┘
                │
        ┌───────┴───────┐
        │               │
     Valid?          Invalid?
        │               │
        v               v
   Instantiate     Raise RequestValidationError (HTTP 422)
   Python Model    with field-level error trace (0 Python loop overhead!)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What makes Pydantic V2 fundamentally faster than V1, and how do you handle cross-field validation?"
>
> **You:** "Pydantic V2 achieves a 5x to 20x performance improvement by moving the entire parsing, validation, and JSON serialization core into Rust via `pydantic-core`. Instead of traversing Python ASTs and executing slow interpreted loops, validation rules are compiled into a optimized Rust state machine. For cross-field validation, V2 replaces V1's `@root_validator` with `@model_validator(mode='after')`, which executes after individual fields are validated and types are guaranteed, allowing clean, type-safe cross-attribute assertions."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An IoT telematics ingest API received 40,000 JSON sensor packets per second. Under Pydantic V1, CPU consumption hovered at 95% and request serialization introduced an 85ms bottleneck per payload batch.
* **Task / Challenge:** Reduce CPU utilization under 40% and cut validation latency under 10ms.
* **Action Taken:** Upgraded FastAPI and migrated schemas to Pydantic V2. Replaced `.dict()` with `.model_dump()` and utilized `pydantic-core` direct JSON serialization via `.model_dump_json()`. Enabled `strict=True` on numerical telemetry fields to eliminate unnecessary type coercion.
* **Result & Business Impact:** Cut CPU utilization from 95% to 28%, decreased batch validation latency from 85ms to 6ms, and reduced required Kubernetes pod replicas by 60%, saving $35,000 annually.
"""

DI_EXTRA = """
---

## 4. 📊 Visual Architecture Diagram

```text
FastAPI Dependency Injection DAG Resolution:

              [ Endpoint: get_user_profile ]
                            │
              Depends(get_current_active_user)
                            │
              Depends(get_current_user)
              ┌─────────────┴─────────────┐
              │                           │
     Depends(get_db_session)      Depends(oauth2_scheme)
     (Yields DB conn via with)   (Extracts Bearer Token)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How does Dependency Injection work in FastAPI, and what are yield dependencies?"
>
> **You:** "FastAPI features a hierarchical Dependency Injection system built on top of `Depends()`. At startup and request time, FastAPI analyzes the dependency graph into a Directed Acyclic Graph (DAG), resolving sub-dependencies in parallel or sequence. Yield dependencies (`def get_db(): try: yield db finally: db.close()`) represent a clean context manager pattern: code prior to `yield` executes before the route handler, and code after `yield` is guaranteed to execute during response finalization, ensuring database connections or transaction locks are cleanly released even if route exceptions occur."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A multi-tenant SaaS application had intermittent database connection leaks that exhausted PostgreSQL connection pools during traffic spikes, crashing the API.
* **Task / Challenge:** Ensure deterministic database session teardown across 120 endpoints.
* **Action Taken:** Centralized database session lifecycle management into a FastAPI `yield` dependency with explicit `try...finally` block. Configured session rollback on uncaught exceptions and ensured auto-closing of the session.
* **Result & Business Impact:** Completely eliminated PostgreSQL connection pool exhaustion, sustaining 100% API availability under 15,000 concurrent tenant connections.
"""

BG_TASKS_EXTRA = """
---

## 4. 📊 Visual Architecture Diagram

```text
BackgroundTasks vs Distributed Celery Workers:

   FastAPI In-Process BackgroundTasks:
   [ Client Request ] ──> [ Route executes & returns HTTP 200 ]
                                      │
                                      └──> Runs task on same server threadpool (lost on pod restart!)

   Distributed Celery Architecture:
   [ Client Request ] ──> [ Celery task.delay() ] ──> [ Push to Redis/RabbitMQ Queue ] ──> Return 202 Accepted
                                                                  │
                                                                  v
                                              [ Independent Celery Worker Pods ]
                                              (Auto-scaling, Persistent, Retries, Dead-Letter)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "When should you use FastAPI's built-in `BackgroundTasks` versus an external task queue like Celery or RQ?"
>
> **You:** "FastAPI's `BackgroundTasks` executes tasks in-process within the same Starlette worker threadpool after returning the HTTP response. It is ideal for lightweight, non-critical tasks like sending a confirmation email or writing an audit log. However, if the server restarts or crashes, pending in-process background tasks are lost forever. For heavy compute (video transcoding, ML inference, batch reports), mission-critical workflows, or jobs requiring retry backoff and monitoring, we use a distributed task queue like Celery or BullMQ backed by Redis or RabbitMQ."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A video processing portal used `BackgroundTasks` to transcode user video uploads. When multiple users uploaded 4K videos simultaneously, the API server ran out of CPU and memory, dropping all incoming HTTP requests and causing cluster restarts that killed in-flight transcoding jobs.
* **Task / Challenge:** Decouple video transcoding from the web API to prevent server crashes and guarantee job recovery.
* **Action Taken:** Decoupled the transcoding pipeline by replacing `BackgroundTasks` with Celery workers backed by Amazon SQS and Redis. The web API immediately responded with HTTP 202 Accepted and the task ID, while dedicated Celery worker containers scaled independently on GPU nodes.
* **Result & Business Impact:** Restored 99.99% API uptime, eliminated lost jobs with automatic SQS visibility retries, and enabled processing 50 concurrent video transcode jobs without impacting web traffic.
"""

ASGI_EXTRA = """
---

## 4. 📊 Visual Architecture Diagram

```text
ASGI vs WSGI Architecture:

   WSGI (Flask / Django):
   [ Web Server (Gunicorn) ] ──> [ 1 Worker Thread = 1 Synchronous HTTP Request ] (Blocks on I/O!)

   ASGI (FastAPI / Starlette / Uvicorn):
   [ Master Process ]
           │
           ├── Worker 1 (Uvicorn with uvloop): [ Single Thread runs Asyncio Event Loop ]
           │       ├── Handles 5,000 concurrent connections via epoll/kqueue non-blocking I/O!
           │       └── Supports WebSockets, Server-Sent Events (SSE), and HTTP/2 Streaming!
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What is the difference between WSGI and ASGI, and why is Uvicorn paired with Gunicorn in production?"
>
> **You:** "WSGI is a synchronous interface standard where one worker thread handles one request at a time, making it ill-suited for WebSockets, long polling, or high-concurrency async I/O. ASGI (Asynchronous Server Gateway Interface) extends this to support asynchronous Python coroutines, WebSockets, and HTTP/2 multiplexing. In production, we run Uvicorn workers managed by Gunicorn (`gunicorn -w 4 -k uvicorn.workers.UvicornWorker`). Gunicorn acts as the robust Unix process manager—handling worker lifecycles, health checks, and graceful zero-downtime restarts—while Uvicorn provides the ultra-fast C-based `uvloop` and `httptools` event loop engine."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A live sports notification service running on standard WSGI crashed under 5,000 concurrent open connections during the World Cup finals due to thread exhaustion.
* **Task / Challenge:** Migrate the notification service to handle 50,000 concurrent long-polling connections with sub-second message dispatch.
* **Action Taken:** Migrated the backend to FastAPI running on ASGI with Uvicorn and `uvloop`. Replaced synchronous database polling with async Redis Pub/Sub channels connected to WebSocket routes.
* **Result & Business Impact:** Handled 65,000 concurrent active WebSocket connections on a single 4-core node with memory usage under 400MB and zero dropped connections.
"""

JWT_EXTRA = """
---

## 4. 📊 Visual Architecture Diagram

```text
Spring Security 6 Stateless JWT Filter Chain:

   Incoming HTTP Request (Authorization: Bearer <token>)
               │
               v
   ┌─────────────────────────────────────────────────────────────┐
   │ SecurityFilterChain                                         │
   │   [ CorsFilter ]                                            │
   │         │                                                   │
   │   [ JwtAuthenticationFilter ]                               │
   │         ├── Extracts Bearer Token                           │
   │         ├── Validates Cryptographic Signature & Expiry      │
   │         ├── Loads UserDetails & GrantedAuthorities          │
   │         └── Sets SecurityContextHolder.getContext()         │
   │                   .setAuthentication(auth)                  │
   │         │                                                   │
   │   [ AuthorizationFilter ] ──> Checks @PreAuthorize roles   │
   └─────────────────────────────────────────────────────────────┘
               │
               v
   [ Spring Controller Method Executed ]
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you implement stateless JWT authentication in Spring Boot 3 and Spring Security 6?"
>
> **You:** "In Spring Boot 3 and Spring Security 6, authentication is configured declaratively using a `SecurityFilterChain` bean, deprecating the legacy `WebSecurityConfigurerAdapter`. We set session creation policy to `SessionCreationPolicy.STATELESS`, disable CSRF because JWTs stored in headers are immune to CSRF, and insert a custom `JwtAuthenticationFilter` before `UsernamePasswordAuthenticationFilter`. The filter parses the Bearer token, validates the HMAC-SHA256 or RSA cryptographic signature and expiration, extracts username and authorities, and populates `SecurityContextHolder`. Method-level authorization is enforced cleanly using `@EnableMethodSecurity` and `@PreAuthorize('hasRole(...)')`."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A banking microservice ecosystem suffered authentication bottlenecks because each downstream service made an internal REST call back to the Auth Service to validate sessions on every single API request, adding 45ms overhead.
* **Task / Challenge:** Reduce authentication latency from 45ms to $< 1\text{ms}$ while maintaining zero-trust token revocation capability.
* **Action Taken:** Migrated to asymmetric RSA-256 JWT tokens. Downstream Spring Boot 3 services verified tokens locally in memory using the Auth Service's public key (0ms network overhead). For instant token revocation upon logout, integrated Redis token blacklisting checking a high-speed in-memory set during JWT filter execution.
* **Result & Business Impact:** Cut authentication overhead from 45ms to 0.4ms across 120 microservices, reducing global API response times by 35%.
"""

RESILIENCE_EXTRA = """
---

## 4. 📊 Visual Architecture Diagram

```text
Resilience4j Circuit Breaker State Machine:

              Failure Rate >= 50%
   ┌─────────┐ ─────────────────> ┌──────────┐
   │ CLOSED  │                    │   OPEN   │ ──> All calls fail fast!
   │ (Normal)│ <───────────────── │ (Tripped)│     (Fallback executed)
   └─────────┘   Success >= 80%   └──────────┘
        ▲                              │
        │                              │ Wait Duration (10s) elapsed
        │        ┌──────────────┐      │
        └─────── │  HALF-OPEN   │ <────┘
                 │ (Test Probe) │
                 └──────────────┘
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How does Resilience4j Circuit Breaker protect Spring Boot microservices from cascading failures?"
>
> **You:** "Resilience4j implements a finite state machine with three states: Closed, Open, and Half-Open. In the Closed state, calls flow normally to downstream services while recording success and failure rates in a sliding window. If the failure rate or slow call rate exceeds a configured threshold (e.g. 50%), the breaker trips to the Open state. In Open, all incoming requests fail fast immediately or route to a predefined fallback method without touching the struggling downstream service. After a configured wait duration, the breaker enters Half-Open, allowing a limited probe set of requests through. If they succeed, it returns to Closed; otherwise, it trips back to Open, preventing cascading system-wide outages."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** During a high-traffic Cyber Monday event, a downstream fraud scoring service suffered database lockups, causing payment service worker threads to block for 30 seconds each, eventually exhausting Tomcat's 200-thread pool and taking down the entire checkout portal.
* **Task / Challenge:** Prevent downstream vendor latency from causing thread starvation in upstream services.
* **Action Taken:** Integrated Resilience4j `@CircuitBreaker` and `@TimeLimiter` on the fraud service Feign client. Configured a 1-second timeout and a sliding window of 20 calls. If failure rate exceeded 40%, the circuit opened immediately, returning a default degraded fraud risk score from the fallback method.
* **Result & Business Impact:** Maintained 100% checkout uptime during subsequent vendor outages; average checkout latency remained flat at 120ms even when the third-party fraud service was completely down.
"""

def append_to_file(filepath, extra_content):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if "Interview Answering Pitch" not in content:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(extra_content.strip() + "\n")
        print(f"Elevated: {filepath}")
    else:
        print(f"Already elevated: {filepath}")

append_to_file(os.path.join(PY_DIR, "09_pydantic_v2_validation_and_serialization.md"), PYDANTIC_EXTRA)
append_to_file(os.path.join(PY_DIR, "10_dependency_injection_system.md"), DI_EXTRA)
append_to_file(os.path.join(PY_DIR, "11_background_tasks_and_celery.md"), BG_TASKS_EXTRA)
append_to_file(os.path.join(PY_DIR, "12_high_performance_asgi_starlette_uvicorn.md"), ASGI_EXTRA)

append_to_file(os.path.join(JAVA_DIR, "12_springboot_security_jwt_oauth2.md"), JWT_EXTRA)
append_to_file(os.path.join(JAVA_DIR, "13_springboot_microservices_and_resilience4j.md"), RESILIENCE_EXTRA)

print("Finished elevating backend files!")
