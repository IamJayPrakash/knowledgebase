# -*- coding: utf-8 -*-
"""
Generator for Track 1: JavaScript Deep Dive & Interview Questions
Generates:
1. 01-javascript/09_es6_classes_under_the_hood.md
2. 01-javascript/13_modules_cjs_vs_esm.md
3. 01-javascript/15_dom_events_delegation_bubbling.md
4. 01-javascript/interview-questions/short_questions_basics.md
5. 01-javascript/interview-questions/output_event_loop_promises.md
6. 01-javascript/interview-questions/output_this_binding.md
7. 01-javascript/interview-questions/coding_deep_clone.md
8. 01-javascript/interview-questions/coding_curry_function.md
9. 01-javascript/interview-questions/coding_event_emitter.md
10. 01-javascript/interview-questions/scenario_memory_leak_debugging.md
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FILES = {
    os.path.join(BASE_DIR, "01-javascript", "09_es6_classes_under_the_hood.md"): """# ES6 Classes Under The Hood & Prototypal Desugaring

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Socho ek purani traditional sweet shop hai jahan mithai banane ki recipe ek purane kagaz (Prototype) pe likhi hoti thi. Beta us kagaz ko dekh kar seekhta tha. 
Jab ES6 aya, unhone dukan ke bahar ek chamchamata neon sign board laga diya: **"Modern Sweet Factory Pvt Ltd" (Class syntax)**. 
Lekin factory ke kitchen ke andar koi robotic machine nahi aayi; kitchen ke andar wahi purana chef purani recipe wali diary (`[[Prototype]]` link) dekh kar hi laddoo bana raha hai!
In JavaScript, **Classes are just syntactical sugar over prototypal inheritance**. There are no real classes in JS engine memory—only functions, prototype objects, and `__proto__` pointer chains.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Syntactic Sugar over Functions**: Declaring `class Car {}` creates a function named `Car` whose `prototype` property holds all instance methods.
2. **`constructor` Method**: The constructor function executes during `new Car()`. If omitted, a default empty constructor (or `constructor(...args) { super(...args); }` in derived classes) is injected.
3. **Temporal Dead Zone (TDZ)**: Unlike function declarations, class declarations are **not hoisted** to an initialized state. Accessing them before declaration throws `ReferenceError`.
4. **Strict Mode by Default**: The entire body of an ES6 class executes strictly in `'use strict'` mode automatically.
5. **Non-enumerable Methods**: Methods defined inside a class are non-enumerable (`enumerable: false`), unlike methods attached to `Car.prototype.drive = ...` manually.
6. **`super` Keyword**: In derived classes (`class Dog extends Animal`), `super()` calls the parent constructor and binds `this`. You **cannot** access `this` before calling `super()`.
7. **Static Methods & Properties**: Bound directly to the constructor function (`Car.compare()`), not to the `Car.prototype`. They are inherited through the prototype chain between constructor functions (`Dog.__proto__ === Animal`).
8. **Private Fields (`#privateField`)**: Hard private encapsulation enforced at language parsing and V8 hidden class level using WeakMaps under the hood; cannot be accessed even via `Object.keys()` or reflection.

---

## 📊 3. Visual Architecture Diagram

```
                 ES6 CLASS IN RUNTIME MEMORY
                 
      [ Class Declaration: class User ]
                     │
                     ▼
      ┌──────────────────────────────┐
      │      User (Function)         │
      │  - [[Prototype]] ────────────┼──────────► Function.prototype
      │  - prototype ────────────────┼───────┐
      │  - static helper()           │       │
      └──────────────────────────────┘       │
                                             │
                     ┌───────────────────────┘
                     ▼
      ┌──────────────────────────────┐
      │      User.prototype          │
      │  - constructor ──────────────┼──────────► Back to User function
      │  - login() (method)          │
      │  - logout() (method)         │
      │  - [[Prototype]] ────────────┼──────────► Object.prototype
      └──────────────────────────────┘
                     ▲
                     │ (Instance [[Prototype]] link)
      ┌──────────────┴───────────────┐
      │   instance = new User()      │
      │  - name: "Alex" (own prop)   │
      │  - #apiKey: 123 (private)    │
      └──────────────────────────────┘
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```javascript
// Step 1: Define an ES6 Base Class with modern features
class DatabaseConnection {
  // Line 2: Declare private class field (V8 creates internal private brand check)
  #connectionSecret;

  // Line 4: Declare static class property attached to the constructor function itself
  static poolCount = 0;

  // Line 7: The constructor initializes own properties on the new instance
  constructor(dbName, secret) {
    // Line 9: Assign public property directly onto the new instance object
    this.dbName = dbName;
    // Line 11: Assign private field; accessible only within this class block
    this.#connectionSecret = secret;
    // Line 13: Increment static counter on the constructor function
    DatabaseConnection.poolCount++;
  }

  // Line 17: Public method placed on DatabaseConnection.prototype (enumerable: false)
  connect() {
    // Line 19: Reads instance property and private secret securely
    return `Connected to ${this.dbName} with secret [${this.#connectionSecret}]`;
  }

  // Line 23: Static method available on DatabaseConnection, NOT on instances
  static getActivePools() {
    // Line 25: Returns the shared static state across all instances
    return DatabaseConnection.poolCount;
  }
}

// Step 2: Desugared ES5 Equivalent (What the JS Engine actually builds)
function ES5DatabaseConnection(dbName, secret) {
  // Line 31: Enforce invocation with 'new' keyword (ES6 classes throw TypeError if invoked without new)
  if (!(this instanceof ES5DatabaseConnection)) {
    throw new TypeError("Cannot call a class as a function");
  }
  // Line 35: Own instance property
  this.dbName = dbName;
  // Line 37: Private encapsulation simulation using closure or symbol
  const _secret = secret;
  // Line 39: Expose privileged reader or use WeakMap
  this.getSecret = function() { return _secret; };
  // Line 41: Increment static property
  ES5DatabaseConnection.poolCount++;
}

// Line 45: Attach static properties to constructor function object
ES5DatabaseConnection.poolCount = 0;
ES5DatabaseConnection.getActivePools = function() {
  return ES5DatabaseConnection.poolCount;
};

// Line 51: Define prototype methods with enumerable: false to match ES6 behavior
Object.defineProperty(ES5DatabaseConnection.prototype, "connect", {
  value: function() {
    return "Connected to " + this.dbName + " with secret [" + this.getSecret() + "]";
  },
  writable: true,
  configurable: true,
  enumerable: false // ES6 class methods are non-enumerable
});

// Step 3: Verifying prototype links
const conn = new DatabaseConnection("PostgresProd", "s3cr3t_p@ss");
// Line 63: Method resolution walks up conn.__proto__ to DatabaseConnection.prototype
console.log(conn.connect()); 
// Line 65: True because instances point directly to constructor prototype
console.log(Object.getPrototypeOf(conn) === DatabaseConnection.prototype); // true
// Line 67: Private field cannot be accessed from outside
// console.log(conn.#connectionSecret); // SyntaxError: Private field '#connectionSecret' must be declared in an enclosing class
```

---

## 🎯 5. The "Interview Pitch"
> "In JavaScript, classes introduced in ES6 do not introduce an object-oriented class-based inheritance model like Java or C++. Under the hood, they are syntactic sugar desugared into constructor functions and prototype chains. When you define a class, V8 creates a constructor function and attaches your methods to its `.prototype` object with `enumerable: false`. Inheritance via `extends` sets up two prototype links: `Child.prototype.__proto__ = Parent.prototype` for instance methods, and `Child.__proto__ = Parent` for static methods. Furthermore, classes enforce strict mode, prevent calling without `new`, remain unhoisted in TDZ, and provide true encapsulation via hash private fields (`#field`)."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an enterprise micro-frontend payment gateway, developers refactored legacy SDK code to ES6 classes. Suddenly, third-party merchants reported `TypeError: Cannot read properties of undefined` whenever payment event callbacks fired.
- **Task**: Identify why class methods failed when passed as callbacks and fix the issue across 45 client payment components without breaking bundle size.
- **Action**: In ES5, developers were binding methods or using object literals. In ES6 classes, class methods are not autobound, and because class bodies execute in `'use strict'`, un-bound callbacks lost their context and `this` evaluated to `undefined` rather than the global `window`. We refactored event listeners to class field arrow functions (`handlePayment = () => {}`) which compile to own-property instance bindings during constructor initialization, preventing prototype lookup loss.
- **Result**: Reduced customer payment drops to 0%, resolved 100% of callback `TypeError` crashes, and added an automated ESLint rule enforcing unbound method detection across all CI pipelines.
""",

    os.path.join(BASE_DIR, "01-javascript", "13_modules_cjs_vs_esm.md"): """# JavaScript Modules: CommonJS (CJS) vs ECMAScript Modules (ESM)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
CommonJS (CJS) ek **Restaurant Delivery** ki tarah hai: Jab tak customer order ka phone nahi karta (runtime `require()`), tab tak kitchen mein koi khana pack nahi hota. Sab kuch step-by-step sync chalta hai, aur aap run-time par decide kar sakte ho ki 2 burger bhejne hain ya 3.
ECMAScript Modules (ESM) ek **Train Time-Table / Rail Network** ki tarah hai: Train chalne se pehle (parsing/compilation phase), station master ko pura route, track, aur stops pehle se pata hone chahiye (`import/export` static analysis). Agar track mein koi gadbad hui, toh train station chhod hi nahi sakti!
ESM allows bundlers like Vite and Rollup to do **Tree Shaking** because exports are statically known before code executes.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Static vs Dynamic Loading**:
   - ESM is **static**: `import` and `export` statements must be at the top level (enabling static tree analysis and tree-shaking).
   - CJS is **dynamic**: `require()` can be called conditionally inside `if` statements, loops, or functions at runtime.
2. **Values vs Live Bindings**:
   - CJS exports a **copy** of values (primitive values are copied at the time of `module.exports`).
   - ESM exports **live read-only bindings** (if the exporter mutates the exported variable, the importer sees the updated value instantly).
3. **Synchronous vs Asynchronous Loading**:
   - CJS resolves file paths synchronously via Node.js disk I/O.
   - ESM executes in 3 phases: Construction (parse & resolve AST), Instantiation (link memory pointers), and Evaluation (execute code), making it natively asynchronous.
4. **Top-Level Await**: ESM supports `await` at the top level without wrapping inside an `async IIFE`. CJS strictly forbids top-level await.
5. **Magic Globals (`__dirname`, `__filename`)**:
   - Present in CJS by default (injected via module wrapper function).
   - Absent in ESM; must be derived using `import.meta.url` and `fileURLToPath()`.
6. **Circular Dependencies Handling**:
   - CJS gives an incomplete copy of `module.exports` object if circular reference occurs.
   - ESM provides reference bindings; TDZ errors occur if uninitialized exported variables are accessed before evaluation.

---

## 📊 3. Visual Architecture Diagram

```
         COMMONJS (CJS) RUNTIME EXECUTION
  require('./utils') ──► Read File ──► Wrap in Function ──► Execute ──► Return module.exports Copy
  (Happens synchronously on demand at runtime)


         ECMASCRIPT MODULES (ESM) 3-STAGE LIFECYCLE
         
  Phase 1: Construction 
  [ Parse JS Code ] ──► Identify imports/exports statically ──► Fetch all files recursively
          │
          ▼
  Phase 2: Instantiation
  [ Allocate Memory ] ──► Link import pointers to export pointers (Live Bindings)
          │
          ▼
  Phase 3: Evaluation
  [ Execute Code ] ──► Fill memory slots with concrete values (Supports Top-Level Await)
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```javascript
// ==========================================
// 1. CommonJS (CJS) Mechanics (math_cjs.js)
// ==========================================
let count = 10;

function increment() {
  // Line 8: Mutates the internal variable
  count++;
}

// Line 12: Exports a snapshot copy of 'count' primitive at this instant
module.exports = {
  count,
  increment
};

// consumer_cjs.js:
const math = require("./math_cjs.js");
// Line 19: Outputs initial value: 10
console.log(math.count); // 10
// Line 21: Calls function that mutates count in math_cjs
math.increment();
// Line 23: Still outputs 10! Because CJS exported a copied primitive value
console.log(math.count); // 10


// ==========================================
// 2. ECMAScript Modules (ESM) Live Bindings (math_esm.mjs)
// ==========================================
// Line 29: Exporting a live binding
export let liveCount = 10;

export function incrementLive() {
  // Line 33: Mutates exported variable
  liveCount++;
}

// consumer_esm.mjs:
import { liveCount, incrementLive } from "./math_esm.mjs";
// Line 38: Initial live value
console.log(liveCount); // 10
// Line 40: Invokes mutation
incrementLive();
// Line 42: Outputs 11! ESM maintains a live memory pointer to original export
console.log(liveCount); // 11
// liveCount = 20; // TypeError: Assignment to constant variable (Imports are read-only)


// ==========================================
// 3. Simulating __dirname & __filename in ESM
// ==========================================
import path from "node:path";
import { fileURLToPath } from "node:url";

// Line 52: Extract absolute file path from current module URL
const __filename = fileURLToPath(import.meta.url);
// Line 54: Extract directory path
const __dirname = path.dirname(__filename);
console.log({ __filename, __dirname });
```

---

## 🎯 5. The "Interview Pitch"
> "CommonJS and ESM differ fundamentally in module resolution, execution timing, and memory bindings. CommonJS is synchronous, dynamically evaluated at runtime, and exports values by copy, meaning primitive exports do not reflect later mutations. It injects wrappers providing `__dirname` and `require`. In contrast, ESM is asynchronous, statically parsed at compile time, and exports live read-only references to memory locations. This static nature allows modern bundlers like Rollup, Webpack, and Vite to construct an exact AST dependency graph and perform dead-code elimination (Tree Shaking). ESM also natively supports top-level await and runs across both browser and Node.js runtimes."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: During a migration of a high-throughput API gateway from CJS to Node.js ESM, our Redis configuration module threw intermittent `ReferenceError: Cannot access 'redisClient' before initialization` crashes during container startup.
- **Task**: Root-cause the initialization crash occurring exclusively in ESM without rolling back to CJS.
- **Action**: In CJS, a circular dependency between `authMiddleware.js` and `redisClient.js` was masked because CJS returned an incomplete `{}` object reference during `require()`. In ESM, the 3-stage module loader instantiated live bindings in TDZ. When `authMiddleware` ran top-level code attempting to use `redisClient.get()`, the variable was uninitialized in memory. We eliminated the circular dependency by refactoring the shared cache client into a dedicated singleton factory (`cacheService.js`) initialized before any route middleware imports.
- **Result**: Startup crash rate dropped to 0%, container boot time improved by 22% due to ESM static parsing, and bundle size was reduced by 14% through bundler tree-shaking.
""",

    os.path.join(BASE_DIR, "01-javascript", "15_dom_events_delegation_bubbling.md"): """# DOM Events: Bubbling, Capturing, and Event Delegation

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Socho ek multi-floor corporate office building hai. Jab 5th floor par ek employee table par emergency button dabata hai:
1. **Capturing Phase (Trickling Down)**: Alarm ka signal sabse pehle building ke ground floor security gate (`window` -> `document` -> `body`) se seedhe 5th floor tak neeche aata hai.
2. **Target Phase**: Signal button tak pahunchta hai (`e.target`).
3. **Bubbling Phase (Floating Up)**: Fir button se alert upar ki taraf sabhi managers aur directors ke cabins se hote hue wapas ground floor security desk tak goonjta hai.
**Event Delegation**: Har desk par alag security guard bithane ke bajaye, aap floor ke main exit door par ek hi guard bitha dete ho jo aane-jaane wale har employee ke badge (`e.target`) ko check kar leta hai. Memory bachti hai aur performance super fast rehti hai!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Three Phases of DOM Event Flow**:
   - **Capturing Phase**: Event moves down from `Window` -> `Document` -> `<html>` -> `<body>` -> ancestors down to target.
   - **Target Phase**: Event arrives at the element that initiated the event (`event.target`).
   - **Bubbling Phase**: Event bubbles back up through ancestors to `Window`.
2. **`addEventListener` Third Argument**:
   - `element.addEventListener('click', handler, false)` (Default) runs in the **bubbling phase**.
   - `element.addEventListener('click', handler, true)` runs in the **capturing phase**.
3. **`e.target` vs `e.currentTarget`**:
   - `e.target`: The deepest element that triggered the event (e.g. the icon inside a button).
   - `e.currentTarget`: The element to which the event listener is currently attached (e.g. the parent `<ul>` or `<form>`).
4. **`e.stopPropagation()` vs `e.stopImmediatePropagation()`**:
   - `e.stopPropagation()`: Stops the event from traveling further up or down the DOM tree.
   - `e.stopImmediatePropagation()`: Stops DOM traversal AND prevents other listeners attached to the **same element** from executing.
5. **`e.preventDefault()`**: Prevents default browser actions (e.g. form submission page reload, link navigation) without halting propagation.
6. **Events that Do NOT Bubble**: `focus`, `blur`, `mouseenter`, `mouseleave`, `load`, `unload`, `scroll` (on element). Use `focusin` / `focusout` if bubbling is required.

---

## 📊 3. Visual Architecture Diagram

```
                THE 3-PHASE DOM EVENT DISPATCH PIPELINE
                
                     Window
                    ▲      │
                    │      ▼ [1. CAPTURING PHASE]
                   Document
                    ▲      │
                    │      ▼
                  <body>
                    ▲      │
                    │      ▼
                 <div id="container">
                    ▲      │
                    │      ▼
                 <button id="submitBtn">
                    │      │
                    └──────┘
              [2. TARGET PHASE]
                     │
                     ▼
         [3. BUBBLING PHASE (UPWARDS)]
```

---

## 💻 4. Line-by-Line Commented Code Snippets

```javascript
// Step 1: HTML Structure Setup Simulation
// <ul id="todo-list">
//    <li data-id="1">Task 1 <button class="delete-btn">Delete</button></li>
//    <li data-id="2">Task 2 <button class="delete-btn">Delete</button></li>
// </ul>

const todoList = document.getElementById("todo-list");

// Step 2: Implement Event Delegation on Parent Element
// Attaching 1 event listener instead of 10,000 listeners on each list item
todoList.addEventListener("click", function(event) {
  // Line 13: event.currentTarget points to the <ul id="todo-list">
  const currentContainer = event.currentTarget;

  // Line 16: event.target points to the exact clicked child element (e.g., button or text)
  const clickedElement = event.target;

  // Line 19: Check if the user clicked the delete button inside any <li>
  if (clickedElement.classList.contains("delete-btn")) {
    // Line 21: Find closest <li> parent using element.closest()
    const listItem = clickedElement.closest("li");
    
    // Line 24: Extract dataset ID
    const taskId = listItem.dataset.id;
    
    // Line 27: Prevent event from bubbling up to higher ancestor containers if necessary
    event.stopPropagation();
    
    // Line 30: Perform deletion
    console.log(`Deleting Task ID: ${taskId}`);
    listItem.remove();
    return;
  }

  // Line 36: If user clicked the list item body itself, toggle selection
  const listItem = clickedElement.closest("li");
  if (listItem && todoList.contains(listItem)) {
    // Line 39: Toggle active class
    listItem.classList.toggle("selected");
    console.log(`Toggled item ${listItem.dataset.id}`);
  }
}, false); // Line 43: false = Listen during Bubbling Phase (Standard practice)


// Step 3: Stop Immediate Propagation Demonstration
const alertBtn = document.getElementById("alert-btn");

alertBtn.addEventListener("click", (e) => {
  console.log("Handler 1 executed");
  // Line 51: Prevents Handler 2 from firing even on the SAME button
  e.stopImmediatePropagation();
});

alertBtn.addEventListener("click", () => {
  // Line 56: This will NEVER execute because Handler 1 called stopImmediatePropagation()
  console.log("Handler 2 executed");
});
```

---

## 🎯 5. The "Interview Pitch"
> "DOM event dispatching operates in three sequential phases: Capturing (propagating down from `window` to the target), Target (executing listeners on the target element), and Bubbling (propagating back up to `window`). By default, `addEventListener` listens in the bubbling phase unless the capture flag is set to true. Event delegation is a critical performance pattern where instead of attaching thousands of event listeners to individual child elements, we attach a single listener to a common ancestor. Inside the handler, we inspect `event.target` using `element.matches()` or `element.closest()` to identify the initiator. This drastically minimizes heap memory consumption and automatically handles dynamically inserted DOM nodes without re-binding listeners."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an e-commerce dashboard with an infinite-scrolling catalog of 5,000 product cards, users experienced severe UI lag and scroll stuttering (FPS dropped to 14 FPS) on low-end mobile devices.
- **Task**: Eliminate scroll jank and reduce heap memory consumption without changing product card features.
- **Action**: Performance profiling in Chrome DevTools showed over 25,000 active DOM event listeners attached individually to 'Add to Cart', 'Wishlist', and 'Quick View' buttons on every loaded card. We removed all individual listeners and implemented a single delegated event listener on the parent container `#product-grid`. We utilized `e.target.closest('[data-action]')` to dispatch actions based on data attributes.
- **Result**: DOM event listener count plunged from 25,000 to just 1. Heap memory decreased by 42 MB, garbage collection pauses were eliminated, and scroll frame rate restored to a silky-smooth 60 FPS.
""",

    os.path.join(BASE_DIR, "01-javascript", "interview-questions", "short_questions_basics.md"): """# JavaScript Core Interview Questions (Quick Recall & High-Frequency)

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

## 3. Explain `Object.freeze()` vs `Object.seal()`.
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
""",

    os.path.join(BASE_DIR, "01-javascript", "interview-questions", "output_event_loop_promises.md"): """# Tricky Output Questions: Event Loop, Microtasks & Macrotasks

---

## Problem 1: The Classic Microtask vs Macrotask Race

### Code:
```javascript
console.log("1");

setTimeout(() => {
  console.log("2");
  Promise.resolve().then(() => {
    console.log("3");
  });
}, 0);

new Promise((resolve, reject) => {
  console.log("4");
  resolve();
}).then(() => {
  console.log("5");
}).then(() => {
  console.log("6");
});

console.log("7");
```

### Output:
```
1
4
7
5
6
2
3
```

### Detailed Execution Trace:
1. `console.log("1")` runs synchronously -> **Prints 1**.
2. `setTimeout` callback registered to Macrotask/Timer Queue with 0ms delay.
3. `new Promise(executor)` executes **synchronously** immediately upon creation. `console.log("4")` runs -> **Prints 4**. `resolve()` changes Promise state to `fulfilled`.
4. First `.then()` callback (`console.log("5")`) pushed to Microtask Queue.
5. `console.log("7")` runs synchronously -> **Prints 7**.
6. Synchronous Call Stack is now empty! Event loop checks the **Microtask Queue** before touching macrotasks.
7. Microtask 1: `console.log("5")` executes -> **Prints 5**. Its resolution schedules the chained `.then()` (`console.log("6")`) into the Microtask Queue.
8. Microtask 2: `console.log("6")` executes -> **Prints 6**.
9. Microtask queue is completely drained. Event loop picks the oldest task from **Macrotask Queue** (`setTimeout` callback).
10. `console.log("2")` runs -> **Prints 2**.
11. Inside `setTimeout`, `Promise.resolve().then(...)` pushes `console.log("3")` to the Microtask Queue.
12. Current macrotask finishes. Event loop drains Microtask Queue before next tick: `console.log("3")` runs -> **Prints 3**.

---

## Problem 2: Async/Await with Chained Promises

### Code:
```javascript
async function async1() {
  console.log("async1 start");
  await async2();
  console.log("async1 end");
}

async function async2() {
  console.log("async2");
}

console.log("script start");

setTimeout(() => {
  console.log("setTimeout");
}, 0);

async1();

new Promise((resolve) => {
  console.log("promise1");
  resolve();
}).then(() => {
  console.log("promise2");
});

console.log("script end");
```

### Output:
```
script start
async1 start
async2
promise1
script end
async1 end
promise2
setTimeout
```

### Explanation:
- `script start` runs synchronously.
- `setTimeout` goes to Macrotask queue.
- `async1()` is invoked. Prints `async1 start`.
- `await async2()` executes `async2()` synchronously, printing `async2`.
- `await` pauses execution of `async1` and queues the remainder (`console.log("async1 end")`) as a microtask.
- `new Promise` executor runs synchronously, printing `promise1`. Chained `.then()` queued as a microtask.
- Synchronous `script end` prints.
- Microtasks execute in FIFO order:
  - First microtask: `async1 end` prints.
  - Second microtask: `promise2` prints.
- Macrotask executes: `setTimeout` prints.
""",

    os.path.join(BASE_DIR, "01-javascript", "interview-questions", "output_this_binding.md"): """# Tricky Output Questions: `this` Binding & Arrow Functions

---

## Problem 1: Object Method vs Detached Callback

### Code:
```javascript
const user = {
  name: "Jay",
  getName() {
    return this.name;
  },
  getArrowName: () => {
    return this.name;
  }
};

const extracted = user.getName;

console.log(user.getName());
console.log(extracted());
console.log(user.getArrowName());
```

### Output:
```
Jay
undefined (or Window name in non-strict browser)
undefined
```

### Explanation:
1. `user.getName()`: Method invocation with dot notation. The object left of the dot (`user`) becomes the `this` context. Returns `"Jay"`.
2. `extracted()`: The function reference was copied to a standalone variable and invoked without dot notation. Default binding applies: in strict mode `this` is `undefined`, in non-strict browser it is `window`. Returns `undefined`.
3. `user.getArrowName()`: Arrow functions do **not** have their own `this`. They capture `this` lexically from the enclosing lexical scope at declaration time. Here, the enclosing scope of the object literal is the global/module scope (not the `user` object!), where `name` is undefined.

---

## Problem 2: Nested Arrow Functions & Arguments

### Code:
```javascript
const obj = {
  count: 10,
  regular() {
    return function() {
      console.log("A:", this.count);
    };
  },
  arrow() {
    return () => {
      console.log("B:", this.count);
    };
  }
};

obj.regular()();
obj.arrow()();
```

### Output:
```
A: undefined
B: 10
```

### Explanation:
- `obj.regular()` returns a standard function. When invoked as `()`, it has default binding (`this` = `global` or `undefined`). Hence `this.count` is `undefined`.
- `obj.arrow()` was invoked with `obj` as `this`. Inside `arrow()`, `this` points to `obj`. The returned arrow function lexically captures this exact `this` reference. When invoked as `()`, it retains `obj` as `this`, printing `10`.
""",

    os.path.join(BASE_DIR, "01-javascript", "interview-questions", "coding_deep_clone.md"): """# Machine Coding: Deep Clone with Circular References & Special Types

---

## 🐣 1. Layman's Analogy
Shallow clone photo copy machine ki tarah hai: agar paper par kisi dusre document ka reference link likha hai, toh copy mein bhi wahi link aayega. Agar link wala original page phat gaya, toh copy bhi bekar.
Deep clone 3D printer ki tarah hai: wo object ke har child, nested structure, date, regex aur circular loop ko bilkul naye fresh memory address pe recreate karta hai.

---

## 💻 2. Line-by-Line Commented Code Solution

```javascript
/**
 * Deep clones any JavaScript object handling:
 * 1. Primitives (numbers, strings, booleans, null, undefined, symbols, bigints)
 * 2. Circular references (via WeakMap memory hash)
 * 3. Dates & RegExp instances
 * 4. Maps & Sets
 * 5. Arrays & Plain Objects
 * 6. Symbol-keyed properties
 */
function deepClone(target, hash = new WeakMap()) {
  // Line 12: Primitives & functions are returned as-is (immutable or shared by reference)
  if (target === null || typeof target !== "object") {
    return target;
  }

  // Line 17: Special object type: Date
  if (target instanceof Date) {
    return new Date(target.getTime());
  }

  // Line 22: Special object type: RegExp
  if (target instanceof RegExp) {
    return new RegExp(target.source, target.flags);
  }

  // Line 27: Circular reference check
  // If we already cloned this object in this path, return existing cloned reference
  if (hash.has(target)) {
    return hash.get(target);
  }

  // Line 33: Handle Set data structure
  if (target instanceof Set) {
    const cloneSet = new Set();
    hash.set(target, cloneSet);
    target.forEach((value) => {
      cloneSet.add(deepClone(value, hash));
    });
    return cloneSet;
  }

  // Line 43: Handle Map data structure
  if (target instanceof Map) {
    const cloneMap = new Map();
    hash.set(target, cloneMap);
    target.forEach((value, key) => {
      cloneMap.set(deepClone(key, hash), deepClone(value, hash));
    });
    return cloneMap;
  }

  // Line 53: Initialize clone with identical prototype chain
  const cloneObj = Array.isArray(target)
    ? []
    : Object.create(Object.getPrototypeOf(target));

  // Line 58: Store cloned instance in hash map BEFORE traversing children to resolve cycles
  hash.set(target, cloneObj);

  // Line 61: Retrieve all own property keys, including non-enumerable and Symbol keys
  const allKeys = [
    ...Object.getOwnPropertyNames(target),
    ...Object.getOwnPropertySymbols(target)
  ];

  // Line 67: Recursively copy property descriptors and values
  for (const key of allKeys) {
    const descriptor = Object.getOwnPropertyDescriptor(target, key);
    
    // Only copy if configurable or writable (skip getters/setters unless defined as value)
    if (descriptor && "value" in descriptor) {
      descriptor.value = deepClone(target[key], hash);
    }
    
    // Line 76: Define property preserving original property flags (enumerable, writable)
    Object.defineProperty(cloneObj, key, descriptor);
  }

  return cloneObj;
}

// ==========================================
// Test Cases & Verification
// ==========================================
const original = {
  num: 42,
  str: "hello",
  date: new Date("2026-01-01"),
  regex: /^[a-z]+$/gi,
  set: new Set([1, 2, 3]),
  map: new Map([["key1", { nested: "val" }]]),
  [Symbol("id")]: 999
};

// Create Circular Reference
original.self = original;

const copy = deepClone(original);

console.log(copy !== original); // true
console.log(copy.self === copy); // true (circular link preserved!)
console.log(copy.date instanceof Date); // true
console.log(copy.map.get("key1") !== original.map.get("key1")); // true (deeply cloned)
```

---

## 🎯 3. The "Interview Pitch"
> "While `structuredClone()` is the modern native browser and Node.js standard for deep cloning, it has key limitations: it cannot clone functions or DOM nodes. In senior technical interviews, writing a custom `deepClone` demonstrates mastery of memory models. The essential technical requirements are: checking for null and primitives first, handling constructors like `Date` and `RegExp`, maintaining a `WeakMap` memo cache to prevent infinite stack overflows from circular references, cloning `Map` and `Set` collections, and extracting all keys via `Object.getOwnPropertyNames` and `Object.getOwnPropertySymbols` while preserving descriptor attributes with `Object.defineProperty`."
""",

    os.path.join(BASE_DIR, "01-javascript", "interview-questions", "coding_curry_function.md"): """# Machine Coding: Infinite Currying & Generalized Currying

---

## 🐣 1. Layman's Analogy
Currying ek assembly line pizza counter ki tarah hai. Ek bar mein pura pizza lene ke bajaye, aap pehle crust select karte ho `order('thin')`, fir agle counter pe cheese `('mozzarella')`, fir agle counter pe toppings `('jalapeno')`. Jab sare mandatory ingredients poore ho jate hain, chef pizza deliver kar deta hai!

---

## 💻 2. Line-by-Line Commented Code Solutions

### Variant A: Generalized Currying based on Function Arity (`fn.length`)

```javascript
/**
 * Transforms a multi-argument function into a curried function
 * that executes once all expected parameters (arity) are supplied.
 */
function curry(fn) {
  // Line 8: Return a wrapper function that collects arguments
  return function curried(...args) {
    // Line 10: Compare collected arguments count with target function arity
    if (args.length >= fn.length) {
      // Line 12: If we have enough arguments, execute the original function
      return fn.apply(this, args);
    } else {
      // Line 15: If not enough, return a new function that accumulates further args
      return function(...nextArgs) {
        // Line 17: Recursively collect and merge arguments
        return curried.apply(this, args.concat(nextArgs));
      };
    }
  };
}

// Testing Generalized Currying
function sum3(a, b, c) {
  return a + b + c;
}

const curriedSum = curry(sum3);
console.log(curriedSum(1)(2)(3)); // 6
console.log(curriedSum(1, 2)(3)); // 6
console.log(curriedSum(1)(2, 3)); // 6
```

---

### Variant B: Infinite Currying with Value Extraction (`sum(1)(2)...(n)()`)

```javascript
/**
 * Infinite currying terminating on empty parentheses invocation ()
 */
function infiniteCurry(a) {
  // Line 38: Return internal collector function
  return function(b) {
    // Line 40: Check if empty argument passed to terminate
    if (b === undefined) {
      return a;
    }
    // Line 44: Recursively return new curry with accumulated sum
    return infiniteCurry(a + b);
  };
}

console.log(infiniteCurry(1)(2)(3)(4)()); // 10
console.log(infiniteCurry(5)(10)());      // 15
```

---

### Variant C: Infinite Currying via `valueOf` / `toString` Override

```javascript
/**
 * Infinite currying that automatically coerces to a primitive number
 * when used in comparisons or arithmetic (e.g. sum(1)(2)(3) == 6)
 */
function autoSum(a) {
  let currentSum = a;

  function inner(b) {
    currentSum += b;
    return inner;
  }

  // Override primitive coercion hooks
  inner.valueOf = function() {
    return currentSum;
  };

  inner.toString = function() {
    return String(currentSum);
  };

  return inner;
}

console.log(autoSum(1)(2)(3) == 6); // true
console.log(Number(autoSum(5)(10)(20))); // 35
```
""",

    os.path.join(BASE_DIR, "01-javascript", "interview-questions", "coding_event_emitter.md"): """# Machine Coding: Production-Ready Custom `EventEmitter`

---

## 🐣 1. Layman's Analogy
`EventEmitter` ek newspaper publishing agency ki tarah hai. Readers aate hain aur kisi topic ke liye subscribe karte hain (`emitter.on('sports', callback)`). Jab bhi sports department nayi khabar print karta hai (`emitter.emit('sports', news)`), agency har subscribed reader ke ghar newspaper bhej deti hai. Agar koi reader subscription cancel kare (`emitter.off('sports', callback)`), use aage se khabar nahi milti.

---

## 💻 2. Line-by-Line Commented Code Solution

```javascript
/**
 * Production EventEmitter with on, once, off, emit, and listener count
 */
class EventEmitter {
  constructor() {
    // Line 8: Internal storage for events: { [eventName: string]: Function[] }
    this._events = Object.create(null);
    // Line 10: Default max listener limit to prevent accidental memory leaks
    this._maxListeners = 10;
  }

  // Line 14: Subscribe a listener to an event
  on(eventName, listener) {
    if (typeof listener !== "function") {
      throw new TypeError("Listener must be a function");
    }

    // Line 20: Initialize listener array if not present
    if (!this._events[eventName]) {
      this._events[eventName] = [];
    }

    // Line 25: Memory leak warning detection
    if (this._events[eventName].length >= this._maxListeners) {
      console.warn(
        `[Warning] Possible EventEmitter memory leak detected. ` +
        `${this._events[eventName].length + 1} ${String(eventName)} listeners added.`
      );
    }

    // Line 33: Add listener to event queue
    this._events[eventName].push(listener);

    // Line 36: Return unsubscription function for ergonomic cleanup
    return () => this.off(eventName, listener);
  }

  // Line 40: Subscribe a one-time listener that self-removes after single trigger
  once(eventName, listener) {
    if (typeof listener !== "function") {
      throw new TypeError("Listener must be a function");
    }

    // Line 46: Create wrapper that unregisters itself before executing callback
    const onceWrapper = (...args) => {
      this.off(eventName, onceWrapper);
      listener.apply(this, args);
    };

    // Line 52: Save original reference so .off(eventName, listener) still works
    onceWrapper.originalListener = listener;

    return this.on(eventName, onceWrapper);
  }

  // Line 58: Trigger all listeners registered under eventName with arguments
  emit(eventName, ...args) {
    const listeners = this._events[eventName];
    if (!listeners || listeners.length === 0) {
      return false;
    }

    // Line 65: Clone listener array with .slice() to prevent mutation issues
    // if a listener calls .off() during execution
    const handlers = listeners.slice();

    for (let i = 0; i < handlers.length; i++) {
      try {
        handlers[i].apply(this, args);
      } catch (error) {
        // Line 73: Isolate handler exceptions so other listeners still execute
        console.error(`Error in event listener for ${String(eventName)}:`, error);
      }
    }

    return true;
  }

  // Line 81: Unsubscribe a specific listener
  off(eventName, listener) {
    const listeners = this._events[eventName];
    if (!listeners || listeners.length === 0) {
      return this;
    }

    // Line 88: Filter out target listener or matching onceWrapper
    this._events[eventName] = listeners.filter(
      (fn) => fn !== listener && fn.originalListener !== listener
    );

    // Line 93: Clean up empty event keys to prevent memory fragmentation
    if (this._events[eventName].length === 0) {
      delete this._events[eventName];
    }

    return this;
  }

  // Line 101: Remove all listeners for a specific event or all events
  removeAllListeners(eventName) {
    if (eventName) {
      delete this._events[eventName];
    } else {
      this._events = Object.create(null);
    }
    return this;
  }

  // Line 111: Get count of active listeners for an event
  listenerCount(eventName) {
    return this._events[eventName] ? this._events[eventName].length : 0;
  }
}

// ==========================================
// Verification Tests
// ==========================================
const bus = new EventEmitter();

const onOrder = (id, amount) => console.log(`Order placed: ${id}, Amount: $${amount}`);
const unsubscribe = bus.on("order", onOrder);

bus.emit("order", "ORD-101", 250); // Order placed: ORD-101, Amount: $250

bus.once("greet", (name) => console.log(`Welcome, ${name}!`));
bus.emit("greet", "Jay"); // Welcome, Jay!
bus.emit("greet", "Jay"); // (Nothing prints, single-fire executed)

unsubscribe();
bus.emit("order", "ORD-102", 500); // (Nothing prints, successfully unsubscribed)
```
""",

    os.path.join(BASE_DIR, "01-javascript", "interview-questions", "scenario_memory_leak_debugging.md"): """# Scenario-Based: Debugging JavaScript Memory Leaks in Production

---

## 🐣 1. Layman's Analogy
Memory leak ek dukan mein empty boxes jama hone jaisa hai. Har baar naya saman aata hai, box khali ho jata hai lekin dukan se bahar dustbin mein fekne ke bajaye aap use kone mein stack karte rehte ho. Shuru mein koi dikkat nahi hoti, lekin 3 mahine baad dukan mein chalne ki jagah nahi bachti aur dukan band karni padti hai (Browser crash ya Node.js OOM kill).
In V8 engine, Garbage Collector tab tak memory free nahi karta jab tak root (`window` ya global scope) se us memory block tak ka rasta (`retaining path`) juda hua hai.

---

## 📌 2. The 4 Major Causes of JS Memory Leaks

1. **Accidental Global Variables**:
   Assigning values to undeclared variables attaches them to `window` or `globalThis`. Since global roots are never collected, the entire object tree remains pinned in memory.
2. **Forgotten Timers & Callbacks**:
   `setInterval` callbacks that reference outer closures will retain all captured variables forever until `clearInterval` is invoked, even if the parent component is destroyed.
3. **Detached DOM Nodes**:
   When an element is removed from the DOM tree (`element.remove()`), but a JavaScript variable or array still holds a reference to that node, V8 cannot garbage collect the DOM node or any of its children.
4. **Closures Retaining Large Outer Scopes**:
   Multiple closures in the same lexical scope share an internal context object. If one closure holds a large buffer and another long-lived closure is retained (e.g. in a global event bus), the large buffer cannot be freed.

---

## 📊 3. Visual Architecture Diagram

```
         V8 GARBAGE COLLECTION RETAINING PATH
         
      [ GC ROOT: Window / Global ]
                  │
                  ▼
      [ Global Event Bus / Cache ]
                  │
                  ▼
      [ Event Listener Callback (Closure) ]
                  │ (Retains Lexical Scope)
                  ▼
      [ Context Scope: { hugePayload, componentRef } ]
                  │
                  ▼
      [ Detached DOM Tree / 50MB Buffer ] ◄── Cannot be Garbage Collected!
```

---

## 💻 4. Practical Reproduction & Remediation Code

```javascript
// ==========================================
// ANTI-PATTERN: The Classic Detached DOM & Timer Leak
// ==========================================
class LeakyWidget {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    // Line 8: Allocating large data payload
    this.largeData = new Array(1000000).fill("heavy-payload-data");
    
    // Line 11: Leaky setInterval retains 'this' and 'largeData' forever
    this.timerId = setInterval(() => {
      console.log("Polling for container:", this.container.id);
    }, 1000);

    // Line 16: Leaky window event listener
    window.addEventListener("resize", this.handleResize);
  }

  handleResize = () => {
    console.log("Window resized for widget");
  };

  // Bad destroy method: Only removes element from DOM, leaving timer & listener!
  badDestroy() {
    this.container.remove(); // DOM node removed, but timer keeps this entire instance alive!
  }
}

// ==========================================
// REMEDIATION: Clean Lifecycle Tear-down
// ==========================================
class CleanWidget {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.largeData = new Array(1000000).fill("heavy-payload-data");

    this.timerId = setInterval(() => {
      this.poll();
    }, 1000);

    window.addEventListener("resize", this.handleResize);
  }

  handleResize = () => {
    console.log("Window resized safely");
  };

  poll() {
    if (this.container) {
      console.log("Polling safely:", this.container.id);
    }
  }

  // Proper Clean-up Method
  destroy() {
    // Line 57: Clear periodic timer
    if (this.timerId) {
      clearInterval(this.timerId);
      this.timerId = null;
    }

    // Line 63: Remove global event listener
    window.removeEventListener("resize", this.handleResize);

    // Line 66: Sever DOM and heavy data references to allow GC reclamation
    if (this.container) {
      this.container.remove();
      this.container = null;
    }
    this.largeData = null;
  }
}
```

---

## 🎯 5. The "Interview Pitch"
> "When diagnosing memory leaks in JavaScript, I follow a systematic 3-step profiling methodology. First, reproduce the suspected workflow in Chrome DevTools under the **Memory Tab** and record a **Heap Snapshot** before and after the action. In the comparison view, I sort by **Retained Size** and inspect constructors like `Detached HTMLDivElement` or `Closure`. Second, I examine the **Retainers Tree** to pinpoint the exact GC Root holding the reference—typically a dangling `setInterval`, an un-removed `window.addEventListener`, or an uncleared cache in a module singleton. Third, in Node.js, I use tools like `clinic doctor` or trigger heap snapshots via `v8.writeHeapSnapshot()` under memory spikes to analyze heap allocation deltas."

---

## 💼 6. Production War Story (STAR Scenario)

- **Situation**: In an enterprise single-page analytics application, users reported that after leaving dashboard tabs open for 4+ hours, the browser tab froze or crashed with `Aw, Snap! Out of Memory`.
- **Task**: Identify the memory leak source, stop the tab crashes, and ensure sustained memory consumption under 150 MB.
- **Action**: We captured three sequential Chrome Heap Snapshots during tab navigation. The comparison view revealed over 1,200 `Detached HTMLCanvasElement` instances consuming 480 MB of retained memory. Investigating the retainers showed that a third-party charting library was subscribing to a custom Redux store event bus inside `useEffect`, but the cleanup return function failed to remove the subscriber. The global store retained references to old canvas DOM nodes. We added strict unsubscription teardown in `useEffect` cleanup and wrapped the cached DOM nodes in a `WeakMap`.
- **Result**: Heap memory dropped from 520 MB to a steady 85 MB over an 8-hour soak test, and zero out-of-memory browser tab crashes occurred over the next 6 months.
"""
}

def main():
    print(f"Generating {len(FILES)} Track 1 JavaScript deep dive files...")
    for path, content in FILES.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Generated: {path}")
    print("Track 1 JavaScript generation complete!")

if __name__ == "__main__":
    main()
