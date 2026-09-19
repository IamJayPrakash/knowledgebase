# DSA Meta-Heuristics and Pattern Recognition Cheat Sheet

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)

DSA problem dekh kar ghabrana ek un-labeled medicine box dekhne jaisa hai.
Lekin agar aapke paas **Doctor ka Symptom Checker (Meta-Heuristics)** ho, toh aap problem ki shakal (Constraints & Keywords) dekh kar 5 second mein pehchan loge:

- "Sorted array hai aur search karna hai?" ➔ **Binary Search ($O(\log N)$)**!
- "Subarray sum / longest substring poocha hai?" ➔ **Sliding Window**!
- "Top K / Most frequent elements?" ➔ **Min-Heap / Max-Heap**!
- "All combinations / permutations?" ➔ **Backtracking**!
- "Shortest path in unweighted graph?" ➔ **BFS (Queue)**!

---

## 📌 2. Master Pattern Recognition Matrix

| If the problem mentions... | Candidate Data Structure / Algorithm | Time Complexity Target |
| :--- | :--- | :--- |
| **Sorted Array & Finding Target/Boundary** | Binary Search (Two Pointers) | $O(\log N)$ |
| **Contiguous Subarray / Substring with condition** | Sliding Window (Two Pointers + Hash Map) | $O(N)$ |
| **Top K, Smallest K, Median in Stream** | Heap / Priority Queue | $O(N \log K)$ |
| **Finding cycles, connected components** | Union-Find (Disjoint Set) or DFS | $O(N \cdot \alpha(N))$ |
| **Shortest path (Unweighted)** | Breadth-First Search (BFS with Queue) | $O(V + E)$ |
| **Shortest path (Weighted, positive edges)** | Dijkstra's Algorithm (Min-Heap) | $O((V + E) \log V)$ |
| **Overlapping subproblems & Optimal substructure** | Dynamic Programming (1D/2D Memoization) | $O(N)$ to $O(N^2)$ |
| **Generate all combinations / subsets** | Backtracking (DFS Recursion tree) | $O(2^N)$ or $O(N!)$ |
| **Next Greater / Smaller Element** | Monotonic Stack | $O(N)$ |
| **Prefix / Word dictionary lookups** | Trie (Prefix Tree) | $O(L)$ where $L$ = word length |

---

## 💻 3. Meta-Heuristic Template: Sliding Window Skeleton

```python
# Universal Sliding Window Pattern Template
def sliding_window_template(arr, condition):
    # Line 3: Window state trackers
    left = 0
    window_state = {}
    optimal_result = 0

    # Line 8: Right pointer expands window
    for right in range(len(arr)):
        # Add incoming element to window state
        current_elem = arr[right]
        window_state[current_elem] = window_state.get(current_elem, 0) + 1

        # Line 14: Contract window from left while condition is violated
        while not condition(window_state):
            left_elem = arr[left]
            window_state[left_elem] -= 1
            if window_state[left_elem] == 0:
                del window_state[left_elem]
            left += 1 # Shrink window

        # Line 22: Update optimal result with valid window
        current_window_len = right - left + 1
        optimal_result = max(optimal_result, current_window_len)

    return optimal_result
```
