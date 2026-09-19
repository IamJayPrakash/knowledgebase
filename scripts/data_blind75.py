# 75 Blind 75 Problem Dataset with 6-Pillar Format
# Every code example has line-by-line comments explaining what and why

BLIND_75_DATA = [
    # 01-Arrays & Hashing (1-8)
    {
        "cat": "01-arrays-and-hashing", "id": 1, "lc": 1, "title": "Two Sum", "diff": "Easy",
        "hinglish": "Budget fix hai (target). Har element dekhte waqt check karo ki (target - current_element) pehle dekha hai ya nahi.",
        "analogy": "Target bill in grocery shopping. Keep a clipboard of prices needed to reach the total.",
        "brute": "Nested loops comparing all pairs (nums[i] + nums[j] == target). Time: O(N^2), Space: O(1).",
        "optimal": "One-pass Hash Map storing number -> index. Lookup complement in O(1). Time: O(N), Space: O(N).",
        "py": """def twoSum(nums, target):
    # Dictionary/Hash Map to store { number: its_index } for O(1) instant lookup
    seen = {}
    
    # Iterate through the array getting both index 'i' and the current value 'n'
    for i, n in enumerate(nums):
        # Calculate the complement needed: target minus current number
        diff = target - n
        
        # Check if the needed complement was already seen in our dictionary
        if diff in seen:
            # If found, return the index of the complement and the current index
            return [seen[diff], i]
            
        # Store the current number with its index in the dictionary for future checks
        seen[n] = i
        
    # Return empty list if no pair is found (safety fallback)
    return []""",
        "js": """function twoSum(nums, target) {
    // Create a Map to store { number => index } for O(1) time complexity lookups
    const map = new Map();
    
    // Loop through each element in the array with index 'i'
    for (let i = 0; i < nums.length; i++) {
        // Calculate the complement needed: target minus current number
        const diff = target - nums[i];
        
        // If our Map already contains the complement we need
        if (map.has(diff)) {
            // Return an array containing the stored index and the current index
            return [map.get(diff), i];
        }
        
        // Otherwise, save the current number and its index in the Map
        map.set(nums[i], i);
    }
    
    // Fallback: return an empty array if no matching pair exists
    return [];
}""",
        "diagram": "[2, 7, 11, 15], Target=9\ni=0: num=2, diff=7, Map={2:0}\ni=1: num=7, diff=2, Map has 2! -> Return [0, 1]",
        "star": "Fintech ledger reconciliation engine matching unsettled credit transactions with pending invoice receipts. Replaced nested loop with hash-set lookup.",
        "metrics": "Execution time dropped from 45 minutes to 7.8 seconds for 50,000 daily transaction batches."
    },

    {
        "cat": "01-arrays-and-hashing", "id": 2, "lc": 217, "title": "Contains Duplicate", "diff": "Easy",
        "hinglish": "Check karo array me koi number 2 ya usse zyada baar aaya hai. Set use karo.",
        "analogy": "Guest list at event door. Check if person's name is already checked in on the sheet.",
        "brute": "Sort array and compare adjacent elements. Time: O(N log N), Space: O(1).",
        "optimal": "Hash Set single pass. If num in set, return True. Time: O(N), Space: O(N).",
        "py": """def containsDuplicate(nums):
    # Create an empty hash set to record numbers we have already seen
    seen = set()
    
    # Traverse through each number in the array
    for n in nums:
        # If the number is already in our set, we found a duplicate!
        if n in seen:
            # Return True immediately without checking remaining elements
            return True
        # Otherwise, record this number in the set
        seen.add(n)
        
    # If the loop finishes without returning, all elements are unique
    return False""",
        "js": """function containsDuplicate(nums) {
    // Create a Set to store unique values with O(1) lookup time
    const set = new Set();
    
    // Iterate through every number in the array
    for (const n of nums) {
        // If the set already has this number, duplicate detected
        if (set.has(n)) {
            return true;
        }
        // Add the current number to the set
        set.add(n);
    }
    
    // No duplicates found after scanning the entire array
    return false;
}""",
        "diagram": "[1, 2, 3, 1]\nSeen: {1} -> {1, 2} -> {1, 2, 3} -> 1 is already in Set! -> Return True",
        "star": "Bulk CSV importer for employee phone numbers. Deduplicated records in memory before running database transactions.",
        "metrics": "Prevented 100% of batch primary key constraint rollbacks and cut processing time from 3 mins to 4 secs."
    },

    {
        "cat": "01-arrays-and-hashing", "id": 3, "lc": 242, "title": "Valid Anagram", "diff": "Easy",
        "hinglish": "Do words anagram tab hain jab dono me exact same letters exact same frequency me hon.",
        "analogy": "Scrabble tiles: both words must be formed by rearranging the identical set of letter tiles.",
        "brute": "Sort both strings and check if sorted(s) == sorted(t). Time: O(N log N), Space: O(N).",
        "optimal": "26-length fixed frequency array. Increment for s, decrement for t. Time: O(N), Space: O(1).",
        "py": """def isAnagram(s: str, t: str) -> bool:
    # If string lengths differ, they cannot be anagrams
    if len(s) != len(t):
        return False
        
    # Fixed size frequency array of 26 zeros for lowercase English letters
    count = [0] * 26
    
    # Iterate through both strings simultaneously
    for a, b in zip(s, t):
        # Increment frequency count for character in string 's'
        count[ord(a) - ord('a')] += 1
        # Decrement frequency count for character in string 't'
        count[ord(b) - ord('a')] -= 1
        
    # If all frequency counts are exactly 0, strings are valid anagrams
    return all(x == 0 for x in count)""",
        "js": """function isAnagram(s, t) {
    // Quick check: strings of unequal length cannot be anagrams
    if (s.length !== t.length) return false;
    
    // Array of 26 zeros to track character frequencies (index 0 = 'a', 25 = 'z')
    const freq = new Array(26).fill(0);
    
    // Count characters in both strings in a single loop
    for (let i = 0; i < s.length; i++) {
        // Increment for string s
        freq[s.charCodeAt(i) - 97]++;
        // Decrement for string t
        freq[t.charCodeAt(i) - 97]--;
    }
    
    // Check if every character count cancelled out to zero
    return freq.every(x => x === 0);
}""",
        "diagram": "s='anagram', t='nagaram'\nFrequency counter counts all characters to 0 -> True",
        "star": "Multilingual search catalog keyword sanitizer. Matched permuted tag search queries without running heavy regex scans.",
        "metrics": "Processed 2.5 million tags with zero heap allocation overhead; dropped query latency from 45ms to 2ms."
    },

    {
        "cat": "01-arrays-and-hashing", "id": 4, "lc": 49, "title": "Group Anagrams", "diff": "Medium",
        "hinglish": "Jo words ek dusre ke anagram hain unko ek group me rakhna hai. Sorted word ya char-frequency tuple ko hashmap key banao.",
        "analogy": "Sorting library books into shelves where all books with the same character combination go to the same shelf.",
        "brute": "Compare every word pair with O(N^2) anagram checks. Time: O(N^2 * K).",
        "optimal": "HashMap with sorted string or 26-char count tuple as key. Time: O(N * K log K) or O(N * K), Space: O(N * K).",
        "py": """from collections import defaultdict

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
    return list(groups.values())""",
        "js": """function groupAnagrams(strs) {
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
}""",
        "diagram": "Input: ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']\nKey 'aet' -> ['eat', 'tea', 'ate']\nKey 'ant' -> ['tan', 'nat']\nKey 'abt' -> ['bat']",
        "star": "E-commerce product catalog deduplication. Clustered scraped vendor titles that only differed in word order.",
        "metrics": "Cleaned up 1.2M duplicate product listings, saving 35% database index storage."
    },

    {
        "cat": "01-arrays-and-hashing", "id": 5, "lc": 347, "title": "Top K Frequent Elements", "diff": "Medium",
        "hinglish": "Array me se k sabse zyada aane wale elements nikalne hain. Bucket sort se O(N) me bina sorting ke solve karo.",
        "analogy": "Counting votes where buckets represent vote counts, reading from highest bucket down.",
        "brute": "HashMap frequency count + sort by count. Time: O(N log N), Space: O(N).",
        "optimal": "Bucket sort where bucket index represents frequency count. Time: O(N), Space: O(N).",
        "py": """def topKFrequent(nums, k):
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
                return res""",
        "js": """function topKFrequent(nums, k) {
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
}""",
        "diagram": "nums=[1,1,1,2,2,3], k=2\nCounts: {1:3, 2:2, 3:1}\nBuckets: [3: [1], 2: [2], 1: [3]] -> Output: [1, 2]",
        "star": "Real-time trending hashtag generation on a high-throughput event live stream.",
        "metrics": "Processed 15k events/sec with sub-10ms response time on trending dashboard widgets."
    },

    {
        "cat": "01-arrays-and-hashing", "id": 6, "lc": 238, "title": "Product of Array Except Self", "diff": "Medium",
        "hinglish": "Har index par baaki sabhi numbers ka product chahiye bina division operator use kiye. Prefix product aur Postfix product multiply karo.",
        "analogy": "Calculating your net balance without looking at your own transaction by multiplying previous transactions with future transactions.",
        "brute": "Nested loop multiplying all other items for each index. Time: O(N^2), Space: O(1).",
        "optimal": "Compute prefix products in first pass, multiply with postfix products in reverse pass. Time: O(N), Space: O(1) auxiliary.",
        "py": """def productExceptSelf(nums):
    # Output array initialized with 1s
    res = [1] * len(nums)
    
    # Step 1: Calculate prefix products (product of all elements to the left)
    prefix = 1
    for i in range(len(nums)):
        # Store prefix product accumulated so far for index i
        res[i] = prefix
        # Update prefix product including current element nums[i]
        prefix *= nums[i]
        
    # Step 2: Calculate postfix products (product of all elements to the right)
    postfix = 1
    for i in range(len(nums) - 1, -1, -1):
        # Multiply current prefix product with postfix product from the right
        res[i] *= postfix
        # Update postfix product including current element nums[i]
        postfix *= nums[i]
        
    # Return the completed product array
    return res""",
        "js": """function productExceptSelf(nums) {
    // Initialize result array with 1s
    const res = new Array(nums.length).fill(1);
    
    // Step 1: Forward pass for prefix products (left of index)
    let prefix = 1;
    for (let i = 0; i < nums.length; i++) {
        res[i] = prefix;
        prefix *= nums[i];
    }
    
    // Step 2: Backward pass for postfix products (right of index)
    let postfix = 1;
    for (let i = nums.length - 1; i >= 0; i--) {
        res[i] *= postfix;
        postfix *= nums[i];
    }
    
    return res;
}""",
        "diagram": "nums =   [1,  2,  3,  4]\nPrefix:  [1,  1,  2,  6]\nPostfix: [24, 12, 4,  1]\nResult:  [24, 12, 8,  6]",
        "star": "Financial portfolio risk analysis engine avoiding floating point division-by-zero errors when calculating variance weights.",
        "metrics": "Prevented division-by-zero crashes on 500k real-time asset evaluations."
    },

    {
        "cat": "02-two-pointers", "id": 9, "lc": 125, "title": "Valid Palindrome", "diff": "Easy",
        "hinglish": "String ko aage aur piche se padhne par same lagna chahiye. Non-alphanumeric hatao aur do pointers (left aur right) se compare karo.",
        "analogy": "Inspecting a mirrored sign from both ends towards the center simultaneously.",
        "brute": "Reverse entire cleaned string and check equality. Time: O(N), Space: O(N).",
        "optimal": "Two pointers (left=0, right=len-1) skipping non-alphanumerics in-place. Time: O(N), Space: O(1).",
        "py": """def isPalindrome(s: str) -> bool:
    # Initialize left pointer at the start and right pointer at the end
    l, r = 0, len(s) - 1
    
    # Continue until both pointers meet in the middle
    while l < r:
        # Move left pointer forward if current character is not alphanumeric
        while l < r and not s[l].isalnum():
            l += 1
            
        # Move right pointer backward if current character is not alphanumeric
        while l < r and not s[r].isalnum():
            r -= 1
            
        # Compare characters case-insensitively
        if s[l].lower() != s[r].lower():
            # Mismatch found: not a palindrome
            return False
            
        # Move both pointers inward for next comparison
        l += 1
        r -= 1
        
    # All characters matched successfully
    return True""",
        "js": """function isPalindrome(s) {
    // Two pointers: left starting at index 0, right starting at the end
    let l = 0, r = s.length - 1;
    
    // Scan inward towards the center
    while (l < r) {
        // Skip non-alphanumeric characters on the left side
        while (l < r && !/[a-zA-Z0-9]/.test(s[l])) l++;
        
        // Skip non-alphanumeric characters on the right side
        while (l < r && !/[a-zA-Z0-9]/.test(s[r])) r--;
        
        // Case-insensitive character comparison
        if (s[l].toLowerCase() !== s[r].toLowerCase()) {
            return false; // Characters do not match
        }
        
        // Move both pointers towards center
        l++;
        r--;
    }
    
    return true; // Symmetric match confirmed
}""",
        "diagram": "'A man, a plan, a canal: Panama'\nL='a', R='a' -> match\nL='m', R='m' -> match -> Valid palindrome!",
        "star": "Data quality validation pipeline checking symmetric ISBN and serial voucher barcodes.",
        "metrics": "Eliminated string memory allocations, speeding up batch data ingestion by 4x."
    },

    {
        "cat": "02-two-pointers", "id": 10, "lc": 15, "title": "3Sum", "diff": "Medium",
        "hinglish": "Teen numbers jinka sum 0 ho. Array sort karo, ek number fix karo aur baaki do par Two Pointers lagao.",
        "analogy": "Forming a 3-person team where the first member is fixed, and the remaining two are selected from both ends.",
        "brute": "Three nested loops checking all triplets. Time: O(N^3), Space: O(1).",
        "optimal": "Sort array, loop i from 0 to N-2, use two pointers for remaining range. Skip duplicates. Time: O(N^2), Space: O(1) or O(N).",
        "py": """def threeSum(nums):
    # Sort array in ascending order to enable Two Pointers technique
    nums.sort()
    res = []
    
    # Fix the first number at index i
    for i in range(len(nums) - 2):
        # Skip duplicate first numbers to prevent duplicate triplets in result
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        # Left pointer starts right after i; Right pointer starts at array end
        l, r = i + 1, len(nums) - 1
        
        while l < r:
            # Calculate sum of triplet
            total = nums[i] + nums[l] + nums[r]
            
            # If sum is too small, move left pointer right to increase sum
            if total < 0:
                l += 1
            # If sum is too large, move right pointer left to decrease sum
            elif total > 0:
                r -= 1
            else:
                # Triplet sum is 0: add to result
                res.append([nums[i], nums[l], nums[r]])
                
                # Skip duplicate left elements
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                # Skip duplicate right elements
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                    
                # Advance both pointers after finding valid triplet
                l += 1
                r -= 1
                
    return res""",
        "js": """function threeSum(nums) {
    // Sort numbers in ascending order
    nums.sort((a, b) => a - b);
    const res = [];
    
    // Fix first element
    for (let i = 0; i < nums.length - 2; i++) {
        // Skip duplicates for the first element
        if (i > 0 && nums[i] === nums[i - 1]) continue;
        
        // Two pointers for remaining range
        let l = i + 1, r = nums.length - 1;
        while (l < r) {
            const sum = nums[i] + nums[l] + nums[r];
            if (sum < 0) {
                l++; // Need bigger sum
            } else if (sum > 0) {
                r--; // Need smaller sum
            } else {
                res.push([nums[i], nums[l], nums[r]]);
                // Skip duplicates for second and third elements
                while (l < r && nums[l] === nums[l + 1]) l++;
                while (l < r && nums[r] === nums[r - 1]) r--;
                l++;
                r--;
            }
        }
    }
    return res;
}""",
        "diagram": "nums=[-1, 0, 1, 2, -1, -4] -> Sorted: [-4, -1, -1, 0, 1, 2]\ni=-1, l=-1, r=2: sum = 0 -> [-1, -1, 2]\ni=-1, l=0, r=1: sum = 0 -> [-1, 0, 1]",
        "star": "Financial arbitrage scanner detecting zero-risk 3-currency triangular currency cycles.",
        "metrics": "Processed 10,000 FX pairs under 15ms avoiding quadratic explosion."
    },

    {
        "cat": "03-sliding-window", "id": 12, "lc": 121, "title": "Best Time to Buy and Sell Stock", "diff": "Easy",
        "hinglish": "Stock saste me kharidna hai aur mehenge me bechna hai. Minimum price track karte chalo aur har din maximum profit calculate karo.",
        "analogy": "Tracking the lowest purchase price you ever saw in history and calculating your profit if you sold today.",
        "brute": "Nested loops checking every buy and sell day pair. Time: O(N^2), Space: O(1).",
        "optimal": "Single pass tracking min_price and max_profit. Time: O(N), Space: O(1).",
        "py": """def maxProfit(prices):
    # Track the lowest price observed so far (start at infinity)
    min_price = float('inf')
    # Track the maximum profit achieved so far
    max_profit = 0
    
    # Iterate through prices on each consecutive day
    for price in prices:
        # Update minimum buy price if current day price is lower
        min_price = min(min_price, price)
        # Calculate profit if sold today, update max_profit if greater
        max_profit = max(max_profit, price - min_price)
        
    # Return highest profit possible (or 0 if only losses were possible)
    return max_profit""",
        "js": """function maxProfit(prices) {
    // Initialize minimum price to Infinity
    let minPrice = Infinity;
    // Initialize maximum profit to 0
    let maxProfit = 0;
    
    // Traverse through daily stock prices
    for (const price of prices) {
        // Keep track of lowest historical purchase price
        minPrice = Math.min(minPrice, price);
        // Calculate profit if sold today, keep track of maximum
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    
    return maxProfit;
}""",
        "diagram": "[7, 1, 5, 3, 6, 4]\nMin so far: 7 -> 1 -> 1 -> 1 -> 1\nProfits: 0, 0, (5-1)=4, (3-1)=2, (6-1)=5 (Max) -> Result = 5",
        "star": "Crypto automated algorithmic trading bot identifying historical dip opportunities.",
        "metrics": "Executed in sub-millisecond O(N) streaming fashion over 1,000,000 tick prices."
    },

    {
        "cat": "03-sliding-window", "id": 13, "lc": 3, "title": "Longest Substring Without Repeating Characters", "diff": "Medium",
        "hinglish": "Bina kisi duplicate character ke sabse lambi substring ka length chahiye. Sliding window + Set ya Map use karo.",
        "analogy": "A camera aperture window that expands right until a duplicate is spotted, then contracts from left until duplicate is expelled.",
        "brute": "Check all substrings for duplicates. Time: O(N^3) or O(N^2), Space: O(min(N, M)).",
        "optimal": "Sliding window with Set/Map. Right pointer expands, Left pointer shrinks window on duplicate. Time: O(N), Space: O(min(N, M)).",
        "py": """def lengthOfLongestSubstring(s: str) -> int:
    # Set to store unique characters currently inside our sliding window
    char_set = set()
    # Left pointer of the sliding window and max length tracker
    l = 0
    max_len = 0
    
    # Expand the right pointer 'r' across the string
    for r in range(len(s)):
        # While the incoming character s[r] is already inside the window
        while s[r] in char_set:
            # Shrink window from the left by removing s[l]
            char_set.remove(s[l])
            l += 1
            
        # Add the new character to the window set
        char_set.add(s[r])
        # Update maximum window length achieved so far
        max_len = max(max_len, r - l + 1)
        
    return max_len""",
        "js": """function lengthOfLongestSubstring(s) {
    // Set to keep track of characters inside active sliding window
    const set = new Set();
    let l = 0, maxLen = 0;
    
    // Move right boundary 'r' forward
    for (let r = 0; r < s.length; r++) {
        // Contract window from left while duplicate character exists
        while (set.has(s[r])) {
            set.delete(s[l]);
            l++;
        }
        // Include right character in window set
        set.add(s[r]);
        // Record max window length
        maxLen = Math.max(maxLen, r - l + 1);
    }
    
    return maxLen;
}""",
        "diagram": "'abcabcbb'\n[a] -> [ab] -> [abc] (len 3)\nNext 'a' -> Shrink window: [bca] -> [cab] -> [abc] -> Max Len = 3",
        "star": "Network packet inspection engine detecting unique header token sequences without repetition.",
        "metrics": "Processed streaming packet buffers in single-pass linear time without memory spikes."
    },

    {
        "cat": "04-stack", "id": 16, "lc": 20, "title": "Valid Parentheses", "diff": "Easy",
        "hinglish": "Brackets sahi order me open aur close hone chahiye. Stack me push karo, closing bracket aane par top element match karo.",
        "analogy": "Stack of cafeteria trays. Last bracket placed on the stack must be the first one taken off and matched.",
        "brute": "Repeatedly replace '()', '[]', '{}' with '' until no changes (O(N^2)).",
        "optimal": "Stack based single pass. Push open brackets, pop and match for closing. Time: O(N), Space: O(N).",
        "py": """def isValid(s: str) -> bool:
    # Stack to hold open brackets in order
    stack = []
    # Mapping of closing bracket -> corresponding open bracket
    mapping = {')': '(', '}': '{', ']': '['}
    
    # Iterate through each character in the string
    for c in s:
        # If character is a closing bracket
        if c in mapping:
            # Check if stack is empty OR top bracket does not match
            if not stack or stack[-1] != mapping[c]:
                return False
            # Valid match: remove the matched open bracket from stack
            stack.pop()
        else:
            # If character is an open bracket, push onto stack
            stack.append(c)
            
    # Valid only if all opened brackets were successfully matched and closed
    return not stack""",
        "js": """function isValid(s) {
    // Stack array to track opening brackets (Last-In, First-Out)
    const stack = [];
    // Hash map defining valid bracket pairs
    const map = { ')': '(', '}': '{', ']': '[' };
    
    // Inspect each bracket character
    for (const c of s) {
        if (map[c]) {
            // Closing bracket encountered: pop top element and verify match
            if (stack.pop() !== map[c]) {
                return false;
            }
        } else {
            // Opening bracket encountered: push to stack
            stack.push(c);
        }
    }
    
    // Stack must be completely empty for balanced parentheses
    return stack.length === 0;
}""",
        "diagram": "s = '([{}])'\nStack: [ ( ] -> [ (, [ ] -> [ (, [, { ] -> pop { -> pop [ -> pop ( -> Empty Stack = Valid!",
        "star": "Custom JSON and AST expression parser for a low-code workflow rule evaluator.",
        "metrics": "Detected syntax errors at parse-time instantly with zero false-positives."
    }
]

print(f"Loaded {len(BLIND_75_DATA)} fully commented Blind 75 core problem definitions.")
