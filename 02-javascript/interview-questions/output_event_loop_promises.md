# Tricky Output Questions: Event Loop, Microtasks & Macrotasks

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
