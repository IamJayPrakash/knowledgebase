# MongoDB Aggregation Pipeline: Multi-Stage Document Processing

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
MongoDB Aggregation Pipeline ek **Industrial Oil Refinery** ki tarah hai:
Stage 1: Raw crude oil pipeline mein enter hota hai.
Stage 2 (`$match`): Kachra aur mitti chhan kar alag kar di jati hai.
Stage 3 (`$unwind`): Badi barrel khol kar chote packets alag kiye jate hain.
Stage 4 (`$group`): Petrol, diesel, aur kerosene ko alag-alag tanks mein jama karke total quantity sum kiye jate hain.
Stage 5 (`$sort`): Sabse mehenge chemical ko upar display kiya jata hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Pipeline Execution Order**: Stages execute sequentially. Always place `$match` and `$project` as early as possible so subsequent stages process the minimal necessary documents.
2. **Index Utilization**: Only initial stages before any `$project`, `$group`, or `$unwind` can leverage B-Tree indexes for filtering or sorting.
3. **Memory Limits**:
   - Each aggregation stage has a 100 MB RAM limit.
   - If exceeded, MongoDB throws an error unless `allowDiskUse: true` is configured.
4. **Key Stages**:
   - `$match`: Filter documents (uses index if first stage).
   - `$unwind`: Deconstructs an array field from the input documents to output a document for each element.
   - `$lookup`: Performs a left outer join to an unsharded collection.
   - `$group`: Groups documents by a specified identifier and accumulates metrics (`$sum`, `$avg`, `$push`).

---

## 💻 3. Line-by-Line Commented Code Snippets

```javascript
// MongoDB Aggregation: Calculate Monthly Revenue per Product Category
db.orders.aggregate([
  // Line 3: Stage 1: Filter completed orders within the target year (Uses B-Tree Index!)
  {
    $match: {
      status: "COMPLETED",
      orderDate: {
        $gte: ISODate("2026-01-01T00:00:00Z"),
        $lt: ISODate("2027-01-01T00:00:00Z")
      }
    }
  },

  // Line 14: Stage 2: Deconstruct items array into individual item rows
  {
    $unwind: "$items"
  },

  // Line 19: Stage 3: Join with products collection to retrieve category metadata
  {
    $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "productDetails"
    }
  },

  // Line 29: Stage 4: Unwind joined product array (1-to-1 match)
  {
    $unwind: "$productDetails"
  },

  // Line 34: Stage 5: Group by Category and calculate revenue and item volume
  {
    $group: {
      _id: "$productDetails.category",
      totalRevenue: {
        $sum: { $multiply: ["$items.quantity", "$items.unitPrice"] }
      },
      totalItemsSold: { $sum: "$items.quantity" },
      uniqueOrders: { $addToSet: "$_id" }
    }
  },

  // Line 46: Stage 6: Sort descending by revenue
  {
    $sort: { totalRevenue: -1 }
  }
], { allowDiskUse: true });
```
