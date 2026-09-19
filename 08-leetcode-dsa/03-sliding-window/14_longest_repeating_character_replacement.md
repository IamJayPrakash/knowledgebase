# 14. Longest Repeating Character Replacement (LeetCode 424) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** K characters ko kisi bhi character se replace kar sakte hain. Window me majority character count track karo.
>
> **Real-World Analogy:** A party where you can bring k non-themed guests into a themed photo window of size W.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [424 - Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** Sliding window valid when (window_len - max_f) <= k
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
s = 'AABABBA', k = 1
Window [AABA] has three 'A' and one 'B'. (4 - 3) = 1 <= k (Valid, len 4)!
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Check all substrings and their character replacements. Time: O(26 * N^2).

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
function characterReplacement(s, k) {
    const count = {};
    let maxF = 0, l = 0, maxLen = 0;
    for (let r = 0; r < s.length; r++) {
        count[s[r]] = (count[s[r]] || 0) + 1;
        maxF = Math.max(maxF, count[s[r]]);
        while ((r - l + 1) - maxF > k) {
            count[s[l]]--;
            l++;
        }
        maxLen = Math.max(maxLen, r - l + 1);
    }
    return maxLen;
}
```

#### Python 3
```python
def characterReplacement(s: str, k: int) -> int:
    count = {}
    max_f, l, max_len = 0, 0, 0
    for r in range(len(s)):
        count[s[r]] = count.get(s[r], 0) + 1
        max_f = max(max_f, count[s[r]])
        while (r - l + 1) - max_f > k:
            count[s[l]] -= 1
            l += 1
        max_len = max(max_len, r - l + 1)
    return max_len
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Longest Repeating Character Replacement?"
>
> **You:** "The naive solution uses check all substrings and their character replacements, which causes inefficient time complexity. We can optimize this using **Sliding window valid when (window_len - max_f) <= k**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Telecom signal burst error correction system allowing k bits of noisy channel distortion.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Sliding window valid when (window_len - max_f) <= k** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Improved signal reconstruction speed by 10x using linear sliding window checks.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling window replacement. I optimized the workflow using Sliding window valid when (window_len - max_f) <= k, which improved signal reconstruction speed by 10x using linear sliding window checks. and ensured zero downtime."*
