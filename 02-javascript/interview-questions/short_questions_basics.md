# JavaScript Core Interview Questions (Quick Recall & High-Frequency)

---

## 1. What is the difference between `null`, `undefined`, and `undeclared`?

- **`undefined`**: A variable has been declared using `var`, `let`, or `const`, but has not been assigned a value. Also the default return value of functions that return nothing.
- **`null`**: An intentional assignment value representing "no object value" or empty state. `typeof null === 'object'` (historical JS bug).
- **`undeclared`**: An identifier that has never been declared in any reachable scope. Accessing it throws `ReferenceError: x is not defined`.

```javascript
let a;
console.log(a); // undefined
let b = null;
console.log(b); // null
// console.log(c); // ReferenceError: c is not defined (undeclared)
```

---

## 2. What is the difference between `==` and `===`?

- `==` (Loose equality) performs **Abstract Equality Comparison** with implicit type coercion (e.g. `'5' == 5` is `true`, `null == undefined` is `true`, `false == 0` is `true`).
- `===` (Strict equality) performs **Strict Equality Comparison** without type coercion. Types and values must both match (`'5' === 5` is `false`).

---

## 3. Explain `Object.freeze()` vs `Object.seal()`

- **`Object.freeze()`**:
  - Cannot add new properties.
  - Cannot remove existing properties.
  - Cannot modify values of existing properties (`writable: false`, `configurable: false`).
- **`Object.seal()`**:
  - Cannot add new properties.
  - Cannot remove existing properties (`configurable: false`).
  - **Can modify** values of existing properties if `writable: true`.
- *Note*: Both are shallow by default; nested objects can still be mutated unless recursively frozen.

---

## 4. What are JavaScript WeakMap and WeakSet, and why do they exist?

- In standard `Map` and `Set`, holding an object as a key or value creates a strong reference that prevents Garbage Collection.
- In `WeakMap` and `WeakSet`, keys must be objects (or non-registered symbols), and references are held **weakly**. If no other references to the key object exist, V8 garbage collects it automatically.
- They are not enumerable (no `.size`, no `.keys()`, no `.forEach()`) because garbage collection timing is non-deterministic.
- *Use case*: Storing private metadata or caching DOM element state without causing memory leaks when DOM elements are removed.

```javascript
// Memory leak prevention with WeakMap
const domMetadata = new WeakMap();

let button = document.createElement("button");
domMetadata.set(button, { clickCount: 0 });

// When button is removed from DOM and dereferenced:
button = null; 
// Memory is automatically collected during next GC cycle!
```

---

## 5. What is the difference between `function declaration` and `function expression`?

- **Function Declaration**: `function foo() {}` is hoisted completely along with its function definition. Can be invoked before its declaration in code.
- **Function Expression**: `const foo = function() {}` variable name is hoisted, but initialized as `undefined` (if `var`) or remains in TDZ (if `const`/`let`). Invoking before assignment throws `TypeError` or `ReferenceError`.
