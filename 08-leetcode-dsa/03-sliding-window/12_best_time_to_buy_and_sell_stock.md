# 12. Best Time to Buy and Sell Stock (LeetCode 121) — Easy

## 1. 🐣 Layman's Analogy (Hinglish + Real-World)
> **Hinglish Intuition:** Stock saste me kharidna hai aur mehenge me bechna hai. Minimum price track karte chalo aur har din maximum profit calculate karo.
>
> **Real-World Analogy:** Tracking the lowest purchase price you ever saw in history and calculating your profit if you sold today.

---

## 2. 📌 Core Mechanics & Edge Cases
- **LeetCode ID:** [121 - Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
- **Difficulty:** `Easy`
- **Pattern / Core Strategy:** Single pass tracking min_price and max_profit
- **Edge Cases:** Empty inputs, boundary limits, single elements, duplicates, negative numbers.

---

## 3. 📊 Visual Diagram

```text
[7, 1, 5, 3, 6, 4]
Min so far: 7 -> 1 -> 1 -> 1 -> 1
Profits: 0, 0, (5-1)=4, (3-1)=2, (6-1)=5 (Max) -> Result = 5
```

---

## 4. 💻 Solutions: Brute Force vs Optimal

### ❌ Solution 1: Brute Force
- **Approach:** Nested loops checking every buy and sell day pair. Time: O(N^2), Space: O(1).

### ✅ Solution 2: Optimal Solution (Line-by-Line Commented)

#### JavaScript / TypeScript
```javascript
function maxProfit(prices) {
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
}
```

#### Python 3
```python
def maxProfit(prices):
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
    return max_profit
```

---

## 5. 🎯 Interview Answering Pitch (Say Exactly This!)
> **Interviewer:** "How do you approach solving Best Time to Buy and Sell Stock?"
>
> **You:** "The naive solution uses nested loops checking every buy and sell day pair, which causes inefficient time complexity. We can optimize this using **Single pass tracking min_price and max_profit**, achieving optimal time complexity with minimal auxiliary space."

---

## 6. 💼 Production War Story & Project Challenge (STAR Scenario)
* **Situation:** Crypto automated algorithmic trading bot identifying historical dip opportunities.
* **Task / Challenge:** Resolving high-latency processing bottlenecks, quadratic execution times, and out-of-memory errors under production load.
* **Action Taken:** Deployed the **Single pass tracking min_price and max_profit** algorithm to replace legacy bottlenecks.
* **Result & Business Impact:** Executed in sub-millisecond O(N) streaming fashion over 1,000,000 tick prices.

🗣️ **Script to Tell Interviewer:**
*"In one of our core backend services, we experienced a performance bottleneck when handling max profit calculation. I optimized the workflow using Single pass tracking min_price and max_profit, which executed in sub-millisecond o(n) streaming fashion over 1,000,000 tick prices. and ensured zero downtime."*
