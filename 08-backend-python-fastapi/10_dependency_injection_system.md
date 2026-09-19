# FastAPI Dependency Injection System (`Depends`)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)

FastAPI ka `Depends()` ek **Automated Butler (Chaudhary)** ki tarah hai. Jab bhi aap kisi function (API Route) mein aate ho, butler pehle se aapke liye:

- Database connection khol ke table par rakh deta hai.
- User ka JWT token verify karke user object haath mein pakda deta hai.
Aur jab aapka function khatam ho jata hai, butler chupke se database connection safely close kar deta hai (`yield` teardown)!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Declarative Composition**: Dependencies can themselves depend on other dependencies, forming a clean **Directed Acyclic Graph (DAG)**.
2. **Resource Teardown via `yield`**: Using `yield` allows executing cleanup logic (closing DB sessions, releasing locks) after the response is sent.
3. **Dependency Caching (`use_cache=True`)**: By default, FastAPI resolves a shared dependency once per request, caching its return value across multiple parameter usages in that single request.

---

## 💻 3. Line-by-Line Commented Code Snippets

```python
from fastapi import FastAPI, Depends, HTTPException, status, Header
from typing import Annotated, Generator

app = FastAPI()

# Line 7: Database session dependency with clean teardown using yield
def get_db_session() -> Generator[str, None, None]:
    session = "PostgresSession[Open]"
    print(f"Acquired: {session}")
    try:
        # Line 12: Passes active session to route
        yield session
    finally:
        # Line 15: Executes cleanup AFTER response is sent to client
        print("Closed: PostgresSession[Released]")

# Line 18: Authentication dependency
def get_current_user(authorization: Annotated[str | None, Header()] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication token"
        )
    token = authorization.split(" ")[1]
    return {"user_id": "usr_99", "role": "admin", "token": token}

# Line 28: Route composing both dependencies
@app.get("/api/v1/profile")
def get_profile(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[str, Depends(get_db_session)]
):
    return {"user": current_user, "db_status": db}
```

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
>
> **Interviewer:** "How does Dependency Injection work in FastAPI, and what are yield dependencies?"
>
> **You:** "FastAPI features a hierarchical Dependency Injection system built on top of `Depends()`. At startup and request time, FastAPI analyzes the dependency graph into a Directed Acyclic Graph (DAG), resolving sub-dependencies in parallel or sequence. Yield dependencies (`def get_db(): try: yield db finally: db.close()`) represent a clean context manager pattern: code prior to `yield` executes before the route handler, and code after `yield` is guaranteed to execute during response finalization, ensuring database connections or transaction locks are cleanly released even if route exceptions occur."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)

- **Situation:** A multi-tenant SaaS application had intermittent database connection leaks that exhausted PostgreSQL connection pools during traffic spikes, crashing the API.
- **Task / Challenge:** Ensure deterministic database session teardown across 120 endpoints.
- **Action Taken:** Centralized database session lifecycle management into a FastAPI `yield` dependency with explicit `try...finally` block. Configured session rollback on uncaught exceptions and ensured auto-closing of the session.
- **Result & Business Impact:** Completely eliminated PostgreSQL connection pool exhaustion, sustaining 100% API availability under 15,000 concurrent tenant connections.
