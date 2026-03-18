# Step 3: Fill the Note

Edit the generated `.md` file to fill in the solution components from Step 2. Update exactly these three sections — leave everything else untouched.

## Section 1: Approach

Find the Approach section and replace the empty callouts with the prepared content.

**Before (template placeholder):**

```markdown
> [!abstract]- Intuition
> 

> [!info]- Algorithm
> 1. 
```

**After (filled in):**

```markdown
> [!abstract]- Intuition
> <key insight — 1-3 sentences explaining WHY this approach works>

> [!info]- Algorithm
> 1. <step that maps to code>
> 2. <next step>
> 3. <...>
```

### Rules

- Keep intuition on a single `> ` continuation line (no blank lines inside the callout)
- Each algorithm step on its own `> N. ` line
- Use inline code for variable/function names: `` `seen` ``, `` `complement` ``

## Section 2: Solutions

Find the Solutions section and replace the skeleton code in both Python tabs.

**Tab 1 — Clean solution:**

Replace:
```markdown
- Python
    ```python
    class Solution:
        def solution(self):
    ```
```

With:
```markdown
- Python
    ```python
    class Solution:
        def actualMethodName(self, param1: type, param2: type) -> returnType:
            # implementation
    ```
```

**Tab 2 — Solution with test runner:**

Replace:
```markdown
- Python ▶️
    ```python
    class Solution:
        def solution(self):
            pass

    if __name__ == "__main__":
        sol = Solution()
        tests = [
            # (input_args, expected),
            ((), None),
        ]
        for i, (args, expected) in enumerate(tests, 1):
            result = sol.solution(*args) if isinstance(args, tuple) else sol.solution(args)
            status = "✅" if result == expected else "❌"
            print(f"Test {i}: {status} | Input: {args} | Expected: {expected} | Got: {result}")
    ```
```

With:
```markdown
- Python ▶️
    ```python
    class Solution:
        def actualMethodName(self, param1: type, param2: type) -> returnType:
            # same implementation as Tab 1

    if __name__ == "__main__":
        sol = Solution()
        tests = [
            ((arg1_val, arg2_val), expected1),
            ((arg1_val, arg2_val), expected2),
            ((edge_arg1, edge_arg2), edge_expected),
        ]
        for i, (args, expected) in enumerate(tests, 1):
            result = sol.actualMethodName(*args) if isinstance(args, tuple) else sol.actualMethodName(args)
            status = "✅" if result == expected else "❌"
            print(f"Test {i}: {status} | Input: {args} | Expected: {expected} | Got: {result}")
    ```
```

### Rules

- The code in both tabs must be **identical** (Tab 2 just adds the test runner below)
- All code lines inside `[tabs]` must be **indented 4 spaces** (tab content requirement)
- Use the **exact method name** from LeetCode's signature (e.g., `twoSum`, `maxProfit`, `isValid`)
- Update `sol.solution(...)` → `sol.actualMethodName(...)` in the test runner loop
- Test case args must be a tuple matching the method's parameter order

## Section 3: Complexity

Find the Complexity table and fill in the values.

**Before:**

```markdown
| Metric    | Complexity | Notes |
| --------- | ---------- | ----- |
| **Time**  |            |       |
| **Space** |            |       |
```

**After:**

```markdown
| Metric    | Complexity | Notes                         |
| --------- | ---------- | ----------------------------- |
| **Time**  | O(...)     | <what drives time cost>       |
| **Space** | O(...)     | <what drives space cost>      |
```

## Complete Example: Two Sum

Here is what the filled sections look like for problem "1. Two Sum":

**Approach:**
```markdown
> [!abstract]- Intuition
> Use a hash map to store each number's index as we iterate. For each element, check if `target - num` already exists in the map — this gives O(1) lookup instead of O(n) nested search.

> [!info]- Algorithm
> 1. Initialize an empty hash map `seen`
> 2. Iterate through `nums` with index `i`
> 3. Compute `complement = target - nums[i]`
> 4. If `complement` exists in `seen`, return `[seen[complement], i]`
> 5. Otherwise, store `nums[i] → i` in `seen`
```

**Solutions:**
```markdown
- Python
    ```python
    class Solution:
        def twoSum(self, nums: list[int], target: int) -> list[int]:
            seen: dict[int, int] = {}
            for i, num in enumerate(nums):
                complement = target - num
                if complement in seen:
                    return [seen[complement], i]
                seen[num] = i
            return []
    ```

- Python ▶️
    ```python
    class Solution:
        def twoSum(self, nums: list[int], target: int) -> list[int]:
            seen: dict[int, int] = {}
            for i, num in enumerate(nums):
                complement = target - num
                if complement in seen:
                    return [seen[complement], i]
                seen[num] = i
            return []

    if __name__ == "__main__":
        sol = Solution()
        tests = [
            (([2, 7, 11, 15], 9), [0, 1]),
            (([3, 2, 4], 6), [1, 2]),
            (([3, 3], 6), [0, 1]),
        ]
        for i, (args, expected) in enumerate(tests, 1):
            result = sol.twoSum(*args) if isinstance(args, tuple) else sol.twoSum(args)
            status = "✅" if result == expected else "❌"
            print(f"Test {i}: {status} | Input: {args} | Expected: {expected} | Got: {result}")
    ```
```

**Complexity:**
```markdown
| Metric    | Complexity | Notes                              |
| --------- | ---------- | ---------------------------------- |
| **Time**  | O(n)       | Single pass through the array      |
| **Space** | O(n)       | Hash map stores at most n elements |
```

## Next

Proceed to [Step 4: Verify and Report](04-verify-and-report.md) to validate the solution.
