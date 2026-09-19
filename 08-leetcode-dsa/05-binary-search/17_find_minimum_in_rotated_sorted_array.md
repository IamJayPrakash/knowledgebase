# 17. Find Minimum in Rotated Sorted Array (LeetCode 153) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Sorted array ko kisi pivot par rotate kiya gaya hai. O(log N) me minimum nikalna hai binary search se.
>
> **Real-World Analogy:** Finding where a sorted phone directory was split and glued back together.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [153 - Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** Binary search comparing mid with right
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
[4, 5, 6, 7, 0, 1, 2]
Mid = 7 > Right = 2 -> Search right half: [0, 1, 2] -> Min = 0
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Linear scan finding the smallest value. Time: O(N), Space: O(1).

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
function findMin(nums) {
    let l = 0, r = nums.length - 1;
    while (l < r) {
        const mid = Math.floor((l + r) / 2);
        if (nums[mid] > nums[r]) l = mid + 1;
        else r = mid;
    }
    return nums[l];
}
```

#### Python 3
```python
def findMin(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]: l = mid + 1
        else: r = mid
    return nums[l]
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Find Minimum in Rotated Sorted Array?"
>
> **You:** "The naive solution uses linear scan finding the smallest value, which causes inefficient time complexity. We can optimize this using **Binary search comparing mid with right**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Distributed log timestamp index lookup on circularly rotated server partition files.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Binary search comparing mid with right** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Reduced partition offset resolution from 200ms to 0.4ms.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling finding rotation inflection. I optimized the workflow using Binary search comparing mid with right, which reduced partition offset resolution from 200ms to 0.4ms. and ensured zero downtime."*
