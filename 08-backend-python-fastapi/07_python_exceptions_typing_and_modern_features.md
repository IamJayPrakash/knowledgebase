# Python Exception Handling, Type Hints & Modern Features (Python 3.10+)

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - `try-except-else-finally`:
>   - `try`: "Main ye kaam karne ki koshish kar raha hoon."
>   - `except`: "Agar koi gadbad hui toh yahan sambhalo."
>   - `else`: "Agar sab kuch bina kisi error ke successfully ho gaya, tabhi ye aage ka kaam karo."
>   - `finally`: "Chahe tufaan aaye ya aag lage, ye aakhri safai (clean up) zaroor hogi!"
> - Walrus Operator (`:=`): Ek teer se do shikaar—variable mein value assign bhi kar lo aur usi line par condition mein check bhi kar lo!
> - Structural Pattern Matching (`match-case`): C/Java ke purane `switch` ka Baap! Ye sirf number ya string match nahi karta, balki object ke andar ke data structure (shape) ko inspect karke match karta hai!
>
> **Real-World Analogy:** A parcel delivery hub with an automated package scanner (`match-case`). The scanner doesn't just read the barcode; it checks the package shape, weight, and contents dynamically, routing oversized fragile boxes to special handling and express letters to air cargo instantly.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **`try...except...else...finally` Flow**:
  - `else`: Runs **only if no exception occurred** in the `try` block. Avoids putting too much code inside `try`!
  - `finally`: **Always executes**, even after `return`, `break`, or `continue`.
- **Custom Exceptions**: Always inherit from `Exception` (Never inherit from `BaseException`, as that catches `KeyboardInterrupt` and `SystemExit`!).
- **Type Annotations**: Python remains dynamically typed at runtime; type annotations (`name: str = "Jay"`) do not enforce types at runtime, but are verified by static type checkers like `mypy` and utilized by FastAPI for automatic request serialization and Swagger validation.
- **The Walrus Operator (`:=`)**: Assigns values to variables as part of a larger expression (`if (n := len(items)) > 10:`).

### 🧓 What an Experienced Candidate Knows:
- **Explicit Exception Chaining (`raise ... from e`)**:
  - In Python 3, when you catch an exception and raise a custom business exception, writing `raise CustomError("failed") from original_exc` populates `__cause__` and outputs `The above exception was the direct cause of the following exception:`.
  - Writing `raise CustomError() from None` explicitly suppresses the context (`__context__`), hiding internal database driver traces from client responses for security.
- **Structural Pattern Matching (`match...case`) Internals (Python 3.10+)**:
  - Sequence patterns: `case [x, y]:`
  - Mapping patterns: `case {"action": "BUY", "qty": qty}:`
  - Class patterns: `case Order(status="PAID", total=t):`
  - Guard conditions: `case [x, y] if x > 0:`
- **`typing.Protocol` (Static Duck Typing)**: Unlike `abc.ABC`, `Protocol` allows static type checkers to verify that a class implements required methods without explicitly inheriting from a base class.

---

## 3. 📊 Visual Architecture Diagram

```text
Exception Flow with try-except-else-finally:

            ┌──────────────────────────┐
            │        try block         │
            └─────────────┬────────────┘
                          │
            Did an exception occur?
             ├── YES ──> ┌──────────────────────────┐
             │           │       except block       │ ──> Handled? ──┐
             │           └──────────────────────────┘                │
             │                                                       │
             └── NO  ──> ┌──────────────────────────┐                │
                         │        else block        │                │
                         └────────────┬─────────────┘                │
                                      │                              │
                                      v                              v
                         ┌─────────────────────────────────────────────┐
                         │                finally block                │
                         │      (Always runs for resource cleanup)     │
                         └─────────────────────────────────────────────┘
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```python
# Line 1: Import dataclass for clean domain modeling
from dataclasses import dataclass
# Line 2: Import typing utilities for robust type contracts
from typing import Optional, Protocol, Union

# Line 3: Custom Domain Exception with cause chaining support
class PaymentProcessingError(Exception):
    def __init__(self, message: str, transaction_id: str):
        super().__init__(message)
        self.transaction_id = transaction_id

# Line 4: Protocol defining a structural contract (Static Duck Typing)
class Serializable(Protocol):
    def to_dict(self) -> dict:
        ...

# Line 5: Dataclass implementing the protocol implicitly
@dataclass
class CheckoutOrder:
    order_id: str
    total_amount: float
    currency: str = "USD"

    def to_dict(self) -> dict:
        return {"id": self.order_id, "amount": self.total_amount, "currency": self.currency}

# Line 6: Function demonstrating try-except-else-finally with exception chaining
def process_order_payment(order: CheckoutOrder, payment_token: Optional[str]) -> bool:
    print(f"Processing order {order.order_id}...")
    try:
        # Line 7: Validate payment token
        if not payment_token:
            raise ValueError("Payment authentication token is missing or expired")
        # Line 8: Simulate payment API call
        print("Charging payment gateway...")
    except ValueError as val_err:
        # Line 9: Explicit exception chaining preserving root cause
        raise PaymentProcessingError(f"Payment failed for {order.order_id}", order.order_id) from val_err
    else:
        # Line 10: else block: executed ONLY if no exceptions were thrown in try
        print("Payment successfully authorized!")
        return True
    finally:
        # Line 11: finally block: guaranteed to execute for audit log flushing
        print("Audit trace finalized for order attempt.")

# Line 12: Modern Python 3.10+ Structural Pattern Matching demonstration
def route_webhook_event(event: dict) -> str:
    # Line 13: match statement inspecting event payload shape
    match event:
        # Line 14: Match exact dictionary pattern with nested keys
        case {"type": "PAYMENT", "payload": {"status": "SUCCESS", "amount": amount}}:
            return f"Processed successful payment: ${amount}"
        # Line 15: Match failure pattern with custom guard clause
        case {"type": "PAYMENT", "payload": {"status": "FAILED", "reason": reason}} if "fraud" in reason.lower():
            return f"CRITICAL: Fraud alert flagged: {reason}"
        case {"type": "PAYMENT", "payload": {"status": "FAILED", "reason": reason}}:
            return f"Payment declined: {reason}"
        # Line 16: Match sequence/list pattern
        case {"type": "BATCH", "items": [first, *rest]}:
            return f"Batch received: First item is {first}, remaining count: {len(rest)}"
        # Line 17: Wildcard default pattern
        case _:
            return "Unknown event format"

# Line 18: Demonstrate Walrus Operator (:=) for in-line assignment & checking
sample_queries = ["SELECT * FROM users", "", "UPDATE accounts SET balance = 0", ""]
# Line 19: Filter and measure non-empty queries using walrus
non_empty_queries = [cleaned for q in sample_queries if (cleaned := q.strip())]
print("Cleaned Queries via Walrus:", non_empty_queries)

# Line 20: Test structural pattern matching
print(route_webhook_event({"type": "PAYMENT", "payload": {"status": "SUCCESS", "amount": 150.0}}))
print(route_webhook_event({"type": "PAYMENT", "payload": {"status": "FAILED", "reason": "Potential Fraud detected"}}))
print(route_webhook_event({"type": "BATCH", "items": ["Task-1", "Task-2", "Task-3"]}))
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What is the purpose of the `else` clause in a `try-except` block, and how does Python 3's `raise ... from` work?"
>
> **You:** "In Python, the `else` clause in a `try-except` block executes only if no exception was raised in the `try` block. Using `else` is a critical best practice because it minimizes the amount of code inside `try`, preventing developers from accidentally catching unintended exceptions from unrelated lines. Regarding exception chaining, Python 3 introduces `raise NewException() from original_exc`. This explicitly links the new high-level exception to the low-level cause in the `__cause__` attribute, preserving the entire causal stack trace for debugging. Alternatively, using `from None` suppresses the underlying context, preventing internal implementation details like database connection strings or passwords from leaking to external clients."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An API gateway converted internal downstream service errors into standard HTTP 500 JSON responses. However, because downstream library exceptions were caught and re-thrown without chaining, all error logs in Datadog displayed generic `InternalServerError: Request failed` without the original HTTP connection timeout or database connection reset stack trace.
* **Task / Challenge:** Restore complete error trace visibility in distributed logs without leaking internal system traces to external API consumers.
* **Action Taken:** Refactored the global exception handler across 24 microservices to use explicit exception chaining (`raise GatewayTimeoutError(...) from exc`). On the client response boundary, custom serializer middleware stripped `__cause__` for external HTTP JSON responses while formatting the full `__cause__` trace into Datadog JSON structured logs.
* **Result & Business Impact:** Cut Mean Time to Resolution (MTTR) for downstream gateway outages from 45 minutes to under 3 minutes.
