# Step 2: Solve the Problem

Analyze the fetched problem and determine the most optimal solution. This step is purely analytical — the note is updated in Step 3.

## Process

1. Read the generated `.md` note from Step 1
2. Parse the **Description** section to understand the problem
3. Identify constraints (input size, value ranges, edge cases)
4. Determine the **most optimal** algorithm:
   - Best time complexity first, then best space complexity
   - If multiple approaches share the same complexity, prefer the simpler one
5. Prepare the solution components listed below

## Solution Components to Prepare

Before moving to Step 3, have these ready:

### Intuition

A 1-3 sentence explanation of the **key insight** — why this approach works, not what it does.

- Focus on the "aha" moment that makes the problem solvable efficiently
- Connect the problem pattern to a known technique (e.g., sliding window, two pointers, monotonic stack)

### Algorithm

Numbered, implementation-oriented steps that map directly to code.

- Each step should correspond to a block of code
- Include data structure choices (e.g., "Initialize a min-heap")
- Mention key conditions and loop invariants

### Code

The optimal Python solution as a `Solution` class.

- Use the **exact method signature** from LeetCode (match `codeSnippets` from the problem data)
- Include type hints (`list[int]`, `Optional[TreeNode]`, etc.)
- Add inline `from` imports only if needed (e.g., `from collections import defaultdict`)
- Write clean, idiomatic Python — no unnecessary comments or blank lines
- Handle edge cases inline (don't add separate if-checks unless necessary)

### Test Cases

2-4 test cases with correct expected values.

- Derive from the problem's examples first
- Add at least one edge case if obvious:
  - Empty input, single element, all duplicates
  - Minimum/maximum constraint values
  - Negative numbers if applicable

### Complexity Analysis

Time and space complexity with brief justification.

- Use standard Big-O notation: O(1), O(log n), O(n), O(n log n), O(n²), etc.
- Notes should explain what drives the complexity (e.g., "Single pass through array", "Sorting dominates")

## Decision Guide

| Problem Pattern | Likely Optimal Approach |
| --- | --- |
| "Find pair/triplet with target sum" | Hash map or two pointers (sorted) |
| "Subarray/substring with condition" | Sliding window |
| "K-th largest/smallest" | Heap or quickselect |
| "Tree traversal" | DFS (recursive or stack) or BFS (queue) |
| "Shortest path (unweighted)" | BFS |
| "Shortest path (weighted)" | Dijkstra or Bellman-Ford |
| "Subsequence/subset/combinations" | Dynamic programming or backtracking |
| "Intervals (merge/overlap)" | Sort by start, then sweep |
| "Linked list cycle/intersection" | Fast-slow pointers |
| "String matching" | KMP, Rabin-Karp, or trie |
| "Range queries" | Prefix sum, segment tree, or BIT |
| "Topological ordering" | Kahn's BFS or DFS with post-order |

## Next

Once the solution components are ready, proceed to [Step 3: Fill Note Sections](03-fill-note-sections.md).
