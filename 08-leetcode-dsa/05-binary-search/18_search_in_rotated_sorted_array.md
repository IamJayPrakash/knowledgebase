# 18. Search in Rotated Sorted Array (LeetCode 33) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Rotated array me target element search karna hai. Har step par pata karo ki kaunsa half normally sorted hai.
>
> **Real-World Analogy:** Searching for a house number on a circular street with a split checkpoint.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [33 - Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** Binary search identifying sorted half
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
[4, 5, 6, 7, 0, 1, 2], target = 0
Mid=7. Left half [4..7] is sorted, target is NOT in [4..7]. Search right half!
Target 0 found at index 4.
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Linear search. Time: O(N), Space: O(1).

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
function search(nums, target) {
    let l = 0, r = nums.length - 1;
    while (l <= r) {
        const mid = Math.floor((l + r) / 2);
        if (nums[mid] === target) return mid;
        if (nums[l] <= nums[mid]) {
            if (nums[l] <= target && target < nums[mid]) r = mid - 1;
            else l = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[r]) l = mid + 1;
            else r = mid - 1;
        }
    }
    return -1;
}
```

#### Python 3
```python
def search(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target: return mid
        if nums[l] <= nums[mid]: # Left sorted
            if nums[l] <= target < nums[mid]: r = mid - 1
            else: l = mid + 1
        else: # Right sorted
            if nums[mid] < target <= nums[r]: l = mid + 1
            else: r = mid - 1
    return -1
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Search in Rotated Sorted Array?"
>
> **You:** "The naive solution uses linear search, which causes inefficient time complexity. We can optimize this using **Binary search identifying sorted half**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Inverted distributed database index partition search under sharded rolling storage.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Binary search identifying sorted half** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Maintained sub-1ms point-lookup SLA over 10M record segment indices.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling lookup in rotated array. I optimized the workflow using Binary search identifying sorted half, which maintained sub-1ms point-lookup sla over 10m record segment indices. and ensured zero downtime."*
