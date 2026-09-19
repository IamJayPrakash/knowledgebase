# JavaScript Master Interview Bank: Part 2 (Q21 - Q40)

## Closures, Lexical Scope, Execution Context & `this`

---

### Q21: What is an Execution Context in JavaScript, and what are its two phases?

**Answer:**
An **Execution Context** is an abstract environment created by the JavaScript engine to evaluate and execute code. Every execution context has two phases:

1. **Creation Phase (Memory Allocation):**
   - The engine creates the **Variable Environment** and **Lexical Environment**.
   - Hoisting occurs: variables (`var`) are registered and initialized to `undefined`; `let` and `const` are allocated in the TDZ; function declarations are stored in memory with their full definitions.
   - The scope chain is linked to its parent lexical environment.
   - The `this` binding is established.

2. **Execution Phase (Code Evaluation):**
   - The engine executes the code line by line from top to bottom.
   - Values are assigned to variables, functions are called, and expressions are evaluated.

---

### Q22: What is the Call Stack and how does a Stack Overflow occur?

**Answer:**

- The **Call Stack** is a Last-In, First-Out (LIFO) data structure that tracks active execution contexts.
- When a script runs, the **Global Execution Context (GEC)** is pushed onto the bottom of the stack.
- When a function is invoked, its **Function Execution Context (FEC)** is pushed onto the stack. When it returns, it is popped off.
- **Stack Overflow:** Occurs when the number of frames pushed onto the call stack exceeds the engine's allocated maximum stack size (typically ~10,000 frames in V8), commonly caused by infinite recursion without a base case.

```javascript
// Stack Overflow trigger:
function recurse() {
  recurse(); // RangeError: Maximum call stack size exceeded
}
```

---

### Q23: What is a Closure and how is it implemented internally in the V8 engine?

**Answer:**

- A **Closure** is the combination of a function bundled together with references to its surrounding lexical state (the lexical environment). It gives an inner function access to an outer function's scope even after the outer function has returned.
- **V8 Engine Internals:**
  - V8 parses function scopes statically during compilation.
  - If an inner function references variables from an outer function, V8 allocates those variables on the **Heap** inside a special internal `Context` object instead of discarding them on stack frame exit.
  - The inner function retains a hidden internal slot `[[Scopes]]` pointing to this Heap `Context`.

```javascript
function createCounter() {
  let count = 0; // Allocated in Heap Context, not stack!
  return function() {
    count++;
    return count;
  };
}

const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

---

### Q24: How do you solve the classic `for (var i = 0; i < 5; i++) setTimeout` problem? Explain all 3 solutions

**Answer:**

```javascript
for (var i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100);
}
// Outputs: 5, 5, 5, 5, 5
```

**Why:** `var` is function-scoped. There is only one shared variable `i`. By the time the macrotask callbacks run after 100ms, the loop has completed and `i === 5`.

**Solution 1: Block Scope with `let` (Modern Standard)**

```javascript
for (let i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100); // Outputs: 0, 1, 2, 3, 4
}
// 'let' creates a new lexical binding per loop iteration!
```

**Solution 2: IIFE (Immediately Invoked Function Expression - ES5)**

```javascript
for (var i = 0; i < 5; i++) {
  (function(j) {
    setTimeout(() => console.log(j), 100);
  })(i);
}
```

**Solution 3: Pass arguments directly to `setTimeout`**

```javascript
for (var i = 0; i < 5; i++) {
  setTimeout((val) => console.log(val), 100, i);
}
```

---

### Q25: What is Function Currying and why is it useful?

**Answer:**

- **Currying** is the mathematical technique of transforming a function that takes multiple arguments into a sequence of nested unary functions that each take a single argument: $f(a, b, c) \to f(a)(b)(c)$.
- **Benefits:**
  1. Higher code reusability via **Partial Application**.
  2. Function composition and point-free style in functional programming pipelines.

```javascript
// Generic auto-currying function:
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...nextArgs) {
      return curried.apply(this, args.concat(nextArgs));
    };
  };
}

function multiply(a, b, c) {
  return a * b * c;
}

const curriedMultiply = curry(multiply);
const doubleAndTriple = curriedMultiply(2)(3);
console.log(doubleAndTriple(5)); // 30
```

---

### Q26: Implement a generic `memoize` function using Closures and Map

**Answer:**

```javascript
function memoize(fn) {
  const cache = new Map();

  return function(...args) {
    // Generate cache key (JSON stringify or Map key)
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key); // O(1) Cache hit
    }

    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const expensiveFib = memoize((n) => {
  if (n <= 1) return n;
  return expensiveFib(n - 1) + expensiveFib(n - 2);
});

console.log(expensiveFib(40)); // Fast calculation without redundant branches
```

---

### Q27: How is `this` determined in JavaScript? List the 4 binding rules in order of precedence

**Answer:**
The value of `this` is not fixed; it is evaluated at **call-site** invocation time according to 4 precedence rules:

1. **`new` Binding (Highest Precedence):**  
   If called with `new Foo()`, `this` binds to the newly allocated object instance.
2. **Explicit Binding:**  
   If called with `.call(context)`, `.apply(context)`, or `.bind(context)`, `this` binds explicitly to `context`.
3. **Implicit Binding:**  
   If called as a method of an object (`obj.method()`), `this` binds to the owning object (`obj`).
4. **Default Binding (Lowest Precedence):**  
   Standalone function call (`fn()`). In strict mode (`"use strict"`), `this` is `undefined`. In non-strict mode, `this` refers to the global object (`window` or `global`).

*Special Exception:* **Arrow Functions** do NOT have their own `this`. They capture `this` lexically from their enclosing scope at definition time.

---

### Q28: What are the differences between `call()`, `apply()`, and `bind()`?

**Answer:**

- **`call(thisArg, arg1, arg2, ...)`**: Invokes the function immediately with `this` bound to `thisArg` and arguments passed individually as a comma-separated list.
- **`apply(thisArg, [argsArray])`**: Invokes the function immediately with `this` bound to `thisArg` and arguments passed as an array-like collection.
- **`bind(thisArg, arg1, ...)`**: Does **not** invoke the function immediately. Instead, it returns a new bound function with `this` permanently set to `thisArg` and optional pre-configured preset arguments.

```javascript
function greet(greeting, punctuation) {
  return `${greeting}, ${this.name}${punctuation}`;
}
const person = { name: "Sarah" };

console.log(greet.call(person, "Hello", "!"));       // "Hello, Sarah!"
console.log(greet.apply(person, ["Hi", "?"]));       // "Hi, Sarah?"
const boundGreet = greet.bind(person, "Hey");
console.log(boundGreet("."));                        // "Hey, Sarah."
```

---

### Q29: Can you re-bind a function created with `.bind()`?

**Answer:**
**No.** A hard-bound function returned by `.bind()` cannot be changed with a subsequent `.bind()`, `.call()`, or `.apply()`.
Under the hood, `bind()` wraps the target function in an internal wrapper closure:

```javascript
// Simplified polyfill of bind:
Function.prototype.myBind = function(context, ...args) {
  const originalFn = this;
  return function(...innerArgs) {
    return originalFn.apply(context, [...args, ...innerArgs]);
  };
};
```

Because `context` is permanently stored in the closure of the returned wrapper, subsequent calls to `.call()` only bind `this` on the outer wrapper, which ignores it and delegates to `originalFn.apply(context)`.

---

### Q30: Why do Arrow Functions not have their own `this`, `arguments`, or `prototype`?

**Answer:**

- Arrow functions were introduced in ES6 primarily for lightweight inline functional programming and callbacks.
- **`this`:** Evaluated lexically from the outer scope, preventing the common bug where callbacks inside `setTimeout` or event listeners unexpectedly rebound `this` to `window` or the DOM node.
- **`arguments`:** Arrow functions do not bind an `arguments` object; use standard ES6 `...rest` parameters instead.
- **No `prototype` / cannot be a constructor:** Arrow functions lack internal `[[Construct]]` method; calling `new ArrowFn()` throws `TypeError: ArrowFn is not a constructor`.

---

### Q31: What is the difference between Function Declarations and Function Expressions?

**Answer:**

- **Function Declaration:**  
  `function foo() {}` is hoisted completely into memory during the creation phase. It can be invoked before its line of appearance in source code.
- **Function Expression:**  
  `const foo = function() {}` assigns an anonymous (or named) function to a variable. The variable declaration is hoisted (into TDZ or `undefined` for `var`), but the function assignment occurs only during the execution phase. Calling it before assignment throws a `ReferenceError` (or `TypeError` for `var`).

---

### Q32: What is an IIFE (Immediately Invoked Function Expression) and why was it vital pre-ES6?

**Answer:**

- Syntax: `(function() { /* private scope */ })();`
- **Purpose:** Before ES6 introduced block-scoped `let` and `const` and ES modules, JavaScript only had function scope.
- Developers used IIFEs to create isolated private scopes (Module Pattern) to avoid polluting the global namespace and leaking variables across third-party scripts.

---

### Q33: How does Scope Chaining work when resolving identifiers?

**Answer:**

- Every Lexical Environment contains an **Environment Record** (local identifiers) and an **Outer Reference** (link to the parent lexical environment).
- When a variable is referenced, the JavaScript engine first checks the local environment record.
- If not found, it traverses up the parent lexical environment via `Outer Reference`.
- This traversal continues until it reaches the Global Scope. If the identifier is still not found in Global Scope, the engine throws `ReferenceError: identifier is not defined`.

---

### Q34: What are Common Sources of Memory Leaks in JavaScript Closures?

**Answer:**

1. **Accidental Global Variables:** Assigning to undeclared identifiers in non-strict mode leaks to the `window`/`global` root.
2. **Forgotten Timers & Intervals:** `setInterval` holding a closure referencing a large object prevents that object from being garbage-collected until `clearInterval()` is called.
3. **Detached DOM Elements retained in Closures:** Keeping references to removed DOM elements inside an event listener callback.
4. **Shared Scope Heap Retention:** In V8, all closures created inside the same parent function share the **same Context object**. If one closure retains a large object, another long-lived closure in that same function will unintentionally keep that large object alive in memory.

---

### Q35: Explain the "Accidental Shared Closure Context" leak in V8

**Answer:**

```javascript
let theThing = null;

function replaceThing() {
  const originalThing = theThing;
  const unused = function() {
    if (originalThing) console.log("hi");
  };

  // theThing gets a new object containing a huge array:
  theThing = {
    longStr: new Array(1000000).join("*"),
    someMethod: function() { /* closure */ }
  };
}
setInterval(replaceThing, 100);
```

**Why it leaks:** `someMethod` and `unused` share the same lexical scope context. Because `unused` references `originalThing`, the entire context keeps `originalThing` alive. Every 100ms, a linked list of old `theThing` objects grows indefinitely in memory until an Out-of-Memory crash occurs.

---

### Q36: What is a Pure Function and what are its properties?

**Answer:**
A function is **Pure** if it satisfies two strict criteria:

1. **Deterministic:** For the same input arguments, it always returns the exact same output.
2. **Zero Side Effects:** It does not mutate external state, modify input arguments, make I/O network requests, write to disk, or alter global variables.

- **Benefits:** Trivially easy to test, safely memoizable, and concurrency-safe.

---

### Q37: How do you implement a once-only (`once`) execution wrapper using Closures?

**Answer:**

```javascript
function once(fn) {
  let executed = false;
  let result;

  return function(...args) {
    if (!executed) {
      executed = true;
      result = fn.apply(this, args);
    }
    return result;
  };
}

const initDb = once((connectionStr) => {
  console.log("Database initialized:", connectionStr);
  return { connected: true };
});

initDb("postgres://localhost"); // Logs: "Database initialized..."
initDb("postgres://localhost"); // Returns cached result without logging
```

---

### Q38: What is Tail Call Optimization (TCO) and does JavaScript support it?

**Answer:**

- **Tail Call:** A subroutine call performed as the final action of a function.
- **Tail Call Optimization:** Reusing the current stack frame instead of allocating a new one when a function returns a tail call, enabling infinite recursion without stack overflow ($O(1)$ stack space).
- **JavaScript Status:** Specified in ES6 for strict mode (`"use strict"`), but **only Safari (WebKit)** implemented it. V8 (Chrome/Node.js) and SpiderMonkey (Firefox) dropped TCO support due to debugging difficulties (erased stack traces in Error objects) and performance edge-case penalties.

---

### Q39: What is Debouncing vs Throttling?

**Answer:**

- **Debounce:** Delays function execution until a specified delay has elapsed **since the last time** it was invoked. (Resets timer on each call).
  - *Use Case:* Search bar autocomplete input, window resize completion.
- **Throttle:** Guarantees that a function is executed **at most once** within a specified time window. (Does not reset timer).
  - *Use Case:* Infinite scroll detection (`window.onscroll`), game loop update ticks, drag-and-drop mouse move events.

---

### Q40: What happens if you call `delete obj.prop` vs `delete varName`?

**Answer:**

- `delete obj.prop`: Removes the own property `prop` from object `obj`. Returns `true` if successful or if the property did not exist. Returns `false` (or throws `TypeError` in strict mode) if the property is non-configurable (`configurable: false`).
- `delete varName`: Throws a `SyntaxError: Delete of an unqualified identifier in strict mode`. Variables declared with `var`, `let`, or `const` cannot be deleted because they are non-configurable properties on their respective scope environment records.
