import os
import re

BASE_DIR = r"D:\Projects\knowledgebase"

# Comprehensive content dictionary for all missing files in 01-javascript, 02-typescript, 03-react, 04-node, 05-fastapi, 06-ai-genai, 07-system-design
MASTER_TOPICS = [
    # JAVASCRIPT
    {
        "folder": "01-javascript",
        "file": "05_closures_and_lexical_scope.md",
        "title": "JavaScript Closures, Lexical Scope & Practical Use Cases",
        "problem_stmt": "Explain how lexical scoping works in JavaScript, how closures are formed in memory, and how to use them for data encapsulation, currying, and memoization.",
        "foundation": "What is Lexical Scope? Scope is defined by the physical location of variables in the code. A Closure is a function bundled together with references to its surrounding lexical state.",
        "hinglish": "Inner function apne parent function ke variables ko yaad rakhta hai, chahe parent function execute hokar stack se hat chuka ho.",
        "analogy": "A student carrying a backpack everywhere: when leaving the house, the lunchbox stays in the backpack.",
        "when_use": "When you need private variables, function factories, memoization, or custom event listeners.",
        "when_not": "When holding large DOM elements or heavy objects without cleanup, as this causes memory leaks.",
        "v1_title": "Naive Global Variable (Pollutes Global Scope)",
        "v1_code": """// Line 1: Global variable accessible and mutable by any script
var counter = 0;

function increment() {
  // Line 2: Modifies global variable directly (Unsafe in enterprise applications!)
  counter++;
  return counter;
}""",
        "v2_title": "Object-Oriented Property (Exposed on Instance)",
        "v2_code": """// Line 1: Class with property
class CounterClass {
  constructor() {
    // Line 2: Exposed property can be overwritten from outside: instance.count = 999
    this.count = 0;
  }
  increment() {
    return ++this.count;
  }
}""",
        "v3_title": "Senior Production Closure with True Data Privacy & Memoization",
        "v3_code": """// Line 1: Factory function creating an encapsulated closure
function createPrivateCounter(initialValue = 0) {
  // Line 2: Private state stored in V8 Heap via closure
  let _count = initialValue;

  return {
    // Line 3: Getter method reading private variable
    get value() {
      return _count;
    },
    // Line 4: Safe increment operation
    increment: function() {
      _count += 1;
      return _count;
    },
    // Line 5: Safe decrement operation
    decrement: function() {
      _count -= 1;
      return _count;
    }
  };
}

const counter = createPrivateCounter(10);
console.log(counter.increment()); // 11
console.log(counter.increment()); // 12
console.log(counter._count);       // undefined (Completely private!)""",
        "pitch": "A closure is a function bundled together with references to its surrounding lexical environment. V8 allocates closed-over variables on the heap instead of the stack. We use closures for data encapsulation and memoization, while taking care to avoid memory leaks by nullifying unneeded references.",
        "star": "Memory leak in a single page dashboard where long-running closures retained old charting datasets.",
        "action": "Audited closures using Chrome DevTools Heap Snapshots and explicitly nulled references on unmount.",
        "metrics": "Eliminated 450MB of leaked memory; stabilized browser memory at 35MB."
    },

    {
        "folder": "01-javascript",
        "file": "07_this_keyword_and_binding.md",
        "title": "The 'this' Keyword: 5 Binding Rules, Call, Apply, Bind & Arrow Functions",
        "problem_stmt": "Explain how the 'this' keyword is evaluated in JavaScript, the 5 rules of binding, and how arrow functions differ.",
        "foundation": "The 'this' keyword is an execution context reference determined at call-site (how a function is called, not where it is defined).",
        "hinglish": "'this' call-time par decide hota hai. Iske 5 rules hote hain: default, implicit, explicit, new, aur arrow functions.",
        "analogy": "The word 'my house': depending on who says it, it refers to a completely different home address.",
        "when_use": "When writing reusable methods, object-oriented prototypes, or event handlers.",
        "when_not": "Avoid using regular functions where lexical scope is required (use arrow functions instead).",
        "v1_title": "Unbound Callback Losing Context",
        "v1_code": """const user = {
  name: 'Jay',
  greet: function() {
    // Line 1: Passing as callback detaches 'this' from user object!
    setTimeout(function() {
      console.log('Hello, ' + this.name); // 'Hello, undefined' (this = window/global) ❌
    }, 100);
  }
};
user.greet();""",
        "v2_title": "Self Variable Hack (Legacy Pattern)",
        "v2_code": """const userLegacy = {
  name: 'Jay',
  greet: function() {
    // Line 1: Storing reference to this manually in local variable
    var self = this;
    setTimeout(function() {
      console.log('Hello, ' + self.name); // 'Hello, Jay' ✅
    }, 100);
  }
};""",
        "v3_title": "Modern Lexical Arrow Functions & Explicit Binding Polyfill",
        "v3_code": """// Line 1: Modern Arrow Function inherits 'this' lexically
const userModern = {
  name: 'Jay',
  greet: function() {
    // Line 2: Arrow function does NOT have its own this; inherits outer this
    setTimeout(() => {
      console.log('Hello, ' + this.name); // 'Hello, Jay' ✅
    }, 100);
  }
};

// Line 3: Function.prototype.bind polyfill
Function.prototype.myBind = function(context, ...boundArgs) {
  const fn = this;
  return function(...args) {
    return fn.apply(context, [...boundArgs, ...args]);
  };
};""",
        "pitch": "The 'this' keyword is determined at call-time by 5 rules: new binding, explicit binding (call/apply/bind), implicit object binding, and default global binding. Arrow functions do not bind their own 'this' and lexically inherit it from their enclosing scope.",
        "star": "React class component event handler losing context and crashing during user submit.",
        "action": "Converted event handlers to arrow function class fields and bound callbacks explicitly in constructors.",
        "metrics": "Resolved 100% of runtime TypeError exceptions on client forms."
    },

    {
        "folder": "01-javascript",
        "file": "08_prototypes_and_inheritance.md",
        "title": "JavaScript Prototypes, Prototype Chain & Prototypal Inheritance",
        "problem_stmt": "Explain how prototype chaining works, the difference between __proto__ and prototype, and how inheritance operates.",
        "foundation": "Objects in JavaScript link to fallback prototype objects via an internal [[Prototype]] link (__proto__).",
        "hinglish": "Agar object ke paas property nahi hai, toh wo apne prototype par dekhega, fir uske prototype par, jab tak Object.prototype (null) na aa jaye.",
        "analogy": "Looking for tools in a workshop: if not on your bench, you check your team shelf, then the master warehouse.",
        "when_use": "When sharing methods across thousands of instances to conserve memory.",
        "when_not": "When deep cloning or modifying built-in prototypes like Array.prototype (monkey patching is an anti-pattern).",
        "v1_title": "Defining Methods Inside Constructor (Wasteful Memory)",
        "v1_code": """function User(name) {
  this.name = name;
  // Line 1: Method duplicated in memory for every single instance! ❌
  this.sayHi = function() { return 'Hi ' + this.name; };
}""",
        "v2_title": "Manual Object.create Linking",
        "v2_code": """// Line 1: Base prototype object
const animal = {
  walk: function() { return 'Walking'; }
};
// Line 2: Create new object with animal as prototype
const dog = Object.create(animal);
dog.bark = function() { return 'Woof'; };""",
        "v3_title": "Optimized Prototype Chain Inheritance",
        "v3_code": """// Line 1: Parent Constructor
function Person(name) {
  this.name = name;
}
// Line 2: Attach method to prototype so all 100,000 instances share 1 copy in RAM
Person.prototype.getName = function() {
  return this.name;
};

// Line 3: Child Constructor
function Employee(name, title) {
  Person.call(this, name); // Super call
  this.title = title;
}
// Line 4: Link prototype chains
Employee.prototype = Object.create(Person.prototype);
Employee.prototype.constructor = Employee;

const dev = new Employee('Jay', 'Lead Architect');
console.log(dev.getName()); // 'Jay'""",
        "pitch": "JavaScript utilizes prototypal inheritance. Objects inherit properties via their internal [[Prototype]] chain. Methods defined on Constructor.prototype are shared across all instances, dramatically reducing heap allocation.",
        "star": "Data grid rendering 50,000 table rows consuming 180MB RAM due to method duplication.",
        "action": "Migrated row instance methods to prototype definition.",
        "metrics": "Reduced memory footprint by 88% (180MB down to 22MB)."
    },

    {
        "folder": "01-javascript",
        "file": "10_event_loop_microtasks_macrotasks.md",
        "title": "JavaScript Event Loop: Call Stack, Microtasks & Macrotasks",
        "problem_stmt": "Explain how the JavaScript Event Loop coordinates synchronous execution, Microtask queue, Macrotask queue, and rendering.",
        "foundation": "JavaScript is single-threaded. The Event Loop continuously checks if the Call Stack is empty; when empty, it drains the Microtask queue completely before running the next Macrotask.",
        "hinglish": "Call Stack khali hone par pehle saare Microtasks (Promises) khatam kiye jaate hain, uske baad ek Macrotask (setTimeout) uthaya jata hai.",
        "analogy": "A hospital emergency room: critical trauma patients (Microtasks) are treated immediately before general appointment checkups (Macrotasks).",
        "when_use": "When scheduling asynchronous I/O, background tasks, or debouncing renders.",
        "when_not": "Never create infinite microtask loops (queueMicrotask recursion) as it will starve macrotasks and freeze the UI.",
        "v1_title": "Blocking Synchronous Loop (Freezes Browser)",
        "v1_code": """// Line 1: Blocks the single JavaScript thread for 5 seconds! ❌
function freezeThread() {
  const start = Date.now();
  while (Date.now() - start < 5000) {
    // UI cannot click, scroll, or repaint
  }
}""",
        "v2_title": "Chunking with setTimeout (Macrotask)",
        "v2_code": """// Line 1: Breaks work into chunks via setTimeout
function processChunks(items) {
  if (items.length === 0) return;
  const chunk = items.splice(0, 100);
  // Process chunk...
  setTimeout(() => processChunks(items), 0); // Yields back to event loop
}""",
        "v3_title": "Precise Microtask vs Macrotask Execution Order",
        "v3_code": """console.log('1: Sync Start');

// Line 1: Macrotask queued
setTimeout(() => {
  console.log('2: Macrotask setTimeout');
}, 0);

// Line 2: Microtask queued
Promise.resolve().then(() => {
  console.log('3: Microtask 1');
}).then(() => {
  console.log('4: Microtask 2');
});

// Line 3: queueMicrotask explicitly queued
queueMicrotask(() => {
  console.log('5: Microtask 3');
});

console.log('6: Sync End');

// Expected Output: 1, 6, 3, 5, 4, 2""",
        "pitch": "The Event Loop enables non-blocking asynchronous execution. After the Call Stack empties, the microtask queue (Promises, queueMicrotask) is drained completely before the browser repaints or executes the next macrotask (setTimeout, I/O).",
        "star": "UI freezing during parsing of massive 50MB JSON datasets on client browser.",
        "action": "Chunked processing using Web Workers and requestIdleCallback yielding to the Event Loop.",
        "metrics": "Eliminated UI jank, maintaining 60 FPS during background parsing."
    },

    {
        "folder": "01-javascript",
        "file": "11_promises_deep_dive.md",
        "title": "Promises Deep Dive: States, Chaining & Combinators (all, allSettled, race, any)",
        "problem_stmt": "Explain Promise states, error propagation, and differences between Promise.all, Promise.allSettled, Promise.race, and Promise.any.",
        "foundation": "A Promise represents an eventual completion (or failure) of an asynchronous operation and its resulting value.",
        "hinglish": "Promise 3 states me hota hai: Pending, Fulfilled, Rejected. Promise.all sabke success par chalta hai, allSettled sabke finish hone par chalta hai chahe fail ho.",
        "analogy": "A food delivery order: Pending while cooking, Fulfilled when delivered, Rejected if out of stock.",
        "when_use": "For all asynchronous network, disk, or timer operations.",
        "when_not": "Do not mix callbacks and promises without wrapping in Promise constructors.",
        "v1_title": "Callback Hell (Pyramid of Doom)",
        "v1_code": """// Line 1: Deeply nested callbacks (Unmaintainable!) ❌
getUser(userId, (user) => {
  getOrders(user.id, (orders) => {
    getOrderDetails(orders[0].id, (details) => {
      console.log(details);
    });
  });
});""",
        "v2_title": "Linear Promise Chaining",
        "v2_code": """// Line 1: Clean linear promise chain
getUser(userId)
  .then(user => getOrders(user.id))
  .then(orders => getOrderDetails(orders[0].id))
  .catch(err => console.error('Error in chain:', err));""",
        "v3_title": "The 4 Promise Combinators Comparison",
        "v3_code": """const p1 = Promise.resolve('A');
const p2 = Promise.reject('Error in B');
const p3 = Promise.resolve('C');

// 1. Promise.all: Fails fast on first rejection
Promise.all([p1, p3]).then(console.log); // ['A', 'C']

// 2. Promise.allSettled: Never rejects; returns status objects for all
Promise.allSettled([p1, p2, p3]).then(results => {
  // results = [{status: 'fulfilled', value: 'A'}, {status: 'rejected', reason: '...'}, ...]
  console.log('All completed regardless of failure');
});

// 3. Promise.race: Returns the fastest settled promise (fulfilled or rejected)
// 4. Promise.any: Returns the fastest FULFILLED promise (ignores rejections)""",
        "pitch": "Promises provide structured asynchronous composition. Promise.all fails fast on first rejection. Promise.allSettled waits for all promises to resolve or reject, making it ideal for independent batch jobs. Promise.race returns the first settled promise, and Promise.any returns the first successfully fulfilled promise.",
        "star": "Microservice dashboard failing entirely if a single non-critical third-party weather widget failed.",
        "action": "Replaced `Promise.all` with `Promise.allSettled` to display partial dashboard widgets gracefully.",
        "metrics": "Increased dashboard availability from 94.2% to 99.98%."
    }
]

def generate_master_topics():
    count = 0
    for topic in MASTER_TOPICS:
        target_dir = os.path.join(BASE_DIR, topic["folder"])
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, topic["file"])

        content = f"""# {topic['title']}

## 1. 📜 Problem / Topic Definition
{topic['problem_stmt']}

---

## 2. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** {topic['hinglish']}
>
> **Real-World Analogy:** {topic['analogy']}

---

## 3. 🧠 Core Mechanics & Foundation (DSA / Architecture)
- **What is it:** {topic['foundation']}
- **When to Use:** {topic['when_use']}
- **When NOT to Use:** {topic['when_not']}

---

## 4. 💻 The 3 Evolution Versions (Newbie ➡️ Intermediate ➡️ Senior)

### ❌ Version 1: {topic['v1_title']}
```javascript
{topic['v1_code']}
```

### ⚠️ Version 2: {topic['v2_title']}
```javascript
{topic['v2_code']}
```

### ✅ Version 3: {topic['v3_title']}
```javascript
{topic['v3_code']}
```

---

## 5. 🎯 Senior Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "Can you explain {topic['title'].split(':')[0]} and how you use it in production?"
>
> **You:** "{topic['pitch']}"

---

## 6. 💼 Real-World Project Challenge (STAR Production Story)
* **Situation:** {topic['star']}
* **Task / Challenge:** Overcoming performance bottlenecks, race conditions, or architecture fragility.
* **Action Taken:** {topic['action']}
* **Result & Business Impact:** {topic['metrics']}

🗣️ **Script to Tell Interviewer:**
*"In one of our core systems, {topic['star'].lower()} I resolved this by {topic['action'].lower()}, which {topic['metrics'].lower()}."*
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"Generated master deep dive: {target_path}")

    print(f"Successfully generated {count} master deep dive files!")

if __name__ == "__main__":
    generate_master_topics()
