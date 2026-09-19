# 06. Product of Array Except Self (LeetCode 238) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Har index par baaki sabhi numbers ka product chahiye bina division operator use kiye. Prefix product aur Postfix product multiply karo.
>
> **Real-World Analogy:** Calculating your net balance without looking at your own transaction by multiplying previous transactions with future transactions.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [238 - Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** Prefix and Postfix product passes
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
nums =   [1,  2,  3,  4]
Prefix:  [1,  1,  2,  6]
Postfix: [24, 12, 4,  1]
Result:  [24, 12, 8,  6]
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Nested loop multiplying all other items for each index. Time: O(N^2), Space: O(1).

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
function productExceptSelf(nums) {
    const res = new Array(nums.length).fill(1);
    let prefix = 1;
    for (let i = 0; i < nums.length; i++) {
        res[i] = prefix;
        prefix *= nums[i];
    }
    let postfix = 1;
    for (let i = nums.length - 1; i >= 0; i--) {
        res[i] *= postfix;
        postfix *= nums[i];
    }
    return res;
}
```

#### Python 3
```python
def productExceptSelf(nums):
    res = [1] * len(nums)
    prefix = 1
    for i in range(len(nums)):
        res[i] = prefix
        prefix *= nums[i]
    postfix = 1
    for i in range(len(nums)-1, -1, -1):
        res[i] *= postfix
        postfix *= nums[i]
    return res
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Product of Array Except Self?"
>
> **You:** "The naive solution uses nested loop multiplying all other items for each index, which causes inefficient time complexity. We can optimize this using **Prefix and Postfix product passes**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Financial portfolio risk analysis engine avoiding floating point division-by-zero errors when calculating variance weights.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Prefix and Postfix product passes** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Prevented division-by-zero crashes on 500k real-time asset evaluations.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling multiplication without division. I optimized the workflow using Prefix and Postfix product passes, which prevented division-by-zero crashes on 500k real-time asset evaluations. and ensured zero downtime."*
