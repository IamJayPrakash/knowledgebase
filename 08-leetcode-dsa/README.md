# 🧮 Data Structures & Algorithms Master Curriculum & Index

> A comprehensive, step-by-step learning roadmap and interview index focusing on **High-Frequency Algorithmic Patterns & System DSA** for Senior Technical Lead & SDE-2/3 interviews.

---

## 📌 How to Use This Section
- Use this `README.md` as your master index and curriculum roadmap for Data Structures & Algorithms.
- Create single concept files inside `08-leetcode-dsa/` (e.g., `01_sliding_window_pattern.md`) as you solve problems and add your notes, optimal code solutions, time/space complexity analysis, and edge cases.

---

## 🗺️ Algorithmic Pattern Roadmap & Concept Index

### 1. Array & String Patterns
- [ ] `01_two_pointers_pattern.md` — Opposite direction pointers, Same direction pointers, Container With Most Water, 3Sum, Trapping Rain Water.
- [ ] `02_sliding_window_pattern.md` — Fixed Window Size vs Variable Window Size, Longest Substring Without Repeating Characters, Minimum Window Substring.
- [ ] `03_prefix_sum_and_hashmap.md` — Prefix Sum array, Subarray Sum Equals K, Longest Consecutive Sequence.
- [ ] `04_merge_intervals_pattern.md` — Overlapping intervals check, Merge Intervals, Insert Interval, Meeting Rooms II (Min Heap / Sweep Line).

### 2. Stack, Queue & Linked List
- [ ] `05_linked_list_manipulation.md` — Reverse Linked List, Reorder List, Fast & Slow Pointers (Floyd's Cycle Detection algorithm), Merge Two Sorted Lists.
- [ ] `06_monotonic_stack_and_queue.md` — Monotonic Increasing/Decreasing Stack, Next Greater Element, Daily Temperatures, Sliding Window Maximum (Monotonic Deque).

### 3. Trees, Tries & Graphs
- [ ] `07_binary_tree_traversals_bfs_dfs.md` — Preorder, Inorder, Postorder traversal, Level Order Traversal (BFS), Lowest Common Ancestor (LCA), Binary Tree Maximum Path Sum.
- [ ] `08_trie_prefix_tree.md` — Trie Node structure (`insert`, `search`, `startsWith`), Autocomplete system foundation.
- [ ] `09_graph_bfs_dfs_topological_sort.md` — Graph representation (Adjacency List), BFS vs DFS, Cycle Detection in Directed/Undirected graphs, Topological Sort (Kahn's BFS algorithm), Course Schedule.
- [ ] `10_disjoint_set_union_dsu.md` — Union-Find with Path Compression and Union by Rank, Number of Connected Components, Redundant Connection.

### 4. Dynamic Programming & Backtracking
- [ ] `11_backtracking_patterns.md` — Decision Trees, Subsets, Permutations, Combination Sum, Word Search, N-Queens.
- [ ] `12_1d_and_2d_dynamic_programming.md` — Memoization vs Tabulation, Climbing Stairs, House Robber, Coin Change, 0/1 Knapsack, Longest Common Subsequence (LCS), Edit Distance.

### 5. System Data Structures (SDE-2/3 Interview Must-Haves)
- [ ] `13_lru_cache_implementation.md` — Designing LRU Cache using Hash Map + Doubly Linked List ($O(1)$ `get` and `put`).
- [ ] `14_lfu_cache_implementation.md` — Designing LFU Cache using Frequency Map + Doubly Linked Lists ($O(1)$ complexity).
- [ ] `15_find_median_from_data_stream.md` — Streaming Median using Max-Heap (left half) + Min-Heap (right half).

---

## 💡 High-Yield Senior Interview Time & Space Complexities Cheat Sheet

| Data Structure / Pattern | Operation / Problem | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Two Pointers** | 3Sum | $O(N^2)$ | $O(1)$ or $O(N)$ |
| **Sliding Window** | Min Window Substring | $O(N)$ | $O(K)$ |
| **Monotonic Stack** | Next Greater Element | $O(N)$ | $O(N)$ |
| **Trie** | Insert / Search Word of length $L$ | $O(L)$ | $O(\text{Alphabet Size} \times L \times N)$ |
| **Topological Sort** | Course Schedule | $O(V + E)$ | $O(V + E)$ |
| **LRU Cache** | Get / Put | $O(1)$ | $O(\text{Capacity})$ |
