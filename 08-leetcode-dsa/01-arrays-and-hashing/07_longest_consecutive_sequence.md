# 07. Longest Consecutive Sequence (LeetCode 128) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Unsorted numbers me se sabse lambi lagataar chalne wali ginti ka length chahiye O(N) me. Set me daal kar check karo agar n-1 nahi hai toh n sequence ka start hai.
>
> **Real-World Analogy:** Finding the longest continuous domino chain on a table by only building from head pieces.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [128 - Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** HashSet checking (num - 1) sequence starts
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
[100, 4, 200, 1, 3, 2]
Starts: 100 (len 1), 200 (len 1), 1 (1->2->3->4 len 4) -> Max = 4
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Sort array and count longest contiguous run. Time: O(N log N), Space: O(1).

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
function longestConsecutive(nums) {
    const set = new Set(nums);
    let longest = 0;
    for (const n of set) {
        if (!set.has(n - 1)) {
            let len = 1;
            while (set.has(n + len)) len++;
            longest = Math.max(longest, len);
        }
    }
    return longest;
}
```

#### Python 3
```python
def longestConsecutive(nums):
    num_set = set(nums)
    longest = 0
    for n in num_set:
        if n - 1 not in num_set:
            length = 1
            while n + length in num_set: length += 1
            longest = max(longest, length)
    return longest
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Longest Consecutive Sequence?"
>
> **You:** "The naive solution uses sort array and count longest contiguous run, which causes inefficient time complexity. We can optimize this using **HashSet checking (num - 1) sequence starts**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** User engagement gamification service calculating unbroken daily login streaks from epoch date integers.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **HashSet checking (num - 1) sequence starts** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Computed streak rewards for 4M daily active users in 3.1 seconds.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling longest unbroken sequence. I optimized the workflow using HashSet checking (num - 1) sequence starts, which computed streak rewards for 4m daily active users in 3.1 seconds. and ensured zero downtime."*
