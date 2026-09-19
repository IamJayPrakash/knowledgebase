import os
import re

BASE_DIR = r"D:\Projects\knowledgebase"

# Master Registry of all topics and files to generate across all folders
REGISTRY = {
    # ==================== 01-JAVASCRIPT ====================
    "01-javascript": [
        ("01_data_types_and_type_coercion.md", "JavaScript Data Types, Primitive vs Reference & Type Coercion",
         "Primitives value se copy hote hain (number, string, boolean, null, undefined, symbol, bigint), jabki objects aur arrays reference (memory address) se pass hote hain.",
         "Buying a printed book (primitive: copying it doesn't change original) vs sharing a Google Doc link (reference: edits reflect for everyone).",
         ["7 Primitive types stored on Stack vs Object references stored on Heap.",
          "Type coercion occurs with `==` (implicit conversion); `===` strictly checks value and type.",
          "`typeof null === 'object'` is a legacy historical JavaScript bug.",
          "`NaN !== NaN`, use `Number.isNaN()` to verify true NaN values."],
         "[Stack Memory: Primitives] ──> a = 10, b = 10\n[Heap Memory: Objects]       ──> obj1 ──┐\n                                         ├──> { name: 'Jay' }\n                                 obj2 ──┘",
         """// Line 1: Primitive assignment copies value
let a = 42;
// Line 2: Modifying b does not affect a
let b = a;
b = 99;
console.log(a, b); // 42, 99

// Line 3: Object reference assignment
const user1 = { name: 'Jay' };
// Line 4: user2 references the exact same memory address on the Heap
const user2 = user1;
user2.name = 'Prakash';
console.log(user1.name); // 'Prakash' (Mutated via shared reference!)

// Line 5: Type Coercion Quirks
console.log(1 + '2');    // '12' (Number coerced to string)
console.log(1 - '2');    // -1   (String coerced to number)
console.log(Boolean('')); // false (Falsy value)
console.log(Boolean(' ')); // true  (Non-empty string is truthy)""",
         "JavaScript has primitive and reference types. Primitives are immutable and stored on the stack, while reference types live on the heap. Loose equality triggers type coercion while strict equality compares without conversion. Always use strict equality and explicit conversions.",
         "E-commerce cart calculations failing due to string concatenation when price query parameters came as strings ('100' + 20 = '10020').",
         "Sanitized all incoming request inputs using explicit `Number.parseFloat()` casting and automated schema validation.",
         "Prevented cart billing errors across 80,000 daily checkouts with 100% calculation accuracy."),

        ("02_var_let_const_hoisting_tdz.md", "var vs let vs const, Hoisting & Temporal Dead Zone (TDZ)",
         "var function-scoped hota hai aur hoist hokar undefined initialize ho jata hai. let aur const block-scoped hote hain aur declaration se pehle unhe access karne par ReferenceError aata hai (TDZ).",
         "Announcing a meeting without setting an agenda (var = undefined) vs reserving a conference room where you cannot enter until the start time (let/const in TDZ).",
         ["`var` is function-scoped and re-declarable; hoisted and initialized with `undefined`.",
          "`let` and `const` are block-scoped (`{}`); hoisted into the Temporal Dead Zone (TDZ) without initialization.",
          "Accessing `let` or `const` in TDZ throws a `ReferenceError`.",
          "`const` prevents reassignment of the variable binding, but object properties can still be mutated."],
         "[Code Execution Flow]\n├── Start Block: { <--- TDZ begins for let/const\n│   ├── Accessing 'x' here throws ReferenceError! (TDZ)\n├── let x = 50; <--- TDZ ends, variable initialized\n└── Accessing 'x' here is safe! Output: 50",
         """// Line 1: Hoisting behavior with var
console.log(hoistedVar); // Output: undefined (Hoisted & initialized)
var hoistedVar = 'I am var';

// Line 2: Temporal Dead Zone with let
try {
  // Line 3: Accessing before declaration triggers TDZ ReferenceError
  console.log(tdzLet);
  let tdzLet = 'I am let';
} catch (err) {
  console.error(err.name); // "ReferenceError: Cannot access 'tdzLet' before initialization"
}

// Line 4: Block Scope Demonstration
{
  var globalVar = 100;
  let blockScoped = 200;
}
console.log(globalVar);   // 100 (Leaked outside block!)
// console.log(blockScoped); // ReferenceError: blockScoped is not defined""",
         "The fundamental differences are scoping and hoisting. var is function-scoped and initialized as undefined during hoisting. let and const are block-scoped and hoisted into the Temporal Dead Zone until initialized. const prevents binding re-assignment. Modern JavaScript standardizes on const by default and let when re-assignment is needed.",
         "Asynchronous analytics tracking loops with `var i` logging the final loop index for all delayed timers.",
         "Replaced `var` with block-scoped `let`, creating an individual lexical binding for each loop iteration.",
         "Fixed index reporting bugs on 1.4 million logged user interaction events."),

        ("03_functions_first_class_higher_order.md", "First-Class Functions, Higher-Order Functions & Currying",
         "JavaScript me functions first-class citizens hote hain: unhe variables me store kar sakte hain, doosre functions me pass kar sakte hain, aur return kar sakte hain.",
         "A musical instrument: you can hold it (variable), pass it to a friend (argument), or build an entire orchestra that creates new instruments (higher-order function).",
         ["First-Class: Functions treated like any other variable/value.",
          "Higher-Order Function (HOF): A function that accepts another function as an argument (`map`, `filter`) or returns a function.",
          "Pure Functions: Deterministic, no side-effects, given same input always returns same output.",
          "Currying: Translating a function callable as `f(a, b, c)` into callable as `f(a)(b)(c)`."],
         "[Function: add(a, b, c)]\n            │ Currying Transformation\n            ▼\n[add(a)] ──> Returns function(b) ──> Returns function(c) ──> a + b + c",
         """// Line 1: Currying implementation supporting arbitrary arguments
function curry(fn) {
  // Line 2: Return wrapper collecting arguments
  return function curried(...args) {
    // Line 3: If enough arguments collected, execute original function
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    // Line 4: Otherwise, return a new function collecting remaining arguments
    return function(...nextArgs) {
      return curried.apply(this, [...args, ...nextArgs]);
    };
  };
}

// Line 5: Standard function taking 3 arguments
const sumThree = (a, b, c) => a + b + c;
// Line 6: Curried version
const curriedSum = curry(sumThree);

console.log(curriedSum(1)(2)(3)); // 6
console.log(curriedSum(1, 2)(3)); // 6""",
         "JavaScript treats functions as first-class citizens, meaning they can be assigned to variables, passed as arguments, and returned from other functions. Higher-Order Functions like map, filter, and reduce abstract data transformations. Currying breaks multi-argument functions into unary function chains, enabling reusable function composition.",
         "Reusable API logger and authorization decorator wrapping diverse microservice route handlers.",
         "Implemented a higher-order function pipeline composing authentication, logging, and error wrappers.",
         "Reduced boilerplate code by 40% across 65 backend endpoints."),

        ("04_execution_context_call_stack.md", "Execution Context, Call Stack & Variable Environment",
         "Jab bhi JS code run hota hai, Global Execution Context banta hai jisme do phases hote hain: Memory Creation Phase (variables allocate hote hain) aur Code Execution Phase (code line-by-line execute hota hai).",
         "A chef preparing a recipe: first laying out all the spices and bowls on the counter (creation phase), then cooking and stirring step-by-step (execution phase).",
         ["Global Execution Context (GEC) is created by default when script loads.",
          "Creation Phase: Memory allocated for variables (`undefined`) and functions (entire definition copied).",
          "Execution Phase: Code executed line by line, assigning real values to variables.",
          "Call Stack: LIFO (Last In First Out) structure tracking which function execution context is active.",
          "Maximum Call Stack Size Exceeded: Triggered by infinite recursion without base cases."],
         "[Call Stack]\n│  Third Function Context  │ (Top - Executing now)\n│  Second Function Context │\n│  First Function Context  │\n│  Global Execution Context│ (Bottom - Persistent)\n└──────────────────────────┘",
         """// Line 1: Demonstrating Execution Context Creation vs Execution Phases
console.log(sampleVar); // undefined (Memory allocated during Creation Phase)
sampleFunc();           // "Hello from Execution Phase" (Hoisted completely!)

var sampleVar = 100;

function sampleFunc() {
  // Line 2: New Functional Execution Context created on top of Call Stack
  const localVal = 50;
  console.log("Hello from Execution Phase", localVal);
}

// Line 3: Stack Overflow Demonstration
function infiniteRecursion() {
  // Line 4: Missing base case pushes infinite frames onto call stack
  return infiniteRecursion();
}
// infiniteRecursion(); // Uncaught RangeError: Maximum call stack size exceeded""",
         "JavaScript executes code inside Execution Contexts managed by a single-threaded Call Stack. Each context undergoes a Creation Phase where memory is allocated for variables and functions, followed by an Execution Phase where code runs line-by-line. When a function returns, its frame is popped from the stack.",
         "Deep nested tree traversal algorithm for a folder structure causing stack overflow on large enterprise directories.",
         "Refactored recursive DFS traversal into an iterative queue-based BFS algorithm using heap memory.",
         "Processed 250,000 deep directory nodes with zero stack overflow exceptions."),

        ("06_v8_memory_garbage_collection.md", "V8 Engine Memory Lifecycle & Garbage Collection Mechanics",
         "V8 heap memory ko do hisson me divide karta hai: Young Generation (naye objects - Scavenge GC) aur Old Generation (lambe chalne wale objects - Mark-Sweep-Compact).",
         "Waste management: small daily kitchen trash is emptied multiple times a day (Scavenger GC), while heavy furniture/garage junk is audited and recycled once a year (Mark-Sweep).",
         ["Young Generation: Subdivided into Eden, From Space, and To Space using the fast Cheney Scavenge algorithm.",
          "Object Promotion: Objects that survive two GC cycles are promoted to the Old Generation.",
          "Old Generation: Collected using Mark-Sweep-Compact to avoid heap fragmentation.",
          "Orphaned References: Memory leaks occur when objects remain reachable from root objects (window/global) unintentionally."],
         "[V8 Heap Memory]\n├── Young Generation (1-64MB)\n│   ├── Eden Space\n│   └── Survivor (From & To Space) ──(Survives 2 cycles)──┐\n└── Old Generation (Up to 1.4GB - 4GB) <─────────────────┘\n    ├── Mark Phase: Trace reachable nodes from GC Roots\n    ├── Sweep Phase: Reclaim memory from un-marked nodes\n    └── Compact Phase: Defragment contiguous memory blocks",
         """// Memory Leak Scenario vs Garbage Collection Clean-up
let heavyCache = [];

function simulateLeak() {
  // Line 1: Global array retains memory indefinitely (Not garbage collected!)
  const largeBuffer = new Array(1000000).fill('leak_data');
  heavyCache.push(largeBuffer);
}

function cleanMemory() {
  // Line 2: Disconnecting references allows Mark-and-Sweep GC to reclaim memory
  heavyCache = null;
}

simulateLeak();
cleanMemory(); // Memory freed during next GC cycle!""",
         "V8 employs a generational garbage collector based on the weak generational hypothesis: most objects die young. Young generation objects are rapidly collected via Scavenger algorithms. Surviving objects migrate to Old Generation, where Mark-Sweep-Compact runs concurrently and incrementally to avoid blocking the main JavaScript thread.",
         "Real-time WebSocket market ticker dashboard browser memory steadily growing by 30MB/minute, crashing tabs after 2 hours.",
         "Used Chrome DevTools Allocation Timeline to isolate uncleared object maps retained by dead WebSocket listeners, adding explicit cleanup handlers on socket close.",
         "Completely eliminated memory drift, maintaining steady 38MB RAM usage across 24-hour sessions.")
    ],

    # ==================== 01-JAVASCRIPT / INTERVIEW-QUESTIONS ====================
    "01-javascript/interview-questions": [
        ("coding_polyfill_promise_all.md", "Machine Coding: Implement Promise.all Polyfill from Scratch",
         "Promise.all saare promises ko parallel me run karta hai aur tabhi resolve hota hai jab saare resolve ho jayein. Agar ek bhi reject hua, toh turant reject ho jata hai.",
         "A team relay race: the team only wins when the last runner crosses the finish line. If any runner drops the baton, the race ends immediately.",
         ["Takes an iterable of promises and returns a single Promise.",
          "Resolves with an array of resolved values in the original input order.",
          "Rejects immediately upon the first promise rejection (Fail-Fast behavior).",
          "Handles non-promise values by wrapping them with `Promise.resolve()`."],
         "[Promise 1 (200ms)] ──┐\n[Promise 2 (100ms)] ──┼──> [Promise.all Counter == Total] ──> Resolves [Val1, Val2, Val3]\n[Promise 3 (300ms)] ──┘",
         """// Polyfill for Promise.all
// Line 1: Define polyfill accepting an array of promises or values
function promiseAllPolyfill(promises) {
  // Line 2: Return a new Promise
  return new Promise((resolve, reject) => {
    // Line 3: Validate input is an array
    if (!Array.isArray(promises)) {
      return reject(new TypeError('Argument must be an array'));
    }
    
    const results = [];
    let completedCount = 0;
    
    // Line 4: Edge case - empty array resolves immediately with empty array
    if (promises.length === 0) {
      return resolve(results);
    }
    
    // Line 5: Loop through each promise with its index
    promises.forEach((promise, index) => {
      // Line 6: Wrap with Promise.resolve() to handle primitive non-promise values
      Promise.resolve(promise)
        .then((val) => {
          // Line 7: Store result at original index (preserves input order!)
          results[index] = val;
          completedCount++;
          
          // Line 8: If all promises resolved, resolve the outer promise
          if (completedCount === promises.length) {
            resolve(results);
          }
        })
        .catch((err) => {
          // Line 9: Fail-fast: reject immediately on first error
          reject(err);
        });
    });
  });
}

// Test Verification
const p1 = Promise.resolve(10);
const p2 = new Promise((res) => setTimeout(() => res(20), 100));
const p3 = 30; // Non-promise primitive

promiseAllPolyfill([p1, p2, p3]).then(console.log); // Output: [10, 20, 30]""",
         "Promise.all coordinates concurrent asynchronous operations. It resolves when all input promises resolve, preserving the original array order regardless of execution completion time, and fails fast if any promise rejects. We implement this by wrapping elements in Promise.resolve, tracking an incremental completion counter, and storing results by input index.",
         "Batching independent third-party KYC verification API calls in an onboarding pipeline where legacy code was executing them sequentially.",
         "Aggregated calls using Promise.all polyfill with bounded timeout wrappers.",
         "Decreased user onboarding latency from 4.8 seconds to 920 milliseconds (80% faster)."),

        ("coding_debounce_and_throttle.md", "Machine Coding: Implement Debounce and Throttle from Scratch",
         "Debounce tab tak wait karta hai jab tak user bolna band na kar de (typing/search). Throttle ek fixed interval me sirf ek baar chalne deta hai chahe kitni bhi events fire hon (scrolling/resizing).",
         "Debounce is an elevator waiting for people to stop walking in before closing. Throttle is a train leaving the station strictly every 10 minutes.",
         ["Debounce: Delays execution until N milliseconds of silence after the last event.",
          "Throttle: Guarantees execution at most once every N milliseconds.",
          "Debounce use-cases: Search bar autocomplete, window resize recalculation, auto-saving drafts.",
          "Throttle use-cases: Window scroll listeners, infinite scroll triggers, game firing rates."],
         "[Debounce] Events: ||||||| ──(wait 300ms)──> [Execute Action]\n[Throttle] Events: ||||||||||||||||||||| ──> [Exec] ──300ms──> [Exec] ──300ms──> [Exec]",
         """// Line 1: Debounce Implementation
function debounce(fn, delay) {
  let timerId = null;
  return function(...args) {
    // Line 2: Clear existing timer on every new trigger
    if (timerId) clearTimeout(timerId);
    // Line 3: Set new timer to execute after quiet period
    timerId = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

// Line 4: Throttle Implementation
function throttle(fn, limit) {
  let inThrottle = false;
  return function(...args) {
    // Line 5: If not cooling down, execute immediately and enter throttle cooldown
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      // Line 6: Reset cooldown flag after limit duration
      setTimeout(() => {
        inThrottle = false;
      }, limit);
    }
  };
}""",
         "Debounce postpones execution until a specified delay has elapsed since the last invocation, ideal for search inputs. Throttle enforces a maximum execution frequency over time, ideal for high-frequency events like scroll and mouse movements. Both utilize closures to maintain timer states.",
         "Window scroll listener calculating reading progress percentage recalculating layout on every scroll pixel, freezing mobile browser rendering.",
         "Throttled the scroll event handler to 100ms and debounced subsequent analytics beacon events.",
         "Eliminated UI frame drops, raising scrolling performance from 18 FPS to a solid 60 FPS.")
    ],

    # ==================== 02-TYPESCRIPT ====================
    "02-typescript": [
        ("01_basic_types_any_unknown_never.md", "TypeScript Types: any vs unknown vs never & Exhaustiveness Checking",
         "any type-checking band kar deta hai (unsafe). unknown safe any hai jisme use karne se pehle type check karna padta hai. never un values ko represent karta hai jo kabhi exist hi nahi kar sakti.",
         "any is an unlocked door with no guard. unknown is a locked vault where you must present ID before entering. never is an impossible black hole that can never be reached.",
         ["`any` completely disables compiler type checks (escapes the type system).",
          "`unknown` accepts any value, but forces type narrowing/guards before performing operations.",
          "`never` represents functions that throw or never return, and exhaustive switch-case validation.",
          "Exhaustive Checking: Using `never` in default cases guarantees compile errors when new union variants are added."],
         "[Type Hierarchy]\nTop Type:    unknown / any (Accepts all values)\n               │\nMid Types:   string | number | boolean | objects\n               │\nBottom Type: never (No value can be assigned to never)",
         """// Line 1: any vs unknown demonstration
let anyVal: any = "hello";
anyVal.nonExistentMethod(); // Compiles fine, crashes at runtime! ❌

let unknownVal: unknown = "hello";
// unknownVal.toUpperCase(); // Compile Error! Must narrow type first ✅

// Line 2: Safe type narrowing with unknown
if (typeof unknownVal === "string") {
  console.log(unknownVal.toUpperCase()); // Safe!
}

// Line 3: Exhaustive Checking with never
type PaymentMethod = "credit_card" | "paypal" | "crypto";

function processPayment(method: PaymentMethod) {
  switch (method) {
    case "credit_card": return "Processed Card";
    case "paypal": return "Processed PayPal";
    case "crypto": return "Processed Crypto";
    default:
      // Line 4: If a new method is added to PaymentMethod, this line causes compile error!
      const _exhaustiveCheck: never = method;
      return _exhaustiveCheck;
  }
}""",
         "any disables the type checker, while unknown requires explicit type narrowing before usage, maintaining full type safety. never represents impossible values and unreachable code. We use never in union switch-cases to enforce exhaustive checking, catching unhandled cases at compile time.",
         "API response parser crashing on unanticipated null fields because types were typed as `any`.",
         "Refactored all untrusted network JSON payloads to `unknown` and validated with Zod/Pydantic schemas.",
         "Eliminated 100% of production runtime `TypeError: undefined is not a function` bugs.")
    ],

    # ==================== 03-REACT ====================
    "03-react": [
        ("04_state_hooks_usestate_usereducer.md", "React State Hooks: useState & useReducer Under The Hood",
         "React me hooks internally ek linked list node hote hain jo Fiber component ke memoizedState par attach hote hain. Isliye hooks ko loops ya if conditions me call karna mana hai taaki linked list order break na ho.",
         "A train of passenger cars linked in sequence: if passengers switch cars randomly (calling hooks inside if/else), the ticket inspector loses track of who belongs where.",
         ["Hook LinkedList: Component's Fiber stores hooks as a singly-linked list (`memoizedState -> next -> next`).",
          "Rules of Hooks: Call hooks only at top-level; never in loops, conditions, or nested functions.",
          "State Updates Batching: React 18 automatically batches state updates across async events, promises, and timeouts.",
          "`useReducer` vs `useState`: `useState` is built on top of `useReducer` internally; use `useReducer` for complex interdependent state transitions."],
         "[Component Fiber]\n       │\n       ▼ memoizedState\n[Hook 1: useState(count)] ──> [Hook 2: useEffect()] ──> [Hook 3: useState(name)] ──> null",
         """// Functional State Updates vs Stale Closures
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  const handleIncorrectBatch = () => {
    // Line 1: Stale closure traps count as 0!
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1); // Result: count becomes 1, NOT 3! ❌
  };

  const handleCorrectBatch = () => {
    // Line 2: Functional state updates receive the guaranteed latest state
    setCount(prev => prev + 1);
    setCount(prev => prev + 1);
    setCount(prev => prev + 1); // Result: count becomes 3! ✅
  };

  return (
    <div>
      <h3>Count: {count}</h3>
      <button onClick={handleCorrectBatch}>Increment Safe (+3)</button>
    </div>
  );
}""",
         "React hooks rely on deterministic call order tracked by an internal singly-linked list on the Fiber node. This is why hooks must only be called at the top level. In React 18, state updates are automatically batched across all microtasks and event handlers. For multiple sequential updates, functional state updaters ensure access to the latest state value.",
         "Multi-step checkout modal displaying stale shipping prices due to sequential `setState` calls reading stale closure values.",
         "Refactored complex checkout state to a `useReducer` state machine with functional dispatch transitions.",
         "Completely eliminated race conditions and price mismatch bugs on order checkout.")
    ]
}

def generate_all():
    count = 0
    for folder, files in REGISTRY.items():
        base_target = os.path.join(BASE_DIR, folder)
        os.makedirs(base_target, exist_ok=True)
        
        for file_info in files:
            fname, title, hinglish, analogy, points, diagram, code, pitch, star, action, metrics = file_info
            target_path = os.path.join(base_target, fname)
            
            points_md = "\n".join([f"- {p}" for p in points])
            
            content = f"""# {title}

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** {hinglish}
>
> **Real-World Analogy:** {analogy}

---

## 2. 📌 Core Mechanics & Key Points
{points_md}

---

## 3. 📊 Visual Architecture Diagram

```text
{diagram}
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
{code}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain {title.split(':')[0]} and your production experience with it?"
>
> **You:** "{pitch}"

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** {star}
* **Task / Challenge:** Overcoming performance bottlenecks, race conditions, or architecture fragility under scale.
* **Action Taken:** {action}
* **Result & Business Impact:** {metrics}

🗣️ **Script to Tell Interviewer:**
*"In our production systems, {star.lower()} I took charge of the architecture by {action.lower()}, successfully achieving {metrics.lower()}."*
"""
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            print(f"[{count}] Generated: {target_path}")

    print(f"Total {count} foundational files generated successfully!")

if __name__ == "__main__":
    generate_all()
