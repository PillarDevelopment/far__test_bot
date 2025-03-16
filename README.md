## Link - [diamond hands frw bot](https://t.me/diamondhandsfrw_bot)

### Base Logic
(Due to technical issues, the search service is temporarily unavailable.)

Here's the English translation of the rating calculation methodology:

---

### **1. Data Collection**  
For each wallet, we track:  
- **Token balance** (`balance`) — current number of coins in the wallet.  
- **Holding duration** (`days_held`) — days since first purchase/transaction.  

---

### **2. Metric Normalization**  
To compare different measurement units (tokens vs days), we use **min-max normalization**:  

```python  
# For balance:  
norm_balance = (balance - min_balance) / (max_balance - min_balance)  

# For holding duration:  
norm_duration = (days_held - min_days) / (max_days - min_days)  
```  

**Example**:  
If in the dataset:  
- Max balance = 1,000,000 tokens  
- Min balance = 1,000 tokens  
- Wallet A: 500,000 tokens → `(500,000 - 1,000) / 999,000 ≈ 0.499`  

---

### **3. Weighted Combination**  
Metrics are combined using configurable weights:  
```python  
score = (0.7 * norm_balance) + (0.3 * norm_duration)  
```  

**Why 70/30**:  
- Balance (70%) — reflects current market influence.  
- Duration (30%) — indicates position stability.  

Adjustable example:  
```python  
# For long-term projects:  
score = (0.5 * norm_balance) + (0.5 * norm_duration)  
```  

---

### **4. Calculation Example**  
**Data**:  
- Wallet 1: balance = 800,000, days = 200  
- Wallet 2: balance = 200,000, days = 500  

**Normalization** (hypothetical):  
- Balance: max=1M, min=50K  
  - Wallet 1: `(800K-50K)/950K ≈ 0.79`  
  - Wallet 2: `(200K-50K)/950K ≈ 0.16`  
- Duration: max=730 days, min=30 days  
  - Wallet 1: `(200-30)/700 ≈ 0.24`  
  - Wallet 2: `(500-30)/700 ≈ 0.67`  

**Rating**:  
- Wallet 1: `0.7*0.79 + 0.3*0.24 = 0.625`  
- Wallet 2: `0.7*0.16 + 0.3*0.67 = 0.313`  

**Result**: Wallet 1 ranks higher due to larger balance despite shorter holding period.  

---

### **5. Current Model Limitations**  
1. **Test data** — uses generated values instead of real transactions.  
2. **No sales verification** — real implementation requires transaction history analysis.  
3. **Linear dependence** — production could benefit from nonlinear transformations (e.g., log balance).  

---

### **Improvement Opportunities**  
1. **Sales detection**:  
   ```python  
   if any(tx["type"] == "SELL" for tx in wallet.transactions):  
       score *= 0.5  # Penalty for sales  
   ```  

2. **Exponential time weighting**:  
   ```python  
   time_score = 1 - math.exp(-0.01 * days_held)  # "Compound interest" of time  
   ```  

3. **Holder clustering**:  
   - Separate ratings for "whales" (>1% supply) vs retail holders.  

Would you like me to:  
- Demonstrate transaction verification implementation?  
- Optimize the formula for a specific token?  
- Visualize holder distribution?  

Ready to enhance the logic for your needs! 🛠️
