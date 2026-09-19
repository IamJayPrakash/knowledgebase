# Python & FastAPI Master Interview Bank: Part 1 (Q1 - Q20)

## Python Core, Mutability, Memory & Data Structures

---

### Q1: Explain the CPython Execution Model: Bytecode compilation and the Python Virtual Machine (PVM)

**Answer:**

```
[.py Source Code]
        │
        ▼ (Parser & AST)
[ Compiler ] ──► Compiles to Python Bytecode (.pyc file in __pycache__)
        │
        ▼
[ Python Virtual Machine (PVM) ] ──► Stack-based interpreter loop (eval loop)
        │
        ▼
   Machine Code execution on OS CPU
```

- Python is interpreted, but compiles `.py` source code to **bytecode** first.
- The **PVM** is a stack-based virtual machine: it pushes arguments onto an evaluation stack, executes bytecode opcodes (e.g. `LOAD_FAST`, `BINARY_ADD`, `STORE_NAME`), and returns results.

---

### Q2: In Python, "variables are not buckets; they are name tags". Explain this concept

**Answer:**

- In C/C++, a variable is a named memory location that directly stores a value (`int a = 10;`).
- In Python, **variables are merely reference labels (name bindings) attached to objects in heap memory**.
- Multiple names can be bound to the exact same underlying object:

  ```python
  a = [1, 2, 3]
  b = a # b is another label referencing the same list in memory!
  b.append(4)
  print(a) # [1, 2, 3, 4]
  ```

---

### Q3: What is the difference between `is` and `==`?

**Answer:**

- **`==` (Value Equality):** Compares whether two objects have equivalent contents or values. Invokes the `__eq__()` dunder method.
- **`is` (Identity / Memory Address Equality):** Compares whether two variables point to the **exact same memory address** in RAM. Equivalent to `id(a) == id(b)`.

```python
list1 = [1, 2, 3]
list2 = [1, 2, 3]

print(list1 == list2) # True (Same values)
print(list1 is list2) # False (Two distinct objects in heap memory!)
```

---

### Q4: What is Small Integer Caching in CPython?

**Answer:**

- In CPython, integer objects are immutable.
- To avoid constantly allocating and deallocating small numbers, CPython pre-allocates an array of integer singleton objects for the range **`-5` to `256`** (inclusive) during interpreter startup.
- Any integer computation resulting in a number in this range returns the shared pre-allocated singleton:

```python
x = 256
y = 256
print(x is y) # True (Shared cached singleton!)

x = 257
y = 257
print(x is y) # False (Allocated as two separate PyLongObject instances)
```

---

### Q5: What is String Interning in Python?

**Answer:**

- **String Interning:** An optimization where Python ensures that only one copy of distinct immutable strings is stored in memory.
- CPython automatically interns:
  1. String literals that look like valid Python identifiers (ASCII letters, digits, underscores).
  2. Empty strings and single-character ASCII strings.
- Explicitly intern any string using `sys.intern(s)` to enable ultra-fast $O(1)$ pointer comparisons (`s1 is s2`) instead of $O(N)$ character-by-character equality checks.

---

### Q6: Which built-in data types are Mutable vs Immutable?

**Answer:**

- **Immutable Types:** `int`, `float`, `complex`, `str`, `tuple`, `frozenset`, `bytes`, `bool`. (Their state cannot be changed after creation; modifications return a brand-new object).
- **Mutable Types:** `list`, `dict`, `set`, `bytearray`, custom class instances. (Can be modified in-place without altering their memory address `id()`).

---

### Q7: Can a Tuple contain Mutable elements? Is such a Tuple Hashable?

**Answer:**

- **Yes, a tuple can contain mutable elements:** `t = (1, [2, 3])`.
- **Hashability:** A tuple is hashable if and only if **all of its elements are themselves hashable**.
  - `(1, 2, "a")` $\to$ Hashable (can be used as a Dict key or Set element).
  - `(1, [2, 3])` $\to$ **Unhashable!** Calling `hash(t)` throws `TypeError: unhashable type: 'list'`. It cannot be used as a Dictionary key or added to a Set!

---

### Q8: How does Python's `list` resizing strategy work internally?

**Answer:**

- In CPython, `list` is implemented as an array of pointers to objects (`PyObject**`).
- When appending elements, if the allocated buffer fills up, CPython resizes the array using an **over-allocation formula** (growth factor $\approx 1.125$):
  $$\text{new\_allocated} = \text{newsize} + (\text{newsize} \gg 3) + (\text{newsize} < 9 \ ? \ 3 : 6)$$
- **Why over-allocate:** Prevents calling `realloc()` on every single `append()`, giving `list.append()` an **amortized $O(1)$ time complexity**.

---

### Q9: How did Python 3.7+ Compact Dict reduce memory usage by ~30%?

**Answer:**

- **Pre-Python 3.6 (Sparse Hash Table):**
  Stored keys, hashes, and values directly in a sparse hash table with lots of empty rows.
- **Python 3.7+ (Split-Table / Compact Dict):**
  1. **`indices` Array (Sparse):** Small array of integers storing hash table indices.
  2. **`entries` Array (Dense):** Contiguous array storing `[hash, key, value]` in the **exact order of insertion**.
- **Benefits:**
  - Saves 25-35% RAM by keeping the large entry structs in a compact contiguous array.
  - **Maintains insertion order by default!**

```
Indices array (sparse):  [-1,  0, -1,  1, -1]
Entries array (dense):   [0: (hash1, "name", "Alice"), 1: (hash2, "age", 30)]
```

---

### Q10: How does a Python `set` work internally and why must Set elements be Hashable?

**Answer:**

- A `set` is implemented using a hash table containing keys without values (effectively a dict with dummy values).
- When checking `x in my_set`:
  1. Computes `hash(x)`.
  2. Jumps to the hash bucket index.
  3. If occupied, verifies `key == x` to resolve collisions.
- **Why Hashable:** If elements could be mutated after insertion, their hash would change, leaving them stranded in the wrong bucket and breaking $O(1)$ lookups.

---

### Q11: What is the difference between `deepcopy` and `copy` in Python?

**Answer:**

- `copy.copy(obj)`: **Shallow Copy**. Constructs a new collection, but inserts references to the original child objects. Mutating nested items mutates both.
- `copy.deepcopy(obj)`: **Deep Copy**. Recursively clones all nested objects, lists, and dicts, and uses an internal memo dictionary to safely preserve **circular references** without infinite recursion.

---

### Q12: Why is using a Mutable Default Argument (`def fn(x=[])`) an anti-pattern?

**Answer:**

```python
def add_item(item, list_holder=[]): # ❌ ANTI-PATTERN!
    list_holder.append(item)
    return list_holder
```

**Why it fails:**
Default argument expressions are evaluated **ONCE when the function definition is executed at module load time**, NOT on each function call.

- The same list instance is shared across all subsequent invocations:
  `add_item(1)` $\to$ `[1]`; `add_item(2)` $\to$ `[1, 2]`!
- **Idiomatic Solution:**

  ```python
  def add_item(item, list_holder=None):
      if list_holder is None:
          list_holder = []
      list_holder.append(item)
      return list_holder
  ```

---

### Q13: What are List Comprehensions vs Generator Expressions?

**Answer:**

- **List Comprehension (`[x * 2 for x in data]`):**
  Eagerly computes and allocates the **entire list in memory** immediately.
  - *Memory:* $O(N)$. Fast for small datasets requiring random access or length checks.
- **Generator Expression (`(x * 2 for x in data)`):**
  Returns a **generator object** that computes items **lazily on-demand** one by one.
  - *Memory:* $O(1)$ constant memory, regardless of whether processing 10 items or 10 billion items!

---

### Q14: What is `collections.deque` and why is it faster than `list` for queues?

**Answer:**

- `list.pop(0)` or `list.insert(0, val)` has **$O(N)$ time complexity** because all subsequent elements must be shifted in contiguous memory.
- **`collections.deque` (Double-Ended Queue):**
  Implemented as a **doubly linked list of fixed-size blocks (62 elements per block)**.
  - Appending and popping from either end (`appendleft()`, `popleft()`) is **strictly $O(1)$**, making it the optimal data structure for queues and breadth-first search (BFS).

---

### Q15: What is `collections.defaultdict` and `collections.Counter`?

**Answer:**

- **`defaultdict(factory)`**: Subclass of `dict` that overrides `__missing__(key)`. If a key is absent, it calls the factory function (e.g. `list`, `int`) to initialize a default value automatically without throwing `KeyError`.
- **`Counter`**: Specialized dictionary designed for counting hashable objects:
  `Counter("banana")` $\to$ `{'a': 3, 'n': 2, 'b': 1}`. Provides `.most_common(n)`.

---

### Q16: What is the Walrus Operator (`:=`) in Python 3.8+?

**Answer:**

- The **Assignment Expression operator (`:=`)** assigns values to variables as part of a larger expression:

  ```python
  # Without walrus:
  line = file.readline()
  while line:
      process(line)
      line = file.readline()

  # With walrus operator:
  while (line := file.readline()):
      process(line)
  ```

- Prevents redundant function calls in list comprehensions:
  `[y for x in data if (y := expensive_calc(x)) > 10]`

---

### Q17: How does Structural Pattern Matching (`match-case`) work in Python 3.10+?

**Answer:**
`match-case` is not a simple C-style switch; it performs **full pattern matching and destructuring** on sequences, mappings, and class instances with guard conditions:

```python
def process_event(event):
    match event:
        case {"type": "CLICK", "x": int(x), "y": int(y)} if x > 0:
            print(f"Positive click at {x}, {y}")
        case ["LOG", *messages]:
            print(f"Log messages: {messages}")
        case _:
            print("Unknown event format")
```

---

### Q18: What is the difference between `str()` and `repr()`?

**Answer:**

- **`str()` (invokes `__str__`)**: Designed to be **readable by end-users**. Clean and informal representation.
- **`repr()` (invokes `__repr__`)**: Designed to be **unambiguous and useful for developers/debugging**. Should ideally look like valid Python code that could recreate the object (`eval(repr(obj)) == obj`).

---

### Q19: What is `__slots__` and how does it optimize memory in Python classes?

**Answer:**

- By default, Python instances store attributes in an internal dictionary: `instance.__dict__`.
- Dictionaries have substantial memory overhead.
- Declaring **`__slots__ = ('name', 'age')`**:
  - Replaces `__dict__` with a fixed-size compact C-array of references.
  - **Saves 40-50% memory per instance** when instantiating millions of small objects.
  - Prevents dynamically adding arbitrary attributes not defined in `__slots__`.

---

### Q20: What is `frozenset` and when should you use it?

**Answer:**

- An **immutable version of a `set`**.
- Because it is immutable, a `frozenset` is **hashable**!
- **Use Cases:**
  1. Using sets as keys in a dictionary.
  2. Storing sets inside another set (sets of sets).
