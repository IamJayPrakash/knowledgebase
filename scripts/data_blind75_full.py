# Full 75 Blind 75 List Metadata with Categories, IDs, Descriptions
# This module supplies the complete catalog of all 75 questions

BLIND_75_FULL_CATALOG = [
    # 01-arrays-and-hashing (1-8)
    (1, 1, "Two Sum", "01-arrays-and-hashing", "Easy", "Hash Map complement lookup", "nums[i] + nums[j] == target"),
    (2, 217, "Contains Duplicate", "01-arrays-and-hashing", "Easy", "Hash Set seen check", "Duplicate detection"),
    (3, 242, "Valid Anagram", "01-arrays-and-hashing", "Easy", "Character frequency array of size 26", "Anagram verification"),
    (4, 49, "Group Anagrams", "01-arrays-and-hashing", "Medium", "HashMap with sorted string or char-count key", "Clustering anagrams"),
    (5, 347, "Top K Frequent Elements", "01-arrays-and-hashing", "Medium", "Bucket sort by frequency counts", "Top frequency extraction"),
    (6, 238, "Product of Array Except Self", "01-arrays-and-hashing", "Medium", "Prefix and Postfix product passes", "Multiplication without division"),
    (7, 128, "Longest Consecutive Sequence", "01-arrays-and-hashing", "Medium", "HashSet checking (num - 1) sequence starts", "Longest unbroken sequence"),
    (8, 271, "Encode and Decode Strings", "01-arrays-and-hashing", "Medium", "Length prefix protocol (len#string)", "Lossless string serialization"),

    # 02-two-pointers (9-11)
    (9, 125, "Valid Palindrome", "02-two-pointers", "Easy", "Two pointers from edges skipping non-alphanumeric", "Symmetric string verification"),
    (10, 15, "3Sum", "02-two-pointers", "Medium", "Sorting + Fixed index with Two Pointers", "Zero sum triplets"),
    (11, 11, "Container With Most Water", "02-two-pointers", "Medium", "Two pointers moving smaller height wall", "Maximizing water trapped"),

    # 03-sliding-window (12-15)
    (12, 121, "Best Time to Buy and Sell Stock", "03-sliding-window", "Easy", "Single pass tracking min_price and max_profit", "Max profit calculation"),
    (13, 3, "Longest Substring Without Repeating Characters", "03-sliding-window", "Medium", "Sliding window with Set contracting on duplicate", "Unique character window"),
    (14, 424, "Longest Repeating Character Replacement", "03-sliding-window", "Medium", "Sliding window valid when (window_len - max_f) <= k", "Window replacement"),
    (15, 76, "Minimum Window Substring", "03-sliding-window", "Hard", "Two pointers expanding right, contracting left on valid", "Shortest substring containing all target chars"),

    # 04-stack (16)
    (16, 20, "Valid Parentheses", "04-stack", "Easy", "Stack matching open brackets with closing", "Syntax balancing"),

    # 05-binary-search (17-18)
    (17, 153, "Find Minimum in Rotated Sorted Array", "05-binary-search", "Medium", "Binary search comparing mid with right", "Finding rotation inflection"),
    (18, 33, "Search in Rotated Sorted Array", "05-binary-search", "Medium", "Binary search identifying sorted half", "Lookup in rotated array"),

    # 06-linked-list (19-24)
    (19, 206, "Reverse Linked List", "06-linked-list", "Easy", "Iterative 3-pointer reversal (prev, curr, next)", "In-place pointer reversal"),
    (20, 21, "Merge Two Sorted Lists", "06-linked-list", "Easy", "Dummy node with two pointer comparison", "Sorted list merging"),
    (21, 143, "Reorder List", "06-linked-list", "Medium", "Find mid + Reverse second half + Interleave nodes", "Palindromic list interleaving"),
    (22, 19, "Remove Nth Node From End of List", "06-linked-list", "Medium", "Fast pointer with n-step lead, then move together", "One pass end removal"),
    (23, 141, "Linked List Cycle", "06-linked-list", "Easy", "Floyd's Tortoise and Hare (slow & fast pointers)", "Cycle detection in O(1) space"),
    (24, 23, "Merge k Sorted Lists", "06-linked-list", "Hard", "Min-Heap priority queue or Divide & Conquer merge", "K-way sorted merging"),

    # 07-trees (25-35)
    (25, 226, "Invert Binary Tree", "07-trees", "Easy", "Recursive swap of left and right child pointers", "Mirroring binary tree"),
    (26, 104, "Maximum Depth of Binary Tree", "07-trees", "Easy", "DFS 1 + max(depth(left), depth(right)) or BFS levels", "Tree height calculation"),
    (27, 100, "Same Tree", "07-trees", "Easy", "Recursive value and structural equality check", "Structural equality"),
    (28, 572, "Subtree of Another Tree", "07-trees", "Easy", "DFS calling isSameTree on every matching root", "Subtree matching"),
    (29, 235, "Lowest Common Ancestor of a BST", "07-trees", "Medium", "BST property: split point where p and q diverge", "BST divergence node"),
    (30, 102, "Binary Tree Level Order Traversal", "07-trees", "Medium", "Queue-based BFS tracking level sizes", "Level-by-level traversal"),
    (31, 98, "Validate Binary Search Tree", "07-trees", "Medium", "DFS with min_val and max_val boundary constraints", "BST boundary validation"),
    (32, 230, "Kth Smallest Element in a BST", "07-trees", "Medium", "Inorder traversal yielding sorted ascending sequence", "Kth item in BST"),
    (33, 105, "Construct Binary Tree from Preorder and Inorder Traversal", "07-trees", "Medium", "Preorder root + Inorder split with Hash Map", "Tree reconstruction"),
    (34, 124, "Binary Tree Maximum Path Sum", "07-trees", "Hard", "Postorder DFS computing max gain per branch", "Max path sum across any nodes"),
    (35, 297, "Serialize and Deserialize Binary Tree", "07-trees", "Hard", "Preorder traversal with '#' null markers and delimiter", "Tree string serialization"),

    # 08-tries (36-38)
    (36, 208, "Implement Trie (Prefix Tree)", "08-tries", "Medium", "TrieNode with children dict and is_end boolean", "Prefix tree data structure"),
    (37, 211, "Design Add and Search Words Data Structure", "08-tries", "Medium", "Trie with DFS backtracking on '.' wildcard character", "Wildcard string search"),
    (38, 212, "Word Search II", "08-tries", "Hard", "Trie of words combined with 2D Grid DFS backtracking", "Multi-word board search"),

    # 09-heap-priority-queue (39-41)
    (39, 23, "Merge k Sorted Lists (Heap)", "09-heap-priority-queue", "Hard", "Min-heap storing k node heads", "K-way heap merge"),
    (40, 347, "Top K Frequent Elements (Heap)", "09-heap-priority-queue", "Medium", "Min-heap of size k tracking highest counts", "Heap-based top elements"),
    (41, 295, "Find Median from Data Stream", "09-heap-priority-queue", "Hard", "Max-Heap (small half) + Min-Heap (large half)", "Dynamic stream median"),

    # 10-backtracking (42-43)
    (42, 39, "Combination Sum", "10-backtracking", "Medium", "Decision tree backtracking choosing candidate again or moving to next", "Target sum combinations"),
    (43, 79, "Word Search", "10-backtracking", "Medium", "Grid DFS with visited set / in-place char mutation", "Board word search"),

    # 11-graphs (44-49)
    (44, 200, "Number of Islands", "11-graphs", "Medium", "Grid BFS/DFS marking visited land '1' to '0'", "Connected components on grid"),
    (45, 133, "Clone Graph", "11-graphs", "Medium", "DFS/BFS with visited HashMap mapping old_node -> new_node", "Deep graph cloning"),
    (46, 417, "Pacific Atlantic Water Flow", "11-graphs", "Medium", "Reverse DFS from ocean borders to higher inland cells", "Ocean drainage intersection"),
    (47, 207, "Course Schedule", "11-graphs", "Medium", "Topological Sort using Kahn's Algorithm (indegree) or DFS cycle check", "DAG cycle detection"),
    (48, 261, "Graph Valid Tree", "11-graphs", "Medium", "Union-Find or BFS checking exactly N-1 edges and no cycles", "Tree connectivity check"),
    (49, 323, "Number of Connected Components in an Undirected Graph", "11-graphs", "Medium", "Disjoint Set Union (DSU) with rank and path compression", "Component counting"),

    # 12-advanced-graphs (50)
    (50, 269, "Alien Dictionary", "12-advanced-graphs", "Hard", "Build character precedence graph from adjacent words + Topological Sort", "Lexicographical order recovery"),

    # 13-1d-dynamic-programming (51-58)
    (51, 70, "Climbing Stairs", "13-1d-dynamic-programming", "Easy", "Fibonacci DP: dp[i] = dp[i-1] + dp[i-2]", "Step combinations"),
    (52, 322, "Coin Change", "13-1d-dynamic-programming", "Medium", "Bottom-up DP: dp[a] = min(dp[a], 1 + dp[a - c])", "Fewest coins for amount"),
    (53, 300, "Longest Increasing Subsequence", "13-1d-dynamic-programming", "Medium", "Patience sorting with Binary Search (bisect_left) in O(N log N)", "Longest strictly increasing subsequence"),
    (54, 139, "Word Break", "13-1d-dynamic-programming", "Medium", "Boolean DP array matching words from dictionary at dp[i]", "Dictionary segmentability"),
    (55, 377, "Combination Sum IV", "13-1d-dynamic-programming", "Medium", "Permutation DP counting order-sensitive sums", "Ordered sum permutations"),
    (56, 198, "House Robber", "13-1d-dynamic-programming", "Medium", "DP: rob = max(prev1, prev2 + num) in O(1) space", "Non-adjacent max sum"),
    (57, 213, "House Robber II", "13-1d-dynamic-programming", "Medium", "Circular DP: max(rob(nums[1:]), rob(nums[:-1]))", "Circular non-adjacent sum"),
    (58, 91, "Decode Ways", "13-1d-dynamic-programming", "Medium", "DP tracking valid single digit (1-9) and valid double digit (10-26)", "Numeric message decodings"),

    # 14-2d-dynamic-programming (59-60)
    (59, 62, "Unique Paths", "14-2d-dynamic-programming", "Medium", "Grid DP: dp[r][c] = dp[r-1][c] + dp[r][c-1]", "Grid paths to bottom right"),
    (60, 1143, "Longest Common Subsequence", "14-2d-dynamic-programming", "Medium", "2D DP matching characters or taking max(dp[i+1][j], dp[i][j+1])", "Common subsequence length"),

    # 15-greedy (61-62)
    (61, 53, "Maximum Subarray", "15-greedy", "Medium", "Kadane's Algorithm: cur_sum = max(num, cur_sum + num)", "Largest contiguous subarray sum"),
    (62, 55, "Jump Game", "15-greedy", "Medium", "Greedy backwards target moving from goal to 0", "Reaching final array index"),

    # 16-intervals (63-67)
    (63, 57, "Insert Interval", "16-intervals", "Medium", "Merge non-overlapping before, merge overlapping, append remaining", "Interval insertion"),
    (64, 56, "Merge Intervals", "16-intervals", "Medium", "Sort by start time, merge if current start <= previous end", "Collapsing overlapping intervals"),
    (65, 435, "Non-overlapping Intervals", "16-intervals", "Medium", "Greedy sort by end time, remove interval with later end on conflict", "Min interval removals"),
    (66, 252, "Meeting Rooms", "16-intervals", "Easy", "Sort by start time, check if intervals[i][0] < intervals[i-1][1]", "Checking schedule conflicts"),
    (67, 253, "Meeting Rooms II", "16-intervals", "Medium", "Min-Heap tracking ongoing meeting end times or Sweep Line", "Min conference rooms required"),

    # 17-math-and-geometry (68-69)
    (68, 48, "Rotate Image", "17-math-and-geometry", "Medium", "Transpose matrix (swap arr[i][j], arr[j][i]) + Reverse each row", "90 degree clockwise rotation"),
    (69, 54, "Spiral Matrix", "17-math-and-geometry", "Medium", "Four boundary pointers (top, bottom, left, right) traversing clockwise", "Spiral array traversal"),

    # 18-bit-manipulation (70-75)
    (70, 191, "Number of 1 Bits", "18-bit-manipulation", "Easy", "Brian Kernighan's Algorithm: n &= (n - 1) clears lowest set bit", "Hamming weight calculation"),
    (71, 338, "Counting Bits", "18-bit-manipulation", "Easy", "Bit DP: dp[i] = dp[i >> 1] + (i & 1)", "Counting bits from 0 to N"),
    (72, 190, "Reverse Bits", "18-bit-manipulation", "Easy", "Bitwise extraction and left shift accumulation across 32 bits", "Reversing 32-bit integer"),
    (73, 268, "Missing Number", "18-bit-manipulation", "Easy", "XOR all numbers from 0..n with array elements or Gauss sum formula", "Finding missing array integer"),
    (74, 371, "Sum of Two Integers", "18-bit-manipulation", "Medium", "Bitwise adder: sum = a ^ b, carry = (a & b) << 1 until carry is 0", "Addition without arithmetic operators"),
    (75, 7, "Reverse Integer", "18-bit-manipulation", "Medium", "Modulo arithmetic extracting digits with 32-bit overflow check", "Integer reversal with overflow")
]

print(f"Loaded complete catalog of {len(BLIND_75_FULL_CATALOG)} Blind 75 questions.")
