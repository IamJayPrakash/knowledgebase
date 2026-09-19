# Machine Coding: Implement Promise.all Polyfill from Scratch

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
>
> **Hinglish Intuition:** Promise.all saare promises ko parallel me run karta hai aur tabhi resolve hota hai jab saare resolve ho jayein. Agar ek bhi reject hua, toh turant reject ho jata hai.
>
> **Real-World Analogy:** A team relay race: the team only wins when the last runner crosses the finish line. If any runner drops the baton, the race ends immediately.

---

## 2. 📌 Core Mechanics & Key Points

- Takes an iterable of promises and returns a single Promise.
- Resolves with an array of resolved values in the original input order.
- Rejects immediately upon the first promise rejection (Fail-Fast behavior).
- Handles non-promise values by wrapping them with `Promise.resolve()`.

---

## 3. 📊 Visual Architecture Diagram

```text
[Promise 1 (200ms)] ──┐
[Promise 2 (100ms)] ──┼──> [Promise.all Counter == Total] ──> Resolves [Val1, Val2, Val3]
[Promise 3 (300ms)] ──┘
```

---

## 4. 💻 Practical Implementation & Code Snippet (Line-by-Line Commented)

```javascript
// Polyfill for Promise.all
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

promiseAllPolyfill([p1, p2, p3]).then(console.log); // Output: [10, 20, 30]
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
>
> **Interviewer:** "Can you explain Machine Coding and your production experience with it?"
>
> **You:** "Promise.all coordinates concurrent asynchronous operations. It resolves when all input promises resolve, preserving the original array order regardless of execution completion time, and fails fast if any promise rejects. We implement this by wrapping elements in Promise.resolve, tracking an incremental completion counter, and storing results by input index."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)

- **Situation:** Batching independent third-party KYC verification API calls in an onboarding pipeline where legacy code was executing them sequentially.
- **Task / Challenge:** Overcoming performance bottlenecks, race conditions, or architecture fragility under scale.
- **Action Taken:** Aggregated calls using Promise.all polyfill with bounded timeout wrappers.
- **Result & Business Impact:** Decreased user onboarding latency from 4.8 seconds to 920 milliseconds (80% faster).

🗣️ **Script to Tell Interviewer:**
*"In our production systems, batching independent third-party kyc verification api calls in an onboarding pipeline where legacy code was executing them sequentially. I took charge of the architecture by aggregated calls using promise.all polyfill with bounded timeout wrappers., successfully achieving decreased user onboarding latency from 4.8 seconds to 920 milliseconds (80% faster).."*
