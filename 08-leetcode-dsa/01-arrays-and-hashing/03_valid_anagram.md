# 03. Valid Anagram (LeetCode 242) — Easy

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Do words anagram tab hain jab dono me exact same letters exact same frequency me hon.
>
> **Real-World Analogy:** Scrabble tiles: both words must be formed by rearranging the identical set of letter tiles.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [242 - Valid Anagram](https://leetcode.com/problems/valid-anagram/)
- **Difficulty:** `Easy`
- **Pattern / Core Strategy:** Character frequency array of size 26
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
s='anagram', t='nagaram'
Frequency counter counts all characters to 0 -> True
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Sort both strings and check if sorted(s) == sorted(t). Time: O(N log N), Space: O(N).

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
function isAnagram(s, t) {
    if (s.length !== t.length) return false;
    const freq = new Array(26).fill(0);
    for (let i = 0; i < s.length; i++) {
        freq[s.charCodeAt(i) - 97]++;
        freq[t.charCodeAt(i) - 97]--;
    }
    return freq.every(x => x === 0);
}
```

#### Python 3
```python
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t): return False
    count = [0] * 26
    for a, b in zip(s, t):
        count[ord(a) - ord('a')] += 1
        count[ord(b) - ord('a')] -= 1
    return all(x == 0 for x in count)
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Valid Anagram?"
>
> **You:** "The naive solution uses sort both strings and check if sorted(s) == sorted(t), which causes inefficient time complexity. We can optimize this using **Character frequency array of size 26**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Multilingual search catalog keyword sanitizer. Matched permuted tag search queries without running heavy regex scans.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Character frequency array of size 26** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Processed 2.5 million tags with zero heap allocation overhead; dropped query latency from 45ms to 2ms.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling anagram verification. I optimized the workflow using Character frequency array of size 26, which processed 2.5 million tags with zero heap allocation overhead and ensured zero downtime."*
