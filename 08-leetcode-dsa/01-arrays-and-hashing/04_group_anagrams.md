# 04. Group Anagrams (LeetCode 49) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Jo words ek dusre ke anagram hain unko ek group me rakhna hai. Sorted word ya char-frequency tuple ko hashmap key banao.
>
> **Real-World Analogy:** Sorting library books into shelves where all books with the same character combination go to the same shelf.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [49 - Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** HashMap with sorted string or char-count key
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
Input: ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
Key 'aet' -> ['eat', 'tea', 'ate']
Key 'ant' -> ['tan', 'nat']
Key 'abt' -> ['bat']
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Compare every word pair with O(N^2) anagram checks. Time: O(N^2 * K).

### ✅ Solution 2: Optimal Solution (Line-by-Line Commented)

#### JavaScript / TypeScript
```javascript
function groupAnagrams(strs) {
    // Hash map to store sorted_string => array_of_anagrams
    const map = {};
    
    // Iterate through every string in the array
    for (const s of strs) {
        // Sort letters alphabetically to form the canonical signature key
        const key = s.split('').sort().join('');
        
        // Initialize an empty array if key doesn't exist yet
        map[key] = map[key] || [];
        
        // Push the original string into its corresponding group
        map[key].push(s);
    }
    
    // Return an array of grouped anagram arrays
    return Object.values(map);
}
```

#### Python 3
```python
from collections import defaultdict

def groupAnagrams(strs):
    # Defaultdict creates an empty list automatically for any new key
    groups = defaultdict(list)
    
    # Process each string in the input list
    for s in strs:
        # Sort the characters of the string to create a unique canonical key
        key = tuple(sorted(s))
        
        # Append the original word to the list matching this sorted key
        groups[key].append(s)
        
    # Return all grouped anagram lists
    return list(groups.values())
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Group Anagrams?"
>
> **You:** "The naive solution uses compare every word pair with o(n^2) anagram checks, which causes inefficient time complexity. We can optimize this using **HashMap with sorted string or char-count key**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** E-commerce product catalog deduplication. Clustered scraped vendor titles that only differed in word order.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **HashMap with sorted string or char-count key** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Cleaned up 1.2M duplicate product listings, saving 35% database index storage.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling clustering anagrams. I optimized the workflow using HashMap with sorted string or char-count key, which cleaned up 1.2m duplicate product listings, saving 35% database index storage. and ensured zero downtime."*
