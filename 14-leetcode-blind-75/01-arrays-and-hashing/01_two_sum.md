# 01. Two Sum (LeetCode 1) — Comprehensive Deep Dive

> **Category:** Arrays & Hashing  
> **Difficulty:** Easy  
> **Target Roles:** SDE-1, SDE-2, SDE-3, Senior Technical Lead, Full-Stack Engineer  

---

## 📜 Official LeetCode Problem Statement

Given an array of integers `nums` and an integer `target`, return **indices of the two numbers such that they add up to `target`**.

You may assume that each input would have **exactly one solution**, and you may not use the *same* element twice.

You can return the answer in any order.

### 📥 Example 1

```text
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

### 📥 Example 2

```text
Input: nums = [3, 2, 4], target = 6
Output: [1, 2]
Explanation: Because nums[1] + nums[2] == 6, we return [1, 2].
```

### 📥 Example 3

```text
Input: nums = [3, 3], target = 6
Output: [0, 1]
Explanation: Both elements are identical, but located at different indices [0, 1].
```

### ⚠️ Constraints & Edge Cases

* `2 <= nums.length <= 10^4` *(Notice: N can be up to 10,000. An $O(N^2)$ algorithm will take $10^8$ operations, risking Time Limit Exceeded!)*
* `-10^9 <= nums[i] <= 10^9` *(Numbers can be negative, zero, or very large integers).*
* `-10^9 <= target <= 10^9` *(Target can also be negative).*
* **Only one valid answer exists.**

---

## 🐣 Layman's Analogy (Hinglish + Real-World)

> **Hinglish Intuition:**
> Socho aap ek dukaan me ho aur aapki jeb me total **₹9** hain (`target = 9`).  
> Counter par items rakhe hain: `[₹2, ₹7, ₹11, ₹15]`.  
>
> * **Newbie Tareeka (Brute Force):** Aap pehle ₹2 ka item uthate ho, fir dukaan ke saare baaki items ek-ek karke check karte ho: *Kya 2+7=9 hai?* Haan! Lekin agar array 10,000 items ka hota, toh aapko har item ke liye baaki 9,999 items baar-baar dekhne padte (Double for-loop: bohot thaka dene wala aur slow).
>
> * **Smart Tareeka (Hash Map Diary):** Aap apne paas ek choti **Notebook (Hash Map)** rakhte ho.  
>
> 1. Aapne pehla item dekha: **₹2**. Aapko kitna aur chahiye ₹9 banane ke liye? `9 - 2 = 7`.  
> 2. Aapne notebook khol ke dekha: *Kya maine pehle kabhi ₹7 dekha hai?* Nahi!  
>    Toh aapne notebook me note kar liya: `Notebook[2] = Index 0` *(Mujhe ₹2 mila tha index 0 par)*.  
> 3. Ab aap agle item par gaye: **₹7**. Aapko kitna aur chahiye? `9 - 7 = 2`.  
> 4. Aapne notebook check ki: *Kya notebook me '₹2' likha hai?* **HAAN!** Pehle index 0 par mila tha!  
> 5. **BINGO!** Aapne bina piche mudke dekhe instant bol diya: **Index 0 aur Index 1** milkar ₹9 banate hain!

---

## 🧠 DSA Foundation: What IS a Hash Map & Why Does It Matter?

If you don't know what a Hash Map is, think of it as a **super-fast index in a book**:

```text
[Normal Array / List Search]
To check if '7' exists in [2, 11, 15, ..., 7]:
You must scan from index 0 to the end.
Time Complexity: O(N) (Linear Scan)

[Hash Map / Hash Table Search]
A Hash Function converts the key (e.g., number 7) directly into a memory address!
Key (7) ──(Hash Function)──> Index [Memory Slot 4092] ──> Instant Value!
Time Complexity: O(1) (Constant Time Instant Lookup)
```

### ❓ When to Apply a Hash Map?

1. Whenever you need **$O(1)$ fast lookups** instead of re-scanning an array.
2. Whenever you need to remember **frequencies** or **indices** of elements you have already visited.
3. Whenever a problem asks for a **pair, complement, or frequency** (e.g., $A + B = \text{Target} \implies B = \text{Target} - A$).

### 🚫 When NOT to Apply a Hash Map?

1. When memory is strictly limited (Hash Maps require $O(N)$ extra heap memory).
2. When the array is already **sorted** (In sorted arrays, **Two Pointers** gives $O(1)$ extra space without needing a Hash Map).
3. When you need elements in strict sorted order (Standard hash tables do not preserve sorting).

---

## 📊 Visual Step-by-Step Tracing

Let's trace `nums = [2, 7, 11, 15]` with `target = 9`:

```text
Step 0: Initialize empty Map: {}

Iteration 0 (i = 0):
  Current Number = 2
  Needed Complement = target - current = 9 - 2 = 7
  Is 7 in Map? NO.
  Action: Save current number in Map -> Map: { 2: 0 }

Iteration 1 (i = 1):
  Current Number = 7
  Needed Complement = target - current = 9 - 7 = 2
  Is 2 in Map? YES! (stored at index 0)
  Action: Found solution! Return [Map[2], current_index] -> [0, 1] 🎉
```

---

## 💻 The 3 Evolution Versions (Newbie ➡️ Intermediate ➡️ Senior)

---

### ❌ Version 1: The Absolute Newbie Approach (Brute Force Nested Loops)

A beginner checks every possible pair using two nested `for` loops.

#### 💡 How the Newbie Thinks

*"Let me take the first number, and compare it with the second, third, fourth... If none match, take the second number and compare with the third, fourth..."*

```javascript
// Time Complexity: O(N^2) | Space Complexity: O(1)
function twoSumBruteForce(nums, target) {
  // Line 1: Outer loop picks the first element 'i' from index 0 to N-1
  for (let i = 0; i < nums.length; i++) {
    // Line 2: Inner loop picks the second element 'j' strictly after 'i' to avoid self-pairing
    for (let j = i + 1; j < nums.length; j++) {
      // Line 3: Check if the sum of both elements equals the target
      if (nums[i] + nums[j] === target) {
        // Line 4: If match found, return the pair of indices
        return [i, j];
      }
    }
  }
  // Line 5: Fallback if no pair exists
  return [];
}
```

#### ⚠️ Why This Fails in Production & Interviews

* For an array of size $N = 10,000$, $N^2 = 100,000,000$ (100 Million comparisons).
* The algorithm will get **Time Limit Exceeded (TLE)** on modern test suites.

---

### ⚠️ Version 2: The Intermediate Approach (Two-Pass Hash Map)

An intermediate developer understands that a Hash Map provides $O(1)$ lookups, so they populate the map first, and then search in a second pass.

```javascript
// Time Complexity: O(N) | Space Complexity: O(N)
function twoSumTwoPass(nums, target) {
  // Line 1: Create map to store number -> index
  const map = new Map();

  // Line 2: Pass 1 - Populate the entire map first
  for (let i = 0; i < nums.length; i++) {
    map.set(nums[i], i);
  }

  // Line 3: Pass 2 - Check for complement for each element
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];

    // Line 4: CRITICAL TRAP: Must check `map.get(complement) !== i` 
    // so an element does NOT use itself! (e.g. nums=[3, 2, 4], target=6; 3+3=6 but index 0 cannot pair with index 0)
    if (map.has(complement) && map.get(complement) !== i) {
      return [i, map.get(complement)];
    }
  }

  return [];
}
```

#### ⚠️ Intermediate Limitations

* It makes **two full passes** over the array.
* It requires careful edge-case logic to prevent an element from matching with itself.

---

### ✅ Version 3: The Senior / Optimal Approach (One-Pass Hash Map)

A senior engineer combines lookup and insertion into a **single pass**. Each element looks *backwards* at what has already been seen. Self-matching is mathematically impossible!

#### JavaScript / TypeScript Implementation

```javascript
// Time Complexity: O(N) | Space Complexity: O(N)
function twoSum(nums, target) {
  // Line 1: Initialize Hash Map to store { number => index }
  const seenMap = new Map();

  // Line 2: Single pass loop visiting each element once
  for (let i = 0; i < nums.length; i++) {
    const currentNum = nums[i];
    // Line 3: Calculate the exact complement needed to reach target
    const complement = target - currentNum;

    // Line 4: Check if complement already exists in our seen history
    if (seenMap.has(complement)) {
      // Line 5: Match found! Return [stored_complement_index, current_index]
      return [seenMap.get(complement), i];
    }

    // Line 6: Store current number and its index in map for subsequent elements to find
    seenMap.set(currentNum, i);
  }

  // Line 7: Default fallback (problem guarantees exactly one solution exists)
  return [];
}
```

#### Python 3 Implementation

```python
# Time Complexity: O(N) | Space Complexity: O(N)
def twoSum(nums: list[int], target: int) -> list[int]:
    # Line 1: Dictionary mapping number -> index
    seen_map = {}
    
    # Line 2: Enumerate yields both index 'i' and value 'num' in a single pass
    for i, num in enumerate(nums):
        # Line 3: Compute mathematical difference needed
        complement = target - num
        
        # Line 4: In Python, dictionary 'in' operator checks keys in O(1) average time
        if complement in seen_map:
            # Line 5: Return pair of indices
            return [seen_map[complement], i]
            
        # Line 6: Record current number into dictionary
        seen_map[num] = i
        
    # Line 7: Fallback empty list
    return []
```

---

## 🎯 The Senior Interview Pitch (Say Exactly This!)

> **Interviewer:** *"Walk me through how you would solve Two Sum."*
>
> **You:**  
> *"The intuitive brute-force solution is to check every pair using two nested loops, giving an $O(N^2)$ time complexity and $O(1)$ space. However, for $N = 10,000$, this will exceed execution limits.*
>
> *We can optimize this to **$O(N)$ linear time** by trading space for time using a **Hash Map**. In a single pass, for each element `x`, we calculate its complement `target - x`. We check if this complement exists in our map. If it does, we immediately return the complement's stored index and the current index. If not, we record `x` and its index in the map.*
>
> *This guarantees an optimal **$O(N)$ time complexity** because Hash Map lookups and insertions run in $O(1)$ average time, with **$O(N)$ auxiliary space**."*

---

## 💼 Real-World Project Challenge (STAR Production Story)

* **Situation:** In an automated financial accounting system, our batch reconciliation job was matching 50,000 daily bank credit records against pending customer invoice ledger balances.
* **The Problem:** The legacy code utilized a nested loop ($O(N^2)$) comparing transactions. The nightly reconciliation job was taking **48 minutes** to finish, blocking midnight reporting pipelines.
* **The Action:** I refactored the matching service to use the **Two Sum Hash Map pattern**. We loaded the invoice balances into an in-memory Hash Map indexed by balance amounts, and streamed the bank credits in a single $O(N)$ pass.
* **The Result & Metrics:**
  * Execution time plummeted from **48 minutes down to 6.2 seconds** (99.7% speedup).
  * Completely eliminated database lock timeouts during end-of-day settlement.

---

## 🔄 Pattern Transferability: Where Else Can You Apply This?

Once you master this **Complement Lookup Pattern**, you can solve:

1. **LeetCode 15 (3Sum):** Sort array, fix element `i`, and turn the remaining problem into a Two Sum target search.
2. **LeetCode 167 (Two Sum II - Input Array Is Sorted):** When array is sorted, replace Hash Map with **Two Pointers** ($O(1)$ space).
3. **LeetCode 560 (Subarray Sum Equals K):** Uses a Hash Map storing **Prefix Sums** to find subarrays summing to $K$ in $O(N)$ time.
4. **LeetCode 128 (Longest Consecutive Sequence):** Uses a Hash Set to check sequence starts `(num - 1)` in $O(1)$ time.
