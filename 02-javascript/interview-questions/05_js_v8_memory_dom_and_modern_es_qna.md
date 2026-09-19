# JavaScript Master Interview Bank: Part 5 (Q81 - Q100)

## V8 Internals, Memory Management, DOM & Modern ECMAScript

---

### Q81: Explain the V8 Engine architecture: Ignition vs TurboFan

**Answer:**

```
JavaScript Source Code
          │
          ▼
      [ Parser ] ──► Abstract Syntax Tree (AST)
          │
          ▼
   [ Ignition Interpreter ] ──► Executes Bytecode immediately (low startup latency)
          │
          ├─► Profiler (Type feedback collection: "Hot Functions")
          │
          ▼
   [ TurboFan Optimizing Compiler ] ──► Machine Code (JIT compilation for peak performance)
          │
          └─► [ Deoptimization Bailout ] ──► If types change, reverts to Ignition Bytecode!
```

1. **Ignition (Bytecode Interpreter):** Quickly parses AST into compact bytecode. Starts executing immediately to minimize page load time and memory usage.
2. **TurboFan (Optimizing Compiler):** Monitors "hot" functions that execute repeatedly. Based on observed types, TurboFan compiles bytecode directly into highly optimized machine code.
3. **Deoptimization:** If an assumed type changes (e.g., passing a string into an optimized math function), TurboFan bails out and deoptimizes back to Ignition bytecode.

---

### Q82: What are Hidden Classes (Shapes) and Inline Caches (IC) in V8?

**Answer:**

- **Hidden Classes (Shapes/Maps):** In dynamic languages like JavaScript, object properties can be added at runtime. V8 assigns an internal hidden class to every object. Objects with the same property order share the same hidden class.
- **Inline Caching (IC):** V8 caches property memory offsets directly in machine code. If subsequent objects share the identical Hidden Class, property lookup is an instant single memory read.
- **Optimization Tip:** Always initialize object properties in the exact same order and avoid deleting properties with `delete` (use `null` or `undefined` instead), which transitions the object into slow dictionary mode.

```javascript
// ✅ FAST: Shares same Hidden Class (M0 -> M1 -> M2)
const p1 = {}; p1.x = 1; p1.y = 2;
const p2 = {}; p2.x = 3; p2.y = 4;

// ❌ SLOW: Creates diverging Hidden Classes!
const p3 = {}; p3.y = 1; p3.x = 2;
```

---

### Q83: How does Garbage Collection work in V8 (Generational Garbage Collection)?

**Answer:**
V8 uses **Generational Garbage Collection** based on the Weak Generational Hypothesis (most objects die young):

1. **Young Generation (New Space):**
   - Sized between 1MB and 64MB. Divided into two semi-spaces: **From Space** and **To Space**.
   - Collected frequently via **Scavenge algorithm (Cheney's Copying Algorithm)**: Active objects are copied to "To Space", and dead memory is wiped instantly in a fast contiguous sweep.
   - Objects surviving two scavenge cycles are **promoted** to Old Space.

2. **Old Generation (Old Space):**
   - Holds long-lived objects.
   - Collected using **Mark-Sweep-Compact**:
     - *Marking:* Traverses GC roots and marks reachable objects.
     - *Sweeping:* Adds dead object addresses to a free-list.
     - *Compacting:* Defragments memory by shifting live objects together.
   - Runs concurrently and incrementally to avoid stopping the main thread.

---

### Q84: What are GC Roots in JavaScript?

**Answer:**
A **GC Root** is an anchor object that is considered unconditionally reachable:

1. Active local variables and function parameters on the Call Stack.
2. The Global Object (`window` in browsers, `global` in Node.js).
3. DOM trees attached to the document.
4. Built-in system classes and active closures referenced by active execution contexts.

*If an object in the heap cannot be reached via any reference path from any GC Root, it is eligible for garbage collection.*

---

### Q85: What are Detached DOM Tree leaks and how do you diagnose them?

**Answer:**

- A **Detached DOM Node** occurs when an HTML element is removed from the DOM tree (`element.remove()` or `parent.removeChild()`), but a JavaScript variable or event listener closure continues to hold a reference to that element or any of its child nodes.
- **Diagnosis:**
  1. Open Chrome DevTools $\to$ **Memory** tab.
  2. Take a **Heap Snapshot**.
  3. Filter class names by `"Detached"`.
  4. Expand `Detached HTMLDivElement` and inspect the **Retainers** tree to locate the JavaScript closure holding the reference.

---

### Q86: Explain Event Propagation: Capturing vs Target vs Bubbling phases

**Answer:**

```
           DOCUMENT
              │   ▲
  1. CAPTURING│   │ 3. BUBBLING
     PHASE    │   │    PHASE
              ▼   │
           <div> Element
              │   ▲
              ▼   │
           <button> Element (2. TARGET PHASE)
```

1. **Capturing Phase (Trickling):** Event travels down from `Window` $\to$ `Document` $\to$ `Body` down to the target element's parent. (Triggered if `addEventListener(..., true)` or `{ capture: true }`).
2. **Target Phase:** Event reaches the actual node on which the user clicked/interacted.
3. **Bubbling Phase (Default):** Event bubbles back up from the target node through its ancestors back to `Window`. (Triggered if `addEventListener(..., false)`).

---

### Q87: What is Event Delegation and why is it superior for dynamic lists?

**Answer:**

- **Event Delegation:** Attaching a single event listener to a common parent element instead of attaching separate listeners to every individual child item.
- It leverages **Event Bubbling**. When a child item is clicked, the event bubbles up to the parent, where `event.target` identifies the specific child.
- **Benefits:**
  1. Drastically reduces memory usage (1 listener vs 10,000 listeners).
  2. Works automatically for dynamically added or deleted children without re-binding.

```javascript
document.getElementById("todo-list").addEventListener("click", (event) => {
  const button = event.target.closest(".delete-btn");
  if (button) {
    const itemId = button.dataset.id;
    deleteItem(itemId);
  }
});
```

---

### Q88: What is the difference between `event.target` and `event.currentTarget`?

**Answer:**

- **`event.target`**: The actual DOM element where the event **originated** (the deepest child clicked by the user).
- **`event.currentTarget`**: The DOM element to which the **event handler is currently attached** (the element processing the listener).

---

### Q89: What is the difference between `event.stopPropagation()` and `event.stopImmediatePropagation()`?

**Answer:**

- **`event.stopPropagation()`**: Stops the event from traveling further up (bubbling) or down (capturing) the DOM tree. However, other event listeners attached to the **same element** will still execute.
- **`event.stopImmediatePropagation()`**: Stops propagation to other elements **AND** prevents any subsequent event listeners attached to the **same element** from running.
- **`event.preventDefault()`**: Does NOT stop propagation; it merely cancels the browser's default behavior (e.g. following a link or submitting a form).

---

### Q90: What is the `MutationObserver` API and when should you use it?

**Answer:**

- `MutationObserver` provides the ability to watch for changes being made to the DOM tree (child list additions/removals, attribute changes, text modifications).
- **Advantage:** Executes asynchronously as a **Microtask** at the end of the current JavaScript turn, batching multiple changes to prevent layout thrashing.
- Replaced obsolete, performance-killing DOM Mutation Events (`DOMNodeInserted`).

```javascript
const observer = new MutationObserver((mutationsList) => {
  for (const mutation of mutationsList) {
    if (mutation.type === "childList") {
      console.log("DOM nodes added/removed:", mutation.addedNodes);
    }
  }
});

observer.observe(document.body, { childList: true, subtree: true });
```

---

### Q91: What is the `IntersectionObserver` API and what problems does it solve?

**Answer:**

- `IntersectionObserver` asynchronously observes changes in the intersection of a target element with an ancestor element or the top-level viewport.
- **Problems Solved:** Replaces scroll event listeners (`window.onscroll` + `getBoundingClientRect()`), which force synchronous layouts and cause jank.
- **Use Cases:** Image lazy-loading, infinite scrolling feeds, tracking ad impressions, animating elements when scrolled into view.

```javascript
const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      observer.unobserve(img); // Stop observing once loaded
    }
  });
});

document.querySelectorAll("img[data-src]").forEach(img => imageObserver.observe(img));
```

---

### Q92: How does the `ResizeObserver` API work?

**Answer:**

- `ResizeObserver` reports changes to the dimensions of an Element's content box or border box.
- Executes before paint, avoiding infinite layout cycles.
- **Ideal Use Case:** Responsive components (Container Queries polyfills, dynamic canvas/chart re-rendering based on parent container size).

---

### Q93: What is the `Proxy` object and what are Interception Traps?

**Answer:**

- `new Proxy(target, handler)` wraps a target object and intercepts fundamental operations.
- The `handler` object contains **traps**—methods that intercept operations:
  - `get(target, prop, receiver)`
  - `set(target, prop, value, receiver)`
  - `has(target, prop)` (intercepts `in` operator)
  - `deleteProperty(target, prop)`
  - `apply(target, thisArg, argumentsList)` (for functions)

```javascript
const state = new Proxy({ count: 0 }, {
  set(target, prop, value) {
    console.log(`Setting ${prop} to ${value}`);
    target[prop] = value;
    // Trigger reactive UI update!
    return true; // Must return boolean indicating success
  }
});

state.count = 5; // Logs: "Setting count to 5"
```

---

### Q94: Why should you always use `Reflect` inside `Proxy` traps?

**Answer:**

- The `Reflect` API contains methods matching all 13 Proxy traps (`Reflect.get`, `Reflect.set`, etc.).
- **Benefits:**
  1. Preserves the correct `this` context across prototypal inheritance using the `receiver` argument.
  2. Returns clean boolean success flags instead of throwing errors (e.g. `Reflect.defineProperty`).
  3. Guarantees default internal engine behavior is invoked cleanly.

```javascript
const proxy = new Proxy(target, {
  get(target, prop, receiver) {
    // Correctly binds receiver so prototype getters evaluate against proxy instance!
    return Reflect.get(target, prop, receiver);
  }
});
```

---

### Q95: What are the differences between CommonJS (CJS) and ES Modules (ESM)?

**Answer:**

| Feature | CommonJS (CJS) | ES Modules (ESM) |
| :--- | :--- | :--- |
| **Syntax** | `require()` / `module.exports` | `import` / `export` |
| **Loading** | **Synchronous** at runtime. Blocks execution. | **Asynchronous** with static parsing phase. |
| **Analysis** | Dynamic (can `require` inside `if` blocks). | **Static** (imports must be at top-level; enables **tree-shaking**). |
| **Export Value** | Copies value on export (snapshots). | Live **read-only bindings** to exported memory. |
| **Top-Level Await** | ❌ Not supported in CJS. | ✅ Native support (`await fetch(...)`). |

---

### Q96: How does Tree-Shaking work and why is ESM mandatory for it?

**Answer:**

- **Tree-Shaking** (Dead Code Elimination) removes unused exports from final production bundles.
- Bundlers (Webpack, Rollup, Vite, esbuild) rely on ESM's **static module structure**. Because `import` and `export` cannot change at runtime, bundlers construct an exact dependency graph during compile-time, identifying which functions are never referenced and pruning them safely.

---

### Q97: What is Top-Level Await in ES2022?

**Answer:**

- Allows using the `await` keyword at the top level of an ES module without wrapping it in an `async IIFE`.
- Execution of dependent consumer modules is paused until the top-level awaited promise resolves.
- **Use Cases:** Dynamic resource loading, database connection initialization, conditional polyfills.

```javascript
// db.js (ES Module)
export const connection = await createDbConnection();
```

---

### Q98: What is `Array.prototype.toSorted()`, `toReversed()`, and `toSpliced()` in ES2023?

**Answer:**

- Introduced to provide **non-mutating, pure counterparts** to mutating array methods:
  - `toSorted()` returns a new sorted array (unlike `sort()` which mutates).
  - `toReversed()` returns a new reversed array (unlike `reverse()`).
  - `toSpliced()` returns a new array with elements removed/inserted (unlike `splice()`).
  - `with(index, value)` returns a new array with an element replaced at `index`.

```javascript
const numbers = [3, 1, 2];
const sorted = numbers.toSorted();
console.log(sorted);  // [1, 2, 3]
console.log(numbers); // [3, 1, 2] (Original untouched!)
```

---

### Q99: What are Web Workers and how do they communicate with the main thread?

**Answer:**

- Web Workers run scripts in background OS threads **completely decoupled from the main UI thread**.
- They have their own execution context, call stack, and memory space (no access to `window`, `document`, or DOM).
- **Communication:** Via message passing (`postMessage()` and `onmessage` event handlers).
- **Data Transfer:** Data is either serialized via the Structured Clone Algorithm (deep copied) or ownership is transferred instantly via **Transferable Objects** (`ArrayBuffer`).

---

### Q100: How do `SharedArrayBuffer` and `Atomics` enable multi-threaded shared memory?

**Answer:**

- **`SharedArrayBuffer`**: Allows allocating raw binary memory accessible simultaneously by the main thread and multiple Web Workers without copying.
- **`Atomics`**: Provides atomic operations (`Atomics.add`, `Atomics.compareExchange`, `Atomics.wait`, `Atomics.notify`) to prevent race conditions and synchronize memory access across threads safely without data corruption.
