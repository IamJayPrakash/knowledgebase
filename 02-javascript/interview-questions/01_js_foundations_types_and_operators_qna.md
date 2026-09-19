# JavaScript Master Interview Bank: Part 1 (Q1 - Q20)
## Foundations, Types, Coercion & Operators

---

### Q1: What are the primitive data types in JavaScript, and how are they stored in memory?
**Answer:**
JavaScript has **7 primitive data types**:
1. `number` (IEEE 754 64-bit float)
2. `string` (immutable sequence of UTF-16 code units)
3. `boolean` (`true` or `false`)
4. `undefined` (variable declared but not assigned a value)
5. `null` (intentional absence of any object value)
6. `symbol` (unique and immutable primitive identifier)
7. `bigint` (arbitrary-precision integer)

**Memory Layout:**
- Primitives are **immutable** and passed by **value**.
- Small primitive values (like numbers, booleans, small strings) are stored directly on the **Call Stack** (or in V8 Smi / small integer representations).
- Objects, Functions, and Arrays are **reference types** stored in the **V8 Heap**, with their memory addresses stored on the Call Stack.

```javascript
let a = 10;
let b = a; // b gets a copy of value 10
b = 20;
console.log(a); // 10 (unchanged)

let obj1 = { name: "Alice" };
let obj2 = obj1; // obj2 copies the reference pointer
obj2.name = "Bob";
console.log(obj1.name); // "Bob" (mutated via shared reference)
```

---

### Q2: Explain `typeof null === 'object'` and `typeof NaN === 'number'`. Why do these quirks exist?
**Answer:**
1. **`typeof null === 'object'`**:
   - In the first implementation of JavaScript (1995), values were stored with a type tag in the bottom 3 bits of their memory representation.
   - The type tag for an object was `000`.
   - The null pointer was represented as `0x00` (all zeros). Consequently, `typeof` inspected the bottom 3 bits, found `000`, and returned `"object"`.
   - This bug is preserved in the ECMAScript specification for backwards compatibility to prevent breaking legacy web code.

2. **`typeof NaN === 'number'`**:
   - `NaN` stands for "Not-a-Number", but according to IEEE 754 floating-point specification, `NaN` is a special numeric value indicating an invalid or unrepresentable arithmetic outcome (e.g., `0 / 0` or `Math.sqrt(-1)`).
   - Because it is technically part of the floating-point number set, its JavaScript type is `'number'`.

---

### Q3: What is the difference between `==` (Abstract Equality) and `===` (Strict Equality)?
**Answer:**
- **`===` (Strict Equality):** Evaluates equality **without** type coercion. If types differ, it returns `false` immediately.
- **`==` (Abstract Equality):** Follows the ECMAScript `Abstract Equality Comparison Algorithm` (ToNumber coercion):
  1. If comparing `number` and `string`, converts string to number: `1 == "1"` $\to$ `1 == 1` (`true`).
  2. If comparing `boolean` to anything, converts boolean to number: `true == "1"` $\to$ `1 == "1"` $\to$ `1 == 1` (`true`).
  3. `null == undefined` is explicitly defined as `true` (and neither equals any other value with `==`).
  4. If comparing `object` to primitive, calls `ToPrimitive(object, Number)` (`valueOf()`, then `toString()`).

```javascript
console.log([] == false); // true! [] -> "" -> 0, false -> 0, 0 == 0 is true
console.log([] == ![]);   // true! ![] is false -> [] == false -> 0 == 0
console.log(null == undefined); // true
console.log(null === undefined); // false
```

---

### Q4: How does `Object.is()` differ from `===`?
**Answer:**
`Object.is(val1, val2)` implements the SameValue algorithm and differs from `===` in exactly two special edge cases:
1. **`NaN` comparison:**
   - `NaN === NaN` is `false` (by IEEE 754 rules).
   - `Object.is(NaN, NaN)` is `true`.
2. **Signed Zero (`+0` vs `-0`):**
   - `+0 === -0` is `true`.
   - `Object.is(+0, -0)` is `false`.

```javascript
console.log(NaN === NaN);            // false
console.log(Object.is(NaN, NaN));   // true

console.log(+0 === -0);             // true
console.log(Object.is(+0, -0));     // false
console.log(1 / +0);                // Infinity
console.log(1 / -0);                // -Infinity
```

---

### Q5: What is the Temporal Dead Zone (TDZ) and why was it introduced for `let` and `const`?
**Answer:**
- When JavaScript enters a scope, all variables (`var`, `let`, `const`, `function`) are **hoisted** (registered during the creation phase of the Execution Context).
- `var` is initialized immediately to `undefined`.
- `let` and `const` are hoisted into uninitialized memory. The time interval between entering the block scope and reaching the variable's declaration line is called the **Temporal Dead Zone (TDZ)**.
- Accessing a variable in its TDZ throws a runtime `ReferenceError: Cannot access 'x' before initialization`.
- **Why introduced:** To eliminate silent bugs where variables are accessed before assignment, and to ensure `const` can never be observed in an uninitialized or mutated state.

```javascript
{
  // TDZ for myVar begins here
  // console.log(myVar); // ReferenceError: Cannot access 'myVar' before initialization
  let myVar = 42; // TDZ ends here
  console.log(myVar); // 42
}
```

---

### Q6: What is the difference between `null`, `undefined`, and `undeclared`?
**Answer:**
- **`undefined`**: A variable has been declared using `var`, `let`, or `const`, but has not yet been assigned a value. Also default return value of functions without an explicit `return`.
- **`null`**: An intentional primitive assignment representing the deliberate absence of an object value or empty reference.
- **`undeclared`**: An identifier that was never declared in any enclosing scope. Accessing it directly throws `ReferenceError: x is not defined`.

```javascript
let a;
console.log(a); // undefined
let b = null;
console.log(b); // null
console.log(typeof notDeclared); // "undefined" (typeof guard), but notDeclared throws ReferenceError
```

---

### Q7: Explain Nullish Coalescing (`??`) vs Logical OR (`||`).
**Answer:**
- **Logical OR (`||`):** Returns the right-hand operand if the left-hand operand is **any falsy value** (`false`, `0`, `""`, `NaN`, `null`, `undefined`).
- **Nullish Coalescing (`??`):** Returns the right-hand operand **only if** the left-hand operand is **nullish** (`null` or `undefined`).

```javascript
const count = 0;
const defaultCount1 = count || 10; // 10 (BUG: 0 is valid but falsy!)
const defaultCount2 = count ?? 10; // 0  (CORRECT: 0 is not null or undefined)

const text = "";
console.log(text || "Default"); // "Default"
console.log(text ?? "Default"); // ""
```

---

### Q8: How does Optional Chaining (`?.`) work under the hood?
**Answer:**
- `?.` evaluates the expression on its left. If the left-hand value is `null` or `undefined`, execution **short-circuits** and immediately returns `undefined` without attempting property access or method invocation.
- It prevents `TypeError: Cannot read properties of undefined (reading 'xyz')`.
- Works with properties (`obj?.a`), arrays (`arr?.[0]`), and function calls (`fn?.()`).

```javascript
const user = { profile: null };
console.log(user.profile?.avatar?.url); // undefined (no TypeError)
console.log(user.getSettings?.());       // undefined (does not crash)
```

---

### Q9: How do `for...in` and `for...of` differ?
**Answer:**
- **`for...in`:** Iterates over all **enumerable property keys** of an object, including properties inherited across its prototype chain. Iteration order is not guaranteed.
- **`for...of`:** Iterates over the **values** of an **iterable object** (objects implementing the `[Symbol.iterator]` protocol: `Array`, `Map`, `Set`, `String`, `TypedArray`, generator objects). Cannot be used on plain objects without `Object.keys()`/`Object.values()`.

```javascript
const arr = ["a", "b", "c"];
arr.customProp = "hello";

for (let key in arr) {
  console.log(key); // "0", "1", "2", "customProp" (indexes + properties)
}

for (let value of arr) {
  console.log(value); // "a", "b", "c" (only iterable elements)
}
```

---

### Q10: What is variable shadowing and how can it lead to bugs?
**Answer:**
- Variable shadowing occurs when a variable declared within an inner scope has the same identifier name as a variable in an outer scope.
- Within the inner scope, the inner identifier shadows (masks) the outer one, making the outer variable inaccessible by name.
- **Bug Vector:** Accidental re-declaration inside loops or nested closures leading to updates targeting the local copy instead of the intended parent state.

```javascript
let total = 100;

function calculateDiscount(items) {
  let total = 0; // Shadows outer 'total'
  items.forEach(item => { total += item.price; });
  return total;
}
calculateDiscount([{ price: 20 }]);
console.log(total); // 100 (outer total untouched)
```

---

### Q11: Explain implicit type coercion in arithmetic operations (`+`, `-`, `*`, `/`).
**Answer:**
- The binary `+` operator performs **string concatenation** if *either* operand is a string. Otherwise, it converts operands to numbers.
- The operators `-`, `*`, `/`, `%` **always** coerce both operands to numeric primitives via `Number()`.

```javascript
console.log(1 + "2");    // "12" (string concatenation)
console.log("6" - 2);    // 4    (coerced to 6 - 2)
console.log("4" * "5");  // 20   (coerced to 4 * 5)
console.log("10" / "2"); // 5    (coerced to 10 / 2)
console.log(true + 1);   // 2    (true coerced to 1)
console.log(false + 1);  // 1    (false coerced to 0)
console.log([] + {});    // "[object Object]" ([] -> "", {} -> "[object Object]")
```

---

### Q12: What is the difference between `freeze()`, `seal()`, and `preventExtensions()` on objects?
**Answer:**
| Method | Can Add Properties? | Can Delete Properties? | Can Modify Existing Values? | Changes Configurable? |
| :--- | :--- | :--- | :--- | :--- |
| `Object.preventExtensions(obj)` | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| `Object.seal(obj)` | ❌ No | ❌ No | ✅ Yes | ❌ No (`configurable: false`) |
| `Object.freeze(obj)` | ❌ No | ❌ No | ❌ No (`writable: false`) | ❌ No (`configurable: false`) |

*Note: All three are shallow by default. Nested objects remain mutable unless deeply frozen.*

---

### Q13: What is the difference between shallow copy and deep copy?
**Answer:**
- **Shallow Copy:** Copies top-level primitive values by value, but copies references for nested objects and arrays. Changes to nested properties in the clone mutate the original.
  - *Examples:* `Object.assign({}, obj)`, spread `{ ...obj }`, `slice()`.
- **Deep Copy:** Recursively duplicates all objects and arrays at all nesting depths, allocating completely independent heap memory.
  - *Native Solution:* `structuredClone(obj)` (supports Circular References, Dates, Maps, Sets, TypedArrays).
  - *Legacy JSON Trick:* `JSON.parse(JSON.stringify(obj))` (Fails on `undefined`, `Symbol`, `Function`, `Date` converted to string, crashes on Circular References).

---

### Q14: How does `structuredClone()` work and what are its limitations?
**Answer:**
- `structuredClone()` is the modern browser/Node.js standard implementing the HTML Structured Clone Algorithm.
- **Capabilities:** Deep clones nested objects, arrays, `Map`, `Set`, `Date`, `RegExp`, `ArrayBuffer`, and safely preserves **circular references**.
- **Limitations:** Cannot clone functions, DOM nodes, Property Descriptors (`getters`/`setters`), or Prototype chains (reconstructed objects always inherit from `Object.prototype`).

```javascript
const original = {
  set: new Set([1, 2, 3]),
  date: new Date(),
};
original.self = original; // Circular reference

const copy = structuredClone(original);
console.log(copy.self === copy); // true (circularity preserved!)
console.log(copy.set !== original.set); // true (independent instance)
```

---

### Q15: What are Symbols in JavaScript and what are their primary use cases?
**Answer:**
- `Symbol()` produces a unique, immutable primitive identifier. Even if two symbols are created with the same description, `Symbol("foo") === Symbol("foo")` is `false`.
- **Primary Use Cases:**
  1. **Hidden Object Properties:** Properties keyed by Symbols are non-enumerable in standard `for...in` loops and `Object.keys()`, preventing naming collisions in libraries.
  2. **Well-Known Symbols (Metaprogramming):** Internal engine hooks such as `Symbol.iterator`, `Symbol.hasInstance`, `Symbol.toPrimitive`, `Symbol.asyncIterator`.

```javascript
const ID = Symbol("id");
const user = {
  name: "Bob",
  [ID]: "SECRET_123"
};

console.log(Object.keys(user)); // ["name"] (ID omitted)
console.log(user[ID]);           // "SECRET_123"
```

---

### Q16: What is the difference between `Map` and a Plain Object?
**Answer:**
| Feature | `Map` | Plain Object (`{}`) |
| :--- | :--- | :--- |
| **Key Types** | Any type (objects, functions, primitives). | Strings and Symbols only. |
| **Key Ordering** | Strictly maintains insertion order. | Integer keys sorted first, followed by insertion order. |
| **Size Determination** | Instant $O(1)$ via `.size`. | $O(N)$ via `Object.keys(obj).length`. |
| **Default Keys** | Contains zero default keys when created. | Inherits prototype keys (`toString`, `constructor`) unless created with `Object.create(null)`. |
| **Performance** | Optimized for frequent addition and deletion of key-value pairs. | Optimized for static property access. |

---

### Q17: What is `WeakMap` and why does it not prevent Garbage Collection?
**Answer:**
- `WeakMap` is a collection of key-value pairs where **keys must be objects** (or non-registered symbols) and are held as **weak references**.
- Because the reference is weak, if there are no other strong references to a key object elsewhere in memory, the V8 garbage collector reclaims the object and silently deletes the key-value entry.
- **Characteristics:** Non-enumerable (no `.size`, `.keys()`, or iteration) because GC timing is non-deterministic.
- **Use Case:** Private data storage for classes, DOM node metadata caching without memory leaks.

```javascript
let element = document.getElementById("button");
const metadata = new WeakMap();

metadata.set(element, { clicks: 0 });

// If element is removed from DOM and dereferenced:
element.remove();
element = null;
// The entry in metadata is automatically garbage collected!
```

---

### Q18: What is `WeakSet` and how is it used?
**Answer:**
- `WeakSet` stores unique objects weakly without preventing garbage collection.
- Only supports `.add()`, `.has()`, `.delete()`.
- **Use Case:** Tagging objects with a boolean state without modifying the object or causing memory leaks (e.g., tracking which objects have already been processed or validated).

```javascript
const processedTasks = new WeakSet();

function processTask(task) {
  if (processedTasks.has(task)) {
    throw new Error("Task already processed!");
  }
  processedTasks.add(task);
  // Execute task...
}
```

---

### Q19: Explain the difference between `Array.prototype.slice()` and `Array.prototype.splice()`.
**Answer:**
- **`slice(start, end)`**:
  - **Pure/Non-mutating:** Does not alter the original array.
  - Returns a shallow copy of a sub-array from index `start` up to (but not including) `end`.
- **`splice(start, deleteCount, ...itemsToAdd)`**:
  - **Impure/Mutating:** Modifies the original array directly in place.
  - Deletes `deleteCount` elements starting at index `start` and inserts new items at that position.
  - Returns an array containing the deleted elements.

```javascript
const list = [1, 2, 3, 4, 5];

const sliced = list.slice(1, 3);
console.log(sliced); // [2, 3]
console.log(list);   // [1, 2, 3, 4, 5] (original unchanged)

const spliced = list.splice(1, 2, 99);
console.log(spliced); // [2, 3] (deleted elements)
console.log(list);    // [1, 99, 4, 5] (original modified!)
```

---

### Q20: What are Tagged Template Literals and how are they used in modern libraries?
**Answer:**
- Tagged Template Literals allow parsing template literals with a function.
- The tag function receives an array of static string chunks as its first parameter, followed by the evaluated interpolation expressions as subsequent arguments.
- **Used by:** `styled-components` (CSS parsing), SQL query sanitizers (escaping SQL injection parameters), and GraphQL AST parsers (`gql` tags).

```javascript
function highlight(strings, ...values) {
  return strings.reduce((acc, str, i) => {
    const val = values[i] !== undefined ? `<mark>${values[i]}</mark>` : "";
    return acc + str + val;
  }, "");
}

const user = "Alex";
const role = "Admin";
const html = highlight`User ${user} has role ${role}.`;
console.log(html); 
// "User <mark>Alex</mark> has role <mark>Admin</mark>."
```
