# Python & FastAPI Master Interview Bank: Part 2 (Q21 - Q40)

## Functions, Scopes, Decorators, OOP & MRO

---

### Q21: Explain the LEGB Scope Rule in Python

**Answer:**
When resolving a variable name, Python searches 4 scopes sequentially from inside out:

1. **L (Local):** Names assigned inside the current function or lambda.
2. **E (Enclosing):** Names in the local scope of any enclosing/outer functions (closures).
3. **G (Global / Module):** Names assigned at the top-level of the current module file or declared via `global`.
4. **B (Built-in):** Built-in functions and constants (`len`, `range`, `ValueError`).

- If an identifier is not found in any of the 4 scopes, Python raises `NameError`.

---

### Q22: What is the difference between `global` and `nonlocal` keywords?

**Answer:**

- **`global var_name`**: Tells Python that assignments to `var_name` inside a function should mutate the variable in the **top-level module scope (Global)**.
- **`nonlocal var_name`**: Introduced in Python 3. Tells Python that assignments to `var_name` should mutate the variable in the **nearest enclosing function scope** (excluding global scope). Essential for stateful closures.

```python
def outer():
    count = 0
    def inner():
        nonlocal count # Modifies outer's count, not a new local variable!
        count += 1
        return count
    return inner
```

---

### Q23: How do Closures work in Python? What is the `__closure__` attribute?

**Answer:**

- A **Closure** is a function object that retains bindings to variables in enclosing lexical scopes even after the enclosing function has exited.
- Python stores closed-over variables in the function's **`__closure__`** tuple as `cell` objects.
- Each `cell` object contains a pointer (`cell_contents`) to the shared heap memory address.

```python
def make_multiplier(x):
    def multiplier(n):
        return x * n
    return multiplier

times3 = make_multiplier(3)
print(times3.__closure__[0].cell_contents) # 3
```

---

### Q24: How do you write a Python Decorator that accepts arguments? Why is `@functools.wraps` mandatory?

**Answer:**

- A decorator taking arguments requires **3 nested function levels**:
  1. Outer function receives decorator arguments.
  2. Middle function receives the target function.
  3. Inner function (`wrapper`) receives target function arguments.
- **`@functools.wraps`**: Copies docstrings, function name (`__name__`), and annotations from the original function to the wrapper. Without it, introspecting `fn.__name__` returns `"wrapper"`, breaking logging and FastAPI route documentation.

```python
import functools

def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times - 1):
                func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    """Greets the user."""
    print(f"Hello, {name}!")

greet("Alice")
print(greet.__name__) # "greet" (Preserved by @wraps!)
```

---

### Q25: What is the difference between `__new__` and `__init__` in Python classes?

**Answer:**

- **`__new__(cls, *args, **kwargs)` (The Creator):**
  - Static method that **creates and returns a new raw instance** of the class in heap memory.
  - Receives `cls` as first argument.
  - Used for customizing creation of immutable types (`int`, `str`, `tuple`) and implementing the **Singleton Pattern**.
- **`__init__(self, *args, **kwargs)` (The Initializer):**
  - Instance method that **initializes the attributes** of the already created instance (`self`).
  - Returns `None`.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

### Q26: What is the difference between `@classmethod`, `@staticmethod`, and Instance Methods?

**Answer:**

| Method Type | First Argument | Access To | Common Use Case |
| :--- | :--- | :--- | :--- |
| **Instance Method** | `self` | Instance attributes & class state | Modifying instance state |
| **`@classmethod`** | `cls` | Class-level state & factory constructors | Factory constructors (`User.from_json(data)`) |
| **`@staticmethod`** | None | No access to `self` or `cls` | Pure utility functions related to the class domain |

---

### Q27: How does the Python Descriptor Protocol work (`@property` under the hood)?

**Answer:**

- A **Descriptor** is an object attribute whose access behavior is overridden by methods in the descriptor protocol:
  - `__get__(self, instance, owner)`
  - `__set__(self, instance, value)`
  - `__delete__(self, instance)`
- **`@property`** is a built-in descriptor that maps attribute access to getter, setter, and deleter methods:

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return (self._celsius * 9 / 5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5 / 9
```

---

### Q28: What is Method Resolution Order (MRO) and C3 Linearization?

**Answer:**

- In multiple inheritance, **MRO** defines the deterministic order in which Python searches parent classes for an attribute or method.
- Calculated using the **C3 Linearization Algorithm** (ensuring local precedence order is preserved and monotonicity is maintained).
- Inspected via `Class.__mro__` or `Class.mro()`.

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print([cls.__name__ for cls in D.mro()])
# ['D', 'B', 'C', 'A', 'object']
```

---

### Q29: How does cooperative `super()` work in Multiple Inheritance?

**Answer:**

- `super()` does NOT simply call the immediate parent class; it calls the **next class in the MRO list** of the caller instance.
- To maintain cooperative inheritance, all methods in the hierarchy must invoke `super().__init__(*args, **kwargs)` with forwarding arguments.

---

### Q30: What are Metaclasses in Python and what is `type`?

**Answer:**

- In Python, **classes are themselves objects** in memory!
- A **Metaclass** is the class of a class (a blueprint that constructs classes).
- By default, all classes are instances of the built-in metaclass **`type`**.
- Metaclasses intercept class creation (`__new__` in metaclass) to validate attributes, enforce architectural rules, or register plugins. (Used extensively by Pydantic and Django ORM).

```python
# Creating a class dynamically via type(name, bases, dict):
MyClass = type("MyClass", (object,), {"x": 10, "say": lambda self: "hi"})
obj = MyClass()
print(obj.x) # 10
```

---

### Q31: What are Abstract Base Classes (ABCs) in Python?

**Answer:**

- Defined in the `abc` module (`from abc import ABC, abstractmethod`).
- Classes inheriting from `ABC` with `@abstractmethod` **cannot be instantiated** unless all abstract methods are overridden by subclasses.

---

### Q32: What is the difference between `__getattr__` and `__getattribute__`?

**Answer:**

- **`__getattribute__(self, name)`**: Invoked **unconditionally on EVERY attribute access**. Easy to cause infinite recursion if you don't call `super().__getattribute__(name)`.
- **`__getattr__(self, name)`**: Invoked **ONLY as a fallback when the attribute was NOT found** in the instance's dictionary or class tree. Ideal for proxy objects and dynamic attribute dispatch.

---

### Q33: How does the Context Manager protocol work (`__enter__` and `__exit__`)?

**Answer:**

- Invoked by the `with` statement:
  1. `__enter__()`: Prepares resources (opens file, acquires lock); returns value bound to `as` target.
  2. Code block executes.
  3. `__exit__(exc_type, exc_val, exc_tb)`: Always executes cleanup.
  - If an exception occurred, arguments contain error details. Returning `True` from `__exit__` suppresses the exception.
- Alternative: `@contextlib.contextmanager` with `yield`.

---

### Q34: What is `dataclasses` in Python 3.7+?

**Answer:**

- `@dataclass` decorator automatically generates boilerplate methods (`__init__`, `__repr__`, `__eq__`, `__hash__`) based on type annotations.
- Supports `frozen=True` (immutable instances) and `slots=True` (Python 3.10+ memory optimization).

---

### Q35: What is Monkey Patching and why is it dangerous?

**Answer:**

- Dynamically updating or overriding modules, classes, or methods at runtime in memory without altering source code files.
- **Danger:** Introduces hidden side effects, breaks code assumptions across third-party libraries, and creates debugging nightmares.

---

### Q36: What is the difference between `__call__` and standard method invocation?

**Answer:**

- Defining `__call__(self, *args, **kwargs)` on a class allows instances of that class to be **invoked like a function**: `instance()`.
- Used for stateful decorators, callable strategy patterns, and API clients.

---

### Q37: What is `functools.lru_cache` and how does it prevent memory leaks?

**Answer:**

- `@functools.lru_cache(maxsize=128)` caches function return values using a Least Recently Used eviction strategy.
- Setting a bounded `maxsize` (e.g. 128) prevents unbounded memory growth compared to naive dictionary caches.

---

### Q38: How does Python's Garbage Collection interact with `__del__`?

**Answer:**

- `__del__` is the destructor method called when an object's reference count drops to 0.
- In legacy Python, objects with `__del__` in circular reference cycles could not be collected. In Python 3.4+ (PEP 442), cyclic GC handles `__del__` cleanly, but relying on `__del__` for resource cleanup is an anti-pattern; always use `with` context managers.

---

### Q39: What are Keyword-Only Arguments and Positional-Only Arguments?

**Answer:**

- **Keyword-Only (`*`):** `def fn(a, *, b):` $\to$ `b` must be passed by keyword (`fn(1, b=2)`).
- **Positional-Only (`/` - Python 3.8+):** `def fn(a, /, b):` $\to$ `a` must be passed by position (`fn(1, 2)` or `fn(1, b=2)`).

---

### Q40: What is `typing.Protocol` (Structural Subtyping / Duck Typing)?

**Answer:**

- Introduced in Python 3.8 (PEP 544).
- Enables **compile-time Duck Typing** (like TypeScript interfaces).
- A class satisfies a `Protocol` if it implements the required methods and attributes, without needing to explicitly inherit from it:

```python
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

class Button: # Does NOT inherit from Renderable!
    def render(self) -> str:
        return "<button></button>"

def display(widget: Renderable):
    print(widget.render())
```
