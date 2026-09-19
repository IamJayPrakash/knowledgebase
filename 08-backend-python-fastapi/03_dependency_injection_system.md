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
