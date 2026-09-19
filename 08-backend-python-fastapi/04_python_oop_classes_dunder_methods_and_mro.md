# Python Object-Oriented Programming: Classes, Dunder Methods & MRO (C3 Linearization)

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
>
> **Hinglish Intuition:**
>
> - Class ek ghar ka **blueprint** hai, aur object us blueprint se bana **asli ghar**.
> - Dunder methods (`__init__`, `__str__`, `__len__`) Python ke secret magic switches hain: jab aap `len(my_obj)` likhte ho, Python parde ke peeche `my_obj.__len__()` ko call karta hai!
> - Multiple Inheritance & MRO: Jab ek bacha do mata-pita se ek jaisi aadat inherit karta hai, toh rulebook (C3 Linearization) tay karti hai ki pehle kiska tareeqa chalega!
>
> **Real-World Analogy:** A smartphone operating system. The base class is a phone (calls, SMS). A camera phone inherits both Phone and DigitalCamera. If both define `take_snapshot()`, the OS uses an unambiguous priority list (Method Resolution Order) so there is zero confusion about which camera lens driver activates.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand

- **`__init__` vs `__new__`**:
  - `__new__`: The actual constructor that allocates the new object instance in memory (rarely overridden except in singletons or immutable subclasses).
  - `__init__`: The initializer that populates instance attributes on `self`.
- **Method Types**:
  - **Instance Method**: Takes `self`, can read and modify instance state.
  - **Class Method (`@classmethod`)**: Takes `cls`, can modify class state across all instances or serve as alternative factory constructors.
  - **Static Method (`@staticmethod`)**: Takes neither `self` nor `cls`, isolated utility function living in class namespace.
- **`@property`**: Allows calling a method using attribute access syntax (`user.full_name` instead of `user.full_name()`), enabling encapsulation and validation.

### 🧓 What an Experienced Candidate Knows

- **Dunder / Magic Methods**:
  - Representation: `__repr__` (unambiguous representation for developers/debugging) vs `__str__` (readable representation for end users).
  - Protocol support: `__len__`, `__getitem__` (makes class indexable like a list), `__iter__` (makes class iterable), `__call__` (makes class instance callable like a function).
  - Equality & Hashing: If you override `__eq__`, you must override `__hash__` if you want instances to be usable as dictionary keys or set elements!
- **The Diamond Problem & C3 Linearization (MRO)**:
  - When class `D` inherits from `B` and `C`, and both inherit from `A`.
  - Python uses the **C3 Linearization algorithm** to produce a deterministic Method Resolution Order (`D.mro()`), guaranteeing children precede parents, and multiple parent orders are preserved without ambiguity.
  - `super()` does NOT mean "call my direct parent"; it means **"call the NEXT class in the MRO chain"**!

---

## 3. 📊 Visual Architecture Diagram

```text
Diamond Inheritance & C3 Method Resolution Order (MRO):

            ┌───────────────┐
            │   Class A     │  def ping(): "A"
            └───────┬───────┘
                    │
         ┌──────────┴──────────┐
         │                     │
  ┌──────┴────────┐     ┌──────┴────────┐
  │   Class B     │     │   Class C     │
  │ def ping():"B"│     │ def ping():"C"│
  └──────┬────────┘     └──────┬────────┘
         │                     │
         └──────────┬──────────┘
                    │
            ┌───────┴───────┐
            │   Class D     │  (Inherits B, then C)
            └───────────────┘

   D.mro() Sequence:
   [ Class D ] ──> [ Class B ] ──> [ Class C ] ──> [ Class A ] ──> [ object ]
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```python
# Line 1: Define a custom Vector class implementing core dunder methods
class Vector:
    # Line 2: Initializer with default 2D coordinates
    def __init__(self, x=0, y=0):
        # Line 3: Private backing attributes with leading underscore
        self._x = float(x)
        self._y = float(y)

    # Line 4: Property getter for x coordinate
    @property
    def x(self):
        return self._x

    # Line 5: Property getter for y coordinate
    @property
    def y(self):
        return self._y

    # Line 6: __repr__ provides unambiguous code representation
    def __repr__(self):
        return f"Vector(x={self._x}, y={self._y})"

    # Line 7: __str__ provides friendly string display
    def __str__(self):
        return f"({self._x}, {self._y})"

    # Line 8: __add__ overloads the '+' operator
    def __add__(self, other):
        # Line 9: Type checking
        if not isinstance(other, Vector):
            return NotImplemented
        # Line 10: Return new Vector instance with summed components
        return Vector(self._x + other.x, self._y + other.y)

    # Line 11: __eq__ overloads the '==' equality operator
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self._x == other.x and self._y == other.y

    # Line 12: __hash__ allows Vector to be stored in sets and used as dict keys
    def __hash__(self):
        # Line 13: Combine hashes of immutable coordinate tuple
        return hash((self._x, self._y))

# Line 13: Demonstrate C3 Linearization and cooperative super()
class Device:
    def boot(self):
        print("Device initialized")

class NetworkDevice(Device):
    def boot(self):
        print("Network interface online")
        super().boot()

class StorageDevice(Device):
    def boot(self):
        print("Storage mounted")
        super().boot()

# Line 14: Server inherits from both NetworkDevice and StorageDevice
class Server(NetworkDevice, StorageDevice):
    def boot(self):
        print("Server boot sequence starting...")
        super().boot()

# Line 15: Instantiate Vector instances
v1 = Vector(3, 4)
v2 = Vector(1, 2)
# Line 16: Operator overloading '+' triggers v1.__add__(v2)
v3 = v1 + v2
print("Summed Vector:", v3)  # (4.0, 6.0)

# Line 17: Use Vectors inside a set (testing __hash__ and __eq__)
vector_set = {v1, v2, Vector(3, 4)}
# Line 18: Set deduplicates Vector(3, 4) correctly!
print("Vector Set Length:", len(vector_set))  # 2

# Line 19: Inspect Server MRO chain
print("Server MRO Chain:")
for idx, cls in enumerate(Server.mro()):
    print(f"  {idx}: {cls.__name__}")

# Line 20: Boot the server and observe cooperative super() execution
server = Server()
server.boot()
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
>
> **Interviewer:** "How does Python solve the diamond inheritance problem, and what does `super()` actually do?"
>
> **You:** "Python resolves multiple inheritance using the C3 Linearization algorithm to compute a deterministic Method Resolution Order (MRO), accessible via `ClassName.mro()`. C3 ensures three things: children always precede parents, original parent declaration order is respected, and no class is visited twice. Crucially, `super()` does not call the direct base class; it calls the next class in the computed MRO chain. When all classes in an inheritance hierarchy use `super()` cooperatively, every class in the diamond is visited exactly once in clean linear order."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)

- **Situation:** In an asynchronous distributed worker framework, task classes inherited from both `LoggingMixin` and `RetryMixin`. During a major outage, retry attempts triggered unhandled infinite recursion exceptions, crashing worker pods.
- **Task / Challenge:** Diagnose why retrying tasks resulted in `RecursionError: maximum recursion depth exceeded`.
- **Action Taken:** Inspected the inheritance hierarchy using `TaskClass.mro()`. Found that `RetryMixin` called `super().__init__()` with explicit hardcoded arguments while `LoggingMixin` did not call `super()` at all, breaking the cooperative chain. Refactored both mixins to take `*args, **kwargs` and pass them to `super().__init__(*args, **kwargs)`.
- **Result & Business Impact:** Restored clean cooperative multiple inheritance across 60 worker nodes, preventing task queue deadlocks.
