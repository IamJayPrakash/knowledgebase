import os

BASE_DIR = r"D:\Projects\knowledgebase"

FULL_FLEET = [
    # 01-JavaScript
    {
        "folder": "01-javascript",
        "file": "12_async_await_generators_iterators.md",
        "title": "Async/Await, Generators & Custom Iterators Under The Hood",
        "problem_stmt": "Explain how async/await works internally using Generators and Promises, and how Symbol.iterator enables custom iteration.",
        "foundation": "async/await is syntactic sugar on top of Generators (function*) and Promises. Generators yield execution, allowing functions to pause and resume state.",
        "hinglish": "async/await asal me Generators aur Promises ka combination hota hai. yield keyword function execution ko pause karta hai aur next() resume karta hai.",
        "analogy": "A book with a bookmark: you read until a difficult chapter (yield/await), place the bookmark, and resume exactly where you left off later.",
        "when_use": "When writing clean sequential asynchronous workflows without deep promise chaining.",
        "when_not": "Avoid unnecessary await inside loops when tasks can run concurrently with Promise.all.",
        "v1_title": "Sequential Await in Loop (Slow / Anti-pattern)",
        "v1_code": """// Line 1: Runs sequentially instead of concurrently! ❌
async function fetchSlow(items) {
  for (const id of items) {
    // Blocks each iteration waiting for previous network response
    await fetch('/api/data/' + id);
  }
}""",
        "v2_title": "Concurrent Promise.all with Async/Await",
        "v2_code": """// Line 1: Concurrent execution with Promise.all ✅
async function fetchFast(items) {
  const promises = items.map(id => fetch('/api/data/' + id));
  const results = await Promise.all(promises);
  return results;
}""",
        "v3_title": "Custom Iterator with Symbol.iterator & Generator",
        "v3_code": """// Line 1: Custom iterable object
const numberRange = {
  from: 1,
  to: 5,
  // Line 2: Generator function implementing Symbol.iterator
  *[Symbol.iterator]() {
    for (let val = this.from; val <= this.to; val++) {
      // Line 3: Yield pause and returns value
      yield val;
    }
  }
};

for (const num of numberRange) {
  console.log(num); // 1, 2, 3, 4, 5
}""",
        "pitch": "async/await is built on ES6 Generators and Promises. Under the hood, Babel/V8 transpiles async functions into generator functions driven by an auto-runner that calls .next() whenever the yielded promise resolves. Custom iterators implement Symbol.iterator to enable for...of traversal.",
        "star": "Sequential data fetching in a reports dashboard taking 14 seconds across 8 API endpoints.",
        "action": "Restructured sequential `await` loops into concurrent `Promise.all` batches.",
        "metrics": "Reduced report load time from 14.2s to 1.8s (87% speedup)."
    },

    {
        "folder": "01-javascript",
        "file": "14_proxy_and_reflect_api.md",
        "title": "Proxy & Reflect API: Metaprogramming & Reactivity Foundations",
        "problem_stmt": "Explain how JavaScript Proxy and Reflect objects allow intercepting and customizing fundamental language operations.",
        "foundation": "A Proxy wraps a target object, intercepting operations (get, set, has, deleteProperty) via handler traps. Reflect provides default forwarding methods.",
        "hinglish": "Proxy ek bodyguard ki tarah hai jo object ke aage khada rehta hai. Jab bhi koi property read ya write hoti hai, Proxy use pakad leta hai (jaise Vue 3 reactivity karta hai).",
        "analogy": "A security receptionist at a building entrance: every visitor must state their purpose before getting access to the building offices.",
        "when_use": "For building reactive state systems (MobX/Vue 3), schema validation, logging, and access control.",
        "when_not": "Avoid overusing for simple object access as proxies add slight micro-overhead to property access times.",
        "v1_title": "Legacy Object.defineProperty (Vue 2 Style - Limited)",
        "v1_code": """const state = {};
// Line 1: Cannot detect newly added properties or array length changes! ❌
Object.defineProperty(state, 'count', {
  get() { return 0; },
  set(v) { console.log('Updated'); }
});""",
        "v2_title": "Basic Proxy Trap",
        "v2_code": """const target = { name: 'Jay' };
const proxy = new Proxy(target, {
  get(obj, prop) {
    return prop in obj ? obj[prop] : 'Default Fallback';
  }
});""",
        "v3_title": "Production Reactive State Store using Proxy & Reflect",
        "v3_code": """// Line 1: Factory creating reactive observed state
function createObservable(target, onChange) {
  return new Proxy(target, {
    // Line 2: Intercept set operations
    set(obj, prop, value, receiver) {
      const oldValue = obj[prop];
      // Line 3: Use Reflect to execute default assignment cleanly
      const success = Reflect.set(obj, prop, value, receiver);
      if (success && oldValue !== value) {
        // Line 4: Trigger reactive subscriber callback
        onChange(prop, value);
      }
      return success;
    }
  });
}

const state = createObservable({ counter: 0 }, (prop, val) => {
  console.log(`[Auto-Reactivity]: State '${prop}' changed to ${val}`);
});

state.counter = 1; // Logs: [Auto-Reactivity]: State 'counter' changed to 1""",
        "pitch": "The Proxy object allows defining custom behaviors for fundamental operations such as property lookup, assignment, and enumeration. Paired with the Reflect API, it serves as the foundational architectural mechanism for modern reactive frameworks like Vue 3 and MobX.",
        "star": "Data mutation tracking in a rich-text collaboration canvas requiring undo/redo history.",
        "action": "Wrapped model trees in a Proxy to automatically snapshot state mutations into an undo/redo stack.",
        "metrics": "Eliminated manual tracking boilerplate across 45 canvas mutation tools."
    },

    # 02-TypeScript
    {
        "folder": "02-typescript",
        "file": "02_unions_intersections_type_guards.md",
        "title": "Unions, Intersections & Custom Type Guards (is Predicate)",
        "problem_stmt": "Explain Union types (|), Intersection types (&), and how to safely narrow types using discriminated unions and user-defined type predicates.",
        "foundation": "Union types represent values that can be one of several types. Type guards narrow down the type inside conditional blocks.",
        "hinglish": "Union ka matlab 'ya toh ye ya wo'. Type Guard (`param is Type`) compiler ko batata hai ki if-condition ke andar type narrow ho chuki hai.",
        "analogy": "A security passport check: until the officer verifies your nationality, you are an unverified traveler; once verified, you enter the designated line.",
        "when_use": "When handling diverse API responses, action dispatch payloads, and state variants.",
        "when_not": "Avoid unnecessary type assertions (`as Type`) which bypass the type checker.",
        "v1_title": "Unsafe Type Assertion (Any/As Bypass)",
        "v1_code": """// Line 1: Forcing compiler to accept type without runtime verification ❌
function handleInput(val: unknown) {
  (val as string).toUpperCase(); // Runtime crash if val is a number!
}""",
        "v2_title": "Typeof & Instanceof Narrowing",
        "v2_code": """function handleInputSafe(val: string | number) {
  if (typeof val === 'string') {
    return val.toUpperCase();
  }
  return val.toFixed(2);
}""",
        "v3_title": "Discriminated Unions & Custom Type Guard (`is` predicate)",
        "v3_code": """// Line 1: Discriminated Union with common discriminator 'status'
type SuccessResponse = { status: 'success'; data: string[] };
type ErrorResponse = { status: 'error'; message: string };
type ApiResponse = SuccessResponse | ErrorResponse;

// Line 2: User-defined Type Guard with 'is' predicate
function isSuccess(res: ApiResponse): res is SuccessResponse {
  return res.status === 'success';
}

function processResponse(res: ApiResponse) {
  // Line 3: Compiler narrows type automatically inside branch
  if (isSuccess(res)) {
    console.log(res.data.join(', ')); // Safe access to data!
  } else {
    console.error(res.message);        // Safe access to error message!
  }
}""",
        "pitch": "Unions model values that can be one of multiple types. Discriminated unions use a common literal tag to enable clean compiler narrowing. When complex object structures require validation, user-defined type guards with 'param is Type' predicates instruct TypeScript to narrow types safely at compile time without risky 'as' type casting.",
        "star": "Multi-provider payment gateway handling 4 different webhook schemas with polymorphic fields.",
        "action": "Implemented discriminated unions for payment events with custom type guards.",
        "metrics": "Eliminated 100% of runtime property access crashes across 500,000 monthly webhook events."
    },

    # 03-React
    {
        "folder": "03-react",
        "file": "02_fiber_architecture_deep_dive.md",
        "title": "React Fiber Architecture: Work Loop, Reconciliation & Double Buffering",
        "problem_stmt": "Explain how React Fiber replaced the Stack Reconciler, how it enables interruptible rendering, and how Double Buffering works.",
        "foundation": "React Fiber is a reimplementation of React's reconciliation engine. It converts the component tree into a singly-linked list of Fiber nodes.",
        "hinglish": "Fiber React ka reconciliation engine hai jo rendering work ko chhote-chhote units me tod deta hai taaki heavy render ke beech me agar user click kare toh UI freeze na ho.",
        "analogy": "A video game rendering engine: using double buffering (front buffer on screen, back buffer being calculated off-screen) to prevent tearing and screen flicker.",
        "when_use": "Understanding Fiber is crucial for debugging performance, concurrent mode (`useTransition`), and React 18/19 rendering behavior.",
        "when_not": "Fiber is internal to React; developers interact with it via hooks like `useTransition` rather than mutating Fibers directly.",
        "v1_title": "Legacy Stack Reconciler (Synchronous Blocking)",
        "v1_code": """// React 15: Traversed component tree recursively synchronously.
// Cannot pause or yield to the browser main thread! ❌""",
        "v2_title": "Fiber Node Data Structure Concept",
        "v2_code": """// A Fiber is a plain JavaScript object representing a unit of work:
const fiberNode = {
  type: 'div',
  key: null,
  child: null,       // Pointer to first child
  sibling: null,     // Pointer to next sibling
  return: null,      // Pointer to parent Fiber
  memoizedState: null, // Linked list of hooks
  alternate: null    // Pointer to double-buffer twin
};""",
        "v3_title": "Fiber Double Buffering & Concurrent Mode with useTransition",
        "v3_code": """import React, { useState, useTransition } from 'react';

function SearchResults() {
  const [query, setQuery] = useState('');
  const [list, setList] = useState([]);
  // Line 1: useTransition hook marks updates as non-urgent
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    // Urgent update: Update input box immediately (60 FPS)
    setQuery(e.target.value);

    // Line 2: Non-urgent update: Yields to browser main thread during Fiber work loop
    startTransition(() => {
      const heavyList = Array.from({ length: 10000 }, (_, i) => `${e.target.value} Item ${i}`);
      setList(heavyList);
    });
  };

  return (
    <div>
      <input value={query} onChange={handleChange} placeholder="Type fast..." />
      {isPending && <p>Filtering 10,000 items in background...</p>}
      <ul>{list.map(item => <li key={item}>{item}</li>)}</ul>
    </div>
  );
}""",
        "pitch": "React Fiber replaced the recursive Stack Reconciler with an interruptible work loop over a linked-list tree of Fiber nodes. It splits rendering into an asynchronous Render Phase (which can pause, yield, or abort) and a synchronous Commit Phase (which applies DOM updates all at once). Double buffering maintains a Current tree (on screen) and a WorkInProgress tree (off-screen) to prevent incomplete UI states.",
        "star": "Complex dashboard filtering 10,000 rows freezing the search input field for 400ms on every keystroke.",
        "action": "Adopted React 18 Concurrent Mode by wrapping the table filter update inside `useTransition`.",
        "metrics": "Keystroke input latency dropped from 400ms to 8ms; frame rate remained steady at 60 FPS."
    }
]

def generate_fleet():
    count = 0
    for item in FULL_FLEET:
        target_dir = os.path.join(BASE_DIR, item["folder"])
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, item["file"])

        content = f"""# {item['title']}

## 1. 📜 Problem / Topic Definition
{item['problem_stmt']}

---

## 2. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** {item['hinglish']}
>
> **Real-World Analogy:** {item['analogy']}

---

## 3. 🧠 Core Mechanics & Foundation (DSA / Architecture)
- **What is it:** {item['foundation']}
- **When to Use:** {item['when_use']}
- **When NOT to Use:** {item['when_not']}

---

## 4. 💻 The 3 Evolution Versions (Newbie ➡️ Intermediate ➡️ Senior)

### ❌ Version 1: {item['v1_title']}
```javascript
{item['v1_code']}
```

### ⚠️ Version 2: {item['v2_title']}
```javascript
{item['v2_code']}
```

### ✅ Version 3: {item['v3_title']}
```javascript
{item['v3_code']}
```

---

## 5. 🎯 Senior Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain {item['title'].split(':')[0]} and how you use it in production?"
>
> **You:** "{item['pitch']}"

---

## 6. 💼 Real-World Project Challenge (STAR Production Story)
* **Situation:** {item['star']}
* **Task / Challenge:** Overcoming performance bottlenecks, race conditions, or architecture fragility.
* **Action Taken:** {item['action']}
* **Result & Business Impact:** {item['metrics']}

🗣️ **Script to Tell Interviewer:**
*"In one of our core systems, {item['star'].lower()} I resolved this by {item['action'].lower()}, which {item['metrics'].lower()}."*
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"Generated fleet guide: {target_path}")

    print(f"Generated {count} full fleet concept files!")

if __name__ == "__main__":
    generate_fleet()
