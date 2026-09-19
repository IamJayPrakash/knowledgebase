# scripts/build_language_basics_newbie_to_expert.py
import os
import shutil

BASE_DIR = r"D:\Projects\knowledgebase"

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# ==============================================================================
# 1. JAVASCRIPT BASICS (NEWBIE TO EXPERIENCED)
# ==============================================================================

JS_OPERATORS_CONTROL_FLOW = """# JavaScript Operators, Type Casting & Control Flow

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Jaise real life mein traffic signal pe green light hone par hi gaadi aage badhti hai (Conditional execution), waise hi code mein decisions lene ke liye operators aur control flow use hote hain. `==` aalsi dost hai jo type check kiye bina 'haan' bol deta hai, jabki `===` strict inspector hai jo ID card (type) aur shakal (value) dono verify karta hai!
>
> **Real-World Analogy:** A security checkpoint: Loose equality (`==`) lets anyone with a printed ticket pass even if the name format is slightly off (e.g. number `5` vs string `'5'`). Strict equality (`===`) checks both the ticket number AND biometric identity (exact type and value).

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Comparison Operators**: Always use strict equality (`===`) instead of loose equality (`==`). `==` triggers implicit type coercion which creates unexpected bugs (`0 == ''` is `true`, `false == []` is `true`).
- **Logical Operators**: `&&` (AND - returns first falsy or last truthy value), `||` (OR - returns first truthy or last falsy value), `!` (NOT - inverts boolean).
- **Falsy Values in JavaScript**: Exactly 8 values: `false`, `0`, `-0`, `0n` (BigInt), `""` (empty string), `null`, `undefined`, `NaN`. Everything else is truthy!
- **Modern Safe Operators**:
  - Nullish Coalescing (`??`): Returns right-hand side ONLY if left-hand side is `null` or `undefined` (unlike `||`, which treats `0` and `""` as falsy).
  - Optional Chaining (`?.`): Safely reads nested properties without throwing `Cannot read properties of undefined`.
- **Loops**:
  - `for`: Standard counter loop.
  - `for...of`: Iterates over **values** of iterables (Arrays, Strings, Maps, Sets).
  - `for...in`: Iterates over **enumerable property keys** of an object (Hazardous on arrays because it visits prototype chain and indices as strings).

### 🧓 What an Experienced Candidate Knows:
- **Bitwise Operators for Performance**: Bitwise operations (`| 0`, `>>`, `<<`) coerce 64-bit IEEE-754 floating point numbers to 32-bit signed integers in V8.
- **Short-Circuit Logical Assignment**: `&&=`, `||=`, `??=` avoid unnecessary re-assignments and setter invocations.
- **Switch Jump Table Optimization**: V8 compiles dense numeric or string `switch` statements into O(1) jump tables or hash lookup tables rather than chained O(N) `if-else` branches.

---

## 3. 📊 Visual Architecture Diagram

```text
Comparison & Evaluation Flow:

   a == b (Loose Equality)
     │
     ├──> Are types identical? ──YES──> Compare values directly
     │
     └───NO──> Coerce via ToPrimitive / ToNumber rules:
                 '5' == 5       ──> Number('5') === 5  ──> TRUE
                 null == undefined                      ──> TRUE
                 [] == false    ──> '' == 0 -> 0 == 0   ──> TRUE (Trap!)

   a === b (Strict Equality)
     │
     ├──> Are types identical? ──NO───> Immediately return FALSE (No coercion!)
     │
     └───YES──> Compare values directly (NaN !== NaN exception)
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
// Line 1: Define an object with optional deeply nested properties
const userProfile = {
  // Line 2: User profile name
  name: 'Jay',
  // Line 3: User settings object
  settings: {
    // Line 4: Notification preferences
    notifications: {
      // Line 5: Explicitly set email notification to false
      email: false,
      // Line 6: SMS alert threshold count set to zero
      smsCount: 0
    }
  }
};

// Line 7: NEWBIE PITFALL: Using logical OR (||) incorrectly overwrites valid 0 and false!
const badSmsCount = userProfile.settings?.notifications?.smsCount || 10;
// Line 8: Logs 10 because 0 is falsy in JavaScript, which accidentally overrides the user's setting of 0!
console.log('Bad SMS Count (||):', badSmsCount); // 10 (Incorrect!)

// Line 9: EXPERIENCED SOLUTION: Using Nullish Coalescing (??) preserves 0 and false
const correctSmsCount = userProfile.settings?.notifications?.smsCount ?? 10;
// Line 10: Logs 0 because ?? only falls back on null or undefined!
console.log('Correct SMS Count (??):', correctSmsCount); // 0 (Correct!)

// Line 11: Safely reading non-existent nested property with Optional Chaining (?.)
const pushToken = userProfile.settings?.push?.token ?? 'DEFAULT_TOKEN';
// Line 12: Logs DEFAULT_TOKEN without throwing a TypeError
console.log('Push Token:', pushToken); // 'DEFAULT_TOKEN'

// Line 13: Difference between for...of and for...in
const scores = [100, 200, 300];
// Line 14: Adding a custom property to prototype to demonstrate for...in trap
Array.prototype.customMethod = () => {};

// Line 15: for...of iterates cleanly over array VALUES
console.log('--- for...of (Values) ---');
for (const score of scores) {
  // Line 16: Outputs each numeric score directly: 100, 200, 300
  console.log('Score value:', score);
}

// Line 17: for...in iterates over KEYS including prototype properties (Hazardous!)
console.log('--- for...in (Keys & Prototype Trap) ---');
for (const key in scores) {
  // Line 18: Outputs indices '0', '1', '2' AND 'customMethod'!
  console.log('Array key:', key);
}

// Line 19: Clean up array prototype
delete Array.prototype.customMethod;
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "What is the difference between `==`, `===`, `||`, and `??` in JavaScript?"
>
> **You:** "In JavaScript, double equals `==` performs implicit type coercion using the abstract equality comparison algorithm, which leads to counter-intuitive truthy results like `[] == false`. Triple equals `===` checks both value and type without coercion, which is the industry standard. For fallback values, logical OR `||` checks for any falsy value, which inadvertently overrides valid values like `0`, empty string `""`, and `false`. Nullish coalescing `??` specifically checks only for `null` or `undefined`, making it the safe, deterministic choice for configuration defaults."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** In an e-commerce checkout service, premium customers configured a `discountPercentage: 0` during specific flash sales, but the cart total calculation used `const discount = user.discount || defaultDiscount (15)`.
* **Task / Challenge:** Customers with zero discount configurations were unexpectedly receiving 15% promotional deductions, leading to revenue leakage during audited vendor campaigns.
* **Action Taken:** Migrated the pricing engine to use strict nullish coalescing `??` and optional chaining `?.`, backed by schema validation that explicitly treated `0` as a valid numeric float.
* **Result & Business Impact:** Eliminated duplicate promotional discounts across 1.2M daily checkout transactions, saving $45,000 in unintended promotional deductions in Q1.
"""

JS_ARRAYS_IN_DEPTH = """# JavaScript Arrays Masterclass: Mutating vs Non-Mutating Methods & Hand-Coded Polyfills

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Array ek dabbe ki tarah hai jisme saman rakha hai. Mutating method (jaise `splice`, `push`) original dabbe ke saman ko tod-marod deta hai. Non-mutating method (jaise `map`, `filter`, `slice`) pehle saman ki Xerox copy banata hai aur naye dabbe mein de deta hai, jisse original safe rehta hai.
>
> **Real-World Analogy:** Editing an original master painting directly with a brush (Mutating - you can never restore the original) vs taking a high-res photo, editing the photo in Photoshop, and saving a new file (Non-mutating / Immutable).

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Mutating Methods (Modifies Original Array)**:
  - `push()` / `pop()`: Adds / removes from the end ($O(1)$).
  - `unshift()` / `shift()`: Adds / removes from the beginning ($O(N)$ because all indices must re-shift).
  - `splice(start, deleteCount, ...items)`: Modifies array in-place.
  - `sort()`: Sorts in-place (Converts elements to strings by default! E.g. `[10, 2].sort()` produces `[10, 2]`).
  - `reverse()`: Reverses in-place.
- **Non-Mutating Methods (Returns New Array / Value)**:
  - `slice(start, end)`: Shallow copies a portion of an array.
  - `concat()`: Merges arrays into a new array.
  - `map(fn)`: Transforms every element into a new array of identical length.
  - `filter(fn)`: Returns a new array containing only elements that satisfy the predicate.
  - `reduce(fn, initialValue)`: Accumulates elements into a single value (object, number, array).
  - Modern ES2023 Non-mutating equivalents: `toSorted()`, `toReversed()`, `toSpliced()`.

### 🧓 What an Experienced Candidate Knows:
- **V8 Array Internals**: Under the hood, V8 optimizes arrays into either **Fast Elements** (contiguous C++ memory vector: SMI for small integers, DOUBLE for floats) or **Dictionary Elements** (hash table for sparse arrays like `arr[10000] = 1`). Sparse arrays degrade performance by $10\times$.
- **The Initial Value Trap in `reduce`**: Calling `reduce` on an empty array without an `initialValue` throws a runtime `TypeError: Reduce of empty array with no initial value`.
- **Reference vs Value in Shallow Copies**: `map`, `filter`, and `slice` produce shallow copies. If array elements are objects, modifying object properties in the new array mutates the original object!

---

## 3. 📊 Visual Architecture Diagram

```text
Array Method Classification:

   Original Array: [1, 2, 3]
         │
         ├── Mutating Methods (In-Place Memory Alteration):
         │     ├── push(4)     ──> Modifies original: [1, 2, 3, 4]
         │     ├── splice(1,1) ──> Modifies original: [1, 3]
         │     └── sort()      ──> Modifies original memory directly!
         │
         └── Non-Mutating Methods (Pure Functions / Immutability):
               ├── slice(0, 2) ──> Returns NEW Array: [1, 2] (Original intact)
               ├── map(x => x*2)─> Returns NEW Array: [2, 4, 6] (Original intact)
               └── filter(x > 1) ─> Returns NEW Array: [2, 3] (Original intact)
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
// Line 1: Define a test array of product items
const cart = [
  // Line 2: Product A
  { id: 101, name: 'Mechanical Keyboard', price: 120, category: 'Electronics' },
  // Line 3: Product B
  { id: 102, name: 'Ergonomic Mouse', price: 80, category: 'Electronics' },
  // Line 4: Product C
  { id: 103, name: 'Desk Mat', price: 25, category: 'Accessories' }
];

// Line 5: Hand-crafting custom Array.prototype.myReduce polyfill to master mechanics
Array.prototype.myReduce = function(callback, initialValue) {
  // Line 6: Validate that callback is a function
  if (typeof callback !== 'function') {
    // Line 7: Throw TypeError if callback is not callable
    throw new TypeError(callback + ' is not a function');
  }
  
  // Line 8: Capture reference to array and its length
  const array = this;
  const length = array.length;
  // Line 9: Pointer variable for current index
  let index = 0;
  // Line 10: Accumulator variable
  let accumulator;

  // Line 11: Check if caller passed an explicit initialValue (handling arguments length)
  if (arguments.length >= 2) {
    // Line 12: Set accumulator to provided initialValue
    accumulator = initialValue;
  } else {
    // Line 13: Edge Case: Array is completely empty and no initialValue provided
    while (index < length && !(index in array)) {
      // Line 14: Skip sparse array holes
      index++;
    }
    // Line 15: If no elements found in array, throw standard TypeError
    if (index >= length) {
      throw new TypeError('Reduce of empty array with no initial value');
    }
    // Line 16: Use the first non-empty element as initial accumulator
    accumulator = array[index++];
  }

  // Line 17: Loop through the rest of the array elements
  for (; index < length; index++) {
    // Line 18: Skip holes in sparse arrays
    if (index in array) {
      // Line 19: Compute next accumulator value via callback
      accumulator = callback(accumulator, array[index], index, array);
    }
  }

  // Line 20: Return final accumulated result
  return accumulator;
};

// Line 21: Calculate total cart price using our custom myReduce
const totalPrice = cart.myReduce((sum, item) => {
  // Line 22: Accumulate item price
  return sum + item.price;
// Line 23: Provide 0 as initial seed value
}, 0);
// Line 24: Output total calculated cart value
console.log('Total Price via myReduce:', totalPrice); // 225

// Line 25: Group products by category using native reduce
const groupedByCategory = cart.reduce((acc, item) => {
  // Line 26: Destructure category
  const cat = item.category;
  // Line 27: Initialize category array if not yet present
  acc[cat] = acc[cat] ?? [];
  // Line 28: Append product to category list
  acc[cat].push(item);
  // Line 29: Return accumulator
  return acc;
// Line 30: Initialize with empty object
}, {});
// Line 31: Output grouped result
console.log('Grouped Products:', groupedByCategory);
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Why is immutability important when manipulating arrays in modern frontend frameworks?"
>
> **You:** "In modern reactive frameworks like React and Angular 21, change detection relies on referential equality checks (`prevProps.items !== nextProps.items`). When you use mutating methods like `push` or `splice`, the memory address of the array stays identical, causing the UI reconciler to skip re-rendering and leading to phantom UI bugs. Non-mutating methods like `map`, `filter`, or ES2023 `toSorted` allocate a fresh array reference, guaranteeing deterministic, bug-free reactivity and pure functional state transitions."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A real-time cryptocurrency dashboard rendered stale prices because state updates used `state.prices.sort()` directly inside Redux reducers.
* **Task / Challenge:** The UI failed to update top-gainer tokens on the screen even though backend WebSocket streams pushed fresh price ticks every 500ms.
* **Action Taken:** Diagnosed the issue using Chrome DevTools memory allocation timeline; discovered `sort()` was mutating state in-place, causing shallow comparison `prev === next` to return `true`. Replaced the sorting logic with `[...prices].sort()` and integrated ESLint rule `no-mutating-methods`.
* **Result & Business Impact:** Fixed the real-time UI freeze across 350,000 active traders with zero performance degradation.
"""

JS_OBJECTS_CLONING = """# JavaScript Objects, Destructuring, Spread/Rest & Deep vs Shallow Cloning

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Shallow copy ek ghar ki chaabi duplicate karne jaisa hai (Bahari darwaza naya hai, par andar ka kamra wahi ek hi hai!). Agar guest room mein aag lagegi, toh dono chaabi walo ke liye lagegi. Deep copy ek naya ghar hubahu banana hai (Har kamra, sofa, furniture alag memory mein create hota hai).
>
> **Real-World Analogy:** A photocopy of a page containing a web link (Shallow Copy): you have a separate piece of paper, but the link points to the exact same website. A Deep Copy prints out the entire website content on fresh physical paper.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Object Destructuring**: Extracting properties into individual variables (`const { name, age = 18 } = user`).
- **Renaming / Aliasing**: `const { name: userName } = user`.
- **Rest Operator (`...`)**: Gathers remaining properties into a new object (`const { id, ...details } = user`).
- **Spread Operator (`...`)**: Copies properties into a new object (`const clone = { ...user }`). Note: **This is a shallow copy!**
- **Shallow Copy vs Deep Copy**:
  - Shallow Copy (`Object.assign({}, obj)` or `{ ...obj }`): Only copies the top-level primitives. Nested objects share the exact same reference on the Heap!
  - Deep Copy (`structuredClone(obj)` or custom recursive copier): Creates brand-new copies of all nested objects and arrays.

### 🧓 What an Experienced Candidate Knows:
- **`JSON.parse(JSON.stringify(obj))` Pitfalls**:
  - Drops `undefined`, functions, and `Symbol` properties completely.
  - Converts `Date` objects to ISO string representations instead of preserving Date instances.
  - Converts `NaN` and `Infinity` to `null`.
  - **Throws an uncaught TypeError on Circular References** (`obj.self = obj`).
- **Modern `structuredClone()` API**: Native browser/Node.js API that handles circular references, `Date`, `RegExp`, `Map`, `Set`, and `ArrayBuffer`. Still cannot copy functions or DOM nodes.
- **`Object.freeze()` vs `Object.seal()`**:
  - `Object.freeze()`: Cannot add, delete, or modify existing property values.
  - `Object.seal()`: Cannot add or delete properties, but **can** modify existing property values.
  - Both are shallow! Nested objects remain fully mutable unless deep-frozen recursively.

---

## 3. 📊 Visual Architecture Diagram

```text
Shallow Copy vs Deep Copy Memory Layout:

   [Original Object]
     id: 101
     profile: ───┐ (Pointer)
                 │
   [Shallow Copy]│
     id: 101     │
     profile: ───┴──> { avatar: 'pic.png', city: 'Pune' } (SHARED HEAP OBJECT!)
                       ^ Mutating clone.profile.city mutates original too!

   [Deep Copy via structuredClone]
     id: 101
     profile: ──────> { avatar: 'pic.png', city: 'Pune' } (INDEPENDENT HEAP MEMORY!)
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
// Line 1: Define a complex object with nested structures and circular reference
const originalUser = {
  // Line 2: Primitive ID
  id: 42,
  // Line 3: String name
  name: 'Jay Prakash',
  // Line 4: Date object
  createdAt: new Date('2026-01-01'),
  // Line 5: Nested address object
  address: {
    // Line 6: City property
    city: 'Bengaluru',
    // Line 7: Coordinates array
    geo: [12.9716, 77.5946]
  }
};

// Line 8: Introduce a circular reference to test deep clone robustness
originalUser.self = originalUser;

// Line 9: Hand-crafting an industrial-strength deep clone function using WeakMap
function deepClone(target, hash = new WeakMap()) {
  // Line 10: Return primitives and functions directly (base case)
  if (target === null || typeof target !== 'object') {
    return target;
  }

  // Line 11: Handle Date objects properly
  if (target instanceof Date) {
    return new Date(target.getTime());
  }

  // Line 12: Handle RegExp objects properly
  if (target instanceof RegExp) {
    return new RegExp(target.source, target.flags);
  }

  // Line 13: Handle Circular References using WeakMap lookup
  if (hash.has(target)) {
    // Line 14: Return existing cloned reference to prevent infinite recursion
    return hash.get(target);
  }

  // Line 15: Create new Array or Object preserving prototype
  const clone = Array.isArray(target) ? [] : Object.create(Object.getPrototypeOf(target));
  // Line 16: Cache cloned reference in WeakMap before traversing children
  hash.set(target, clone);

  // Line 17: Reflect.ownKeys retrieves both enumerable and symbol properties
  for (const key of Reflect.ownKeys(target)) {
    // Line 18: Recursively clone every property
    clone[key] = deepClone(target[key], hash);
  }

  // Line 19: Return fully isolated deep clone
  return clone;
}

// Line 20: Execute deep clone
const clonedUser = deepClone(originalUser);

// Line 21: Verify mutation independence
clonedUser.address.city = 'Mumbai';
// Line 22: Original city remains untouched!
console.log('Original City:', originalUser.address.city); // 'Bengaluru'
// Line 23: Cloned city reflects new value
console.log('Cloned City:', clonedUser.address.city);     // 'Mumbai'
// Line 24: Verify circular reference integrity
console.log('Circular Ref Check:', clonedUser.self === clonedUser); // true
// Line 25: Verify deep clone is distinct object reference
console.log('Distinct Objects:', clonedUser !== originalUser);      // true
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Why shouldn't you use `JSON.parse(JSON.stringify(object))` for deep cloning in production?"
>
> **You:** "While `JSON.parse(JSON.stringify())` works for simple primitive trees, it breaks down in production. It silently strips `undefined`, functions, and `Symbol` keys, coerces `Date` objects into plain strings, converts `NaN` to `null`, and throws a fatal uncaught exception when encountering circular references. In modern Node.js and browsers, we should prefer native `structuredClone()`, or use an explicit recursive cloner with a `WeakMap` to cleanly handle cyclic references and special object types."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** In an insurance underwriting platform, policy drafts allowed underwriters to test quote adjustments. When an underwriter altered a draft deductible, the live underwriting policy was inadvertently mutated.
* **Task / Challenge:** Tracking down why production policies were changing without a save action being submitted.
* **Action Taken:** Root cause analysis revealed the draft creation service was doing a shallow spread `{ ...livePolicy }`. While top-level fields were cloned, the `pricingTiers` array and nested discount objects pointed to the production database cache. Replaced the shallow spread with `structuredClone()`.
* **Result & Business Impact:** Completely eliminated policy cross-contamination and passed regulatory financial audits with zero data corruption.
"""

# ==============================================================================
# 2. PYTHON CORE BASICS (NEWBIE TO EXPERIENCED)
# ==============================================================================

PY_FUNDAMENTALS = """# Python Fundamentals: Syntax, Dynamic Typing, Variables & Mutability

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** C++ ya Java mein variable ek **dabba (box)** hota hai jisme data band rehta hai. Lekin Python mein variable dabba nahi, balki ek **luggage tag (sticky label)** hota hai jo memory mein rakhe kisi object par chipka diya jata hai! Agar do label ek hi bag par lage hain, toh bag mein saman badalne par dono label wahi badla hua bag dikhayenge.
>
> **Real-World Analogy:** A luggage tag at an airport. The suitcase on the conveyor belt is the object in heap memory. The name tag you tie to the handle is the Python variable. You can tie multiple tags (`a = b`) to the same physical suitcase.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Dynamic Typing**: You don't declare types (`int x = 5`). Python infers types at runtime. Type is a property of the **object**, not the variable name!
- **Everything is an Object**: In Python, functions, modules, classes, and integers are all first-class objects in heap memory.
- **Mutability vs Immutability**:
  - **Immutable Objects**: Cannot be changed after creation. If you alter them, Python allocates a brand-new object in memory. Examples: `int`, `float`, `str`, `tuple`, `frozenset`, `bool`.
  - **Mutable Objects**: Can be modified in-place without changing their memory address (`id()`). Examples: `list`, `dict`, `set`, custom class instances.
- **Identity (`is`) vs Equality (`==`)**:
  - `==` checks **value equality** (do these objects contain the same data?).
  - `is` checks **object identity** (do these variables point to the exact same address in memory?).

### 🧓 What an Experienced Candidate Knows:
- **CPython Small Integer Caching**: CPython pre-allocates an internal array of integer objects for all numbers in the range **`[-5, 256]`** during interpreter startup. Therefore, `a = 250; b = 250; a is b` evaluates to `True`, but `a = 257; b = 257; a is b` may evaluate to `False`!
- **String Interning**: CPython automatically interns compile-time string constants that look like valid Python identifiers to optimize dictionary lookup speeds.
- **The Mutable Default Argument Bug**: Writing `def append_to(item, target=[])` causes all calls sharing the default parameter to mutate the exact same list, because default arguments are evaluated **once at function definition time**, not at call time!

---

## 3. 📊 Visual Architecture Diagram

```text
CPython Memory Model: Variables as Name Bindings (Luggage Tags):

   Code:
     a = [1, 2, 3]
     b = a
     b.append(4)

   Memory Layout (Heap):
     Variable Name 'a' ──┐
                         ├──> [ PyListObject: id=0x10a40 ]
     Variable Name 'b' ──┘       ├── ob_refcnt: 2
                                 ├── ob_size: 4
                                 └── ob_item: [1, 2, 3, 4] (Mutated In-Place!)

   Code:
     x = 10
     y = x
     x = x + 1

   Memory Layout:
     Variable 'y' ──────────> [ PyLongObject(10): id=0x0010 ]
     Variable 'x' ──────────> [ PyLongObject(11): id=0x0018 ] (New Object Allocated!)
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```python
# Line 1: Define an integer variable; Python binds label 'x' to an int object 100
x = 100
# Line 2: Print the memory address of the integer object 100 using id()
print("Memory ID of x:", id(x))

# Line 3: Assign y to x; both labels now reference the exact same memory address
y = x
# Line 4: Check identity: x and y point to the exact same object
print("x is y:", x is y)  # True

# Line 5: Modifying x creates a NEW integer object because integers are IMMUTABLE
x = x + 1
# Line 6: x now has a new memory address
print("New Memory ID of x:", id(x))
# Line 7: y still points to the original integer 100
print("Value of y:", y)  # 100

# Line 8: MUTABILITY DEMONSTRATION with a List
list_a = [10, 20, 30]
# Line 9: list_b references the exact same list object on the heap
list_b = list_a
# Line 10: Record list_a's memory ID
original_id = id(list_a)

# Line 11: Mutate the list in-place by appending an element
list_b.append(40)
# Line 12: Memory address is unchanged after mutation!
print("Is Memory ID unchanged after append?:", id(list_a) == original_id)  # True
# Line 13: Both variables reflect the mutation
print("list_a contents:", list_a)  # [10, 20, 30, 40]

# Line 14: CPython Small Integer Caching Gotcha
val1 = 256
val2 = 256
# Line 15: True because 256 is within the pre-allocated [-5, 256] range
print("256 is 256:", val1 is val2)  # True

val3 = 300
val4 = 300
# Line 16: Evaluates to False in interactive REPL (outside single code block optimization)
print("300 is 300 identity check:", val3 is val4)

# Line 17: The classic Mutable Default Argument Trap and the Idiomatic Fix
def safe_append(item, target=None):
    # Line 18: Check if caller did not provide an explicit list
    if target is None:
        # Line 19: Allocate a fresh list per function call
        target = []
    # Line 20: Append item safely
    target.append(item)
    # Line 21: Return modified list
    return target

# Line 22: First call
print("Call 1:", safe_append("first"))   # ['first']
# Line 23: Second call: completely isolated fresh list!
print("Call 2:", safe_append("second"))  # ['second'] (Bug avoided!)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How does Python handle variable assignment and parameter passing under the hood?"
>
> **You:** "In Python, variables are not memory containers; they are name tags bound to objects on the heap. Parameter passing is strictly 'Call by Object Reference' (or 'Call by Sharing'). If you pass an immutable object like an `int` or `str`, any modification inside the function rebinds a local reference to a newly allocated object without affecting the caller. If you pass a mutable object like a `list` or `dict`, modifying it in-place mutates the caller's object directly. This distinction between object identity (`is`) and value equality (`==`) is foundational to writing bug-free Python code."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A machine learning batch feature service had a utility function `def extract_features(data, features=[])`. During production inference, the response payload size kept growing steadily until the server ran out of memory (OOM).
* **Task / Challenge:** Identify why memory usage swelled by 8GB over 4 hours under steady request load.
* **Action Taken:** Profiling with `tracemalloc` revealed that the default `features=[]` list was never garbage collected and retained all extracted feature arrays across millions of incoming requests. Replaced default parameter with `features=None` and initialized `features = []` inside the function body.
* **Result & Business Impact:** Completely resolved the memory leak, stabilizing inference container RAM at 250MB with zero downtime.
"""

PY_COLLECTIONS = """# Python Collections Framework: Lists, Tuples, Sets, Dictionaries & Internal Hash Tables

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - `list`: Ek stretchy rubber-band notebook jisme jab chahe naya panna jod sakte ho ($O(1)$ append).
> - `tuple`: Ek laminated certificate jo ek baar ban gaya toh badla nahi ja sakta (Immutable, fast, thread-safe).
> - `set`: Ek VIP party guest list jisme duplicates allowed nahi hain aur security guard turant bata deta hai guest aya hai ya nahi ($O(1)$ search).
> - `dict`: Phonebook jisme naam (Key) bolte hi number (Value) mil jata hai ($O(1)$ lookup via Hash Table).
>
> **Real-World Analogy:** An address book vs a diary. A list is a chronological diary where you add entries at the end. A dictionary is an indexed rolodex where you look up a person's name directly by their unique alphabetical tab without flipping through every page.

---

## 2. 📌 Core Mechanics & Time Complexities (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **`list`**: Ordered, mutable, allows duplicates.
  - Append to end: $O(1)$ amortized.
  - Insert/Delete at beginning: $O(N)$ (must shift all remaining elements in memory!).
  - Access by index: $O(1)$.
- **`tuple`**: Ordered, immutable, allows duplicates. Uses less memory than lists and can be used as dictionary keys if all its elements are hashable.
- **`set`**: Unordered, mutable, unique elements only.
  - Add / Remove / Contains (`x in s`): Average $O(1)$.
  - Set operations: Union `|`, Intersection `&`, Difference `-`.
- **`dict`**: Key-value mappings. Keys must be **hashable** (immutable objects like strings, numbers, tuples).
  - Lookup / Insert / Delete: Average $O(1)$.
- **Comprehensions**: Clean, pythonic syntax for generating collections:
  - List: `[x * 2 for x in nums if x > 0]`
  - Dict: `{k: v for k, v in pairs}`
  - Set: `{x for x in nums}`

### 🧓 What an Experienced Candidate Knows:
- **List Over-Allocation Strategy**: CPython dynamic arrays do not grow element-by-element. When the allocated buffer is full, CPython resizes using the formula: `new_allocated = (size >> 3) + (size < 9 ? 3 : 6) + size`. This ensures amortized $O(1)$ appends.
- **Python 3.7+ Compact Dict Architecture**: Historically, Python dicts were sparse hash tables (wasting 66% memory). Since 3.7, dicts use a split structure: a dense `entries` array holding `[hash, key, value]` in insertion order, and a compact sparse `indices` table. This reduced dict memory footprint by **20% to 25%** and guaranteed insertion order iteration!
- **Collision Resolution**: CPython dictionaries resolve hash collisions via **open addressing with pseudo-random probing** (perturbation algorithm: `j = ((5*j) + 1 + perturb) >> 5`), preventing clustering vulnerabilities.

---

## 3. 📊 Visual Architecture Diagram

```text
Python 3.7+ Compact Dictionary Architecture:

   Hash Table Indices (Sparse Array of small integer offsets):
   [ -1,  0, -1,  1, -1, -1,  2, -1 ]  <── Size determined by hash modulo
          │       │           │
          v       v           v
   Dense Entries Array (Ordered by insertion time!):
   Index 0: [ hash=0x34a, key='name',  value='Jay' ]
   Index 1: [ hash=0x8b1, key='role',  value='Lead' ]
   Index 2: [ hash=0x2c9, key='score', value=100 ]

   Result: Iterating dict visits entries[0], entries[1], entries[2] sequentially in O(N) cache-friendly memory!
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```python
# Line 1: Demonstrate List over-allocation and memory growth
import sys

# Line 2: Initialize an empty list
numbers = []
# Line 3: Capture initial empty list size in bytes
print(f"Empty list size: {sys.getsizeof(numbers)} bytes")

# Line 4: Append elements and track when CPython reallocates memory
prev_size = sys.getsizeof(numbers)
for i in range(20):
    # Line 5: Append item
    numbers.append(i)
    # Line 6: Check new size in bytes
    current_size = sys.getsizeof(numbers)
    # Line 7: If size jumped, reallocation occurred
    if current_size != prev_size:
        print(f"Length: {len(numbers):2d} | Reallocated Size: {current_size} bytes")
        prev_size = current_size

# Line 8: Tuple vs List memory efficiency comparison
sample_tuple = (1, 2, 3, 4, 5)
sample_list = [1, 2, 3, 4, 5]
# Line 9: Tuples are more compact because they don't need resize over-allocation headroom
print(f"Tuple size: {sys.getsizeof(sample_tuple)} bytes vs List size: {sys.getsizeof(sample_list)} bytes")

# Line 10: Set Operations for fast deduplication and set math
set_a = {"apple", "banana", "cherry"}
set_b = {"banana", "dragonfruit", "elderberry"}
# Line 11: Set union (all unique fruits)
print("Union:", set_a | set_b)
# Line 12: Set intersection (common fruits)
print("Intersection:", set_a & set_b)  # {'banana'}
# Line 13: Set difference (fruits in A but not in B)
print("Difference (A - B):", set_a - set_b)

# Line 14: Dictionary Comprehension & Modern Inversion
scores = {"Alice": 95, "Bob": 80, "Charlie": 95, "David": 60}
# Line 15: Filter high scorers using dict comprehension
top_scorers = {name: score for name, score in scores.items() if score >= 90}
print("Top Scorers:", top_scorers)

# Line 16: Invert dictionary to group students by score (handling collisions)
score_to_names = {}
for name, score in scores.items():
    # Line 17: setdefault initializes list if score key is missing, then appends
    score_to_names.setdefault(score, []).append(name)
# Line 18: Output grouped mapping
print("Score to Students Grouping:", score_to_names)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Why is checking membership in a set `O(1)` while in a list it is `O(N)`?"
>
> **You:** "In a list, elements are stored sequentially in a contiguous array. To find an item (`x in my_list`), Python must perform a linear scan comparing each element until a match is found, resulting in $O(N)$ time complexity. In contrast, a `set` is backed by a hash table. Python immediately hashes the target element using `hash(x)`, masks the hash to find the bucket index, and directly looks up the memory bucket in average $O(1)$ time. This is why converting lists to sets before membership filtering yields massive performance gains in large datasets."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A fraud detection engine checked incoming transactions against a blacklist of 500,000 compromised card tokens. Under peak load of 3,000 transactions per second, API latency spiked to 2.8 seconds and caused gateway timeouts.
* **Task / Challenge:** Reduce transaction evaluation latency from 2.8s to sub-10ms.
* **Action Taken:** Profiling with `cProfile` showed 94% of CPU time was spent in `token in blacklist_list`, where `blacklist_list` was stored as a Python `list`. Converted the blacklist storage to a Python `set` with $O(1)$ hash lookups.
* **Result & Business Impact:** Cut membership lookup time from 180ms per query to 0.05ms, reducing 99th percentile API latency from 2.8s to 4ms and maintaining 100% SLA during Black Friday.
"""

PY_FUNCTIONS_DECORATORS = """# Python Functions, Scopes, *args, **kwargs & Decorators Masterclass

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - First-class functions: Python mein function ko ek aam variable ki tarah treat kiya ja sakta hai (Kisi variable mein store karo, doosre function mein pass karo, ya return karo).
> - Decorator: Ek gift box ya gift wrapping paper ki tarah hai. Original gift (function) wahi rehta hai, lekin decorator uske upar nayi khubsurti ya security features (jaise logging, authentication, timing) add kar deta hai bina original gift ko chhue!
>
> **Real-World Analogy:** A security metal detector gate at an airport terminal. Every passenger (function call) must pass through the detector (decorator) before boarding the flight. The passenger's behavior doesn't change, but the security gate adds verification and audit logging seamlessly.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **`*args`**: Captures variable number of positional arguments into a **tuple**.
- **`**kwargs`**: Captures variable number of keyword arguments into a **dictionary**.
- **LEGB Scope Rule**: Python resolves variable names in this strict order:
  1. **L**ocal (Inside current function).
  2. **E**nclosing (Inside outer enclosing functions in nested closures).
  3. **G**lobal (Module level).
  4. **B**uilt-in (`len`, `range`, `print`).
- **Keywords `global` and `nonlocal`**:
  - `global x`: Binds local assignment to the module-level variable.
  - `nonlocal x`: Binds assignment to the nearest enclosing non-global scope (essential for closures).

### 🧓 What an Experienced Candidate Knows:
- **Closures Mechanics**: A closure occurs when a nested function retains access to variables from its enclosing lexical scope even after the outer function has finished executing and returned. Python stores these free variables in `func.__closure__` as `cell` objects.
- **Why `@functools.wraps` is Mandatory**: When you wrap a function with a decorator, the wrapper replaces the original function. Without `@functools.wraps(fn)`, the function loses its original `__name__`, `__doc__`, and signature metadata, breaking introspection, debugging, and tools like Sphinx or FastAPI OpenAPI generation!
- **Decorator Factory with Arguments**: When a decorator accepts parameters (e.g. `@rate_limit(max_per_sec=5)`), it requires **3 levels of nested functions**: outer factory -> decorator -> wrapper.

---

## 3. 📊 Visual Architecture Diagram

```text
Decorator Execution Pipeline & Closure Cell:

   @timing_decorator
   def calculate_tax(amount):
       ...

   Under the hood:
     calculate_tax = timing_decorator(calculate_tax)

   Calling calculate_tax(100):
     Caller ──> wrapper(100)
                 │
                 ├── 1. Record start_time = time.perf_counter()
                 │
                 ├── 2. result = original_func(100) ──> [Executes actual tax logic]
                 │
                 ├── 3. Record elapsed = time.perf_counter() - start_time
                 │      Log("Execution took X ms")
                 │
                 └── 4. Return result to Caller
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```python
# Line 1: Import functools to preserve function metadata in decorators
import functools
# Line 2: Import time module for latency benchmarking
import time

# Line 3: Define a parameter-accepting Decorator Factory for retrying failed operations
def retry(max_attempts=3, delay_seconds=0.1):
    # Line 4: Outer decorator receiving the target function
    def decorator(func):
        # Line 5: functools.wraps copies __name__, __doc__, and type annotations from func to wrapper
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Line 6: Track current attempt count
            attempts = 0
            # Line 7: Loop until max attempts reached
            while attempts < max_attempts:
                try:
                    # Line 8: Attempt executing original function
                    return func(*args, **kwargs)
                except Exception as exc:
                    # Line 9: Increment failure counter
                    attempts += 1
                    # Line 10: Log failure details
                    print(f"[Retry Warning] {func.__name__} failed attempt {attempts}/{max_attempts}: {exc}")
                    # Line 11: If max attempts exhausted, re-raise original exception
                    if attempts >= max_attempts:
                        raise
                    # Line 12: Sleep before retrying
                    time.sleep(delay_seconds)
        # Line 13: Return configured wrapper function
        return wrapper
    # Line 14: Return decorator
    return decorator

# Line 15: Define a closure demonstrating the nonlocal keyword
def create_rate_limiter(max_tokens=5):
    # Line 16: Free variable stored in enclosing scope
    tokens = max_tokens
    
    # Line 17: Inner function forming closure
    def consume():
        # Line 18: Declare nonlocal to mutate tokens in the enclosing scope
        nonlocal tokens
        # Line 19: Check token availability
        if tokens > 0:
            tokens -= 1
            return True, f"Success. Remaining tokens: {tokens}"
        # Line 20: Reject when exhausted
        return False, "Rate limit exceeded! Try again later."
    
    # Line 21: Return closure function
    return consume

# Line 22: Apply the retry decorator to an unstable network simulation function
@retry(max_attempts=3, delay_seconds=0.05)
def fetch_payment_status(transaction_id):
    # Line 23: Simulated counter to demonstrate recovery on attempt 2
    fetch_payment_status.counter = getattr(fetch_payment_status, 'counter', 0) + 1
    if fetch_payment_status.counter < 2:
        # Line 24: Simulate transient network glitch
        raise ConnectionResetError("Connection dropped by payment gateway")
    # Line 25: Return successful response
    return {"txn_id": transaction_id, "status": "SUCCESS"}

# Line 26: Test the retry decorator in action
print("Executing decorated network call:")
response = fetch_payment_status("TXN_99881")
print("Final Response:", response)
# Line 27: Verify original metadata was preserved by @functools.wraps
print("Preserved Function Name:", fetch_payment_status.__name__)  # 'fetch_payment_status'

# Line 28: Test the closure rate limiter
limiter = create_rate_limiter(max_tokens=2)
print(limiter())  # (True, 'Success. Remaining tokens: 1')
print(limiter())  # (True, 'Success. Remaining tokens: 0')
print(limiter())  # (False, 'Rate limit exceeded! Try again later.')
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do closures work in Python, and why is `@functools.wraps` critical when writing decorators?"
>
> **You:** "A closure occurs when an inner function references variables from its enclosing scope. When the outer function returns, Python packages those variables into `__closure__` cell objects so they outlive the outer function's execution frame. When building decorators, we wrap the target function inside a wrapper. If we omit `@functools.wraps(func)`, the decorated function's name becomes `wrapper` and its docstring is erased. In production systems, this breaks logging, tracing tools, and web frameworks like FastAPI that inspect function signatures to generate Swagger/OpenAPI documentation."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An enterprise microservice used a custom `@audit_log` decorator on all REST endpoints. Following a production upgrade, automated OpenTelemetry distributed tracing and endpoint monitoring stopped categorizing metrics by route name—all metrics collapsed under the name `wrapper`.
* **Task / Challenge:** Restore granular per-endpoint tracing without modifying hundreds of individual service methods.
* **Action Taken:** Inspected the `@audit_log` decorator implementation and found the developer had forgotten `@functools.wraps(func)`. Added `@functools.wraps(func)` to the decorator wrapper.
* **Result & Business Impact:** Restored individual endpoint metric reporting across 45 microservices within minutes, saving over 30 engineer-hours of debugging.
"""

PY_OOP_MRO = """# Python Object-Oriented Programming: Classes, Dunder Methods & MRO (C3 Linearization)

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - Class ek ghar ka **blueprint** hai, aur object us blueprint se bana **asli ghar**.
> - Dunder methods (`__init__`, `__str__`, `__len__`) Python ke secret magic switches hain: jab aap `len(my_obj)` likhte ho, Python parde ke peeche `my_obj.__len__()` ko call karta hai!
> - Multiple Inheritance & MRO: Jab ek bacha do mata-pita se ek jaisi aadat inherit karta hai, toh rulebook (C3 Linearization) tay karti hai ki pehle kiska tareeqa chalega!
>
> **Real-World Analogy:** A smartphone operating system. The base class is a phone (calls, SMS). A camera phone inherits both Phone and DigitalCamera. If both define `take_snapshot()`, the OS uses an unambiguous priority list (Method Resolution Order) so there is zero confusion about which camera lens driver activates.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **`__init__` vs `__new__`**:
  - `__new__`: The actual constructor that allocates the new object instance in memory (rarely overridden except in singletons or immutable subclasses).
  - `__init__`: The initializer that populates instance attributes on `self`.
- **Method Types**:
  - **Instance Method**: Takes `self`, can read and modify instance state.
  - **Class Method (`@classmethod`)**: Takes `cls`, can modify class state across all instances or serve as alternative factory constructors.
  - **Static Method (`@staticmethod`)**: Takes neither `self` nor `cls`, isolated utility function living in class namespace.
- **`@property`**: Allows calling a method using attribute access syntax (`user.full_name` instead of `user.full_name()`), enabling encapsulation and validation.

### 🧓 What an Experienced Candidate Knows:
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
> **Interviewer:** "How does Python solve the diamond inheritance problem, and what does `super()` actually do?"
>
> **You:** "Python resolves multiple inheritance using the C3 Linearization algorithm to compute a deterministic Method Resolution Order (MRO), accessible via `ClassName.mro()`. C3 ensures three things: children always precede parents, original parent declaration order is respected, and no class is visited twice. Crucially, `super()` does not call the direct base class; it calls the next class in the computed MRO chain. When all classes in an inheritance hierarchy use `super()` cooperatively, every class in the diamond is visited exactly once in clean linear order."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** In an asynchronous distributed worker framework, task classes inherited from both `LoggingMixin` and `RetryMixin`. During a major outage, retry attempts triggered unhandled infinite recursion exceptions, crashing worker pods.
* **Task / Challenge:** Diagnose why retrying tasks resulted in `RecursionError: maximum recursion depth exceeded`.
* **Action Taken:** Inspected the inheritance hierarchy using `TaskClass.mro()`. Found that `RetryMixin` called `super().__init__()` with explicit hardcoded arguments while `LoggingMixin` did not call `super()` at all, breaking the cooperative chain. Refactored both mixins to take `*args, **kwargs` and pass them to `super().__init__(*args, **kwargs)`.
* **Result & Business Impact:** Restored clean cooperative multiple inheritance across 60 worker nodes, preventing task queue deadlocks.
"""

PY_GENERATORS_CONTEXT_MANAGERS = """# Python Generators, Iterators & Context Managers Masterclass

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - Regular List: Ek saath 100 samosa mangwa kar table par rakh dena (Bahut saari jagah/memory gher lega, chahe aap 1 hi khao!).
> - Generator (`yield`): Ek chef jo counter par khada hai—aap bolte ho "Next!", toh wo ek garam samosa nikaal kar deta hai aur wait karta hai (Memory bachti hai kyunki ek time par ek hi item banta hai).
> - Context Manager (`with`): Ek automated automatic door jisme ghuste hi light on hoti hai (`__enter__`) aur bahar nikalte hi light off ho jati hai (`__exit__`), chahe andar kitna bhi hungama (exception) kyun na hua ho!
>
> **Real-World Analogy:** Netflix video streaming vs downloading a 4K Blu-ray movie. A list downloads the entire 50GB file onto your hard drive before playing. A generator streams 2-second chunks one by one in real-time, using just a few megabytes of RAM.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Iterable vs Iterator**:
  - **Iterable**: Any object that implements `__iter__()` or `__getitem__()` (e.g., list, tuple, string).
  - **Iterator**: An object representing a stream of data that implements `__next__()` and `__iter__()`. Calling `next(it)` returns the next item until it raises `StopIteration`.
- **Generators & `yield`**:
  - A function containing `yield` is a **Generator Function**.
  - Calling it returns a **Generator Iterator** without executing the function body immediately.
  - When `next()` is called, execution proceeds until the `yield` statement, which pauses the function and preserves its local stack frame!
- **Context Managers (`with` statement)**:
  - Automates resource allocation and deallocation (closing files, releasing locks, closing database connections).
  - Implements `__enter__()` (sets up resource) and `__exit__(exc_type, exc_val, exc_tb)` (tears down resource even if an unhandled exception occurred).

### 🧓 What an Experienced Candidate Knows:
- **Memory Consumption Benchmarking**: Generating 10,000,000 integers with a list comprehension consumes ~800MB of RAM. Generating the same 10,000,000 integers with a generator expression `(x for x in range(10_000_000))` consumes **112 bytes**!
- **Generator Advanced Methods**:
  - `gen.send(value)`: Passes data into the generator, resuming it and setting the result of the `yield` expression.
  - `gen.throw(type, val)`: Raises an exception at the suspension point inside the generator.
  - `gen.close()`: Raises `GeneratorExit` inside the generator to trigger cleanup.
- **Suppressing Exceptions in `__exit__`**: If `__exit__` returns `True`, Python suppresses the exception; if it returns `False` or `None`, the exception bubbles up normally.

---

## 3. 📊 Visual Architecture Diagram

```text
Generator Suspension & Resume Lifecycle:

   Caller                       Generator Function (with yield)
     │                                     │
     ├── 1. gen = stream_data() ──────────>│ (Suspended at entry point; 0 bytes consumed)
     │                                     │
     ├── 2. item = next(gen) ─────────────>│ Runs code until yield item1
     │<── Returns item1 ───────────────────┤ (Pauses execution; retains stack frame!)
     │                                     │
     ├── 3. item = next(gen) ─────────────>│ Resumes immediately after previous yield
     │<── Returns item2 ───────────────────┤ Runs until yield item2, then pauses again!
     │                                     │
     ├── 4. item = next(gen) ─────────────>│ Reaches end of function
     │<── Raises StopIteration ────────────┤
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```python
# Line 1: Import contextmanager utility from standard library
from contextlib import contextmanager
# Line 2: Import sys to measure object memory footprint
import sys
# Line 3: Import time for simulated timing
import time

# Line 4: Generator function to stream large numbers lazily
def infinite_fibonacci():
    # Line 5: Initial fibonacci states
    a, b = 0, 1
    # Line 6: Infinite loop produces numbers on-demand without unbounded memory growth
    while True:
        # Line 7: yield pauses execution and returns current value
        yield a
        # Line 8: State progression upon next() invocation
        a, b = b, a + b

# Line 9: Industrial Class-Based Context Manager for Database Transactions
class DatabaseTransaction:
    def __init__(self, connection_name):
        self.connection_name = connection_name

    # Line 10: __enter__ executes when entering the 'with' block
    def __enter__(self):
        print(f"[{self.connection_name}] BEGIN TRANSACTION (Acquired Lock)")
        return self

    # Line 11: __exit__ executes upon leaving 'with', handling exceptions
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Line 12: An exception occurred inside the with block: ROLLBACK
            print(f"[{self.connection_name}] ROLLBACK due to error: {exc_val}")
            # Line 13: Returning False allows exception to propagate to caller
            return False
        # Line 14: Clean exit with no errors: COMMIT
        print(f"[{self.connection_name}] COMMIT TRANSACTION (Released Lock)")
        return True

# Line 15: Functional Context Manager using @contextmanager decorator
@contextmanager
def execution_timer(label):
    # Line 16: Setup phase (before yield)
    start_time = time.perf_counter()
    print(f"[{label}] Timer started...")
    try:
        # Line 17: yield gives control back to the with-body block
        yield
    finally:
        # Line 18: Teardown phase (guaranteed to execute even on error)
        elapsed = (time.perf_counter() - start_time) * 1000
        print(f"[{label}] Finished in {elapsed:.2f} ms")

# Line 19: Memory comparison: Generator Expression vs List Comprehension
list_mem = sys.getsizeof([x * 2 for x in range(100000)])
gen_mem = sys.getsizeof((x * 2 for x in range(100000)))
print(f"List Comprehension Memory: {list_mem:,} bytes")
print(f"Generator Expression Memory: {gen_mem:,} bytes (99.9% smaller!)")

# Line 20: Test lazy Fibonacci generator
fib = infinite_fibonacci()
first_six = [next(fib) for _ in range(6)]
print("First 6 Fibonacci Numbers:", first_six)  # [0, 1, 1, 2, 3, 5]

# Line 21: Test successful database transaction
with DatabaseTransaction("Production-DB") as tx:
    print("  -> Inserting user record...")

# Line 22: Test timing context manager
with execution_timer("Heavy Calculation"):
    total = sum(i * i for i in range(500000))
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do generators optimize memory, and how do context managers guarantee resource safety?"
>
> **You:** "Generators turn functions into stateful iterators using the `yield` keyword. Instead of allocating a multi-gigabyte collection in heap memory all at once, a generator produces one element at a time on-demand, consuming an $O(1)$ constant memory footprint regardless of dataset size. Context managers complement this by implementing the `__enter__` and `__exit__` dunder methods within the `with` statement. The runtime guarantees that `__exit__` is executed regardless of whether the block completes normally, hits a `return`, or throws an unhandled exception, completely eliminating file descriptor and connection pool leaks."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** An ETL data pipeline parsed 15GB daily CSV audit logs into memory using `csv.DictReader(open(file))`, calling `.read().splitlines()`. Whenever two files were processed concurrently, the Kubernetes worker pod ran out of memory and was killed with exit code 137 (`OOMKilled`).
* **Task / Challenge:** Process multi-gigabyte log files on constrained 512MB RAM worker containers without dropping events.
* **Action Taken:** Refactored the log ingestion to use a Python generator that yielded line-by-line using a streaming context manager `with open(filepath) as f: for line in f: yield parse(line)`.
* **Result & Business Impact:** Slashed container memory consumption from 15GB to 42MB (a 99.7% reduction), enabling 10 concurrent ingestion workers to run on a single low-cost node.
"""

PY_MEMORY_GC_GIL = """# Python Memory Management: Reference Counting, Cyclic GC & GIL Internals

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:**
> - Reference Counting: Har memory object ke gale mein ek counter laga hai. Jab bhi koi variable use point karta hai, counter +1 hota hai. Jab variable hat jata hai, counter -1 hota hai. Jaise hi counter 0 hua, CPython us object ko turant delete kar deta hai!
> - Cyclic Garbage Collector: Agar do dost ek doosre ka haath pakad ke khade ho jayein (Circular reference `a.b = b; b.a = a`), toh dono ka counter kabhi 0 nahi hoga. CPython ka cyclic GC periodic rounds laga kar aise isolated groups ko dhundh kar saaf karta hai.
> - GIL (Global Interpreter Lock): Ek restaurant kitchen mein ek hi Master Chef (One CPU thread executing bytecode at any instant) allowed hai, taaki do chef ek saath same recipe book (memory counters) mein overwrite na kar dein!
>
> **Real-World Analogy:** A library book checkout system. The library tracks how many active student cards have borrowed a book. When the active borrower count hits zero, the book is returned to the stacks. However, if two students hold books referencing each other and both leave school, an auditor (Cyclic GC) must periodically inspect the abandoned lockers.

---

## 2. 📌 Core Mechanics & Edge Cases (Newbie ➡️ Experienced)

### 👶 What a Newbie Needs to Understand:
- **Primary Memory Manager: Reference Counting**:
  - Every Python object header (`PyObject`) has a field called `ob_refcnt`.
  - When `ob_refcnt == 0`, memory is deallocated **immediately**.
  - Increment triggers: Assignment (`b = a`), passing as argument, storing in list/dict.
  - Decrement triggers: Variable goes out of scope, reassignment (`a = None`), `del a`, removal from container.
- **Secondary Memory Manager: Cyclic GC**:
  - Reference counting alone cannot detect **circular references** (`a.next = b; b.next = a`).
  - Python's `gc` module runs periodically in the background using a **generational algorithm** with 3 generations (Gen 0: new objects, Gen 1: survived 1 collection, Gen 2: long-lived objects).
- **The GIL (Global Interpreter Lock)**:
  - CPython's memory allocator is not thread-safe. To prevent race conditions on `ob_refcnt`, CPython uses a global mutex called the GIL.
  - **Crucial Takeaway**: Python multi-threading CANNOT execute Python bytecode on multiple CPU cores simultaneously.

### 🧓 What an Experienced Candidate Knows:
- **Concurrency Decision Matrix**:
  - **I/O-Bound Workloads** (Network requests, DB calls, Disk I/O): Use `asyncio` or `threading`. When a thread waits for I/O, it releases the GIL, allowing other threads to run.
  - **CPU-Bound Workloads** (Data crunching, Image processing, ML inference): Multi-threading is ineffective due to GIL contention! You MUST use `multiprocessing` (separate Python processes with independent GILs) or native C/Rust extensions (e.g. NumPy, PyO3).
- **Python 3.12/3.13 Free-Threaded Python (PEP 703)**: Modern Python is actively implementing optional free-threaded builds that remove the GIL via mimalloc thread-safe memory management and biased reference counting.

---

## 3. 📊 Visual Architecture Diagram

```text
CPython Memory Allocator Hierarchy & GIL Contention:

   [ Application Code: Python Bytecode ]
                │
                v
   ┌─────────────────────────────────────────┐
   │      Global Interpreter Lock (GIL)       │  <── Only 1 thread executes bytecode!
   └─────────────────────────────────────────┘
                │
                v
   ┌─────────────────────────────────────────┐
   │ PyObject Header: [ ob_refcnt | ob_type ]│
   └─────────────────────────────────────────┘
                │
       ┌────────┴────────┐
       │                 │
  ob_refcnt == 0?   Circular Reference?
       │                 │
       v                 v
  Immediate Free    Cyclic GC (Generations 0, 1, 2)
  via PyObject_Free via Mark-and-Sweep of container objects
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```python
# Line 1: Import sys module to inspect reference counts
import sys
# Line 2: Import gc module to inspect and control garbage collection
import gc

# Line 3: Create a test object
data = ["alpha", "beta", "gamma"]
# Line 4: Note: sys.getrefcount() temporarily increments count by 1 because it takes an argument!
print("Initial refcount:", sys.getrefcount(data))  # Typically 2 (variable + argument)

# Line 5: Add an additional reference
alias = data
print("Refcount after alias:", sys.getrefcount(data))  # 3

# Line 6: Remove alias
del alias
print("Refcount after deleting alias:", sys.getrefcount(data))  # 2

# Line 7: Demonstrate Circular Reference handling with Cyclic GC
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbor = None

    def __repr__(self):
        return f"Node({self.name})"

# Line 8: Disable automatic GC temporarily to prove circular reference persistence
gc.disable()

# Line 9: Create two nodes forming a circular reference
node_a = Node("A")
node_b = Node("B")
node_a.neighbor = node_b
node_b.neighbor = node_a

# Line 10: Delete local references
del node_a
del node_b

# Line 11: Even though local names are gone, objects remain trapped in heap memory due to circular refcount!
print("Is garbage collector active?:", gc.isenabled())  # False

# Line 12: Manually invoke cyclic garbage collector
unreachable_count = gc.collect()
# Line 13: GC successfully identifies and frees the orphaned circular cycle!
print(f"Cyclic GC collected {unreachable_count} unreachable circular objects!")

# Line 14: Re-enable automatic garbage collector
gc.enable()

# Line 15: Concurrency demonstration logic
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def cpu_intensive_task(n):
    # Line 16: Pure CPU calculation bound by the GIL in threads
    return sum(i * i for i in range(n))

# Line 17: For CPU bound tasks, ProcessPoolExecutor bypasses the GIL by spawning distinct OS processes
with ProcessPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(cpu_intensive_task, [1000000, 1000000]))
print("CPU Task completed across processes:", len(results))
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How does CPython manage memory, and why does Python have a Global Interpreter Lock?"
>
> **You:** "CPython manages memory primarily through Reference Counting, providing deterministic, immediate deallocation the moment an object's reference count drops to zero. To handle circular references that reference counting cannot resolve, CPython employs a generational cyclic garbage collector across three generations. The GIL was introduced because CPython's memory allocator and reference counters are not thread-safe. The GIL ensures only one OS thread executes Python bytecode at any moment, preventing race conditions. Therefore, for CPU-bound tasks, we scale horizontally using `multiprocessing`, while for I/O-bound tasks, we use `asyncio` or `threading` since threads release the GIL during I/O wait states."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** A real-time sports analytics API built with multithreading was designed to utilize an 8-core AWS EC2 instance to crunch live match physics. Under load, CPU utilization plateaued at exactly 12.5% (1 core) while latency tripled.
* **Task / Challenge:** Enable the calculation service to utilize all 8 CPU cores and achieve target 50ms calculation latency.
* **Action Taken:** Diagnosed that the calculation was purely mathematical and CPU-bound; multiple Python threads were thrashing on the GIL lock, resulting in lock contention overhead rather than parallelism. Migrated the task from `ThreadPoolExecutor` to `ProcessPoolExecutor` with pre-forked worker pools.
* **Result & Business Impact:** CPU utilization scaled across all 8 cores (reaching 96%), cutting average compute latency from 380ms to 42ms and sustaining 25,000 live match queries per second.
"""

print("Writing files...")
create_file(os.path.join(BASE_DIR, "02-javascript", "02_operators_control_flow_and_loops.md"), JS_OPERATORS_CONTROL_FLOW)
create_file(os.path.join(BASE_DIR, "02-javascript", "03_arrays_in_depth_methods_and_iteration.md"), JS_ARRAYS_IN_DEPTH)
create_file(os.path.join(BASE_DIR, "02-javascript", "04_objects_destructuring_rest_spread_and_cloning.md"), JS_OBJECTS_CLONING)

create_file(os.path.join(BASE_DIR, "08-backend-python-fastapi", "01_python_fundamentals_syntax_types_and_mutability.md"), PY_FUNDAMENTALS)
create_file(os.path.join(BASE_DIR, "08-backend-python-fastapi", "02_python_collections_lists_tuples_dicts_sets.md"), PY_COLLECTIONS)
create_file(os.path.join(BASE_DIR, "08-backend-python-fastapi", "03_python_functions_scopes_args_kwargs_and_decorators.md"), PY_FUNCTIONS_DECORATORS)
create_file(os.path.join(BASE_DIR, "08-backend-python-fastapi", "04_python_oop_classes_dunder_methods_and_mro.md"), PY_OOP_MRO)
create_file(os.path.join(BASE_DIR, "08-backend-python-fastapi", "05_python_generators_iterators_and_context_managers.md"), PY_GENERATORS_CONTEXT_MANAGERS)
create_file(os.path.join(BASE_DIR, "08-backend-python-fastapi", "06_python_memory_gc_gil_and_concurrency.md"), PY_MEMORY_GC_GIL)
