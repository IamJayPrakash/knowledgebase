# 08. Encode and Decode Strings (LeetCode 271) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Strings ki list ko single string me encode karna hai aur wapas decode karna hai. Delimiter me length prefix use karte hain (jaise '4#lint').
>
> **Real-World Analogy:** Packing luggage where every parcel has a tag stating its exact byte length before content starts.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [271 - Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** Length prefix protocol (len#string)
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
['lint', 'co#de'] -> '4#lint5#co#de' -> Decoded correctly preserving '#'
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Join with comma (breaks if strings contain commas).

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
function encode(strs) {
    return strs.map(s => `${s.length}#${s}`).join('');
}
function decode(s) {
    const res = [];
    let i = 0;
    while (i < s.length) {
        const hashIdx = s.indexOf('#', i);
        const len = parseInt(s.slice(i, hashIdx));
        res.push(s.slice(hashIdx + 1, hashIdx + 1 + len));
        i = hashIdx + 1 + len;
    }
    return res;
}
```

#### Python 3
```python
def encode(strs):
    return ''.join(f'{len(s)}#{s}' for s in strs)
def decode(s):
    res, i = [], 0
    while i < len(s):
        j = s.find('#', i)
        length = int(s[i:j])
        res.append(s[j+1 : j+1+length])
        i = j + 1 + length
    return res
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Encode and Decode Strings?"
>
> **You:** "The naive solution uses join with comma (breaks if strings contain commas), which causes inefficient time complexity. We can optimize this using **Length prefix protocol (len#string)**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Custom binary RPC protocol handling user-generated text containing emoji and control delimiters.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Length prefix protocol (len#string)** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Zero parsing errors across 100M+ payloads; 40% bandwidth savings compared to JSON.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling lossless string serialization. I optimized the workflow using Length prefix protocol (len#string), which zero parsing errors across 100m+ payloads and ensured zero downtime."*
