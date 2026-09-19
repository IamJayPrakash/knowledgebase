import os
import sys

BASE_DIR = r"D:\Projects\knowledgebase"

# 75 Blind 75 Problems definition with categories, difficulty, LeetCode IDs
BLIND_75 = [
    # 01-Arrays & Hashing
    {"cat": "01-arrays-and-hashing", "id": 1, "lc": 1, "title": "Two Sum", "diff": "Easy",
     "hinglish": "Socho shopping me total budget fix hai (target). Har item dekhte waqt check karo ki (target - item_price) pehle dekha hai ya nahi.",
     "analogy": "Grocery shopping with a target total bill. As you pick items, you check if the complement was already seen in your basket cart.",
     "brute": "Double nested loop checking all pairs (nums[i] + nums[j] == target). Time: O(N^2), Space: O(1).",
     "optimal": "One-pass Hash Map storing seen numbers and indices. Check if (target - num) exists. Time: O(N), Space: O(N).",
     "py_code": "def twoSum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []",
     "js_code": "function twoSum(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const diff = target - nums[i];\n        if (map.has(diff)) return [map.get(diff), i];\n        map.set(nums[i], i);\n    }\n    return [];\n}",
     "diagram": "[2, 7, 11, 15] Target=9\ni=0: num=2, diff=7, Map={2:0}\ni=1: num=7, diff=2, Map has 2! -> Return [0, 1]",
     "star_story": "Fintech reconciliation engine matching unsettled credit batches against invoice ledger balances. Nested loop was taking 45 minutes for 50k transactions. Implemented hash-table complement lookup reducing runtime to 8 seconds.",
     "metrics": "Processing latency reduced by 99.7% (45 mins -> 8 secs); eliminated midnight DB read contention."},

    {"cat": "01-arrays-and-hashing", "id": 2, "lc": 217, "title": "Contains Duplicate", "diff": "Easy",
     "hinglish": "Check karna hai ki array me koi number ek se zyada baar aaya hai ya nahi. Set use karo, agar item pehle se set me hai toh duplicate mila!",
     "analogy": "Guest list at an event door. As guests enter, check if their name is already on the checked-in clipboard.",
     "brute": "Nested loops or sort array first then check adjacent elements. Time: O(N log N), Space: O(1).",
     "optimal": "Hash Set single pass. If element in set return True, else add to set. Time: O(N), Space: O(N).",
     "py_code": "def containsDuplicate(nums):\n    seen = set()\n    for n in nums:\n        if n in seen:\n            return True\n        seen.add(n)\n    return False",
     "js_code": "function containsDuplicate(nums) {\n    const set = new Set();\n    for (const n of nums) {\n        if (set.has(n)) return true;\n        set.add(n);\n    }\n    return false;\n}",
     "diagram": "[1, 2, 3, 1]\nSeen: {1} -> {1, 2} -> {1, 2, 3} -> 1 is already in Set! -> Return True",
     "star_story": "User onboarding CSV bulk upload service with 100,000 user rows. Detected duplicate phone numbers using in-memory Set deduplication before triggering batch PostgreSQL inserts, preventing primary key collision rollbacks.",
     "metrics": "Eliminated 100% of batch database rollback errors; reduced upload processing time from 3 minutes to 4.2 seconds."},

    {"cat": "01-arrays-and-hashing", "id": 3, "lc": 242, "title": "Valid Anagram", "diff": "Easy",
     "hinglish": "Do words anagram tab hote hain jab dono me exact same characters exact same frequency me hon, bas order alag ho (jaise 'anagram' aur 'nagaram').",
     "analogy": "Rearranging magnetic letters on a fridge. If both words use the exact same letter tiles, they are anagrams.",
     "brute": "Sort both strings and compare if sorted(s) == sorted(t). Time: O(N log N), Space: O(1) or O(N).",
     "optimal": "Frequency array of size 26 or HashMap counting character counts. Increment for s, decrement for t. Time: O(N), Space: O(1).",
     "py_code": "def isAnagram(s: str, t: str) -> bool:\n    if len(s) != len(t): return False\n    count = [0] * 26\n    for a, b in zip(s, t):\n        count[ord(a) - ord('a')] += 1\n        count[ord(b) - ord('a')] -= 1\n    return all(x == 0 for x in count)",
     "js_code": "function isAnagram(s, t) {\n    if (s.length !== t.length) return false;\n    const freq = new Array(26).fill(0);\n    for (let i = 0; i < s.length; i++) {\n        freq[s.charCodeAt(i) - 97]++;\n        freq[t.charCodeAt(i) - 97]--;\n    }\n    return freq.every(x => x === 0);\n}",
     "diagram": "s='anagram', t='nagaram'\nFrequency counter: 'a':+3-3=0, 'n':+1-1=0, 'g':+1-1=0, 'r':+1-1=0, 'm':+1-1=0\nAll counts zero -> Valid Anagram!",
     "star_story": "Search index preprocessor for a multilingual content repository. Normalized and matched keyword variants across localized catalogs using character histogram hashing instead of slow regex scans.",
     "metrics": "Indexed 2.5 million tags with 0-allocation fixed size histograms; decreased search query parsing latency from 45ms to 2ms."},

    {"cat": "01-arrays-and-hashing", "id": 4, "lc": 49, "title": "Group Anagrams", "diff": "Medium",
     "hinglish": "Saare words jinke letters same hain unko ek group me daalna hai. Har word ka character count ya sorted string ko HashMap ka key banao.",
     "analogy": "Sorting mail into pigeonholes where letters with the same character inventory share the same slot.",
     "brute": "Compare every string with every other string by sorting. Time: O(N^2 * K log K).",
     "optimal": "Use sorted string or 26-char frequency tuple as dictionary key, group list of words in value. Time: O(N * K), Space: O(N * K).",
     "py_code": "from collections import defaultdict\ndef groupAnagrams(strs):\n    groups = defaultdict(list)\n    for s in strs:\n        count = [0] * 26\n        for c in s:\n            count[ord(c) - ord('a')] += 1\n        groups[tuple(count)].append(s)\n    return list(groups.values())",
     "js_code": "function groupAnagrams(strs) {\n    const map = {};\n    for (const s of strs) {\n        const key = s.split('').sort().join('');\n        if (!map[key]) map[key] = [];\n        map[key].push(s);\n    }\n    return Object.values(map);\n}",
     "diagram": "['eat', 'tea', 'tan', 'ate', 'nat', 'bat']\nKey 'aet' -> ['eat', 'tea', 'ate']\nKey 'ant' -> ['tan', 'nat']\nKey 'abt' -> ['bat']",
     "star_story": "Product catalog deduplication system in an e-commerce platform. Grouped scraped product title variations and SKU identifiers having permuted word tokens into canonical product clusters.",
     "metrics": "Cleaned up 1.2M duplicate product listings, saving 35% database index storage and improving search relevancy score."},

    {"cat": "01-arrays-and-hashing", "id": 5, "lc": 347, "title": "Top K Frequent Elements", "diff": "Medium",
     "hinglish": "Array me jo elements sabse zyada baar aaye hain unme se top K nikalne hain. Bucket Sort approach se bina sorting ke O(N) me solve hota hai.",
     "analogy": "Counting votes in an election and taking the top K candidates with the most ballots.",
     "brute": "Hash map counts + sort by frequency. Time: O(N log N), Space: O(N).",
     "optimal": "Count frequencies with Map, then use Bucket Sort where index = frequency, array = numbers. Time: O(N), Space: O(N).",
     "py_code": "def topKFrequent(nums, k):\n    count = {}\n    for n in nums: count[n] = count.get(n, 0) + 1\n    buckets = [[] for _ in range(len(nums) + 1)]\n    for n, c in count.items(): buckets[c].append(n)\n    res = []\n    for i in range(len(buckets) - 1, 0, -1):\n        for n in buckets[i]:\n            res.append(n)\n            if len(res) == k: return res",
     "js_code": "function topKFrequent(nums, k) {\n    const count = new Map();\n    for (const n of nums) count.set(n, (count.get(n) || 0) + 1);\n    const buckets = Array.from({length: nums.length + 1}, () => []);\n    for (const [n, c] of count) buckets[c].push(n);\n    const res = [];\n    for (let i = buckets.length - 1; i > 0 && res.length < k; i--) {\n        if (buckets[i].length) res.push(...buckets[i]);\n    }\n    return res.slice(0, k);\n}",
     "diagram": "nums=[1,1,1,2,2,3], k=2\nCounts: {1:3, 2:2, 3:1}\nBucket: [freq 1: [3], freq 2: [2], freq 3: [1]]\nRead from back: [1, 2]",
     "star_story": "Real-time trending hashtags generator on a live event feed. Aggregated incoming tag streams in Redis and fetched the top K most popular tags in O(N) using bucket frequencies without locking sorted sets.",
     "metrics": "Handled 15,000 tweets/sec stream with sub-10ms response time on trending topic dashboard widgets."},

    {"cat": "01-arrays-and-hashing", "id": 6, "lc": 238, "title": "Product of Array Except Self", "diff": "Medium",
     "hinglish": "Har index par baaki saare elements ka product chahiye bina division operator use kiye. Prefix product aur Postfix product ka combination use karo.",
     "analogy": "Calculating your net balance without looking at your own transaction by multiplying everything that happened before you with everything that happened after you.",
     "brute": "Double loops computing product of all other elements for each index. Time: O(N^2), Space: O(1).",
     "optimal": "Prefix array traversal left to right, then Postfix multiplication right to left in a single output array. Time: O(N), Space: O(1) auxiliary.",
     "py_code": "def productExceptSelf(nums):\n    res = [1] * len(nums)\n    prefix = 1\n    for i in range(len(nums)):\n        res[i] = prefix\n        prefix *= nums[i]\n    postfix = 1\n    for i in range(len(nums) - 1, -1, -1):\n        res[i] *= postfix\n        postfix *= nums[i]\n    return res",
     "js_code": "function productExceptSelf(nums) {\n    const res = new Array(nums.length).fill(1);\n    let prefix = 1;\n    for (let i = 0; i < nums.length; i++) {\n        res[i] = prefix;\n        prefix *= nums[i];\n    }\n    let postfix = 1;\n    for (let i = nums.length - 1; i >= 0; i--) {\n        res[i] *= postfix;\n        postfix *= nums[i];\n    }\n    return res;\n}",
     "diagram": "nums =   [1,  2,  3,  4]\nPrefix:  [1,  1,  2,  6]  (products to the left)\nPostfix: [24, 12, 4,  1]  (products to the right)\nResult:  [24, 12, 8,  6]",
     "star_story": "Financial portfolio risk analysis engine. Calculated independent variance contribution of individual investment assets by multiplying total portfolio weighting factors excluding the target asset without costly float divisions.",
     "metrics": "Prevented floating point precision loss and division-by-zero crashes while crunching 500k assets in real-time."},

    {"cat": "01-arrays-and-hashing", "id": 7, "lc": 128, "title": "Longest Consecutive Sequence", "diff": "Medium",
     "hinglish": "Unsorted numbers me se sabse lambi lagataar chalne wali sequence (e.g., 1, 2, 3, 4) ka length nikalna hai O(N) time me. Set me dalo aur check karo agar (num - 1) exist nahi karta, toh wo sequence ka start hai!",
     "analogy": "Finding the longest train of consecutive domino tiles scattered on a table by only starting to count from the head of each sequence.",
     "brute": "Sort array and count longest contiguous run. Time: O(N log N), Space: O(1).",
     "optimal": "Store in HashSet. For each element `n`, check if `n-1` is in set. If NOT, `n` is a sequence start! Count `n+1, n+2...` while present. Time: O(N), Space: O(N).",
     "py_code": "def longestConsecutive(nums):\n    num_set = set(nums)\n    longest = 0\n    for n in num_set:\n        if (n - 1) not in num_set: # Start of sequence\n            length = 1\n            while (n + length) in num_set:\n                length += 1\n            longest = max(longest, length)\n    return longest",
     "js_code": "function longestConsecutive(nums) {\n    const set = new Set(nums);\n    let longest = 0;\n    for (const n of set) {\n        if (!set.has(n - 1)) {\n            let len = 1;\n            while (set.has(n + len)) len++;\n            longest = Math.max(longest, len);\n        }\n    }\n    return longest;\n}",
     "diagram": "[100, 4, 200, 1, 3, 2]\nStarts detected: 100 (len 1), 200 (len 1), 1 (1->2->3->4 len 4)\nMax Length = 4",
     "star_story": "User gaming loyalty platform tracking consecutive daily streak logins across millions of historical timestamp logs. Converted date integers into a set to compute users with the longest unbroken activity streak.",
     "metrics": "Scaled daily rewards pipeline to evaluate 4 million user activity records in 3.1 seconds with O(N) time complexity."},

    {"cat": "01-arrays-and-hashing", "id": 8, "lc": 271, "title": "Encode and Decode Strings", "diff": "Medium",
     "hinglish": "List of strings ko ek single string me encode karna hai aur fir bina data loss ke wapas list me decode karna hai. Delimiter me length prefix use karte hain (jaise '4#lint4#code').",
     "analogy": "Packing luggage where each item has a tag stating its exact byte length before the content starts.",
     "brute": "Join with comma or special char like `@#$` (fails if the string itself contains `@#$`).",
     "optimal": "Length prefix protocol: for each string `s`, append `len(s) + '#' + s`. Parser reads length until `#`, then extracts exactly that many characters. Time: O(N), Space: O(1).",
     "py_code": "def encode(strs):\n    return ''.join(f'{len(s)}#{s}' for s in strs)\n\ndef decode(s):\n    res, i = [], 0\n    while i < len(s):\n        j = s.find('#', i)\n        length = int(s[i:j])\n        res.append(s[j + 1 : j + 1 + length])\n        i = j + 1 + length\n    return res",
     "js_code": "function encode(strs) {\n    return strs.map(s => `${s.length}#${s}`).join('');\n}\nfunction decode(s) {\n    const res = [];\n    let i = 0;\n    while (i < s.length) {\n        const hashIdx = s.indexOf('#', i);\n        const len = parseInt(s.slice(i, hashIdx));\n        res.push(s.slice(hashIdx + 1, hashIdx + 1 + len));\n        i = hashIdx + 1 + len;\n    }\n    return res;\n}",
     "diagram": "['lint', 'co#de']\nEncode -> '4#lint' + '5#co#de' -> '4#lint5#co#de'\nDecode reads: 4 chars after first '#' -> 'lint', 5 chars after next '#' -> 'co#de'",
     "star_story": "Custom binary RPC serialization protocol between microservices. Handled arbitrary user payloads containing emoji, commas, and newlines without delimiter collision bugs.",
     "metrics": "Zero deserialization bugs across 100M+ RPC calls; 40% lower serialization overhead compared to verbose JSON payloads."}
]

# Write function
def generate_leetcode_files():
    base_path = os.path.join(BASE_DIR, "08-leetcode-dsa")
    os.makedirs(base_path, exist_ok=True)

    for item in BLIND_75:
        cat_dir = os.path.join(base_path, item["cat"])
        os.makedirs(cat_dir, exist_ok=True)
        fname = f"{item['id']:02d}_{item['title'].lower().replace(' ', '_').replace('-', '_')}.md"
        fpath = os.path.join(cat_dir, fname)

        content = f"""# {item['id']:02d}. {item['title']} (LeetCode {item['lc']}) — {item['diff']}

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** {item['hinglish']}
>
> **Real-World Analogy:** {item['analogy']}

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [{item['lc']} - {item['title']}](https://leetcode.com/problems/{item['title'].lower().replace(' ', '-')}/)
- **Difficulty:** `{item['diff']}`
- **Core Strategy:** {item['optimal'].split('.')[0]}
- **Edge Cases to Watch:** Empty inputs, single element, negative numbers, large duplicate entries, boundary overflows.

---

## 3. 📊 Visual Diagram

```text
{item['diagram']}
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** {item['brute']}

### ✅ Solution 2: Optimal Solution

#### JavaScript / TypeScript
```javascript
{item['js_code']}
```

#### Python 3
```python
{item['py_code']}
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving {item['title']}?"
> 
> **You:** "The brute force method involves {item['brute'].split('.')[0].lower()}, which results in poor time complexity. 
> To optimize this to {item['optimal'].split('Time: ')[1].split(',')[0]} time, we utilize {item['optimal'].split('.')[0].lower()}. 
> We maintain {item['optimal'].split('Space: ')[1].replace('.', '')} auxiliary space to keep track of state, avoiding redundant passes."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** {item['star_story']}
* **Task / Challenge:** Overcoming performance bottlenecks, timeouts, and scaling limits under high load.
* **Action Taken:** Deployed the exact optimal algorithmic pattern ({item['optimal'].split('.')[0]}) to restructure in-memory state lookup.
* **Result & Business Impact:** {item['metrics']}

🗣️ **Script to Tell Interviewer:**
*"In one of our high-volume production services, we faced a severe bottleneck where {item['star_story'].split('.')[1].strip()}. I identified that the algorithm was executing in quadratic time and refactored the pipeline using {item['optimal'].split('.')[0]}, achieving {item['metrics'].split(';')[0].lower()}."*
"""
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated: {fpath}")

if __name__ == "__main__":
    generate_leetcode_files()
    print("Completed initial LeetCode generation!")
