# 05. Top K Frequent Elements (LeetCode 347) — Medium

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Array me se k sabse zyada aane wale elements nikalne hain. Bucket sort se O(N) me bina sorting ke solve karo.
>
> **Real-World Analogy:** Counting votes where buckets represent vote counts, reading from highest bucket down.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [347 - Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)
- **Difficulty:** `Medium`
- **Pattern / Core Strategy:** Bucket sort by frequency counts
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
nums=[1,1,1,2,2,3], k=2
Counts: {1:3, 2:2, 3:1}
Buckets: [3: [1], 2: [2], 1: [3]] -> Output: [1, 2]
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** HashMap frequency count + sort by count. Time: O(N log N), Space: O(N).

### ✅ Solution 2: Optimal Solution (Line-by-Line Commented)

#### JavaScript / TypeScript
```javascript
function topKFrequent(nums, k) {
    // Step 1: Build frequency map
    const count = new Map();
    for (const n of nums) {
        count.set(n, (count.get(n) || 0) + 1);
    }
    
    // Step 2: Create buckets array where index is the frequency
    const buckets = Array.from({ length: nums.length + 1 }, () => []);
    for (const [n, c] of count) {
        buckets[c].push(n);
    }
    
    // Step 3: Collect top k elements starting from highest frequency bucket
    const res = [];
    for (let i = buckets.length - 1; i > 0 && res.length < k; i--) {
        if (buckets[i].length) {
            res.push(...buckets[i]);
        }
    }
    
    // Return exactly k elements
    return res.slice(0, k);
}
```

#### Python 3
```python
def topKFrequent(nums, k):
    # Step 1: Count frequency of each number using a hash map
    count = {}
    for n in nums:
        # Increment frequency count for number n
        count[n] = count.get(n, 0) + 1
        
    # Step 2: Bucket array where index = frequency, value = list of numbers
    buckets = [[] for _ in range(len(nums) + 1)]
    for n, c in count.items():
        # Place number 'n' into bucket corresponding to its frequency 'c'
        buckets[c].append(n)
        
    # Step 3: Iterate backwards from highest frequency bucket down to 1
    res = []
    for i in range(len(buckets) - 1, 0, -1):
        for n in buckets[i]:
            # Add element to results
            res.append(n)
            # Stop immediately once we have collected k elements
            if len(res) == k:
                return res
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Top K Frequent Elements?"
>
> **You:** "The naive solution uses hashmap frequency count + sort by count, which causes inefficient time complexity. We can optimize this using **Bucket sort by frequency counts**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Real-time trending hashtag generation on a high-throughput event live stream.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Bucket sort by frequency counts** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Processed 15k events/sec with sub-10ms response time on trending dashboard widgets.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling top frequency extraction. I optimized the workflow using Bucket sort by frequency counts, which processed 15k events/sec with sub-10ms response time on trending dashboard widgets. and ensured zero downtime."*
