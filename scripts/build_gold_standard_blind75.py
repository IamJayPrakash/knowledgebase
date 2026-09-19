import os
import sys

BASE_DIR = r"D:\Projects\knowledgebase"
LEETCODE_BASE = os.path.join(BASE_DIR, "08-leetcode-dsa")

# Comprehensive definitions for Blind 75 problems
BLIND_75_GOLD = [
    # -------------------------------------------------------------
    # 01-arrays-and-hashing
    # -------------------------------------------------------------
    {
        "cat": "01-arrays-and-hashing", "id": 2, "lc": 217, "title": "Contains Duplicate", "diff": "Easy",
        "statement": "Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.",
        "examples": """Input: nums = [1,2,3,1]
Output: true
Explanation: The element 1 occurs at the indices 0 and 3.

Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct.

Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true""",
        "constraints": """* 1 <= nums.length <= 10^5
* -10^9 <= nums[i] <= 10^9
* Time limit: 1.00s (O(N^2) brute force will time out for N = 100,000!)""",
        "hinglish": "Check karna hai ki array me koi number ek se zyada baar aaya hai ya nahi. Agar ek bhi number repeat hua toh true, varna false.",
        "analogy": "Guest list at an event door. As guests enter, you check if their name is already on your checked-in clipboard.",
        "foundation_name": "Hash Set (Hash Table with Only Keys)",
        "foundation_desc": "A Hash Set stores unique keys without values. It uses a hash function to map keys to bucket addresses in O(1) time.",
        "when_use": "Whenever you need to check existence or deduplicate items in O(1) time.",
        "when_not": "When strict O(1) auxiliary memory is required and in-place sorting is acceptable.",
        "visual_trace": """nums = [1, 2, 3, 1]
Set starts empty: set = {}
i = 0: num = 1 -> Not in set -> Add 1 -> set = {1}
i = 1: num = 2 -> Not in set -> Add 2 -> set = {1, 2}
i = 2: num = 3 -> Not in set -> Add 3 -> set = {1, 2, 3}
i = 3: num = 1 -> ALREADY IN SET! -> Return true 🎉""",
        "v1_title": "The Absolute Newbie Approach (Nested Loops O(N^2))",
        "v1_why": "Compares every element with every other element. Takes N*(N-1)/2 comparisons, causing Time Limit Exceeded for N=100,000.",
        "v1_code": """function containsDuplicateBrute(nums) {
  // Line 1: Outer loop picks the first element
  for (let i = 0; i < nums.length; i++) {
    // Line 2: Inner loop compares with every subsequent element
    for (let j = i + 1; j < nums.length; j++) {
      // Line 3: If equal, duplicate found
      if (nums[i] === nums[j]) {
        return true;
      }
    }
  }
  // Line 4: No duplicates found
  return false;
}""",
        "v2_title": "The Intermediate Approach (Sorting O(N log N))",
        "v2_why": "Sorts the array first so duplicates become adjacent, then checks neighboring elements in a single pass. Modifies input array or requires O(N) sort space.",
        "v2_code": """function containsDuplicateSort(nums) {
  // Line 1: Sort array in ascending order in O(N log N)
  nums.sort((a, b) => a - b);

  // Line 2: Single pass checking adjacent neighbors
  for (let i = 1; i < nums.length; i++) {
    // Line 3: If adjacent items are identical, duplicate exists
    if (nums[i] === nums[i - 1]) {
      return true;
    }
  }
  return false;
}""",
        "v3_title": "The Senior / Optimal Approach (Hash Set O(N) Time, O(N) Space)",
        "v3_js": """function containsDuplicate(nums) {
  // Line 1: Initialize empty Set for O(1) membership lookups
  const seen = new Set();

  // Line 2: Traverse array once
  for (let i = 0; i < nums.length; i++) {
    const n = nums[i];
    // Line 3: Check if number was already visited
    if (seen.has(n)) {
      // Duplicate found immediately in O(1)
      return true;
    }
    // Line 4: Store current number in Set
    seen.add(n);
  }

  // Line 5: All elements are distinct
  return false;
}""",
        "v3_py": """def containsDuplicate(nums: list[int]) -> bool:
    # Line 1: Initialize hash set
    seen = set()
    
    # Line 2: Single pass traversal
    for n in nums:
        # Line 3: Constant time O(1) lookup
        if n in seen:
            return True
        # Line 4: Add number to set
        seen.add(n)
        
    # Line 5: No duplicates present
    return False""",
        "pitch": "The naive solution compares all pairs in O(N^2) time. Sorting improves this to O(N log N) time with O(1) auxiliary space. The optimal approach uses a Hash Set in O(N) time and O(N) space, checking membership in O(1) average time per element and returning true on the first collision.",
        "star": "User CSV bulk upload service processing 100,000 phone records causing database duplicate primary key rollbacks.",
        "action": "Implemented in-memory Hash Set deduplication prior to opening PostgreSQL transaction batches.",
        "metrics": "Eliminated 100% of batch database rollback errors; reduced upload duration from 3.2 minutes to 4.1 seconds.",
        "transfer": "LeetCode 219 (Contains Duplicate II with sliding window index distance k), LeetCode 287 (Find the Duplicate Number with Floyd's Cycle)."
    },

    {
        "cat": "01-arrays-and-hashing", "id": 3, "lc": 242, "title": "Valid Anagram", "diff": "Easy",
        "statement": "Given two strings s and t, return true if t is an anagram of s, and false otherwise. An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "examples": """Input: s = "anagram", t = "nagaram"
Output: true

Input: s = "rat", t = "car"
Output: false""",
        "constraints": """* 1 <= s.length, t.length <= 5 * 10^4
* s and t consist of lowercase English letters.""",
        "hinglish": "Do words anagram tab hote hain jab dono me exact same letters exact same frequency me hon, bas order badal gaya ho.",
        "analogy": "Scrabble tiles: you must build the second word using the exact same letter tiles from the first word without adding or dropping any tile.",
        "foundation_name": "Frequency Array / Character Histogram",
        "foundation_desc": "When the character set is bounded (e.g., 26 lowercase English letters), an array of fixed size 26 acts as a direct-mapped hash table with zero hash collision overhead.",
        "when_use": "Whenever counting character frequencies or permutation equivalence across bounded alphabets.",
        "when_not": "When the alphabet is arbitrarily large Unicode (use a generic Hash Map instead).",
        "visual_trace": """s = "anagram", t = "nagaram"
freq array [26 zeros]
Traverse both simultaneously:
'a' in s (+1), 'n' in t (-1)
After all characters:
'a': +3 -3 = 0
'n': +1 -1 = 0
'g': +1 -1 = 0
'r': +1 -1 = 0
'm': +1 -1 = 0
All 26 indices are 0 -> Valid Anagram! 🎉""",
        "v1_title": "The Absolute Newbie Approach (Character Removal O(N^2))",
        "v1_why": "For each character in s, finds and removes its first occurrence in t. String slicing inside a loop takes quadratic time.",
        "v1_code": """function isAnagramBrute(s, t) {
  if (s.length !== t.length) return false;
  let tArr = t.split('');
  for (let i = 0; i < s.length; i++) {
    const idx = tArr.indexOf(s[i]);
    if (idx === -1) return false;
    tArr.splice(idx, 1); // Costly O(N) deletion in loop!
  }
  return tArr.length === 0;
}""",
        "v2_title": "The Intermediate Approach (Sorting O(N log N))",
        "v2_why": "Converts both strings to arrays, sorts them, and checks if the sorted strings are identical.",
        "v2_code": """function isAnagramSort(s, t) {
  if (s.length !== t.length) return false;
  return s.split('').sort().join('') === t.split('').sort().join('');
}""",
        "v3_title": "The Senior / Optimal Approach (26-Char Frequency Array O(N) Time, O(1) Space)",
        "v3_js": """function isAnagram(s, t) {
  // Line 1: If lengths differ, cannot be anagrams
  if (s.length !== t.length) return false;

  // Line 2: Fixed size 26 array for lowercase 'a'-'z' (O(1) auxiliary space!)
  const count = new Array(26).fill(0);

  // Line 3: Single loop counting both strings
  for (let i = 0; i < s.length; i++) {
    // Increment for string s
    count[s.charCodeAt(i) - 97]++;
    // Decrement for string t
    count[t.charCodeAt(i) - 97]--;
  }

  // Line 4: Ensure every character count cancelled out to 0
  for (let i = 0; i < 26; i++) {
    if (count[i] !== 0) return false;
  }

  return true;
}""",
        "v3_py": """def isAnagram(s: str, t: str) -> bool:
    # Line 1: Quick length check
    if len(s) != len(t):
        return False
        
    # Line 2: Fixed size 26 frequency list
    count = [0] * 26
    
    # Line 3: Traverse both strings simultaneously
    for a, b in zip(s, t):
        count[ord(a) - ord('a')] += 1
        count[ord(b) - ord('a')] -= 1
        
    # Line 4: Check if all character balance counts are zero
    return all(x == 0 for x in count)""",
        "pitch": "Sorting both strings takes O(N log N) time and O(N) space. The optimal solution uses a fixed-size 26-element integer array. In a single pass, we increment counts for characters in s and decrement for t, verifying all counts are zero. This achieves O(N) linear time with true O(1) constant auxiliary space.",
        "star": "Search catalog keyword sanitizer normalizing and matching permuted localized tag searches.",
        "action": "Replaced regex-based permutation matching with fixed-size character frequency histograms.",
        "metrics": "Parsed 2.5 million tags with zero heap allocation overhead; dropped query latency from 45ms to 2ms.",
        "transfer": "LeetCode 49 (Group Anagrams), LeetCode 438 (Find All Anagrams in a String using Sliding Window)."
    },

    # -------------------------------------------------------------
    # 02-two-pointers
    # -------------------------------------------------------------
    {
        "cat": "02-two-pointers", "id": 9, "lc": 125, "title": "Valid Palindrome", "diff": "Easy",
        "statement": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers. Given a string s, return true if it is a palindrome, or false otherwise.",
        "examples": """Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters. Since an empty string reads the same forward and backward, it is a palindrome.""",
        "constraints": """* 1 <= s.length <= 2 * 10^5
* s consists only of printable ASCII characters.""",
        "hinglish": "String ko aage aur piche se padhne par exact same lagna chahiye. Capital/Small ka farak nahi padta aur spaces/symbols ignore karne hain.",
        "analogy": "Inspecting a mirrored sign: you start at both outer edges simultaneously and walk towards the center, checking that every character mirrors its opposite.",
        "foundation_name": "Two Pointers (Opposite Direction Convergence)",
        "foundation_desc": "Two Pointers technique places one pointer at the start (left = 0) and one at the end (right = len - 1), moving inward until they meet.",
        "when_use": "In symmetric checks, finding pairs in sorted arrays, reversing collections, or container volume problems.",
        "when_not": "When the collection has no random access (e.g., singly-linked list without length or reversal).",
        "visual_trace": """s = "A man, a plan, a canal: Panama"
Cleaned conceptually: "amanaplanacanalpanama"
L = 0 ('a'), R = 20 ('a') -> Match! L++, R--
L = 1 ('m'), R = 19 ('m') -> Match! L++, R--
...
Pointers cross in the middle -> Valid Palindrome! 🎉""",
        "v1_title": "The Absolute Newbie Approach (Regex + Reverse String O(N) Space)",
        "v1_why": "Cleans the string with regex, creates a reversed copy, and compares strings. Requires allocating brand new strings in memory.",
        "v1_code": """function isPalindromeNewbie(s) {
  // Line 1: Regex strips non-alphanumerics into new string
  const clean = s.toLowerCase().replace(/[^a-z0-9]/g, '');
  // Line 2: Creates reversed copy in memory
  const reversed = clean.split('').reverse().join('');
  return clean === reversed;
}""",
        "v2_title": "The Intermediate Approach (Array Conversion Two Pointers)",
        "v2_why": "Cleans characters into an array first, then uses two pointers. Better, but still uses O(N) extra space for the array.",
        "v2_code": """function isPalindromeIntermediate(s) {
  const chars = [];
  for (const c of s.toLowerCase()) {
    if ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')) chars.push(c);
  }
  let l = 0, r = chars.length - 1;
  while (l < r) {
    if (chars[l] !== chars[r]) return false;
    l++; r--;
  }
  return true;
}""",
        "v3_title": "The Senior / Optimal Approach (In-Place Two Pointers O(N) Time, O(1) Space)",
        "v3_js": """function isPalindrome(s) {
  // Line 1: Left pointer at index 0, Right pointer at end
  let l = 0, r = s.length - 1;

  // Line 2: Helper to check alphanumeric characters without regex overhead
  const isAlphanumeric = (c) => {
    const code = c.charCodeAt(0);
    return (code >= 48 && code <= 57) ||  // 0-9
           (code >= 65 && code <= 90) ||  // A-Z
           (code >= 97 && code <= 122);   // a-z
  };

  // Line 3: Move pointers towards center
  while (l < r) {
    // Skip non-alphanumeric characters on left
    while (l < r && !isAlphanumeric(s[l])) l++;
    // Skip non-alphanumeric characters on right
    while (l < r && !isAlphanumeric(s[r])) r--;

    // Compare characters case-insensitively
    if (s[l].toLowerCase() !== s[r].toLowerCase()) {
      return false;
    }

    l++;
    r--;
  }

  return true;
}""",
        "v3_py": """def isPalindrome(s: str) -> bool:
    # Line 1: Two pointers at edges
    l, r = 0, len(s) - 1
    
    # Line 2: Scan towards center
    while l < r:
        # Line 3: Skip non-alphanumeric on left
        while l < r and not s[l].isalnum():
            l += 1
        # Line 4: Skip non-alphanumeric on right
        while l < r and not s[r].isalnum():
            r -= 1
            
        # Line 5: Compare case-insensitively
        if s[l].lower() != s[r].lower():
            return False
            
        l += 1
        r -= 1
        
    return True""",
        "pitch": "Reversing the cleaned string takes O(N) time and O(N) memory allocation. The optimal solution uses an in-place two-pointer approach, skipping non-alphanumeric characters on the fly. This achieves O(N) time complexity with true O(1) auxiliary space, avoiding garbage collection pressure on large text buffers.",
        "star": "Data quality ingestion pipeline validating symmetric ISBN voucher codes across 10 million daily records.",
        "action": "Eliminated regex and string reversal allocations in favor of ASCII code point two-pointer validation.",
        "metrics": "Reduced memory consumption by 92%; boosted pipeline throughput from 1,200 records/sec to 18,500 records/sec.",
        "transfer": "LeetCode 680 (Valid Palindrome II with one deletion), LeetCode 11 (Container With Most Water)."
    },

    # -------------------------------------------------------------
    # 03-sliding-window
    # -------------------------------------------------------------
    {
        "cat": "03-sliding-window", "id": 12, "lc": 121, "title": "Best Time to Buy and Sell Stock", "diff": "Easy",
        "statement": "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "examples": """Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.""",
        "constraints": """* 1 <= prices.length <= 10^5
* 0 <= prices[i] <= 10^4""",
        "hinglish": "Stock saste me kharidna hai aur aage chal kar mehenge me bechna hai. History ka sabse lowest price yaad rakho aur roz ka profit calculate karo.",
        "analogy": "Tracking the lowest historic price of a flight ticket: you buy at the lowest valley, and sell at the highest subsequent peak.",
        "foundation_name": "Sliding Window / Running Minimum Tracking",
        "foundation_desc": "Maintains a running state of the minimum buy price observed so far, comparing each subsequent price to compute potential profit.",
        "when_use": "When maximizing difference between two elements where the smaller element must precede the larger element.",
        "when_not": "When multiple buy-sell transactions are allowed (use Greedy LeetCode 122 instead).",
        "visual_trace": """prices = [7, 1, 5, 3, 6, 4]
Day 0: price = 7, min = 7, profit = 0
Day 1: price = 1, min = 1, profit = 0
Day 2: price = 5, min = 1, profit = 5 - 1 = 4
Day 3: price = 3, min = 1, profit = 3 - 1 = 2
Day 4: price = 6, min = 1, profit = 6 - 1 = 5 (Max!)
Day 5: price = 4, min = 1, profit = 4 - 1 = 3
Max Profit = 5 🎉""",
        "v1_title": "The Absolute Newbie Approach (Nested Loops O(N^2))",
        "v1_why": "Checks every buy day and every future sell day. Quadratic time complexity causes TLE for N=100,000.",
        "v1_code": """function maxProfitBrute(prices) {
  let maxProfit = 0;
  for (let i = 0; i < prices.length; i++) {
    for (let j = i + 1; j < prices.length; j++) {
      const profit = prices[j] - prices[i];
      maxProfit = Math.max(maxProfit, profit);
    }
  }
  return maxProfit;
}""",
        "v2_title": "The Intermediate Approach (Auxiliary Max Future Array O(N) Space)",
        "v2_why": "Builds an array of maximum future prices looking right-to-left, then compares in a second pass. Uses O(N) extra space.",
        "v2_code": """function maxProfitTwoPass(prices) {
  const n = prices.length;
  const maxFuture = new Array(n);
  maxFuture[n - 1] = prices[n - 1];
  for (let i = n - 2; i >= 0; i--) {
    maxFuture[i] = Math.max(prices[i], maxFuture[i + 1]);
  }
  let maxProfit = 0;
  for (let i = 0; i < n; i++) {
    maxProfit = Math.max(maxProfit, maxFuture[i] - prices[i]);
  }
  return maxProfit;
}""",
        "v3_title": "The Senior / Optimal Approach (One-Pass Running Minimum O(N) Time, O(1) Space)",
        "v3_js": """function maxProfit(prices) {
  // Line 1: Track lowest purchase price seen so far
  let minPrice = Infinity;
  // Line 2: Track maximum profit achieved
  let maxProfit = 0;

  // Line 3: Single pass over daily prices
  for (let i = 0; i < prices.length; i++) {
    const currentPrice = prices[i];
    // Update minimum price if current day is cheaper
    if (currentPrice < minPrice) {
      minPrice = currentPrice;
    } else {
      // Calculate profit if sold today and update maxProfit
      const profit = currentPrice - minPrice;
      if (profit > maxProfit) {
        maxProfit = profit;
      }
    }
  }

  return maxProfit;
}""",
        "v3_py": """def maxProfit(prices: list[int]) -> int:
    # Line 1: Running minimum price and maximum profit trackers
    min_price = float('inf')
    max_profit = 0
    
    # Line 2: Single pass O(N)
    for price in prices:
        # Update minimum buy price
        min_price = min(min_price, price)
        # Update maximum profit if sold today
        max_profit = max(max_profit, price - min_price)
        
    return max_profit""",
        "pitch": "The brute-force method checks every pair in O(N^2) time. The optimal solution uses a single-pass running minimum strategy in O(N) time and O(1) space. By tracking the lowest price seen so far, we calculate the potential profit at each step and update the global maximum, guaranteeing optimal execution in a single pass.",
        "star": "Cryptocurrency algorithmic trading feed identifying peak historical dip opportunities across high-frequency tick prices.",
        "action": "Implemented streaming single-pass running-minimum window tracking.",
        "metrics": "Processed 1,000,000 live tick prices in sub-millisecond real-time with zero memory allocations.",
        "transfer": "LeetCode 53 (Maximum Subarray / Kadane's Algorithm), LeetCode 122 (Best Time to Buy and Sell Stock II)."
    },

    # -------------------------------------------------------------
    # 04-stack
    # -------------------------------------------------------------
    {
        "cat": "04-stack", "id": 16, "lc": 20, "title": "Valid Parentheses", "diff": "Easy",
        "statement": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets, and open brackets must be closed in the correct order, and every close bracket has a corresponding open bracket of the same type.",
        "examples": """Input: s = "()"
Output: true

Input: s = "()[]{}"
Output: true

Input: s = "(]"
Output: false""",
        "constraints": """* 1 <= s.length <= 10^4
* s consists of parentheses only '()[]{}'.""",
        "hinglish": "Brackets sahi order me open aur close hone chahiye. Jo bracket sabse last me open hua hai, wahi sabse pehle close hona chahiye (LIFO - Last In First Out).",
        "analogy": "A stack of plates in a cafeteria: the plate placed on top last must be picked up first.",
        "foundation_name": "Stack (Last-In, First-Out - LIFO)",
        "foundation_desc": "A Stack pushes elements on top and pops from the top. It is the fundamental data structure for nested matching, syntax parsing, and call execution.",
        "when_use": "Whenever dealing with nested structures, balanced tags, undo operations, or expression parsing.",
        "when_not": "When first-come, first-served order is needed (use a Queue FIFO instead).",
        "visual_trace": """s = "([{}])"
Char '(': Push to stack -> Stack: ['(']
Char '[': Push to stack -> Stack: ['(', '[']
Char '{': Push to stack -> Stack: ['(', '[', '{']
Char '}': Closing bracket! Pop top: '{' matches '}' -> Stack: ['(', '[']
Char ']': Closing bracket! Pop top: '[' matches ']' -> Stack: ['(']
Char ')': Closing bracket! Pop top: '(' matches ')' -> Stack: []
Stack is empty -> Valid Parentheses! 🎉""",
        "v1_title": "The Absolute Newbie Approach (String Replace Loop O(N^2))",
        "v1_why": "Continuously replaces '()', '[]', '{}' with '' until string length stops changing. Extremely slow O(N^2) due to string reallocations.",
        "v1_code": """function isValidBrute(s) {
  let prevLen = -1;
  while (s.length !== prevLen) {
    prevLen = s.length;
    s = s.replace('()', '').replace('[]', '').replace('{}', '');
  }
  return s.length === 0;
}""",
        "v2_title": "The Intermediate Approach (Stack with If/Else Branches)",
        "v2_why": "Uses a stack but hardcodes multiple nested if/else statements instead of a clean hash map lookup table.",
        "v2_code": """function isValidIntermediate(s) {
  const stack = [];
  for (const c of s) {
    if (c === '(' || c === '[' || c === '{') stack.push(c);
    else if (c === ')' && stack.pop() !== '(') return false;
    else if (c === ']' && stack.pop() !== '[') return false;
    else if (c === '}' && stack.pop() !== '{') return false;
  }
  return stack.length === 0;
}""",
        "v3_title": "The Senior / Optimal Approach (Stack with Hash Map O(N) Time, O(N) Space)",
        "v3_js": """function isValid(s) {
  // Odd length strings can never be balanced!
  if (s.length % 2 !== 0) return false;

  // Line 1: Stack to hold open brackets
  const stack = [];
  // Line 2: Map closing bracket -> corresponding opening bracket
  const map = {
    ')': '(',
    '}': '{',
    ']': '['
  };

  // Line 3: Process characters one by one
  for (let i = 0; i < s.length; i++) {
    const char = s[i];

    // If character is a closing bracket
    if (map[char]) {
      // Check if top of stack matches the expected opening bracket
      if (stack.pop() !== map[char]) {
        return false;
      }
    } else {
      // Opening bracket: push to stack
      stack.push(char);
    }
  }

  // Line 4: Stack must be completely empty
  return stack.length === 0;
}""",
        "v3_py": """def isValid(s: str) -> bool:
    # Odd length strings can never be valid
    if len(s) % 2 != 0:
        return False
        
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # Pop top element or dummy character if stack empty
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack""",
        "pitch": "A Stack data structure naturally models LIFO nested matching. As we iterate through the string, open brackets are pushed onto the stack. For every closing bracket, we check if it matches the top of the stack. If it does not, or if the stack is empty, the string is invalid. This achieves optimal O(N) time and O(N) space complexity.",
        "star": "Expression evaluation parser in a low-code rule engine crashing on unbalanced parentheses.",
        "action": "Engineered a pre-compilation syntax validation pass using a Stack and symbol map.",
        "metrics": "Caught 100% of syntax errors before query execution; reduced runtime execution crashes to zero.",
        "transfer": "LeetCode 71 (Simplify Path), LeetCode 150 (Evaluate Reverse Polish Notation)."
    }
]

def update_gold_standard():
    count = 0
    for item in BLIND_75_GOLD:
        cat_dir = os.path.join(LEETCODE_BASE, item["cat"])
        os.makedirs(cat_dir, exist_ok=True)
        fname = f"{item['id']:02d}_{item['title'].lower().replace(' ', '_').replace('-', '_')}.md"
        fpath = os.path.join(cat_dir, fname)

        content = f"""# {item['id']:02d}. {item['title']} (LeetCode {item['lc']}) — Comprehensive Deep Dive

> **Category:** {item['cat'].replace('-', ' ').title()}  
> **Difficulty:** {item['diff']}  
> **Target Roles:** SDE-1, SDE-2, SDE-3, Senior Technical Lead, System Architect  

---

## 📜 Official LeetCode Problem Statement

{item['statement']}

### 📥 Examples:
```text
{item['examples']}
```

### ⚠️ Constraints & Edge Cases:
{item['constraints']}

---

## 🐣 Layman's Analogy (Hinglish + Real-World)

> **Hinglish Intuition:**  
> {item['hinglish']}
>
> **Real-World Analogy:**  
> {item['analogy']}

---

## 🧠 DSA Foundation: What IS {item['foundation_name']} & Why Does It Matter?

{item['foundation_desc']}

### ❓ When to Apply?
- {item['when_use']}

### 🚫 When NOT to Apply?
- {item['when_not']}

---

## 📊 Visual Step-by-Step Tracing

```text
{item['visual_trace']}
```

---

## 💻 The 3 Evolution Versions (Newbie ➡️ Intermediate ➡️ Senior)

---

### ❌ Version 1: {item['v1_title']}

#### 💡 How the Newbie Thinks & Why It Fails:
*{item['v1_why']}*

```javascript
{item['v1_code']}
```

---

### ⚠️ Version 2: {item['v2_title']}

#### 💡 How the Intermediate Thinks:
*{item['v2_why']}*

```javascript
{item['v2_code']}
```

---

### ✅ Version 3: {item['v3_title']}

#### JavaScript / TypeScript Implementation (Line-by-Line Commented)
```javascript
{item['v3_js']}
```

#### Python 3 Implementation (Line-by-Line Commented)
```python
{item['v3_py']}
```

---

## 🎯 The Senior Interview Pitch (Say Exactly This!)

> **Interviewer:** *"Walk me through how you solve {item['title']}."*
>
> **You:**  
> *"{item['pitch']}"*

---

## 💼 Real-World Project Challenge (STAR Production Story)

* **Situation:** {item['star']}
* **The Problem:** Resolving scalability bottlenecks, excessive CPU/RAM consumption, or operational failures.
* **The Action:** {item['action']}
* **The Result & Metrics:** {item['metrics']}

---

## 🔄 Pattern Transferability: Where Else Can You Apply This?

Once you master this pattern, you can apply it directly to:
- **{item['transfer']}**
"""
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"Generated Gold-Standard problem: {fpath}")

    print(f"Successfully generated {count} Gold-Standard problem files!")

if __name__ == "__main__":
    update_gold_standard()
